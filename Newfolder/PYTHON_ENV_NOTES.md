# 🐍 PYTHON ENVIRONMENT & PATH SETUP NOTES

## 🚨 CRITICAL ENVIRONMENT INFORMATION

### 📍 Python Environment Details:
- **System Python**: `C:\Users\rgunalan\AppData\Local\anaconda3\python.exe` (Anaconda)
- **Virtual Environment**: `.venv` (THIS IS WHAT WE MUST USE!)
- **Virtual Environment Python**: `.venv\Scripts\python.exe`
- **Virtual Environment Location**: `c:\users\rgunalan\onedrive - college board\documents\github\myrepo\new folder\.venv`

### ⚠️ CRITICAL ISSUE WE SOLVED:
**Problem**: System Python (Anaconda) does NOT have Playwright installed
**Solution**: ALWAYS use virtual environment `.venv` which HAS Playwright installed

### 🔧 Environment Activation:
```batch
REM In batch files:
call .venv\Scripts\activate.bat

REM In PowerShell:
.venv\Scripts\Activate.ps1
```

### 📦 Installed Packages in Virtual Environment:
- **playwright**: v1.54.0 ✅
- **pandas**: For Excel/CSV reading ✅  
- **openpyxl**: For Excel file handling ✅
- **pyee**: v13.0.0 (Playwright dependency) ✅
- **greenlet**: v3.2.3 (Playwright dependency) ✅

### 🌐 Browser Installation:
- **Location**: `C:\Users\rgunalan\AppData\Local\ms-playwright\`
- **Chromium**: v139.0.7258.5 (build v1181) ✅
- **Firefox**: v140.0.2 (build v1489) ✅  
- **Webkit**: v26.0 (build v2191) ✅

### 🚨 COMMON MISTAKES TO AVOID:

1. **Using System Python**: 
   - ❌ `python script.py` (uses Anaconda without Playwright)
   - ✅ Activate venv first, then run

2. **PowerShell Syntax**:
   - ❌ `\run_excel_test.bat` 
   - ✅ `.\run_excel_test.bat`

3. **Excel File Issues**:
   - Problem: "File is not a zip file" 
   - Solution: Scripts auto-fallback to CSV

### 🎯 WORKING COMMAND SEQUENCE:
```batch
# Activate virtual environment
call .venv\Scripts\activate.bat

# Run automation  
python test_with_excel.py
```

### 📁 Project Structure:
```
Project Root: c:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\New folder\
├── .venv\                    # Virtual environment (CRITICAL!)
├── form_data.xlsx           # Input data (355 bytes, July 24 2025 11:49 PM)
├── form_data.csv            # Backup data file (355 bytes, July 24 2025 11:49 PM)
├── run_excel_test.bat       # Main runner (auto-activates venv)
├── test_with_excel.py       # Data loader & test runner
├── test_privacy_portal.py   # Core automation logic
├── setup_browsers.bat       # One-time browser installation
└── screenshots\             # Output screenshots
```

### 📊 Data Files Details:
- **Excel File**: `C:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\New folder\form_data.xlsx`
- **CSV File**: `C:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\New folder\form_data.csv`
- **Size**: 355 bytes each
- **Key Data**: stateOrProvince = "New York", Email = palmny1@mailinator.com
- **Content**: Complete OneTrust form data (14 fields)

### 🔄 Environment Verification Commands:
```python
# Check if in virtual environment
import sys
print(sys.executable)
# Should show: .venv\Scripts\python.exe

# Check Playwright installation
from playwright.sync_api import sync_playwright
print("Playwright working!")
```

### 📝 AUTOMATION WORKFLOW:
1. **Activate venv** → `.venv\Scripts\activate.bat`
2. **Load data** → Excel/CSV with `engine='openpyxl'`
3. **Launch browser** → Chromium from `.venv` environment
4. **Fill form** → OneTrust Privacy Portal
5. **Select state** → Improved "New York" selection
6. **Submit** → Success confirmation

### 🚨 TROUBLESHOOTING CHECKLIST:
- [ ] Virtual environment activated?
- [ ] Using `.\` syntax in PowerShell?
- [ ] Excel file readable or CSV fallback working?
- [ ] Browsers installed in virtual environment?
- [ ] State selection using improved logic?

### 🎉 SUCCESS INDICATORS:
- ✅ "Virtual environment activated!"
- ✅ "Successfully loaded CSV file!" (or Excel)
- ✅ Browser window opens
- ✅ "Successfully selected 'New York'"
- ✅ "Thank you for your interest in submitting..."

---
**Last Updated**: January 2025
**Status**: Fully Working with Virtual Environment Setup
