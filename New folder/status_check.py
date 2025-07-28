#!/usr/bin/env python3
"""
Quick status check to see what happened in the last run
"""

import os
from datetime import datetime

print("🔍 AUTOMATION STATUS CHECK")
print("=" * 50)

# Check if Excel file exists and is readable
try:
    import pandas as pd
    if os.path.exists("form_data.xlsx"):
        df = pd.read_excel("form_data.xlsx", engine='openpyxl')
        data = df.iloc[0]
        print("✅ Excel file is working!")
        print(f"📊 State value: {data['stateOrProvince']}")
        print(f"📧 Email: {data['Email Address']}")
    else:
        print("❌ Excel file not found")
except Exception as e:
    print(f"⚠️  Excel error: {e}")

# Check recent screenshots
screenshots_dir = "screenshots"
if os.path.exists(screenshots_dir):
    files = os.listdir(screenshots_dir)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(screenshots_dir, x)), reverse=True)
    
    print(f"\n📸 Recent screenshots (last 5):")
    for i, file in enumerate(files[:5]):
        if file.endswith('.png'):
            filepath = os.path.join(screenshots_dir, file)
            mtime = os.path.getmtime(filepath)
            timestamp = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            print(f"  {i+1}. {file} - {timestamp}")

print(f"\n🏁 Status check complete!")
print("💡 If you see recent screenshots, the automation ran!")
