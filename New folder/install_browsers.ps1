# PowerShell script to install Playwright browsers
Write-Host "Installing Playwright browsers..." -ForegroundColor Green

# Navigate to the project directory
Set-Location "C:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\New folder"

# Activate virtual environment and install browsers
& ".\.venv\Scripts\Activate.ps1"
python -m playwright install

Write-Host "Playwright browsers installation completed!" -ForegroundColor Green
