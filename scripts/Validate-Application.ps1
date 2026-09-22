[CmdletBinding()]
param(
    [string]$PythonPath,
    [switch]$SkipTests
)

$ErrorActionPreference = "Stop"

function Invoke-PythonCommand {
    param([string[]]$Arguments)

    & $script:PythonExecutable @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Python command failed with exit code ${LASTEXITCODE}: python $($Arguments -join ' ')"
    }
}

try {
    $projectRoot = Split-Path -Parent $PSScriptRoot

    if ($PythonPath) {
        $PythonExecutable = $PythonPath
    }
    else {
        $virtualEnvironmentCandidates = @(
            (Join-Path $projectRoot ".venv/Scripts/python.exe"),
            (Join-Path $projectRoot ".venv/bin/python")
        )
        $PythonExecutable = $virtualEnvironmentCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1

        if (-not $PythonExecutable) {
            $PythonExecutable = (Get-Command python -ErrorAction Stop).Source
        }
    }

    if (-not (Test-Path $PythonExecutable)) {
        throw "Python executable was not found: $PythonExecutable"
    }

    Write-Host "Using Python: $PythonExecutable"
    Invoke-PythonCommand @("--version")

    Push-Location $projectRoot
    try {
        Write-Host "Checking Python syntax..."
        Invoke-PythonCommand @("-m", "compileall", "-q", "app.py")

        if (-not $SkipTests) {
            Write-Host "Running tests..."
            Invoke-PythonCommand @("-m", "pytest", "-q")
        }
    }
    finally {
        Pop-Location
    }

    Write-Host "Application validation succeeded." -ForegroundColor Green
    exit 0
}
catch {
    Write-Error "Application validation failed: $($_.Exception.Message)"
    exit 1
}
