#!/usr/bin/env python3
"""
Script to create an updated Excel file with proper close account columns
"""

import pandas as pd
import os
from datetime import datetime

def create_updated_excel():
    """Create a new Excel file with proper close account columns"""
    
    excel_file = "dsr/data/form_data.xlsx"
    backup_file = f"dsr/data/form_data_updated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
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
        
        print(f"\n📊 Current Record 5 data:")
        if len(df) >= 5:
            record_5 = df.iloc[4]  # 5th record (0-indexed)
            print(f"  Request_type: '{record_5.get('Request_type', '')}'")
            print(f"  delete_student: '{record_5.get('delete_student', '')}'")
            print(f"  delete_educator: '{record_5.get('delete_educator', '')}'")
        
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
        
        # Save the updated Excel file with a new name
        print(f"\n💾 Saving updated Excel file as: {backup_file}")
        df.to_excel(backup_file, index=False, engine='openpyxl')
        print(f"✅ Updated Excel file created successfully!")
        
        print(f"\n📊 Updated Record 5 close account columns:")
        if len(df) >= 5:
            record_5 = df.iloc[4]  # 5th record (0-indexed)
            print(f"  🎓 close_student: '{record_5.get('close_student', '')}'")
            print(f"  👨‍🏫 close_educator: '{record_5.get('close_educator', '')}'")
        
        print(f"\n🔄 Next Steps:")
        print(f"1. Close the current Excel file ({excel_file})")
        print(f"2. Rename the updated file ({backup_file}) to replace the original")
        print(f"3. Or update the script to use the new file name")
        
        return backup_file
        
    except Exception as e:
        print(f"❌ Error creating updated Excel file: {str(e)}")
        return None

if __name__ == "__main__":
    create_updated_excel()
