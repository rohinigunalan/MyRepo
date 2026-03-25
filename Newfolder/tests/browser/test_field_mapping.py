#!/usr/bin/env python3
"""
Quick test to check field mapping for International Parent Excel file
"""

import pandas as pd
import os

def test_field_mapping():
    excel_file = r"C:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\Newfolder\dsr\data\International_Parent_form_data.xlsx"
    
    try:
        df = pd.read_excel(excel_file, engine='openpyxl', na_filter=True, keep_default_na=True, dtype=str)
        print("✅ International Parent Excel file loaded successfully!")
        
        print(f"\n📋 Available columns in Excel file:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. '{col}'")
        
        print(f"\n📊 First record data:")
        if len(df) > 0:
            first_record = df.iloc[0].to_dict()
            
            # Test the field mapping with actual data
            parent_first = (first_record.get(' First_Name_of parent_guardian') or 
                          first_record.get('First_Name_of parent_guardian') or 'N/A')
            parent_last = (first_record.get('Last Name of parent/guardian') or 'N/A')
            child_first = (first_record.get('First Name') or 'N/A')
            child_last = (first_record.get('Last Name') or 'N/A')
            
            print(f"  👨‍👩‍👧‍👦 Parent: {parent_first} {parent_last}")
            print(f"  👶 Child: {child_first} {child_last}")
            print(f"  📧 Parent Email: {first_record.get('Primary Email Address', 'N/A')}")
            print(f"  📧 Child Email: {first_record.get('Email of Child (Data Subject)', 'N/A')}")
            print(f"  📋 Request Type: {first_record.get('Request_type', 'N/A')}")
            print(f"  🌍 Country: {first_record.get('country', 'N/A')}")
        
        # Show specific record 20 (index 19)
        if len(df) >= 20:
            print(f"\n📊 Record 20 data:")
            record_20 = df.iloc[19].to_dict()
            
            parent_first = (record_20.get(' First_Name_of parent_guardian') or 
                          record_20.get('First_Name_of parent_guardian') or 'N/A')
            parent_last = (record_20.get('Last Name of parent/guardian') or 'N/A')
            child_first = (record_20.get('First Name') or 'N/A')
            child_last = (record_20.get('Last Name') or 'N/A')
            
            print(f"  👨‍👩‍👧‍👦 Parent: {parent_first} {parent_last}")
            print(f"  👶 Child: {child_first} {child_last}")
            print(f"  📧 Parent Email: {record_20.get('Primary Email Address', 'N/A')}")
            print(f"  📧 Child Email: {record_20.get('Email of Child (Data Subject)', 'N/A')}")
            print(f"  📋 Request Type: {record_20.get('Request_type', 'N/A')}")
            print(f"  🌍 Country: {record_20.get('country', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_field_mapping()
