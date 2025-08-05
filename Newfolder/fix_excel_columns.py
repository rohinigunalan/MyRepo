#!/usr/bin/env python3
"""
Script to fix column names in the Excel file to match what the automation script expects
"""

import pandas as pd
import os
from datetime import datetime

def fix_excel_columns():
    """Fix column names in the Excel file"""
    print("🔧 FIXING EXCEL COLUMN NAMES...")
    
    # Excel file path
    excel_file = r"C:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\Newfolder\dsr\data\Domestic_Parent_form_data.xlsx"
    backup_file = r"C:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\Newfolder\dsr\data\Domestic_Parent_form_data_BACKUP.xlsx"
    
    try:
        # Read the current Excel file
        print(f"📂 Reading Excel file: {excel_file}")
        df = pd.read_excel(excel_file, engine='openpyxl', na_filter=False, keep_default_na=False, dtype=str)
        
        print(f"📊 Loaded {len(df)} records")
        print(f"📋 Current columns: {list(df.columns)}")
        
        # Create backup first
        print(f"💾 Creating backup: {backup_file}")
        df.to_excel(backup_file, index=False, engine='openpyxl')
        print("✅ Backup created successfully!")
        
        # Fix column names
        column_mapping = {
            ' Date of Birth': 'Date of Birth',  # Remove leading space
            'Phone Number': 'phone',            # Change to expected name
        }
        
        print("\n🔧 Applying column name fixes:")
        
        # Apply column renames
        df_fixed = df.rename(columns=column_mapping)
        
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns:
                print(f"   ✅ Renamed: '{old_name}' → '{new_name}'")
            else:
                print(f"   ⚠️ Column '{old_name}' not found in Excel")
        
        print(f"\n📋 New columns: {list(df_fixed.columns)}")
        
        # Also fix any birth date data that shows as 'N/A' - replace with '04/25/2014'
        if 'Date of Birth' in df_fixed.columns:
            # Count how many birth dates are N/A or empty
            na_count = (df_fixed['Date of Birth'] == 'N/A').sum()
            empty_count = (df_fixed['Date of Birth'] == '').sum()
            
            if na_count > 0 or empty_count > 0:
                print(f"\n🎂 FIXING BIRTH DATES:")
                print(f"   Found {na_count} 'N/A' birth dates")
                print(f"   Found {empty_count} empty birth dates")
                
                # Replace N/A and empty with the standard birth date
                df_fixed['Date of Birth'] = df_fixed['Date of Birth'].replace('N/A', '04/25/2014')
                df_fixed['Date of Birth'] = df_fixed['Date of Birth'].replace('', '04/25/2014')
                
                print(f"   ✅ Replaced all N/A and empty birth dates with '04/25/2014'")
        
        # Save the fixed Excel file
        print(f"\n💾 Saving fixed Excel file: {excel_file}")
        df_fixed.to_excel(excel_file, index=False, engine='openpyxl')
        
        print("\n🎉 SUCCESS! Excel file has been fixed:")
        print("   ✅ Column names corrected")
        print("   ✅ Birth dates standardized")
        print("   ✅ Phone column renamed")
        print(f"   ✅ Backup saved as: {backup_file}")
        
        # Show sample of fixed data
        print("\n📊 Sample of fixed data (Records 20-24):")
        for i in range(19, min(24, len(df_fixed))):
            record = df_fixed.iloc[i]
            record_num = i + 1
            print(f"   Record {record_num}: Birth Date = '{record.get('Date of Birth', 'N/A')}', Phone = '{record.get('phone', 'N/A')}'")
            
    except Exception as e:
        print(f"❌ Error fixing Excel file: {str(e)}")

if __name__ == "__main__":
    fix_excel_columns()
