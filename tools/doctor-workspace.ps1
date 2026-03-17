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

function Invoke-PythonSnippet {
    param(
        [pscustomobject]$PythonRuntime,
        [string]$Code
    )
    if (-not $PythonRuntime.Command) {
        return [PSCustomObject]@{
            Status = 'FAIL'
            Detail = 'Python runtime is unavailable.'
        }
    }

    try {
        $output = & $PythonRuntime.Command @($PythonRuntime.PrefixArgs) -c $Code 2>&1 | Out-String
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

function Test-StorageWrite {
    param([string]$StorageDir)
    try {
        $probeFile = Join-Path $StorageDir 'doctor-write-test.tmp'
        Set-Content -Path $probeFile -Value 'ok' -Encoding UTF8
        Remove-Item $probeFile -Force
        return [PSCustomObject]@{
            Status = 'PASS'
            Detail = $StorageDir
        }
    } catch {
        return [PSCustomObject]@{
            Status = 'FAIL'
            Detail = $_.Exception.Message
        }
    }
}

function Test-OllamaEndpoint {
    param([string]$BaseUrl)
    if (-not $BaseUrl) {
        return [PSCustomObject]@{
            Status = 'FAIL'
            Detail = 'No Ollama base URL configured.'
        }
    }

    try {
        $tagsUrl = ($BaseUrl.TrimEnd('/')) + '/api/tags'
        $resp = Invoke-WebRequest -Uri $tagsUrl -UseBasicParsing -TimeoutSec 5
        if ($resp.StatusCode -ge 200 -and $resp.StatusCode -lt 300) {
            return [PSCustomObject]@{
                Status = 'PASS'
                Detail = $tagsUrl
                Content = $resp.Content
            }
        }
        return [PSCustomObject]@{
            Status = 'FAIL'
            Detail = $tagsUrl
            Content = $resp.Content
        }
    } catch {
        return [PSCustomObject]@{
            Status = 'FAIL'
            Detail = $_.Exception.Message
            Content = ''
        }
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
$requiredTemplates = @(
    'memory\config.template.yaml',
    'configs\data-access.template.yaml',
    'configs\evals.template.yaml',
    'configs\recovery.template.yaml',
    'configs\role-profiles.template.yaml',
    'configs\runtime-manifest.template.yaml'
)
$requiredRoleFiles = @(
    'codex\agents\router.md',
    'codex\agents\archivist.md',
    'codex\agents\researcher.md',
    'codex\agents\architect.md',
    'codex\agents\implementer.md',
    'codex\agents\reviewer.md',
    'codex\agents\tester.md',
    'codex\agents\test-strategist.md',
    'codex\agents\test-automation-engineer.md',
    'codex\agents\qa-browser.md'
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

$requiredTemplates + $requiredRoleFiles | ForEach-Object {
    $path = Join-Path $workspace $_
    $results.Add([PSCustomObject]@{
        Check = "support:$($_)"
        Status = if (Test-Path $path) { 'PASS' } else { 'FAIL' }
        Detail = $path
    })
}

$preferredLauncher = Read-RuntimeManifestLauncher -ManifestPath $runtimeManifestPath
$pythonExecution = Get-PythonRuntime -PreferredLauncher $preferredLauncher
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
    $ollamaBaseUrl = Read-ConfigValue -Content $config -Key 'base_url'
    $ollamaModel = Read-ConfigValue -Content $config -Key 'model'

    $results.Add([PSCustomObject]@{
        Check = 'config:memory-config'
        Status = 'PASS'
        Detail = $configPath
    })

    if ($vaultPath) {
        $results.Add([PSCustomObject]@{
            Check = 'config:vault-path'
            Status = if (Test-Path $vaultPath) { 'PASS' } else { 'FAIL' }
            Detail = $vaultPath
        })
    }

    if ($storageDir) {
        $results.Add([PSCustomObject]@{
            Check = 'config:storage-dir'
            Status = if (Test-Path $storageDir) { 'PASS' } else { 'FAIL' }
            Detail = $storageDir
        })

        $storageWrite = Test-StorageWrite -StorageDir $storageDir
        $results.Add([PSCustomObject]@{
            Check = 'storage-write'
            Status = $storageWrite.Status
            Detail = $storageWrite.Detail
        })

        try {
            $vectorDir = Join-Path $storageDir 'doctor-vector-open-test'
            New-Item -ItemType Directory -Force -Path $vectorDir | Out-Null
            Remove-Item $vectorDir -Force
            $results.Add([PSCustomObject]@{
                Check = 'vector-storage-open'
                Status = 'PASS'
                Detail = $storageDir
            })
        } catch {
            $results.Add([PSCustomObject]@{
                Check = 'vector-storage-open'
                Status = 'FAIL'
                Detail = $_.Exception.Message
            })
        }

        $sqliteSmoke = Invoke-PythonSnippet -PythonRuntime $pythonExecution -Code ("import sqlite3; p = r'{0}\doctor-sqlite-smoke.sqlite3'; conn = sqlite3.connect(p); conn.execute('create table if not exists t(x integer)'); conn.close(); print('sqlite-ok')" -f $storageDir)
        $results.Add([PSCustomObject]@{
            Check = 'sqlite-open'
            Status = $sqliteSmoke.Status
            Detail = $sqliteSmoke.Detail
        })

        $sqliteSmokePath = Join-Path $storageDir 'doctor-sqlite-smoke.sqlite3'
        if (Test-Path $sqliteSmokePath) {
            Remove-Item $sqliteSmokePath -Force -ErrorAction SilentlyContinue
        }
    }

    $endpointCheck = Test-OllamaEndpoint -BaseUrl $ollamaBaseUrl
    $results.Add([PSCustomObject]@{
        Check = 'embedding-endpoint'
        Status = $endpointCheck.Status
        Detail = $endpointCheck.Detail
    })

    $results.Add([PSCustomObject]@{
        Check = 'embedding-model'
        Status = if ($ollamaModel -and $endpointCheck.Content -match [regex]::Escape($ollamaModel)) { 'PASS' } else { 'FAIL' }
        Detail = if ($ollamaModel) { $ollamaModel } else { 'No model configured.' }
    })

    $agentNames = @('archivist', 'router', 'researcher', 'architect', 'implementer', 'reviewer', 'tester', 'test-strategist', 'test-automation-engineer', 'qa-browser')
    foreach ($agentName in $agentNames) {
        $present = [regex]::IsMatch($config, "(?m)^\s{2}$([regex]::Escape($agentName)):\s*$")
        $results.Add([PSCustomObject]@{
            Check = "agent-profile:$agentName"
            Status = if ($present) { 'PASS' } else { 'FAIL' }
            Detail = $configPath
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
    Status = if (Test-Path $runtimeManifestPath) { 'PASS' } else { 'FAIL' }
    Detail = $runtimeManifestPath
})

$results | Format-Table -AutoSize

$failed = @($results | Where-Object { $_.Status -eq 'FAIL' }).Count
if ($failed -gt 0) {
    Write-Error "Doctor failed. Fix required files or directories first."
}
