import pandas as pd
import os

# Create educator data based on your table structure
educator_data = [
    {
        # Agent Information (from your table)
        'Who is making this request': 'Authorized Agent on behalf of someone else',
        'Agent First Name': 'edutwo',
        'Agent Last Name': 'edubehalfofStu',
        'Agent Email Address': 'palmone@mailinator.com',
        
        # Student Information (placeholder data - you may need to add these columns)
        'First Name': 'student1',
        'Last Name': 'test',
        'Email of Child (Data Subject)': 'student1.test@mailinator.com',
        
        # Contact Information
        'birthDate': '01/15/2010',
        'phone': '5712345580',
        'country': 'US',
        'stateOrProvince': 'Virginia',
        'postalCode': '22101',
        'city': 'McLean',
        'streetAddress': '123 Education Lane',
        
        # Additional Details
        'studentSchoolName': 'McLean High School',
        'studentGraduationYear': '2028',
        'educatorSchoolAffiliation': 'McLean High School',
        
        # Request Information
        'Request_type': 'request to delete my data',
        'additional_details': 'Educator requesting deletion on behalf of student'
    },
    {
        # Agent Information
        'Who is making this request': 'Authorized Agent on behalf of someone else',
        'Agent First Name': 'eduthree',
        'Agent Last Name': 'edubehalfofStu',
        'Agent Email Address': 'palmone@mailinator.com',
        
        # Student Information
        'First Name': 'student2',
        'Last Name': 'info',
        'Email of Child (Data Subject)': 'student2.info@mailinator.com',
        
        # Contact Information
        'birthDate': '03/22/2011',
        'phone': '5712345581',
        'country': 'US',
        'stateOrProvince': 'Virginia',
        'postalCode': '22102',
        'city': 'McLean',
        'streetAddress': '456 School Drive',
        
        # Additional Details
        'studentSchoolName': 'McLean High School',
        'studentGraduationYear': '2029',
        'educatorSchoolAffiliation': 'McLean High School',
        
        # Request Information
        'Request_type': 'request to copy of my data',
        'additional_details': ''
    },
    {
        # Agent Information
        'Who is making this request': 'Authorized Agent on behalf of someone else',
        'Agent First Name': 'edufour',
        'Agent Last Name': 'edubehalfofStu',
        'Agent Email Address': 'palmone@mailinator.com',
        
        # Student Information
        'First Name': 'student3',
        'Last Name': 'opt',
        'Email of Child (Data Subject)': 'student3.opt@mailinator.com',
        
        # Contact Information
        'birthDate': '07/10/2012',
        'phone': '5712345582',
        'country': 'US',
        'stateOrProvince': 'Virginia',
        'postalCode': '22103',
        'city': 'McLean',
        'streetAddress': '789 Academic Road',
        
        # Additional Details
        'studentSchoolName': 'McLean High School',
        'studentGraduationYear': '2030',
        'educatorSchoolAffiliation': 'McLean High School',
        
        # Request Information
        'Request_type': 'Opt out of search',
        'additional_details': ''
    }
]

# Create DataFrame
df = pd.DataFrame(educator_data)

# Create the directory if it doesn't exist
os.makedirs('dsr/data', exist_ok=True)

# Save to Excel file
df.to_excel('dsr/data/Educatoronbehalfofstudent_form_data.xlsx', index=False, engine='openpyxl')

print("✅ Educatoronbehalfofstudent_form_data.xlsx created successfully!")
print(f"📊 Created {len(educator_data)} educator records:")
print("\n🔍 Data Summary:")
for i, record in enumerate(educator_data):
    print(f"  Record {i+1}: {record['Agent First Name']} {record['Agent Last Name']}")
    print(f"    Student: {record['First Name']} {record['Last Name']}")
    print(f"    Agent Email: {record['Agent Email Address']}")
    print(f"    Student Email: {record['Email of Child (Data Subject)']}")
    print(f"    Request: {record['Request_type']}")
    print()

print("📋 All educator/agent form fields are now included in the Excel file!")
