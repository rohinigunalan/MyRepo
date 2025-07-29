#!/usr/bin/env python3
"""
Update Excel file to test Close Account sub-options with different scenarios
"""

import pandas as pd
import os

def update_excel_for_close_account_testing():
    """Update the Excel file with different close account test scenarios"""
    
    excel_file = "dsr/data/form_data.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"❌ Excel file not found: {excel_file}")
        return
    
    # Read existing data
    print(f"📊 Reading existing data from {excel_file}")
    df = pd.read_excel(excel_file, engine='openpyxl', na_filter=False, keep_default_na=False, dtype=str)
    
    print("📋 Current columns:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")
    
    print(f"\n📊 Current data ({len(df)} records):")
    for i, row in df.iterrows():
        name = row.get('First_Name', 'Unknown') + ' ' + row.get('Last_Name', '')
        request_type = row.get('Request_type', 'Unknown')
        print(f"  Record {i+1}: {name} - {request_type}")
    
    # Add close account columns if they don't exist
    if 'close_student' not in df.columns:
        df['close_student'] = ''
        print("✅ Added 'close_student' column")
    
    if 'close_educator' not in df.columns:
        df['close_educator'] = ''
        print("✅ Added 'close_educator' column")
    
    # Update Record 5 (the close account record) with different test scenarios
    close_account_records = df[df['Request_type'].str.contains('Close', case=False, na=False)]
    
    if len(close_account_records) == 0:
        print("❌ No close account records found!")
        return
    
    print(f"\n🎯 Found {len(close_account_records)} close account record(s)")
    
    # Get the index of the first close account record (Record 5)
    close_record_index = close_account_records.index[0]
    
    print(f"\n🧪 TEST SCENARIOS FOR CLOSE ACCOUNT SUB-OPTIONS:")
    print("Choose a test scenario:")
    print("1. Select BOTH Student and Educator accounts")
    print("2. Select ONLY Student account") 
    print("3. Select ONLY Educator account")
    print("4. Select NEITHER (empty - skip both)")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        # Both options
        df.loc[close_record_index, 'close_student'] = 'Student account (if any)'
        df.loc[close_record_index, 'close_educator'] = 'Educator account (if any)'
        scenario = "BOTH Student and Educator"
    elif choice == "2":
        # Only student
        df.loc[close_record_index, 'close_student'] = 'Student account (if any)'
        df.loc[close_record_index, 'close_educator'] = ''
        scenario = "ONLY Student"
    elif choice == "3":
        # Only educator
        df.loc[close_record_index, 'close_student'] = ''
        df.loc[close_record_index, 'close_educator'] = 'Educator account (if any)'
        scenario = "ONLY Educator"
    elif choice == "4":
        # Neither
        df.loc[close_record_index, 'close_student'] = ''
        df.loc[close_record_index, 'close_educator'] = ''
        scenario = "NEITHER (skip both)"
    else:
        print("❌ Invalid choice!")
        return
    
    # Save updated Excel file
    df.to_excel(excel_file, index=False, engine='openpyxl')
    print(f"\n✅ Excel file updated with scenario: {scenario}")
    
    # Show the updated data
    print(f"\n📊 Updated Record 5 (Close Account):")
    close_row = df.loc[close_record_index]
    print(f"  Name: {close_row['First_Name']} {close_row['Last_Name']}")
    print(f"  Request Type: {close_row['Request_type']}")
    print(f"  🎓 Student Option: '{close_row['close_student']}'")
    print(f"  👨‍🏫 Educator Option: '{close_row['close_educator']}'")
    
    print(f"\n🚀 Ready to test! Run the automation script to see the conditional selection in action.")
    print(f"Expected behavior:")
    if choice == "1":
        print("  ✅ Should select BOTH Student and Educator options")
    elif choice == "2":
        print("  ✅ Should select ONLY Student option")
    elif choice == "3":
        print("  ✅ Should select ONLY Educator option")
    elif choice == "4":
        print("  ⏭️ Should SKIP both options (no selections)")

if __name__ == "__main__":
    update_excel_for_close_account_testing()
