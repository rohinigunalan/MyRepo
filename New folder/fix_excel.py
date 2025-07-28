#!/usr/bin/env python3
"""
Fix the corrupted Excel file by recreating it from CSV data
"""

import pandas as pd
import os

print("🔧 Fixing Excel file...")

try:
    # Read from CSV first
    if os.path.exists("form_data.csv"):
        print("📊 Reading data from CSV...")
        df = pd.read_csv("form_data.csv")
        
        print("✅ CSV data loaded:")
        print(df.iloc[0].to_dict())
        
        # Create new Excel file
        print("\n💾 Creating new Excel file...")
        df.to_excel("form_data.xlsx", index=False, engine='openpyxl')
        
        print("✅ New Excel file created successfully!")
        
        # Test reading the new Excel file
        print("\n🧪 Testing the new Excel file...")
        test_df = pd.read_excel("form_data.xlsx", engine='openpyxl')
        print("✅ Excel file reads correctly!")
        print("📋 Excel data:")
        print(test_df.iloc[0].to_dict())
        
    else:
        print("❌ CSV file not found!")

except Exception as e:
    print(f"❌ Error: {str(e)}")
