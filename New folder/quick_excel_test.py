#!/usr/bin/env python3
"""
Quick test to verify Excel file is working
"""

import pandas as pd
import os

print("🧪 Quick Excel Test")
print("=" * 30)

try:
    if os.path.exists("form_data.xlsx"):
        print("📁 Excel file exists")
        df = pd.read_excel("form_data.xlsx", engine='openpyxl')
        data = df.iloc[0].to_dict()
        print("✅ Excel file reads successfully!")
        print(f"🎯 State value: {data.get('stateOrProvince')}")
        print("📋 All data keys:", list(data.keys()))
    else:
        print("❌ Excel file not found")
        
    if os.path.exists("form_data.csv"):
        print("📁 CSV file exists")
        df_csv = pd.read_csv("form_data.csv")
        data_csv = df_csv.iloc[0].to_dict()
        print("✅ CSV file reads successfully!")
        print(f"🎯 State value from CSV: {data_csv.get('stateOrProvince')}")
    else:
        print("❌ CSV file not found")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")

print("\n🏁 Test complete!")
