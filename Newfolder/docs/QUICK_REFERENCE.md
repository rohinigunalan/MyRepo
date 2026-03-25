# 🚀 QUICK REFERENCE CARD - OneTrust Automation

## 📋 ENVIRONMENT ESSENTIALS

### 🐍 Python Paths:
- **System**: `C:\Users\rgunalan\AppData\Local\anaconda3\python.exe` ❌ (No Playwright)
- **Virtual**: `.venv\Scripts\python.exe` ✅ (Has Playwright)

### 🌐 Browser Location:
`C:\Users\rgunalan\AppData\Local\ms-playwright\`

### 📦 Key Packages:
- playwright: v1.54.0
- pandas: Excel/CSV handling  
- openpyxl: Excel engine

## ⚡ QUICK COMMANDS

### 🏃‍♂️ Run Automation:
```powershell
.\run_excel_test.bat
```

### 🔧 One-Time Setup:
```powershell
.\setup_browsers.bat
```

### 🔄 Fix Excel Issues:
```powershell
python fix_excel.py
```

### 👨‍👩‍👧‍👦 Domestic Parent Automation (Records 20+):
```powershell
.\.venv\Scripts\python.exe -m pytest "dsr\scripts\Domestic_Parent_requesttypes_submission_MULTIPLE.py::TestPrivacyPortal::test_privacy_form_submission" -v -s
```

## 🚨 COMMON ERRORS & FIXES

| Error | Fix |
|-------|-----|
| "No module named playwright" | Use `.\run_excel_test.bat` (not direct python) |
| "File is not a zip file" | Run `python fix_excel.py` |
| No browser opens | Run `.\setup_browsers.bat` |
| State field blank | Using improved selection logic ✅ |
| PowerShell syntax error | Use `.\` not `\` |

## ✅ SUCCESS CHECKLIST

- [ ] Run `.\run_excel_test.bat`
- [ ] See "Virtual environment activated!"
- [ ] Excel/CSV data loads successfully
- [ ] Browser opens to OneTrust portal
- [ ] Form fills with Excel data
- [ ] "New York" selected correctly
- [ ] Success message appears

## 📁 File Structure
```
├── .venv\                   # Virtual environment (CRITICAL)
├── run_excel_test.bat       # Main runner ⭐
├── test_with_excel.py       # Data loader
├── test_privacy_portal.py   # Core automation
├── form_data.xlsx          # Input data
├── form_data.csv           # Backup data
└── screenshots\            # Results
```

**Remember**: Always use `.\run_excel_test.bat` - it handles everything! 🎯
