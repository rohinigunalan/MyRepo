#!/usr/bin/env python3
"""
Update Excel data with Colorado information
"""
import pandas as pd
import os

def update_excel_data():
    """Update both Excel and CSV files with new Colorado data"""
    
    # New Colorado data based on user input
    new_data = {
        'Email Address': 'ethan.mitchell@mailinator.com',
        'First_Name': 'Ethan',
        'Last_Name': 'Mitchell', 
        'birthDate': '11/8/2004',
        'phone': '5712345572',
        'country': 'US',
        'stateOrProvince': 'Colorado',  # CO -> Colorado (full name for dropdown)
        'postalCode': '80209-3456',
        'city': 'Denver',
        'streetAddress': '1625 Cherry Creek Drive, Apt 3C',
        'studentSchoolName': 'Cherry Creek High School',  # Default school for Colorado
        'studentGraduationYear': '2022',  # Default graduation year
        'educatorSchoolAffiliation': 'N/A',
        'Request_type': 'Request a copy of my data'
    }
    
    print("📊 Creating new data with Colorado information...")
    print("📧 Email:", new_data['Email Address'])
    print("👤 Name:", new_data['First_Name'], new_data['Last_Name'])
    print("🏛️ State:", new_data['stateOrProvince'])
    print("🏠 Address:", new_data['streetAddress'])
    print("🏫 City:", new_data['city'])
    print()
    
    # Create DataFrame
    df = pd.DataFrame([new_data])
    
    # Save to CSV first (more reliable)
    csv_file = "form_data.csv"
    df.to_csv(csv_file, index=False)
    print(f"✅ Updated {csv_file}")
    
    # Save to Excel
    excel_file = "form_data.xlsx"
    try:
        df.to_excel(excel_file, index=False, engine='openpyxl')
        print(f"✅ Updated {excel_file}")
    except Exception as e:
        print(f"⚠️ Could not update Excel file: {e}")
        print("💡 CSV file will be used as fallback")
    
    # Verify the data
    print("\n🔍 Verifying updated data...")
    try:
        # Try to read Excel first
        verify_df = pd.read_excel(excel_file, engine='openpyxl')
        print("📊 Excel file verification:")
    except:
        # Fallback to CSV
        verify_df = pd.read_csv(csv_file)
        print("📊 CSV file verification:")
    
    row = verify_df.iloc[0]
    print(f"  📧 Email: {row['Email Address']}")
    print(f"  👤 Name: {row['First_Name']} {row['Last_Name']}")
    print(f"  🏛️ State: {row['stateOrProvince']}")
    print(f"  🏠 Address: {row['streetAddress']}")
    print(f"  🏫 City: {row['city']}")
    
    print("\n✅ Data update completed!")
    return True

if __name__ == "__main__":
    update_excel_data()
