@echo off
REM ========================================
REM   Dynamic Request Types Test 
REM ========================================
echo.
echo ========================================
echo    Dynamic Request Types Automation
echo ========================================
echo.
echo 🎯 This script uses Request_type from Excel to automatically
echo    select the appropriate form option dynamically!
echo.
echo 📊 Current Excel Request_type: 
.venv\Scripts\python.exe -c "import pandas as pd; df = pd.read_excel('form_data.xlsx', engine='openpyxl'); print(f'   {df.iloc[0][\"Request_type\"]}')"
echo.
echo 🚀 Activating virtual environment...
echo 📍 CRITICAL: Using .venv (NOT system Python!)
echo.
echo 💡 Data source: form_data.xlsx (fallback: form_data.csv)
echo 💡 Target: OneTrust Privacy Portal  
echo 💡 Dynamic selection: Based on Request_type field
echo.

REM Activate virtual environment and run test
.venv\Scripts\python.exe run_dynamic_request_test.py

echo.
echo ========================================
echo Dynamic request types test completed!
echo ========================================
echo 📍 Check screenshots/ folder for results
echo 📍 If issues occurred, see SETUP_NOTES.md or PYTHON_ENV_NOTES.md
echo 📍 For environment details, see comments in this batch file
pause
