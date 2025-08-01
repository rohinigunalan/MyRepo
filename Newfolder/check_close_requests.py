#!/usr/bin/env python3
"""Check the close request data in Excel file"""

import pandas as pd

def check_close_requests():
    """Check what request types are in records 8-10"""
    try:
        # Read the Excel file
        df = pd.read_excel('International_Educatoronbehalfofstudent_form_data.xlsx')
        
        print(f"Total records in Excel: {len(df)}")
        print("\n" + "="*60)
        print("CHECKING RECORDS 8-10 (close requests)")
        print("="*60)
        
        # Check records 8-10 (index 7-9)
        for i in range(7, min(10, len(df))):
            record_num = i + 1
            row = df.iloc[i]
            request_type = str(row.get('Request_type', '')).strip()
            
            print(f"\nRecord {record_num}:")
            print(f"  Request_type: '{request_type}'")
            
            # Check if it contains close-related keywords
            close_keywords = ['close', 'deactivate', 'cancel', 'account']
            contains_close = any(keyword.lower() in request_type.lower() for keyword in close_keywords)
            print(f"  Contains close keywords: {contains_close}")
            
            # Show close-related columns if they exist
            if 'close_student' in row:
                print(f"  close_student: '{row.get('close_student', '')}'")
            if 'close_educator' in row:
                print(f"  close_educator: '{row.get('close_educator', '')}'")
                
        print("\n" + "="*60)
        print("ALL REQUEST TYPES:")
        print("="*60)
        for i, request_type in enumerate(df['Request_type'].values):
            print(f"Record {i+1}: '{request_type}'")
            
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")

if __name__ == "__main__":
    check_close_requests()
