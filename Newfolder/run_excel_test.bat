@echo off
REM ================================================================
REM  OneTrust Privacy Portal Automation - Main Runner
REM ================================================================
REM 
REM 🚨 CRITICAL ENVIRONMENT NOTES:
REM 
REM PYTHON ENVIRONMENT SETUP:
REM - System Python: C:\Users\rgunalan\AppData\Local\anaconda3\python.exe (NO Playwright!)
REM - Virtual Env: .venv (HAS Playwright!) 
REM - Virtual Env Python: .venv\Scripts\python.exe
REM - Virtual Env Location: c:\users\rgunalan\onedrive - college board\documents\github\myrepo\new folder\.venv
REM 
REM INSTALLED PACKAGES IN VENV:
REM - playwright: v1.54.0 ✅
REM - pandas: For Excel/CSV reading ✅  
REM - openpyxl: For Excel file handling ✅
REM 
REM BROWSERS INSTALLED:
REM - Location: C:\Users\rgunalan\AppData\Local\ms-playwright\
REM - Chromium: v139.0.7258.5 (build v1181) ✅
REM - Firefox: v140.0.2 (build v1489) ✅  
REM - Webkit: v26.0 (build v2191) ✅
REM 
REM DATA FILES INFORMATION:
REM - Excel File: C:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\New folder\form_data.xlsx
REM - CSV File: C:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\New folder\form_data.csv
REM - File Size: 355 bytes each
REM - Last Modified: July 24, 2025, 11:49 PM
REM - Key Data: stateOrProvince="New York", Email="palmny1@mailinator.com"
REM - Content: 14 fields total (Email, Name, State, Address, Phone, etc.)
REM - Excel Engine: openpyxl (REQUIRED for reading .xlsx files)
REM 
REM DATA STRUCTURE:
REM Email Address,First_Name,Last_Name,birthDate,phone,country,stateOrProvince,
REM postalCode,city,streetAddress,studentSchoolName,studentGraduationYear,
REM educatorSchoolAffiliation,Request_type
REM 
REM CRITICAL ISSUES WE SOLVED:
REM 
REM 1. VIRTUAL ENVIRONMENT CRITICAL: 
REM    - Must activate .venv first (this script does it automatically)
REM    - System Python (Anaconda) doesn't have Playwright installed
REM    - NEVER run: python test_with_excel.py (uses wrong Python!)
REM    - ALWAYS run: .\run_excel_test.bat (activates venv first)
REM 
REM 2. EXCEL FILE ISSUES:
REM    - If you get "File is not a zip file" error, run: python fix_excel.py
REM    - Scripts auto-fallback to CSV file if Excel corrupted
REM    - MUST use engine='openpyxl' when reading Excel files
REM 
REM 3. BROWSER SETUP:
REM    - If no browser opens, run: .\setup_browsers.bat (one time)
REM    - Browsers must be installed in virtual environment
REM    - Browser location: C:\Users\rgunalan\AppData\Local\ms-playwright\
REM 
REM 4. STATE SELECTION:
REM    - Uses improved approach: click → clear → type "New York" → select option
REM    - Multiple fallback methods for dropdown selection
REM    - Don't overcomplicate the dropdown interaction
REM 
REM 5. POWERSHELL SYNTAX:
REM    - WRONG: \run_excel_test.bat
REM    - RIGHT: .\run_excel_test.bat (note the dot!)
REM 
REM TROUBLESHOOTING CHECKLIST:
REM - [ ] Virtual environment activated? (this script does it)
REM - [ ] Using .\ syntax in PowerShell?
REM - [ ] Excel file readable or CSV fallback working?
REM - [ ] Browsers installed in virtual environment?
REM - [ ] State selection using improved logic?
REM 
REM SUCCESS INDICATORS:
REM - ✅ "Virtual environment activated!"
REM - ✅ "Successfully loaded CSV file!" (or Excel)
REM - ✅ Browser window opens
REM - ✅ "Successfully selected 'New York'"  
REM - ✅ "Thank you for your interest in submitting..."
REM 
REM ================================================================

echo ========================================
echo    Privacy Portal Test with Excel Data
echo ========================================
echo.
echo 🔧 Activating virtual environment...
echo 💡 CRITICAL: Using .venv (NOT system Python!)

REM CRITICAL: Activate virtual environment first
REM This ensures we use Python with Playwright installed
call .venv\Scripts\activate.bat

if errorlevel 1 (
    echo ❌ Failed to activate virtual environment!
    echo 💡 Make sure .venv folder exists
    echo 💡 If missing, recreate with: python -m venv .venv
    echo 💡 Then install: pip install playwright pandas openpyxl
    echo 💡 Then install browsers: python -m playwright install
    pause
    exit /b 1
)

echo ✅ Virtual environment activated!
echo 💡 Now using: .venv\Scripts\python.exe
echo.
echo 🚀 Running automation with Excel data...
echo 💡 Data source: form_data.xlsx (fallback: form_data.csv)
echo 💡 Target: OneTrust Privacy Portal
echo 💡 State: New York (improved selection logic)
echo.

python test_with_excel.py

echo.
echo ========================================
echo Test with Excel data completed!
echo ========================================
echo.
echo 💡 Check screenshots/ folder for results
echo 💡 If issues occurred, see SETUP_NOTES.md or PYTHON_ENV_NOTES.md
echo 💡 For environment details, see comments in this batch file
pause
