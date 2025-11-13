@echo off
echo Setting up Playwright for Privacy Portal Testing...
echo.

REM Navigate to the project directory
cd /d "C:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\New folder"

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run setup verification
python setup_check.py

REM Keep window open
pause
