#!/usr/bin/env python3
"""
Update Excel and CSV files with delete data options columns
"""
import pandas as pd
import os

def update_data_with_delete_options():
    """Add delete options columns to the data files"""
    
    print("📊 Updating data files with delete options columns...")
    
    # Try to read existing data
    try:
        # Try Excel first
        try:
            df = pd.read_excel("form_data.xlsx", engine='openpyxl')
            print("✅ Read existing Excel file")
        except:
            # Fall back to CSV
            df = pd.read_csv("form_data.csv")
            print("✅ Read existing CSV file")
    except Exception as e:
        print(f"❌ Error reading data files: {e}")
        return False
    
    # Check if delete columns already exist
    delete_columns = ['delete_student', 'delete_parent', 'delete_educator']
    existing_delete_cols = [col for col in delete_columns if col in df.columns]
    
    if len(existing_delete_cols) == 3:
        print("✅ Delete option columns already exist!")
        return True
    
    # Add missing delete columns with default values
    for col in delete_columns:
        if col not in df.columns:
            if col == 'delete_student':
                df[col] = 'yes'  # Default: delete student data
            elif col == 'delete_parent':
                df[col] = 'no'   # Default: don't delete parent data
            elif col == 'delete_educator':
                df[col] = 'no'   # Default: don't delete educator data
            print(f"➕ Added column: {col}")
    
    # Also update Request_type to delete if it's not already
    if df.iloc[0]['Request_type'] != 'request to delete my data':
        df.iloc[0, df.columns.get_loc('Request_type')] = 'request to delete my data'
        print("✅ Updated Request_type to 'request to delete my data'")
    
    # Save to both files
    try:
        df.to_csv("form_data.csv", index=False)
        print("✅ Updated CSV file")
        
        df.to_excel("form_data.xlsx", index=False, engine='openpyxl')
        print("✅ Updated Excel file")
    except Exception as e:
        print(f"⚠️ Error saving files: {e}")
        return False
    
    # Display updated data
    print("\n📋 Updated data with delete options:")
    print("-" * 50)
    row = df.iloc[0]
    for col, value in row.items():
        print(f"  {col}: {value}")
    
    print("\n🎯 Delete Options Summary:")
    print(f"  🎓 Student data: {row.get('delete_student', 'NOT SET')}")
    print(f"  👨‍👩‍👧‍👦 Parent data: {row.get('delete_parent', 'NOT SET')}")
    print(f"  👨‍🏫 Educator data: {row.get('delete_educator', 'NOT SET')}")
    
    return True

if __name__ == "__main__":
    success = update_data_with_delete_options()
    if success:
        print("\n✅ Data files updated successfully!")
    else:
        print("\n❌ Failed to update data files!")
