# 📋 OneTrust Privacy Portal Automation - IMPORTANT NOTES!

## 🚨 CRITICAL SETUP REMINDERS - READ BEFORE EVERY RUN!

### ⚠️ Key Issues We Solved (Remember These!):

1. **Excel File Corruption**: "File is not a zip file" error
   - **Solution**: Scripts auto-fallback to CSV file
   - **Fix**: Always use `engine='openpyxl'` when reading Excel

2. **Virtual Environment Critical**: MUST use `.venv`, NOT system Python
   - **Problem**: System Python (Anaconda) lacks Playwright
   - **Solution**: All batch files now activate venv first

3. **Browser Installation**: Must install in virtual environment
   - **Problem**: Browsers installed in wrong Python environment
   - **Solution**: Run `.\setup_browsers.bat` first time

4. **State Selection**: Simple approach works best
   - **Solution**: click → clear → type "New York" → Enter

---

## 🚀 COMMANDS TO RUN (In Order):

### 🔧 First Time Setup:
```batch
.\setup_browsers.bat    # Install browsers in venv
python fix_excel.py     # Fix Excel corruption
.\run_excel_test.bat    # Run automation
```

### 🔄 Regular Use:
```batch
.\run_excel_test.bat    # Just run this!
```

---

## 📁 KEY FILES & WHAT THEY DO:

- **run_excel_test.bat** - Main script (auto-activates venv)
- **test_with_excel.py** - Shows Excel data + runs automation  
- **test_privacy_portal.py** - Core automation with clean state selection
- **form_data.xlsx** - Input data (auto-falls back to CSV if corrupt)
- **setup_browsers.bat** - One-time browser installation
- **fix_excel.py** - Fixes Excel corruption issues

---

## 🎯 STATE SELECTION (Current Working Method):

**Clean Simple Approach**:
1. Click state dropdown
2. Clear existing text  
3. Type "New York"
4. Press Enter

**Why This Works**: No complex keyboard navigation, reliable

---

## 🔧 TROUBLESHOOTING GUIDE:

| Error | Cause | Fix |
|-------|-------|-----|
| "No module named playwright" | Wrong Python environment | Use batch files (auto-activate venv) |
| "File is not a zip file" | Excel corruption | Run `python fix_excel.py` |
| No browser opens | Browsers not installed | Run `.\setup_browsers.bat` |
| State selection fails | Complex dropdown logic | Using simple approach now |

---

## 📊 FORM DATA BEING FILLED:

- **Email**: palmny1@mailinator.com
- **Name**: RobNY EdisonNY  
- **State**: New York (critical field)
- **Address**: 507 Central Avenue, North Collins, NY 14111
- **Request Type**: Request a copy of my data

---

## ✅ SUCCESS CHECKLIST:

□ Excel data displays without errors  
□ Browser window opens and navigates to form  
□ All form fields get filled correctly  
□ State dropdown shows "New York"  
□ Form submits successfully  
□ Screenshots saved in screenshots/ folder  

---

## 🚨 REMEMBER FOR NEXT TIME:

1. **Virtual Environment is CRITICAL** - Never use system Python
2. **Excel fallback to CSV** - Don't worry if Excel corrupts
3. **Simple state selection** - Don't overcomplicate dropdown
4. **Browser setup once** - Then just run main script
5. **Check screenshots** - Visual confirmation automation worked

---

## 📞 QUICK REFERENCE:

```batch
# If starting fresh
.\setup_browsers.bat

# If Excel broken  
python fix_excel.py

# Normal run
.\run_excel_test.bat

# Quick browser test
python simple_test.py
```

**Status**: ✅ Working with all major issues resolved  
**Last Updated**: January 2025  
**Key Fix**: Virtual environment activation in all batch files
