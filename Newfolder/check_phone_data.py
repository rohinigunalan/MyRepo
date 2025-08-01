#!/usr/bin/env python3
"""Check phone number data in Excel file"""

import pandas as pd

def check_phone_data():
    """Check what phone numbers are in the Excel file"""
    try:
        # Read the Excel file
        df = pd.read_excel('dsr/data/International_Educatoronbehalfofstudent_form_data.xlsx', na_filter=False, keep_default_na=False, dtype=str)
        
        print(f"Total records in Excel: {len(df)}")
        print("\n" + "="*60)
        print("PHONE NUMBER COLUMN VALUES:")
        print("="*60)
        
        # Check all phone number values
        for i, phone in enumerate(df['Phone Number'].values):
            print(f"Record {i+1}: Phone Number = '{phone}'")
            
        print("\n" + "="*60)
        print("ALL COLUMN NAMES:")
        print("="*60)
        for col in df.columns:
            print(f"'{col}'")
            
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")

if __name__ == "__main__":
    check_phone_data()
