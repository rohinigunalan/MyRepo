import pandas as pd

print("🎯 MASTER EXCEL TEMPLATE CONTENTS")
print("="*60)

# Read the Excel file
df = pd.read_excel('dsr/scripts/Combined/MASTER_TEMPLATE.xlsx')

print(f"📊 Total Records: {len(df)}")
print(f"📋 Total Columns: {len(df.columns)}")

print("\n🔍 KEY ROUTING COLUMNS:")
print(df[['Request_Category', 'Request_Type', 'First name', 'Last name']].to_string(index=False))

print("\n🎯 AUTOMATION TYPE BREAKDOWN:")
print("="*50)

for i, row in df.iterrows():
    category = row['Request_Category']
    req_type = row['Request_Type'] 
    name = f"{row['First name']} {row['Last name']}"
    email = row['Email']
    request = row.get('Which of the following types of requests would you like to make?', 'N/A')
    option = row.get('What option do you want us to take with the data we find?', 'N/A')
    close = row.get('If we find data, would you like us to close the account?', 'N/A')
    
    print(f"\n📋 Record {i+1}: {category} {req_type}")
    print(f"   👤 Name: {name}")
    print(f"   📧 Email: {email}")
    print(f"   🎯 Request Type: {request}")
    print(f"   ⚙️  Action: {option}")
    print(f"   🔒 Close Account: {close}")
    
    # Show special fields for each type
    if req_type == 'Parent':
        child_name = row.get('What is the name of the person whose information you are requesting?', '')
        if pd.notna(child_name) and str(child_name).strip():
            print(f"   👶 Child Name: {child_name}")
    elif req_type == 'Educator':
        school = row.get('What is the name of your school or educational institution?', '')
        student = row.get('Name of the student whose information you are requesting', '')
        if pd.notna(school) and str(school).strip():
            print(f"   🏫 School: {school}")
        if pd.notna(student) and str(student).strip():
            print(f"   🎓 Student: {student}")

print(f"\n📁 Template File: dsr/scripts/Combined/MASTER_TEMPLATE.xlsx")
print("✅ Ready for Master_All_Requests_AUTOMATION.py!")
