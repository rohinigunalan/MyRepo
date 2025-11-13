import pandas as pd

try:
    # Read Excel file now that it's closed
    print("📊 Reading Excel file...")
    df = pd.read_excel('form_data.xlsx', engine='openpyxl')
    
    print(f"✅ Excel file loaded successfully!")
    print(f"📊 Total records found: {len(df)}")
    print("=" * 60)
    
    # Show all records
    for i in range(len(df)):
        record = df.iloc[i]
        print(f"\n📋 Record {i+1}:")
        print(f"  👤 Name: {record.get('First_Name', 'N/A')} {record.get('Last_Name', 'N/A')}")
        print(f"  📧 Email: {record.get('Email Address', 'N/A')}")
        print(f"  🏠 State: {record.get('stateOrProvince', 'N/A')}")
        print(f"  📋 Request: {record.get('Request_type', 'N/A')}")
        print(f"  🗑️ Delete Options:")
        print(f"    Student: {record.get('delete_student', 'N/A')}")
        print(f"    Parent: {record.get('delete_parent', 'N/A')}")
        print(f"    Educator: {record.get('delete_educator', 'N/A')}")
        
        if i < len(df) - 1:
            print("-" * 40)
    
    # Update CSV to match Excel
    if len(df) > 1:
        print(f"\n🔄 Updating CSV file to match Excel with {len(df)} records...")
        df.to_csv('form_data.csv', index=False)
        print("✅ CSV file updated!")
    
except Exception as e:
    print(f"❌ Error reading Excel: {str(e)}")
    print("📊 Using CSV file instead...")
    df = pd.read_csv('form_data.csv', keep_default_na=False, na_values=[''])
    print(f"CSV records: {len(df)}")
