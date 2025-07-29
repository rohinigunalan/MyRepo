#!/usr/bin/env python3
"""
Quick test for Record 5 close account sub-options with updated Excel file
"""

import pandas as pd
import os

def test_record_5_close_options():
    """Test the close account options for Record 5"""
    
    excel_file = "dsr/data/form_data_updated_20250729_015139.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"❌ Updated Excel file not found: {excel_file}")
        return
    
    try:
        # Read the updated Excel file
        print(f"📂 Reading updated Excel file: {excel_file}")
        df = pd.read_excel(excel_file, engine='openpyxl', na_filter=False, keep_default_na=False, dtype=str)
        
        print(f"📊 Found {len(df)} records in the file")
        
        # Get Record 5 (index 4)
        if len(df) >= 5:
            record_5 = df.iloc[4]  # 5th record (0-indexed)
            
            print(f"\n🎯 RECORD 5 ANALYSIS:")
            print(f"  Name: {record_5.get('First_Name', '')} {record_5.get('Last_Name', '')}")
            print(f"  Request Type: '{record_5.get('Request_type', '')}'")
            
            print(f"\n📊 Close account columns:")
            close_student = str(record_5.get('close_student', '')).strip()
            close_educator = str(record_5.get('close_educator', '')).strip()
            
            print(f"  🎓 close_student: '{close_student}'")
            print(f"  👨‍🏫 close_educator: '{close_educator}'")
            
            # Test the selection logic
            def should_select_option(excel_value):
                if excel_value is None:
                    return False
                excel_str = str(excel_value).strip()
                if excel_str.lower() in ['nan', '', 'none', 'no', 'false', '0', 'n']:
                    return False
                if excel_str.lower() in ['yes', 'true', '1', 'y']:
                    return True
                if any(keyword in excel_str.lower() for keyword in ['account', 'student', 'educator']):
                    return True
                return len(excel_str) > 0
            
            student_should_select = should_select_option(close_student)
            educator_should_select = should_select_option(close_educator)
            
            print(f"\n📋 Selection logic test:")
            print(f"  🎓 Student account: {'SELECT' if student_should_select else 'SKIP'} (Excel: '{close_student}')")
            print(f"  👨‍🏫 Educator account: {'SELECT' if educator_should_select else 'SKIP'} (Excel: '{close_educator}')")
            print(f"  📊 Total options to select: {sum([student_should_select, educator_should_select])}")
            
            if student_should_select and educator_should_select:
                print(f"\n✅ EXPECTED RESULT: Both Student and Educator options should be selected!")
            elif student_should_select:
                print(f"\n✅ EXPECTED RESULT: Only Student option should be selected!")
            elif educator_should_select:
                print(f"\n✅ EXPECTED RESULT: Only Educator option should be selected!")
            else:
                print(f"\n⚠️ EXPECTED RESULT: No options should be selected!")
                
        else:
            print("❌ Record 5 not found in Excel file")
            
    except Exception as e:
        print(f"❌ Error reading Excel file: {str(e)}")

if __name__ == "__main__":
    test_record_5_close_options()
