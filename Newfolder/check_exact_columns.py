#!/usr/bin/env python3
"""
Check the exact column names and child email values in the educator Excel file.
"""

import pandas as pd

def check_educator_excel_columns():
    """Check the exact column structure of the educator Excel file"""
    
    print("🔍 CHECKING EDUCATOR EXCEL COLUMN STRUCTURE...")
    
    try:
        # Load the Excel file the same way the script does
        df = pd.read_excel('dsr/data/Educatoronbehalfofstudent_form_data.xlsx', 
                          engine='openpyxl', na_filter=False, keep_default_na=False, dtype=str)
        
        print(f"📊 File loaded with {len(df)} rows and {len(df.columns)} columns")
        
        print(f"\n📝 EXACT COLUMN NAMES:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i:2d}. '{col}'")
        
        print(f"\n📧 LOOKING FOR EMAIL COLUMNS:")
        email_columns = [col for col in df.columns if 'email' in col.lower()]
        for col in email_columns:
            print(f"   Email column: '{col}'")
        
        print(f"\n📧 LOOKING FOR PRIMARY EMAIL COLUMNS:")
        primary_columns = [col for col in df.columns if 'primary' in col.lower()]
        for col in primary_columns:
            print(f"   Primary column: '{col}'")
        
        print(f"\n📊 FIRST RECORD DATA:")
        first_record = df.iloc[0]
        for col in df.columns:
            if 'email' in col.lower() or 'primary' in col.lower():
                value = first_record[col]
                print(f"   {col}: '{value}'")
        
        print(f"\n🔍 TESTING DIFFERENT CHILD EMAIL COLUMN NAMES:")
        possible_child_email_columns = [
            'Email of Child (Data Subject)',
            'Primary Email address',
            'Primary Email Address',
            'Child Email',
            'Student Email'
        ]
        
        for col_name in possible_child_email_columns:
            try:
                value = first_record.get(col_name, 'NOT_FOUND')
                print(f"   '{col_name}': '{value}'")
            except Exception as e:
                print(f"   '{col_name}': ERROR - {str(e)}")
        
        print(f"\n📋 ALL DATA FOR FIRST RECORD:")
        for col, value in first_record.items():
            print(f"   '{col}': '{value}'")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    check_educator_excel_columns()
