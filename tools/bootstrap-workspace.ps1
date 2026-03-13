param(
    [string]$WorkspaceRoot = (Get-Location).Path,
    [string]$VaultDir = '',
    [string]$StorageDir = '',
    [string]$OllamaUrl = 'http://127.0.0.1:11434',
    [string]$ModelName = 'nomic-embed-text-v2-moe'
)

$ErrorActionPreference = 'Stop'

function Ensure-Dir {
    param([string]$Path)
    New-Item -ItemType Directory -Force -Path $Path | Out-Null
}

$workspace = (Resolve-Path $WorkspaceRoot).Path
if (-not $VaultDir) {
    $VaultDir = Join-Path $workspace 'obsidian-vault'
}
if (-not $StorageDir) {
    $StorageDir = Join-Path $workspace 'memory\data'
}

$dirs = @(
    $VaultDir,
    (Join-Path $VaultDir '.obsidian'),
    (Join-Path $VaultDir 'Inbox'),
    (Join-Path $VaultDir 'Conversations'),
    (Join-Path $VaultDir 'Important'),
    (Join-Path $VaultDir 'Projects'),
    (Join-Path $VaultDir 'Notes'),
    (Join-Path $VaultDir 'Agents'),
    (Join-Path $VaultDir 'Shared'),
    (Join-Path $VaultDir 'Decisions'),
    (Join-Path $VaultDir 'Logs'),
    (Join-Path $VaultDir 'Playbooks'),
    (Join-Path $workspace 'memory'),
    $StorageDir,
    (Join-Path $workspace 'configs')
)
foreach ($dir in $dirs) { Ensure-Dir $dir }

$templatePath = Join-Path $workspace 'memory\config.template.yaml'
$configPath = Join-Path $workspace 'memory\config.yaml'
if (-not (Test-Path $templatePath)) {
    throw "Template not found: $templatePath"
}

$template = Get-Content $templatePath -Raw
$template = $template.Replace('<YOUR_VAULT_PATH>', $VaultDir)
$template = $template.Replace('<YOUR_STORAGE_PATH>', $StorageDir)
$template = $template.Replace('<YOUR_OLLAMA_URL>', $OllamaUrl)
$template = $template.Replace('<YOUR_MODEL_NAME>', $ModelName)
if (-not (Test-Path $configPath)) {
    Set-Content -Path $configPath -Value $template -Encoding UTF8
}

$reportPath = Join-Path $workspace 'BOOTSTRAP_REPORT.md'
$lines = @(
    '# Bootstrap Report',
    '',
    "Generated at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')",
    '',
    '## Created or ensured',
    '',
    "- Workspace: $workspace",
    "- Vault: $VaultDir",
    "- Storage: $StorageDir",
    "- Memory config: $configPath",
    "- Ollama URL: $OllamaUrl",
    "- Model: $ModelName",
    '',
    '## Next steps',
    '',
    '- Open docs/AGENT_SYSTEM_OPERATIONS_DASHBOARD.md',
    '- Read docs/NEW_DEVICE_SETUP.md',
    '- Review docs/CODEX_BOOTSTRAP_PROMPT.md',
    '- Verify memory/config.yaml before first run',
    '- Keep production access disabled by default'
)
Set-Content -Path $reportPath -Value $lines -Encoding UTF8
Write-Output "Bootstrap complete. Report: $reportPath"
