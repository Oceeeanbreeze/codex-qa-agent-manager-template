param(
    [string]$WorkspaceRoot = (Get-Location).Path
)

$ErrorActionPreference = 'Stop'

function Test-CommandAvailable {
    param([string[]]$Names)
    foreach ($name in $Names) {
        $cmd = Get-Command $name -ErrorAction SilentlyContinue
        if ($cmd) { return $cmd.Source }
    }
    return $null
}

function Read-ConfigValue {
    param(
        [string]$Content,
        [string]$Key
    )
    $match = [regex]::Match($Content, "(?m)^$([regex]::Escape($Key)):\s*(.+)$")
    if ($match.Success) {
        return $match.Groups[1].Value.Trim()
    }
    return ''
}

function Read-RuntimeManifestLauncher {
    param([string]$ManifestPath)
    if (-not (Test-Path $ManifestPath)) {
        return $null
    }
    $content = Get-Content $ManifestPath -Raw
    $match = [regex]::Match($content, "(?m)^\s*python_launcher:\s*(.+)$")
    if ($match.Success) {
        return $match.Groups[1].Value.Trim()
    }
    return $null
}

function Test-PythonExecution {
    param([string]$PreferredLauncher)
    $candidates = @(
        @{ Name = 'py'; Args = @('-3', '--version') },
        @{ Name = 'python'; Args = @('--version') }
    )

    if ($PreferredLauncher) {
        $tokens = $PreferredLauncher -split '\s+'
        if ($tokens.Count -gt 0) {
            $candidates = ,@{ Name = $tokens[0]; Args = @($tokens[1..($tokens.Count - 1)]) + @('--version') } + $candidates
        }
    }

    foreach ($candidate in $candidates) {
        $cmd = Get-Command $candidate.Name -ErrorAction SilentlyContinue
        if (-not $cmd) { continue }

        try {
            $output = & $candidate.Name @($candidate.Args) 2>&1
            if ($LASTEXITCODE -eq 0 -or $output) {
                return [PSCustomObject]@{
                    Status = 'PASS'
                    Detail = (($output | Out-String).Trim())
                }
            }
        } catch {
            return [PSCustomObject]@{
                Status = 'WARN'
                Detail = $_.Exception.Message
            }
        }
    }

    return [PSCustomObject]@{
        Status = 'WARN'
        Detail = 'No working Python launcher found in current shell.'
    }
}

$workspace = (Resolve-Path $WorkspaceRoot).Path
$configPath = Join-Path $workspace 'memory\config.yaml'
$runtimeManifestPath = Join-Path $workspace 'configs\runtime-manifest.local.yaml'
$requiredFiles = @(
    'AGENTS.md',
    'codex\WORKFLOW.md',
    'codex\SKILL_ROUTING.md',
    'memory\ROLE_TOOLING.md',
    'docs\REFERENCE_ARCHITECTURE.md',
    'docs\FULL_RECONSTRUCTION_GUIDE.md',
    'docs\RUNTIME_PARAMETER_MATRIX.md',
    'docs\HEALTH_AND_DOCTOR.md',
    'docs\BATTLE_READY_CHECKLIST.md'
)

$requiredDirs = @(
    'obsidian-vault',
    'memory',
    'configs',
    'tools'
)

$results = [System.Collections.Generic.List[object]]::new()

foreach ($file in $requiredFiles) {
    $path = Join-Path $workspace $file
    $results.Add([PSCustomObject]@{
        Check = "file:$file"
        Status = if (Test-Path $path) { 'PASS' } else { 'FAIL' }
        Detail = $path
    })
}

foreach ($dir in $requiredDirs) {
    $path = Join-Path $workspace $dir
    $results.Add([PSCustomObject]@{
        Check = "dir:$dir"
        Status = if (Test-Path $path) { 'PASS' } else { 'FAIL' }
        Detail = $path
    })
}

$preferredLauncher = Read-RuntimeManifestLauncher -ManifestPath $runtimeManifestPath
$pythonExecution = Test-PythonExecution -PreferredLauncher $preferredLauncher
$results.Add([PSCustomObject]@{
    Check = 'python-runtime'
    Status = $pythonExecution.Status
    Detail = $pythonExecution.Detail
})

$ollamaSource = Test-CommandAvailable -Names @('ollama')
$results.Add([PSCustomObject]@{
    Check = 'ollama-cli'
    Status = if ($ollamaSource) { 'PASS' } else { 'WARN' }
    Detail = if ($ollamaSource) { $ollamaSource } else { 'Ollama CLI not found in current shell.' }
})

if (Test-Path $configPath) {
    $config = Get-Content $configPath -Raw
    $vaultPath = Read-ConfigValue -Content $config -Key 'vault_path'
    $storageDir = Read-ConfigValue -Content $config -Key 'storage_dir'

    $results.Add([PSCustomObject]@{
        Check = 'config:memory-config'
        Status = 'PASS'
        Detail = $configPath
    })

    if ($vaultPath) {
        $results.Add([PSCustomObject]@{
            Check = 'config:vault-path'
            Status = if (Test-Path $vaultPath) { 'PASS' } else { 'WARN' }
            Detail = $vaultPath
        })
    }

    if ($storageDir) {
        $results.Add([PSCustomObject]@{
            Check = 'config:storage-dir'
            Status = if (Test-Path $storageDir) { 'PASS' } else { 'WARN' }
            Detail = $storageDir
        })
    }
} else {
    $results.Add([PSCustomObject]@{
        Check = 'config:memory-config'
        Status = 'FAIL'
        Detail = $configPath
    })
}

$results.Add([PSCustomObject]@{
    Check = 'config:runtime-manifest'
    Status = if (Test-Path $runtimeManifestPath) { 'PASS' } else { 'WARN' }
    Detail = $runtimeManifestPath
})

$results | Format-Table -AutoSize

$failed = @($results | Where-Object { $_.Status -eq 'FAIL' }).Count
if ($failed -gt 0) {
    Write-Error "Doctor failed. Fix required files or directories first."
}
