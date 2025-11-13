# Privacy Portal Test Automation with Playwright

This project provides automated testing for the OneTrust Privacy Portal using Playwright and Python.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.12+ (already configured in your virtual environment)
- VS Code
- Windows PowerShell

### 2. Installation Steps

The Python environment and packages are already set up. To install Playwright browsers:

**Option A: Using PowerShell Script**
```powershell
# Run this in PowerShell
.\install_browsers.ps1
```

**Option B: Manual Installation**
```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install browsers
python -m playwright install
```

### 3. Running Tests

**Option A: Simple Python Script**
```bash
python run_test.py
```

**Option B: Using pytest**
```bash
pytest test_privacy_portal.py -v
```

**Option C: Direct test execution**
```bash
python test_privacy_portal.py
```

## 📋 Test Features

### What the test does:
1. **Form Inspection**: Automatically discovers form elements on the page
2. **Data Entry**: Fills out the privacy portal form with test data from your JSON
3. **Screenshots**: Captures screenshots before and after form submission
4. **Error Handling**: Takes screenshots on errors for debugging

### Test Data (from your JSON):
- First Name: Gerlyn
- Last Name: Figueroa
- Email: testdsremail@cbreston.org
- Phone: 800-867-5309
- Birth Date: 09/22/2007
- Address: 4435 W Avalon Ave, Fresno, CA 93722
- Alternate Email: zzikyepez@epsilon.cbreston.org

---

**Ready to test!** 🎯 Run `python run_test.py` to get started.

## Original Python Project

### How to Run

1. Make sure you have Python installed.
2. Run the following command in your terminal:

```
python hello.py
```
