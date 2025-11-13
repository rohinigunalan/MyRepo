@echo off
echo ===============================================
echo   Privacy Portal Test - Quick Start
echo ===============================================
echo.

cd /d "%~dp0"

echo Step 1: Activating Python environment...
call .venv\Scripts\activate.bat

echo.
echo Step 2: Installing Playwright browsers (this may take a few minutes)...
python -m playwright install chromium

echo.
echo Step 3: Running simple test...
python simple_test.py

echo.
echo Step 4: Running privacy portal test...
python inforequest_submission.py

echo.
echo Test completed! Check the screenshots in this folder.
pause
