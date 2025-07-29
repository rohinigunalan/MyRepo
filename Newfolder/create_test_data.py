import pandas as pd

# Create sample data with 2 records for testing
data = [
    {
        'Email Address': 'ethan.mitchell@mailinator.com',
        'First_Name': 'Ethan',
        'Last_Name': 'Mitchell',
        'birthDate': '11/8/2004',
        'phone': '5712345572',
        'country': 'US',
        'stateOrProvince': 'Colorado',
        'postalCode': '80209-3456',
        'city': 'Denver',
        'streetAddress': '1625 Cherry Creek Drive, Apt 3C',
        'studentSchoolName': 'Cherry Creek High School',
        'studentGraduationYear': '2022',
        'educatorSchoolAffiliation': 'N/A',
        'Request_type': 'request to delete my data',
        'delete_student': 'Student data (if any)',
        'delete_parent': 'Parent data (if any)',
        'delete_educator': ''
    },
    {
        'Email Address': 'sarah.johnson@mailinator.com',
        'First_Name': 'Sarah',
        'Last_Name': 'Johnson',
        'birthDate': '03/15/2005',
        'phone': '5712345573',
        'country': 'US',
        'stateOrProvince': 'New York',
        'postalCode': '10001',
        'city': 'New York',
        'streetAddress': '123 Broadway Ave',
        'studentSchoolName': 'Manhattan High School',
        'studentGraduationYear': '2023',
        'educatorSchoolAffiliation': 'N/A',
        'Request_type': 'Request a copy of my data',
        'delete_student': '',
        'delete_parent': '',
        'delete_educator': ''
    }
]

# Create DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv('form_data_multirecord.csv', index=False)

print("✅ Created test file with 2 records:")
print(f"📊 Total records: {len(df)}")
print("\n📋 Record 1:")
print(f"  Name: {df.iloc[0]['First_Name']} {df.iloc[0]['Last_Name']}")
print(f"  Email: {df.iloc[0]['Email Address']}")
print(f"  State: {df.iloc[0]['stateOrProvince']}")
print(f"  Request: {df.iloc[0]['Request_type']}")

print("\n📋 Record 2:")
print(f"  Name: {df.iloc[1]['First_Name']} {df.iloc[1]['Last_Name']}")
print(f"  Email: {df.iloc[1]['Email Address']}")
print(f"  State: {df.iloc[1]['stateOrProvince']}")
print(f"  Request: {df.iloc[1]['Request_type']}")

print("\n✅ File saved as 'form_data_multirecord.csv'")
