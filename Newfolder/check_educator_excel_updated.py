#!/usr/bin/env python3
"""
Quick script to examine the updated Educatoronbehalfofstudent_form_data.xlsx file 
with the new "Authorized Agent Company Name" column
"""
import pandas as pd
import os

def examine_updated_excel():
    """Examine the updated Excel file structure"""
    excel_file = "dsr/data/Educatoronbehalfofstudent_form_data.xlsx"
    
    try:
        if os.path.exists(excel_file):
            print(f"📊 Reading updated educator Excel file: {excel_file}")
            df = pd.read_excel(excel_file, engine='openpyxl', na_filter=False, keep_default_na=False, dtype=str)
            
            print(f"\n📋 Updated Excel file structure:")
            print(f"   Rows: {len(df)}")
            print(f"   Columns: {len(df.columns)}")
            
            print(f"\n📝 Column Names:")
            for i, col in enumerate(df.columns):
                print(f"   {i+1}. '{col}'")
            
            print(f"\n📊 Sample Data (first 3 rows):")
            for index, row in df.head(3).iterrows():
                print(f"\n   Record {index + 1}:")
                print(f"     Who is making this request: '{row.get('Who is making this request', 'N/A')}'")
                print(f"     Authorized Agent Company Name: '{row.get('Authorized Agent Company Name', 'N/A')}'")
                print(f"     Agent First Name: '{row.get('Agent First Name', 'N/A')}'")
                print(f"     Agent Last Name: '{row.get('Agent Last Name', 'N/A')}'")
                print(f"     Agent Email Address: '{row.get('Agent Email Address', 'N/A')}'")
                print(f"     Student First Name: '{row.get('First Name', 'N/A')}'")
                print(f"     Student Last Name: '{row.get('Last Name', 'N/A')}'")
                print(f"     Request Type: '{row.get('Request_type', 'N/A')}'")
            
            print(f"\n✅ Updated Excel file examination completed!")
            return df
            
        else:
            print(f"❌ Excel file not found: {excel_file}")
            return None
            
    except Exception as e:
        print(f"❌ Error reading updated Excel file: {str(e)}")
        return None

if __name__ == "__main__":
    examine_updated_excel()
