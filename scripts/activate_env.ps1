# activate_env.ps1
Write-Host "Activating virtual environment..."
$venvPath = "venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    & $venvPath
} else {
    Write-Host "Virtual environment not found. Please run setup_env.py first."
}
