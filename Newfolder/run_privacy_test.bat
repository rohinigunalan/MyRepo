@echo off
echo =============================================
echo Privacy Portal Test Runner
echo =============================================
echo.
echo Changing to project directory...
cd /d "c:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\New folder"
echo Current directory: %CD%
echo.
echo Checking if virtual environment exists...
if exist ".\.venv\Scripts\activate.bat" (
    echo Virtual environment found!
    echo Activating Python virtual environment...
    call .\.venv\Scripts\activate.bat
    echo Virtual environment activated!
) else (
    echo ERROR: Virtual environment not found at .\.venv\Scripts\activate.bat
    echo Please check if the virtual environment is properly set up.
    pause
    exit /b 1
)
echo.
echo Checking if test file exists...
if exist "inforequest_submission.py" (
    echo Test file found!
    echo Running privacy portal test...
    python inforequest_submission.py
) else (
    echo ERROR: inforequest_submission.py not found in current directory
    echo Current directory contents:
    dir /b *.py
    pause
    exit /b 1
)
echo.
echo Test completed!
pause
