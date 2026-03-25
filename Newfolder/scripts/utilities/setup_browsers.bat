@echo off
echo ========================================
echo    Activating Virtual Environment
echo ========================================
echo.

REM Activate the virtual environment
call .venv\Scripts\activate.bat

echo Virtual environment activated!
echo.

echo ========================================
echo    Installing Playwright Browsers
echo ========================================
echo.

REM Install playwright in the virtual environment
python -m pip install playwright

echo.
echo Installing browsers...
python -m playwright install

echo.
echo ========================================
echo    Testing Browser Installation
echo ========================================
echo.

REM Test the browser
python simple_test.py

echo.
echo ========================================
echo Browser setup completed!
echo ========================================
pause
