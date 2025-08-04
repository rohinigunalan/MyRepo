#!/usr/bin/env python3
"""
Quick script to check if the Excel file has data at row 20
"""

import pandas as pd
import os

def check_excel_row_20():
    excel_file = "dsr/data/Domestic_Educatoronbehalfofstudent_form_data.xlsx"
    
    print(f"🔍 Checking Excel file: {excel_file}")
    
    if not os.path.exists(excel_file):
        print(f"❌ File not found: {excel_file}")
        return
    
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file, engine='openpyxl', na_filter=False, keep_default_na=False, dtype=str)
        
        print(f"📊 Total rows in Excel file: {len(df)}")
        print(f"📊 Total columns in Excel file: {len(df.columns)}")
        
        # Show first few column names
        print(f"📋 Column names: {list(df.columns)[:5]}...")
        
        # Check if row 20 exists (index 19 since 0-based)
        if len(df) >= 20:
            print(f"✅ Row 20 EXISTS in the Excel file!")
            
            # Show data from row 20
            row_20_data = df.iloc[19]  # Index 19 = Row 20
            print(f"\n📋 ROW 20 DATA:")
            for column, value in row_20_data.items():
                if pd.isna(value) or value == '':
                    print(f"   {column}: [EMPTY]")
                else:
                    print(f"   {column}: {value}")
                    
            # Show a few more rows around row 20
            print(f"\n📊 ROWS AVAILABLE STARTING FROM ROW 20:")
            available_rows = len(df) - 19  # How many rows from row 20 onwards
            print(f"   Records that can be processed starting from row 20: {available_rows}")
            
            for i in range(19, min(len(df), 25)):  # Show rows 20-25
                agent_first = df.iloc[i].get('Agent First Name', 'N/A')
                agent_last = df.iloc[i].get('Agent Last Name', 'N/A')
                student_first = df.iloc[i].get('First Name', 'N/A')
                student_last = df.iloc[i].get('Last Name', 'N/A')
                request_type = df.iloc[i].get('Request_type', 'N/A')
                print(f"   Row {i+1}: Agent: {agent_first} {agent_last} | Student: {student_first} {student_last} | Request: {request_type}")
                
        else:
            print(f"❌ Row 20 DOES NOT EXIST in the Excel file!")
            print(f"❌ File only has {len(df)} rows, but you need at least 20 rows.")
            print(f"📝 Available rows to show:")
            
            for i in range(len(df)):
                agent_first = df.iloc[i].get('Agent First Name', 'N/A')
                agent_last = df.iloc[i].get('Agent Last Name', 'N/A')
                student_first = df.iloc[i].get('First Name', 'N/A')
                student_last = df.iloc[i].get('Last Name', 'N/A')
                request_type = df.iloc[i].get('Request_type', 'N/A')
                print(f"   Row {i+1}: Agent: {agent_first} {agent_last} | Student: {student_first} {student_last} | Request: {request_type}")
        
    except Exception as e:
        print(f"❌ Error reading Excel file: {str(e)}")

if __name__ == "__main__":
    check_excel_row_20()
