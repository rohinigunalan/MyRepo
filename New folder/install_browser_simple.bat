@echo off
echo Installing browsers for Playwright...
echo.

REM Method 1: Try pip install with browsers
pip install playwright[chromium]

echo.
echo Method 2: Installing browsers separately...
playwright install chromium

echo.
echo Method 3: Using Python module...
python -c "import subprocess; subprocess.run(['playwright', 'install', 'chromium'])"

echo.
echo Installation attempts completed!
echo Try running your test now.
pause
