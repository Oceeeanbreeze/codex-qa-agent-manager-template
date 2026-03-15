param(
    [string]$WorkspaceRoot = (Get-Location).Path
)

$ErrorActionPreference = 'Stop'

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

$workspace = (Resolve-Path $WorkspaceRoot).Path
$configPath = Join-Path $workspace 'memory\config.yaml'
if (-not (Test-Path $configPath)) {
    throw "Missing config: $configPath"
}

$config = Get-Content $configPath -Raw
$vaultPath = Read-ConfigValue -Content $config -Key 'vault_path'
$storageDir = Read-ConfigValue -Content $config -Key 'storage_dir'
$ollamaBaseUrl = Read-ConfigValue -Content $config -Key 'base_url'
$ollamaModel = Read-ConfigValue -Content $config -Key 'model'

$checks = [System.Collections.Generic.List[object]]::new()
$checks.Add([PSCustomObject]@{
    Check = 'config-load'
    Status = 'PASS'
    Detail = $configPath
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
            Status = 'WARN'
            Detail = $_.Exception.Message
        })
    }
}

$checks | Format-Table -AutoSize

$failed = @($checks | Where-Object { $_.Status -eq 'FAIL' }).Count
if ($failed -gt 0) {
    Write-Error 'Health check failed.'
}
