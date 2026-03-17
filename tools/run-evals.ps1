param(
    [string]$ConfigPath = '.\configs\evals.local.yaml',
    [switch]$Strict
)

$ErrorActionPreference = 'Stop'

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

function Resolve-PythonCommand {
    param([string]$PreferredLauncher)

    $candidates = @()
    foreach ($envVar in @('CODEX_PYTHON', 'PYTHON', 'PYTHON_EXECUTABLE')) {
        $raw = [Environment]::GetEnvironmentVariable($envVar)
        if (-not $raw) { continue }
        $tokens = $raw -split '\s+'
        if ($tokens.Count -gt 0) {
            $candidates += ,@($tokens[0], @($tokens[1..($tokens.Count - 1)]))
        }
    }

    if ($PreferredLauncher) {
        $tokens = $PreferredLauncher -split '\s+'
        if ($tokens.Count -gt 0) {
            $prefixArgs = @()
            if ($tokens.Count -gt 1) {
                $prefixArgs = @($tokens[1..($tokens.Count - 1)])
            }
            $candidates += ,@($tokens[0], $prefixArgs)
        }
    }

    $candidates += ,@('python', @())
    $candidates += ,@('py', @('-3'))

    foreach ($candidate in $candidates) {
        $exe = $candidate[0]
        $args = @($candidate[1])
        $resolved = $null
        if (Test-Path $exe) {
            $resolved = (Resolve-Path $exe).Path
        } else {
            $cmd = Get-Command $exe -ErrorAction SilentlyContinue
            if ($cmd) {
                $resolved = $cmd.Source
            }
        }
        if (-not $resolved) { continue }
        try {
            & $resolved @args --version *> $null
            if ($LASTEXITCODE -eq 0) {
                return [PSCustomObject]@{
                    Command = $resolved
                    PrefixArgs = $args
                }
            }
        } catch {
            continue
        }
    }

    throw 'Unable to locate a usable Python launcher for run-evals.'
}

$workspaceRoot = (Get-Location).Path
$manifestPath = Join-Path $workspaceRoot 'configs\runtime-manifest.local.yaml'
$preferredLauncher = Read-RuntimeManifestLauncher -ManifestPath $manifestPath
$python = Resolve-PythonCommand -PreferredLauncher $preferredLauncher
$scriptPath = Join-Path $workspaceRoot 'memory\scripts\run_evals.py'
$resolvedConfig = Resolve-Path $ConfigPath -ErrorAction SilentlyContinue

if (-not $resolvedConfig) {
    throw "Evals config not found: $ConfigPath"
}

$command = @(
    $python.Command
) + $python.PrefixArgs + @(
    $scriptPath,
    '--config',
    $resolvedConfig.Path
)

if ($Strict) {
    $command += '--strict'
}

& $command[0] @($command[1..($command.Count - 1)])
exit $LASTEXITCODE
