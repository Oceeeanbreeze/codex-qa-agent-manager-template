param(
    [string]$WorkspaceRoot = (Get-Location).Path,
    [string]$ModelName = 'nomic-embed-text-v2-moe',
    [switch]$SkipPython,
    [switch]$SkipOllama,
    [switch]$SkipModel,
    [switch]$SkipRequirements
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

function Ensure-Winget {
    $winget = Test-CommandAvailable -Names @('winget')
    if (-not $winget) {
        throw 'winget is not available. Install Python and Ollama manually, then rerun this script with -SkipPython and/or -SkipOllama.'
    }
    return $winget
}

function Install-WithWinget {
    param(
        [string]$Id,
        [string]$Name
    )
    Write-Output "Installing $Name via winget..."
    & winget install --id $Id --accept-source-agreements --accept-package-agreements -e
}

$workspace = (Resolve-Path $WorkspaceRoot).Path
$requirementsPath = Join-Path $workspace 'requirements.txt'

if (-not $SkipPython) {
    $python = Test-CommandAvailable -Names @('py', 'python')
    if (-not $python) {
        Ensure-Winget | Out-Null
        Install-WithWinget -Id 'Python.Python.3.12' -Name 'Python 3.12'
    } else {
        Write-Output "Python launcher already available: $python"
    }
}

if (-not $SkipOllama) {
    $ollama = Test-CommandAvailable -Names @('ollama')
    if (-not $ollama) {
        Ensure-Winget | Out-Null
        Install-WithWinget -Id 'Ollama.Ollama' -Name 'Ollama'
    } else {
        Write-Output "Ollama already available: $ollama"
    }
}

$pythonCommand = Test-CommandAvailable -Names @('py', 'python')
if (-not $SkipRequirements -and (Test-Path $requirementsPath)) {
    if (-not $pythonCommand) {
        throw 'Python is still not available for requirements installation.'
    }
    if ((Split-Path $pythonCommand -Leaf).ToLower() -eq 'py.exe') {
        & py -3 -m pip install -r $requirementsPath
    } else {
        & $pythonCommand -m pip install -r $requirementsPath
    }
}

if (-not $SkipModel) {
    $ollama = Test-CommandAvailable -Names @('ollama')
    if (-not $ollama) {
        throw 'Ollama is still not available for model pull.'
    }
    Write-Output "Pulling embedding model: $ModelName"
    & ollama pull $ModelName
}

Write-Output 'Runtime prerequisites installation flow completed.'
