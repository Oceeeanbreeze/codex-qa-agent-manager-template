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
    $match = [regex]::Match($Content, "(?m)^\s*$([regex]::Escape($Key)):\s*(.+)$")
    if ($match.Success) {
        return $match.Groups[1].Value.Trim()
    }
    return ''
}

function Read-RuntimeManifestCommand {
    param(
        [string]$Content,
        [string]$Key
    )
    $match = [regex]::Match($Content, "(?m)^\s*$([regex]::Escape($Key)):\s*(.+)$")
    if ($match.Success) {
        return $match.Groups[1].Value.Trim()
    }
    return ''
}

function Format-PythonFailureDetail {
    param(
        [string]$FailureText,
        [string]$PreferredLauncher
    )

    if ($FailureText -match 'No installed Python found') {
        if ($PreferredLauncher) {
            return "Python launcher '$PreferredLauncher' is available but no installed Python runtime was found. Install Python 3.12 or update configs/runtime-manifest.local.yaml."
        }
        return 'A Python launcher is available but no installed Python runtime was found. Install Python 3.12 or configure a working launcher.'
    }

    if ($FailureText -match 'No working Python launcher found') {
        return 'No working Python launcher was found in the current shell. Install Python 3.12 or configure CODEX_PYTHON / python_launcher.'
    }

    if ($FailureText -match 'Access is denied|NativeCommandFailed|ResourceUnavailable') {
        return 'Python is installed but the current host cannot execute it from this shell. Use an unsandboxed operator shell or configure a permitted launcher override.'
    }

    return $FailureText
}

function Get-EnvPythonCandidates {
    $envVars = @('CODEX_PYTHON', 'PYTHON', 'PYTHON_EXECUTABLE')
    $candidates = @()
    foreach ($envVar in $envVars) {
        $raw = [Environment]::GetEnvironmentVariable($envVar)
        if (-not $raw) { continue }
        $tokens = $raw -split '\s+'
        if ($tokens.Count -eq 0) { continue }
        $prefixArgs = @()
        if ($tokens.Count -gt 1) {
            $prefixArgs = @($tokens[1..($tokens.Count - 1)])
        }
        $candidates += @{ Name = $tokens[0]; PrefixArgs = $prefixArgs }
    }
    return $candidates
}

function Resolve-ExecutableCandidate {
    param([string]$Name)

    if (-not $Name) {
        return $null
    }

    if (Test-Path $Name) {
        return (Resolve-Path $Name).Path
    }

    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if ($cmd) {
        return $cmd.Source
    }

    return $null
}

function Get-PythonRuntime {
    param([string]$PreferredLauncher)
    $candidates = @(
        @{ Name = 'py'; PrefixArgs = @('-3') },
        @{ Name = 'python'; PrefixArgs = @() }
    )

    $envCandidates = Get-EnvPythonCandidates
    if ($envCandidates.Count -gt 0) {
        $candidates = @($envCandidates) + $candidates
    }

    if ($PreferredLauncher) {
        $tokens = $PreferredLauncher -split '\s+'
        if ($tokens.Count -gt 0) {
            $prefixArgs = @()
            if ($tokens.Count -gt 1) {
                $prefixArgs = @($tokens[1..($tokens.Count - 1)])
            }
            $candidates = ,@{ Name = $tokens[0]; PrefixArgs = $prefixArgs } + $candidates
        }
    }

    $lastFailure = 'No working Python launcher found in current shell.'
    foreach ($candidate in $candidates) {
        $resolvedCommand = Resolve-ExecutableCandidate -Name $candidate.Name
        if (-not $resolvedCommand) { continue }

        try {
            $output = & $resolvedCommand @($candidate.PrefixArgs) --version 2>&1 | Out-String
            if ($LASTEXITCODE -eq 0 -and $output -match 'Python') {
                return [PSCustomObject]@{
                    Status = 'PASS'
                    Detail = $output.Trim()
                    Command = $resolvedCommand
                    PrefixArgs = $candidate.PrefixArgs
                }
            }
            $lastFailure = $output.Trim()
        } catch {
            $lastFailure = $_.Exception.Message
        }
    }

    return [PSCustomObject]@{
        Status = 'FAIL'
        Detail = (Format-PythonFailureDetail -FailureText $lastFailure -PreferredLauncher $PreferredLauncher)
        Command = $null
        PrefixArgs = @()
    }
}

