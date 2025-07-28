#!/usr/bin/env python3
"""
Display Excel data and run privacy portal test

🚨 CRITICAL ENVIRONMENT NOTES:
- This script MUST run in virtual environment (.venv)
- System Python (Anaconda) does NOT have Playwright
- Virtual env location: .venv\\Scripts\\python.exe
- Packages in venv: playwright v1.54.0, pandas, openpyxl
- Browsers: Chromium v139.0.7258.5, Firefox v140.0.2, Webkit v26.0
- Browser location: C:\\Users\\rgunalan\\AppData\\Local\\ms-playwright\\

USAGE:
- Run via: .\run_excel_test.bat (activates venv automatically)
- Never run: python test_with_excel.py (uses wrong Python!)

DATA SOURCES:
- Primary: form_data.xlsx (with engine='openpyxl')
- Fallback: form_data.csv (auto-fallback if Excel corrupted)

AUTOMATION TARGET:
- OneTrust Privacy Portal form automation
- State selection: "New York" with improved dropdown logic
- Success indicator: "Thank you for your interest in submitting..."
"""

import pandas as pd
import os
import sys

# Environment verification
print("🔍 Environment Check:")
print(f"📍 Python executable: {sys.executable}")
if ".venv" in sys.executable:
    print("✅ Using virtual environment (.venv)")
else:
    print("⚠️  WARNING: Not using virtual environment!")
    print("💡 This may cause 'No module named playwright' errors")

# File location verification
print("\n📁 Data Files Check:")
excel_path = os.path.abspath("form_data.xlsx")
csv_path = os.path.abspath("form_data.csv")
print(f"📊 Excel file: {excel_path}")
print(f"📄 CSV file: {csv_path}")

if os.path.exists("form_data.xlsx"):
    size = os.path.getsize("form_data.xlsx")
    mtime = os.path.getmtime("form_data.xlsx")
    import datetime
    mod_time = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
    print(f"✅ Excel exists: {size} bytes, modified {mod_time}")
else:
    print("❌ Excel file not found")

if os.path.exists("form_data.csv"):
    size = os.path.getsize("form_data.csv")
    mtime = os.path.getmtime("form_data.csv")
    mod_time = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
    print(f"✅ CSV exists: {size} bytes, modified {mod_time}")
else:
    print("❌ CSV file not found")
print()

print("📊 Reading data from form_data files...")
print("=" * 50)

try:
    # Try Excel first, then CSV as fallback
    if os.path.exists("form_data.xlsx"):
        try:
            df = pd.read_excel("form_data.xlsx", engine='openpyxl')
            data = df.iloc[0].to_dict()
            print("✅ Successfully loaded Excel file!")
        except Exception as excel_error:
            print(f"⚠️  Excel file error: {excel_error}")
            print("🔄 Falling back to CSV file...")
            if os.path.exists("form_data.csv"):
                df = pd.read_csv("form_data.csv")
                data = df.iloc[0].to_dict()
                print("✅ Successfully loaded CSV file!")
            else:
                raise FileNotFoundError("Neither Excel nor CSV file found!")
    elif os.path.exists("form_data.csv"):
        df = pd.read_csv("form_data.csv")
        data = df.iloc[0].to_dict()
        print("✅ Successfully loaded CSV file!")
    else:
        print("❌ Neither form_data.xlsx nor form_data.csv file found!")
        print("� Please make sure at least one data file exists in the current directory.")
        raise FileNotFoundError("No data files found!")
        
    # Display the data that will be used
    print("\n📋 Data that will be used in the form:")
    print("-" * 40)
    for key, value in data.items():
        print(f"  {key}: {value}")
    
    print("\n🎯 Key field for state selection:")
    print(f"  stateOrProvince: {data.get('stateOrProvince', 'NOT FOUND')}")
    
    print("\n" + "=" * 50)
    print("🚀 Now running privacy portal test with this data...")
    print("=" * 50)
    
    # Import and run the test
    from inforequest_submission import TestPrivacyPortal
    
    test = TestPrivacyPortal()
    test.setup_method()  # Call setup method to initialize url and form_data
    test.test_privacy_form_submission()
    
    print("\n✅ Test completed! Check the browser and screenshots folder.")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")

print("\n🏁 Script completed!")
