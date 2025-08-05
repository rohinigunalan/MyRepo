#!/usr/bin/env python3
"""
Quick diagnostic script to check what data is actually in the Excel file
"""

import pandas as pd
import os

def check_excel_data():
    """Check the actual data in the Excel file"""
    print("🔍 DIAGNOSTIC: Checking Excel file data...")
    
    # Use the same Excel file path as the automation script
    excel_file = r"C:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\Newfolder\dsr\data\Domestic_Parent_form_data.xlsx"
    
    try:
        if os.path.exists(excel_file):
            print(f"📂 Found Excel file: {excel_file}")
            
            # Read Excel file with same settings as automation script
            df = pd.read_excel(excel_file, engine='openpyxl', na_filter=False, keep_default_na=False, dtype=str)
            print(f"✅ Excel file loaded successfully!")
            print(f"📊 Total records: {len(df)}")
            print(f"📋 Columns found: {list(df.columns)}")
            
            # Check records 20-24 specifically (the ones being processed)
            print("\n" + "="*80)
            print("🎯 RECORDS 20-24 DATA (Records being processed by automation):")
            print("="*80)
            
            for i in range(19, min(24, len(df))):  # Records 20-24 (0-based index 19-23)
                record = df.iloc[i]
                record_num = i + 1
                print(f"\n📋 RECORD {record_num}:")
                print(f"   Parent First: '{record.get(' First_Name_of parent_guardian', 'N/A')}'")
                print(f"   Parent Last: '{record.get('Last Name of parent/guardian', 'N/A')}'")
                print(f"   Parent Email: '{record.get('Primary Email Address', 'N/A')}'")
                print(f"   Child First: '{record.get('First Name', 'N/A')}'")
                print(f"   Child Last: '{record.get('Last Name', 'N/A')}'")
                print(f"   Child Email: '{record.get('Email of Child (Data Subject)', 'N/A')}'")
                print(f"   Birth Date: '{record.get('Date of Birth', 'N/A')}'")
                print(f"   Phone: '{record.get('phone', 'N/A')}'")
                print(f"   Phone Number: '{record.get('Phone Number', 'N/A')}'")
                print(f"   State: '{record.get('stateOrProvince', 'N/A')}'")
                print(f"   Request: '{record.get('Request_type', 'N/A')}'")
                
                # Check for any phone-related columns
                phone_columns = []
                for col in record.index:
                    if 'phone' in col.lower() or 'tel' in col.lower():
                        phone_columns.append(f"{col}: '{record[col]}'")
                
                if phone_columns:
                    print(f"   📞 Phone-related columns: {phone_columns}")
                else:
                    print(f"   📞 No phone-related columns found")
            
            # Check if there are any null/empty values in key columns
            print("\n" + "="*80)
            print("🔍 NULL/EMPTY VALUE CHECK:")
            print("="*80)
            
            key_columns = [' First_Name_of parent_guardian', 'Last Name of parent/guardian', 
                          'Primary Email Address', 'First Name', 'Last Name', 
                          'Email of Child (Data Subject)', 'Date of Birth', 'phone', 'Phone Number']
            
            for col in key_columns:
                if col in df.columns:
                    null_count = df[col].isna().sum()
                    empty_count = (df[col] == '').sum()
                    print(f"   {col}: {null_count} nulls, {empty_count} empties")
                else:
                    print(f"   {col}: COLUMN NOT FOUND")
                    
        else:
            print(f"❌ Excel file not found: {excel_file}")
            
    except Exception as e:
        print(f"❌ Error reading Excel file: {str(e)}")

if __name__ == "__main__":
    check_excel_data()