function Invoke-PythonScript {
    param(
        [pscustomobject]$PythonRuntime,
        [string]$ScriptPath,
        [string[]]$Arguments
    )
    if (-not $PythonRuntime.Command) {
        return [PSCustomObject]@{
            Status = 'FAIL'
            Detail = 'Python runtime is unavailable.'
        }
    }

    try {
        $output = & $PythonRuntime.Command @($PythonRuntime.PrefixArgs) $ScriptPath @Arguments 2>&1 | Out-String
        if ($LASTEXITCODE -eq 0) {
            return [PSCustomObject]@{
                Status = 'PASS'
                Detail = $output.Trim()
            }
        }
        return [PSCustomObject]@{
            Status = 'FAIL'
            Detail = $output.Trim()
        }
    } catch {
        return [PSCustomObject]@{
            Status = 'FAIL'
            Detail = $_.Exception.Message
        }
    }
}

function Get-IncludePaths {
    param([string]$Content)
    $paths = [System.Collections.Generic.List[string]]::new()
    $insideIncludePaths = $false
    foreach ($line in ($Content -split "`r?`n")) {
        if ($line -match '^\s*include_paths:\s*$') {
            $insideIncludePaths = $true
            continue
        }
        if ($insideIncludePaths -and $line -match '^\s{6}-\s+(.+)$') {
            $paths.Add($matches[1].Trim())
            continue
        }
        if ($insideIncludePaths -and $line -match '^\s{4}[A-Za-z0-9_-]+:\s*$') {
            $insideIncludePaths = $false
        }
    }
    return $paths | Select-Object -Unique
}

$workspace = (Resolve-Path $WorkspaceRoot).Path
$configPath = Join-Path $workspace 'memory\config.yaml'
$runtimeManifestPath = Join-Path $workspace 'configs\runtime-manifest.local.yaml'
if (-not (Test-Path $configPath)) {
    throw "Missing config: $configPath"
}

$config = Get-Content $configPath -Raw
$runtimeManifest = if (Test-Path $runtimeManifestPath) { Get-Content $runtimeManifestPath -Raw } else { '' }
$vaultPath = Read-ConfigValue -Content $config -Key 'vault_path'
$storageDir = Read-ConfigValue -Content $config -Key 'storage_dir'
$ollamaBaseUrl = Read-ConfigValue -Content $config -Key 'base_url'
$ollamaModel = Read-ConfigValue -Content $config -Key 'model'
$pythonLauncher = if ($runtimeManifest) { Read-RuntimeManifestCommand -Content $runtimeManifest -Key 'python_launcher' } else { '' }
$includePaths = Get-IncludePaths -Content $config

$checks = [System.Collections.Generic.List[object]]::new()
$checks.Add([PSCustomObject]@{
    Check = 'config-load'
    Status = 'PASS'
    Detail = $configPath
})

$checks.Add([PSCustomObject]@{
    Check = 'runtime-manifest'
    Status = if (Test-Path $runtimeManifestPath) { 'PASS' } else { 'FAIL' }
    Detail = $runtimeManifestPath
})

$pythonRuntime = Get-PythonRuntime -PreferredLauncher $pythonLauncher
$checks.Add([PSCustomObject]@{
    Check = 'python-runtime'
    Status = $pythonRuntime.Status
    Detail = $pythonRuntime.Detail
})

$ollamaSource = Test-CommandAvailable -Names @('ollama')
$checks.Add([PSCustomObject]@{
    Check = 'ollama-cli'
    Status = if ($ollamaSource) { 'PASS' } else { 'WARN' }
    Detail = if ($ollamaSource) { $ollamaSource } else { 'Ollama endpoint may still work, but the ollama CLI is not available in the current shell.' }
})

