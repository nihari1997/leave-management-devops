[CmdletBinding()]
param(
    [string]$BaseUrl = "http://127.0.0.1:5050",
    [ValidateRange(1, 10)]
    [int]$RetryCount = 3,
    [ValidateRange(1, 60)]
    [int]$RetryDelaySeconds = 2
)

$ErrorActionPreference = "Stop"
$healthUrl = "$($BaseUrl.TrimEnd('/'))/api/health"

for ($attempt = 1; $attempt -le $RetryCount; $attempt++) {
    try {
        Write-Host "Health-check attempt $attempt of ${RetryCount}: $healthUrl"
        $response = Invoke-RestMethod -Uri $healthUrl -Method Get -TimeoutSec 5

        if ($response.status -ne "healthy") {
            throw "Unexpected health status: $($response.status)"
        }

        Write-Host "Application is healthy." -ForegroundColor Green
        exit 0
    }
    catch {
        if ($attempt -eq $RetryCount) {
            Write-Error "Health check failed after ${RetryCount} attempt(s): $($_.Exception.Message)"
            exit 1
        }

        Write-Warning "Health check failed: $($_.Exception.Message). Retrying in $RetryDelaySeconds second(s)."
        Start-Sleep -Seconds $RetryDelaySeconds
    }
}
