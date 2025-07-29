#!/usr/bin/env python3
"""
Script to update the Excel file with proper close account columns
"""

import pandas as pd
import os

def update_excel_with_close_columns():
    """Update Excel file to add close_student and close_educator columns"""
    
    excel_file = "dsr/data/form_data.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"❌ Excel file not found: {excel_file}")
        return
    
    try:
        # Read the current Excel file
        print(f"📂 Reading Excel file: {excel_file}")
        df = pd.read_excel(excel_file, engine='openpyxl', na_filter=False, keep_default_na=False, dtype=str)
        
        print("📊 Current columns:")
        for col in df.columns:
            print(f"  - {col}")
        
        print(f"\n📊 Current data:")
        print(df.to_string())
        
        # Add close_student and close_educator columns if they don't exist
        if 'close_student' not in df.columns:
            df['close_student'] = ''
            print("\n✅ Added 'close_student' column")
        
        if 'close_educator' not in df.columns:
            df['close_educator'] = ''
            print("✅ Added 'close_educator' column")
        
        # For Record 5 (Close account request), copy values from delete columns
        print(f"\n🔍 Looking for close account requests...")
        
        for index, row in df.iterrows():
            request_type = str(row.get('Request_type', '')).strip().lower()
            
            # Check if this is a close account request
            if any(keyword in request_type for keyword in ['close', 'deactivate', 'cancel']):
                print(f"\n🎯 Found close account request in row {index + 1}: '{row.get('Request_type', '')}'")
                
                # Copy values from delete columns to close columns for this row
                delete_student = str(row.get('delete_student', '')).strip()
                delete_educator = str(row.get('delete_educator', '')).strip()
                
                if delete_student and delete_student.lower() not in ['', 'nan', 'none']:
                    df.at[index, 'close_student'] = delete_student
                    print(f"  🎓 Set close_student = '{delete_student}'")
                
                if delete_educator and delete_educator.lower() not in ['', 'nan', 'none']:
                    df.at[index, 'close_educator'] = delete_educator
                    print(f"  👨‍🏫 Set close_educator = '{delete_educator}'")
        
        # Save the updated Excel file
        print(f"\n💾 Saving updated Excel file...")
        df.to_excel(excel_file, index=False, engine='openpyxl')
        print(f"✅ Excel file updated successfully!")
        
        print(f"\n📊 Updated data:")
        print(df.to_string())
        
        # Show the specific columns for Record 5
        print(f"\n🔍 Record 5 close account columns:")
        if len(df) >= 5:
            record_5 = df.iloc[4]  # 5th record (0-indexed)
            print(f"  🎓 close_student: '{record_5.get('close_student', '')}'")
            print(f"  👨‍🏫 close_educator: '{record_5.get('close_educator', '')}'")
        
    except Exception as e:
        print(f"❌ Error updating Excel file: {str(e)}")

if __name__ == "__main__":
    update_excel_with_close_columns()
