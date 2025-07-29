import pandas as pd
import os

# Create the data structure that matches what the script expects
parent_data = [
    {
        'First Name': 'new',
        'Last Name': 'deletedsr',
        'Primary Email Address': 'new.deletedsr@mailinator.com',
        'Email of Child (Data Subject)': 'child.new@mailinator.com',
        'Child_First_Name': 'ChildNew',
        'Child_Last_Name': 'Delete',
        'Phone': '555-0101',
        'Date of Birth': '01/15/2010',
        'Address': '123 Main St',
        'City': 'Denver',
        'State': 'Colorado',
        'ZIP': '80202',
        'Country': 'United States',
        'Request_type': 'request to delete my data',
        'Student School Name': 'N/A',
        'Graduation Year': 'N/A',
        'Delete Additional Details': 'N/A',
        'Delete Student Data': '',
        'Delete Parent Data': '',
        'Delete Educator Data': '',
        'Close Student Account': '',
        'Close Educator Account': ''
    },
    {
        'First Name': 'kiran',
        'Last Name': 'infodsr',
        'Primary Email Address': 'kiran.infodsr@mailinator.com',
        'Email of Child (Data Subject)': 'child.kiran@mailinator.com',
        'Child_First_Name': 'ChildKiran',
        'Child_Last_Name': 'Info',
        'Phone': '555-0102',
        'Date of Birth': '03/22/2009',
        'Address': '456 Oak Ave',
        'City': 'Denver',
        'State': 'Colorado',
        'ZIP': '80203',
        'Country': 'United States',
        'Request_type': 'request to copy of my data',
        'Student School Name': 'N/A',
        'Graduation Year': 'N/A',
        'Delete Additional Details': 'N/A',
        'Delete Student Data': '',
        'Delete Parent Data': '',
        'Delete Educator Data': '',
        'Close Student Account': '',
        'Close Educator Account': ''
    },
    {
        'First Name': 'kayal',
        'Last Name': 'optdsr',
        'Primary Email Address': 'kayal.optdsr@mailinator.com',
        'Email of Child (Data Subject)': 'child.kayal@mailinator.com',
        'Child_First_Name': 'ChildKayal',
        'Child_Last_Name': 'Opt',
        'Phone': '555-0103',
        'Date of Birth': '07/10/2011',
        'Address': '789 Pine Rd',
        'City': 'Denver',
        'State': 'Colorado',
        'ZIP': '80204',
        'Country': 'United States',
        'Request_type': 'Opt out of search',
        'Student School Name': 'N/A',
        'Graduation Year': 'N/A',
        'Delete Additional Details': 'N/A',
        'Delete Student Data': '',
        'Delete Parent Data': '',
        'Delete Educator Data': '',
        'Close Student Account': '',
        'Close Educator Account': ''
    },
    {
        'First Name': 'amur',
        'Last Name': 'parentccdsr',
        'Primary Email Address': 'amur.parentccdsr@mailinator.com',
        'Email of Child (Data Subject)': 'child.amur@mailinator.com',
        'Child_First_Name': 'ChildAmur',
        'Child_Last_Name': 'Parent',
        'Phone': '555-0104',
        'Date of Birth': '12/05/2008',
        'Address': '321 Elm St',
        'City': 'Denver',
        'State': 'Colorado',
        'ZIP': '80205',
        'Country': 'United States',
        'Request_type': 'Remove my parent\'s cc information',
        'Student School Name': 'N/A',
        'Graduation Year': 'N/A',
        'Delete Additional Details': 'N/A',
        'Delete Student Data': '',
        'Delete Parent Data': '',
        'Delete Educator Data': '',
        'Close Student Account': '',
        'Close Educator Account': ''
    },
    {
        'First Name': 'test',
        'Last Name': 'closedsr',
        'Primary Email Address': 'test.closedsr@mailinator.com',
        'Email of Child (Data Subject)': 'child.test@mailinator.com',
        'Child_First_Name': 'ChildTest',
        'Child_Last_Name': 'Close',
        'Phone': '555-0105',
        'Date of Birth': '09/18/2012',
        'Address': '654 Maple Dr',
        'City': 'Denver',
        'State': 'Colorado',
        'ZIP': '80206',
        'Country': 'United States',
        'Request_type': 'Close/deactivate/cancel my College Board account',
        'Student School Name': 'N/A',
        'Graduation Year': 'N/A',
        'Delete Additional Details': 'N/A',
        'Delete Student Data': '',
        'Delete Parent Data': '',
        'Delete Educator Data': '',
        'Close Student Account': '',
        'Close Educator Account': ''
    }
]

# Create DataFrame
df = pd.DataFrame(parent_data)

# Create the directory if it doesn't exist
os.makedirs('dsr/data', exist_ok=True)

# Save to Excel file
df.to_excel('dsr/data/Parent_form_data.xlsx', index=False, engine='openpyxl')

print("✅ Parent_form_data.xlsx created successfully!")
print(f"📊 Created {len(parent_data)} parent records:")
for i, record in enumerate(parent_data):
    print(f"  Record {i+1}: {record['First Name']} {record['Last Name']} - Request: {record['Request_type']}")
