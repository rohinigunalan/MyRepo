import pandas as pd

# Read the CSV file with proper N/A handling
df = pd.read_csv('form_data.csv', keep_default_na=False, na_values=[''])

print(f"📊 Number of records in Excel/CSV: {len(df)}")
print("=" * 60)

for i in range(len(df)):
    print(f"\n📋 Record {i+1}:")
    print("-" * 40)
    record = df.iloc[i]
    for key, value in record.items():
        print(f"  {key}: {value}")
    
    # Show key fields for this record
    print(f"\n🎯 Key fields for Record {i+1}:")
    print(f"  Name: {record.get('First_Name', 'N/A')} {record.get('Last_Name', 'N/A')}")
    print(f"  Email: {record.get('Email Address', 'N/A')}")
    print(f"  State: {record.get('stateOrProvince', 'N/A')}")
    print(f"  Request Type: {record.get('Request_type', 'N/A')}")
    print(f"  Delete Student: {record.get('delete_student', 'N/A')}")
    print(f"  Delete Parent: {record.get('delete_parent', 'N/A')}")
    print(f"  Delete Educator: {record.get('delete_educator', 'N/A')}")
    
    if i < len(df) - 1:
        print("\n" + "=" * 60)