$checks.Add([PSCustomObject]@{
    Check = 'vault-path'
    Status = if ($vaultPath -and (Test-Path $vaultPath)) { 'PASS' } else { 'FAIL' }
    Detail = $vaultPath
})

$checks.Add([PSCustomObject]@{
    Check = 'storage-dir'
    Status = if ($storageDir -and (Test-Path $storageDir)) { 'PASS' } else { 'FAIL' }
    Detail = $storageDir
})

try {
    $probeFile = Join-Path $storageDir 'health-write-test.tmp'
    Set-Content -Path $probeFile -Value 'ok' -Encoding UTF8
    Remove-Item $probeFile -Force
    $checks.Add([PSCustomObject]@{
        Check = 'storage-write'
        Status = 'PASS'
        Detail = $storageDir
    })
} catch {
    $checks.Add([PSCustomObject]@{
        Check = 'storage-write'
        Status = 'FAIL'
        Detail = $_.Exception.Message
    })
}

if ($ollamaBaseUrl) {
    try {
        $tagsUrl = ($ollamaBaseUrl.TrimEnd('/')) + '/api/tags'
        $resp = Invoke-WebRequest -Uri $tagsUrl -UseBasicParsing -TimeoutSec 5
        $checks.Add([PSCustomObject]@{
            Check = 'embedding-endpoint'
            Status = if ($resp.StatusCode -ge 200 -and $resp.StatusCode -lt 300) { 'PASS' } else { 'WARN' }
            Detail = $tagsUrl
        })

        if ($ollamaModel -and ($resp.Content -match [regex]::Escape($ollamaModel))) {
            $checks.Add([PSCustomObject]@{
                Check = 'embedding-model'
                Status = 'PASS'
                Detail = $ollamaModel
            })
        } else {
            $checks.Add([PSCustomObject]@{
                Check = 'embedding-model'
                Status = 'WARN'
                Detail = if ($ollamaModel) { "Model not found in tags response: $ollamaModel" } else { 'No model configured.' }
            })
        }
    } catch {
        $checks.Add([PSCustomObject]@{
            Check = 'embedding-endpoint'
            Status = 'FAIL'
            Detail = $_.Exception.Message
        })
        $checks.Add([PSCustomObject]@{
            Check = 'embedding-model'
            Status = 'FAIL'
            Detail = if ($ollamaModel) { "Model not verified: $ollamaModel" } else { 'No model configured.' }
        })
    }
}

if ($vaultPath -and (Test-Path $vaultPath)) {
    foreach ($includePath in $includePaths) {
        $fullPath = Join-Path $vaultPath ($includePath -replace '/', '\')
        $checks.Add([PSCustomObject]@{
            Check = "markdown-root:$includePath"
            Status = if (Test-Path $fullPath) { 'PASS' } else { 'FAIL' }
            Detail = $fullPath
        })
    }
}

$indexSmoke = Invoke-PythonScript -PythonRuntime $pythonRuntime -ScriptPath (Join-Path $workspace 'memory\scripts\index_memory.py') -Arguments @(
    '--config',
    $configPath,
    '--agent',
    'archivist',
    '--changed-path',
    'Notes/runtime-verification-smoke.md'
)
$checks.Add([PSCustomObject]@{
    Check = 'index-smoke'
    Status = $indexSmoke.Status
    Detail = $indexSmoke.Detail
})

$finalizeSmoke = Invoke-PythonScript -PythonRuntime $pythonRuntime -ScriptPath (Join-Path $workspace 'memory\scripts\finalize_task.py') -Arguments @(
    '--config',
    $configPath,
    '--title',
    'Health smoke',
    '--user-text',
    'health check',
    '--assistant-text',
    'health check',
    '--roles',
    'archivist',
    '--reindex-mode',
    'none',
    '--dry-run'
)
$checks.Add([PSCustomObject]@{
    Check = 'finalize-dry-run'
    Status = $finalizeSmoke.Status
    Detail = $finalizeSmoke.Detail
})

$checks | Format-Table -AutoSize

$failed = @($checks | Where-Object { $_.Status -eq 'FAIL' }).Count
if ($failed -gt 0) {
    Write-Error 'Health check failed.'
}
