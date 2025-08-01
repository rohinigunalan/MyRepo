#!/usr/bin/env python3
"""
Quick script to check the structure of International_Parent_form_data.xlsx
"""

import pandas as pd
import os

def check_excel_structure():
    # Check the International Parent Excel file
    excel_file = "dsr/data/International_Parent_form_data.xlsx"
    
    print(f"🔍 Checking Excel file: {excel_file}")
    
    if not os.path.exists(excel_file):
        print(f"❌ File not found: {excel_file}")
        
        # List what files are actually in the data directory
        data_dir = "dsr/data"
        if os.path.exists(data_dir):
            print(f"\n📂 Files in {data_dir}:")
            for file in os.listdir(data_dir):
                print(f"  - {file}")
        else:
            print(f"❌ Data directory not found: {data_dir}")
        
        # Also check root directory for any Excel files
        print(f"\n📂 Excel files in current directory:")
        for file in os.listdir("."):
            if file.endswith(('.xlsx', '.xls')):
                print(f"  - {file}")
        
        return
    
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file, engine='openpyxl')
        
        print(f"✅ File loaded successfully!")
        print(f"📊 Rows: {len(df)}, Columns: {len(df.columns)}")
        
        print(f"\n📋 Column names (exact):")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. '{col}'")
        
        print(f"\n📝 First 3 rows of data:")
        print(df.head(3).to_string())
        
        print(f"\n📞 Phone-related columns:")
        phone_cols = [col for col in df.columns if 'phone' in col.lower()]
        if phone_cols:
            for col in phone_cols:
                print(f"  - '{col}'")
                # Show sample values
                sample_values = df[col].head(3).tolist()
                print(f"    Sample values: {sample_values}")
        else:
            print("  No phone columns found")
        
        print(f"\n🗽 State-related columns:")
        state_cols = [col for col in df.columns if 'state' in col.lower()]
        if state_cols:
            for col in state_cols:
                print(f"  - '{col}'")
                # Show sample values
                sample_values = df[col].head(3).tolist()
                print(f"    Sample values: {sample_values}")
        else:
            print("  No state columns found")
        
        print(f"\n🌍 Country-related columns:")
        country_cols = [col for col in df.columns if 'country' in col.lower()]
        if country_cols:
            for col in country_cols:
                print(f"  - '{col}'")
                # Show sample values
                sample_values = df[col].head(3).tolist()
                print(f"    Sample values: {sample_values}")
        else:
            print("  No country columns found")
        
        print(f"\n📧 Email-related columns:")
        email_cols = [col for col in df.columns if 'email' in col.lower()]
        if email_cols:
            for col in email_cols:
                print(f"  - '{col}'")
                # Show sample values
                sample_values = df[col].head(3).tolist()
                print(f"    Sample values: {sample_values}")
        else:
            print("  No email columns found")
        
        print(f"\n📋 All column data types:")
        print(df.dtypes)
        
        # Check for NaN values
        print(f"\n🔍 NaN/missing value check:")
        for col in df.columns:
            nan_count = df[col].isna().sum()
            if nan_count > 0:
                print(f"  '{col}': {nan_count} missing values")
        
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")

if __name__ == "__main__":
    check_excel_structure()
