import pandas as pd
import os

# Create comprehensive parent data matching what the script successfully filled
parent_data = [
    {
        # Parent Information (from your original data)
        'Who is making this request': 'Parent on behalf of child',
        ' First_Name_of parent_guardian': 'Parentone',
        'Last Name of parent/guardian': 'ParentbehalfofStu',
        'Primary Email Address': 'palmone@mailinator.com',
        
        # Child Information (from your original data)
        'First Name': 'new',
        'Last Name': 'deletedsr',
        'Email of Child (Data Subject)': 'new.deletedsr@mailinator.com',
        
        # Contact Information (what the script fills)
        ' Date of Birth': '11/8/2004',
        'Phone Number': '5712345572',
        'country': 'US',
        'stateOrProvince': 'Colorado',
        'postalCode': '80209-3456',
        'city': 'Denver',
        'streetAddress': '1625 Cherry Creek Drive, Apt 3C',
        
        # Additional Details (what the script fills)
        'studentSchoolName': 'N/A',
        'studentGraduationYear': 'N/A',
        'educatorSchoolAffiliation': 'N/A',
        
        # Request Information
        'Request_type': 'request to delete my data',
        'inlinedatafordelete': 'DSR test'
    },
    {
        # Parent Information
        'Who is making this request': 'Parent on behalf of child',
        ' First_Name_of parent_guardian': 'Parenttwo',
        'Last Name of parent/guardian': 'ParentbehalfofStu',
        'Primary Email Address': 'palmtwo@mailinator.com',
        
        # Child Information
        'First Name': 'kiran',
        'Last Name': 'infodsr',
        'Email of Child (Data Subject)': 'kiran.infodsr@mailinator.com',
        
        # Contact Information
        ' Date of Birth': '03/22/2009',
        'Phone Number': '5712345573',
        'country': 'US',
        'stateOrProvince': 'Colorado',
        'postalCode': '80210-1234',
        'city': 'Denver',
        'streetAddress': '456 Oak Avenue, Suite 2B',
        
        # Additional Details
        'studentSchoolName': 'N/A',
        'studentGraduationYear': 'N/A',
        'educatorSchoolAffiliation': 'N/A',
        
        # Request Information
        'Request_type': 'request to copy of my data',
        'inlinedatafordelete': ''
    },
    {
        # Parent Information
        'Who is making this request': 'Parent on behalf of child',
        ' First_Name_of parent_guardian': 'parentthree',
        'Last Name of parent/guardian': 'ParentbehalfofStu',
        'Primary Email Address': 'palmthree@mailinator.com',
        
        # Child Information
        'First Name': 'kayal',
        'Last Name': 'optdsr',
        'Email of Child (Data Subject)': 'kayal.optdsr@mailinator.com',
        
        # Contact Information
        ' Date of Birth': '07/10/2011',
        'Phone Number': '5712345574',
        'country': 'US',
        'stateOrProvince': 'Colorado',
        'postalCode': '80211-5678',
        'city': 'Denver',
        'streetAddress': '789 Pine Road, Unit 4A',
        
        # Additional Details
        'studentSchoolName': 'N/A',
        'studentGraduationYear': 'N/A',
        'educatorSchoolAffiliation': 'N/A',
        
        # Request Information
        'Request_type': 'Opt out of search',
        'inlinedatafordelete': ''
    },
    {
        # Parent Information
        'Who is making this request': 'Parent on behalf of child',
        ' First_Name_of parent_guardian': 'Parentfour',
        'Last Name of parent/guardian': 'ParentbehalfofStu',
        'Primary Email Address': 'palmfour@mailinator.com',
        
        # Child Information
        'First Name': 'amur',
        'Last Name': 'parentccdsr',
        'Email of Child (Data Subject)': 'amur.parentccdsr@mailinator.com',
        
        # Contact Information
        ' Date of Birth': '12/05/2008',
        'Phone Number': '5712345575',
        'country': 'US',
        'stateOrProvince': 'Colorado',
        'postalCode': '80212-9012',
        'city': 'Denver',
        'streetAddress': '321 Elm Street, Apt 1C',
        
        # Additional Details
        'studentSchoolName': 'N/A',
        'studentGraduationYear': 'N/A',
        'educatorSchoolAffiliation': 'N/A',
        
        # Request Information
        'Request_type': 'Remove my parent\'s cc information',
        'inlinedatafordelete': ''
    },
    {
        # Parent Information
        'Who is making this request': 'Parent on behalf of child',
        ' First_Name_of parent_guardian': 'Parentfive',
        'Last Name of parent/guardian': 'ParentbehalfofStu',
        'Primary Email Address': 'palmfive@mailinator.com',
        
        # Child Information
        'First Name': 'test',
        'Last Name': 'closedsr',
        'Email of Child (Data Subject)': 'test.closedsr@mailinator.com',
        
        # Contact Information
        ' Date of Birth': '09/18/2012',
        'Phone Number': '5712345576',
        'country': 'US',
        'stateOrProvince': 'Colorado',
        'postalCode': '80213-3456',
        'city': 'Denver',
        'streetAddress': '654 Maple Drive, Unit 5B',
        
        # Additional Details
        'studentSchoolName': 'N/A',
        'studentGraduationYear': 'N/A',
        'educatorSchoolAffiliation': 'N/A',
        
        # Request Information
        'Request_type': 'Close/deactivate/cancel my College Board account',
        'inlinedatafordelete': ''
    }
]

# Create DataFrame
df = pd.DataFrame(parent_data)

# Create the directory if it doesn't exist
os.makedirs('dsr/data', exist_ok=True)

# Backup the existing file first
backup_file = 'dsr/data/Parent_form_data_backup.xlsx'
if os.path.exists('dsr/data/Parent_form_data.xlsx'):
    import shutil
    shutil.copy('dsr/data/Parent_form_data.xlsx', backup_file)
    print(f"✅ Backup created: {backup_file}")

# Save to Excel file
df.to_excel('dsr/data/Parent_form_data.xlsx', index=False, engine='openpyxl')

print("✅ Parent_form_data.xlsx updated successfully with complete form data!")
print(f"📊 Updated {len(parent_data)} parent records with all form fields:")
print("\n🔍 Data Summary:")
for i, record in enumerate(parent_data):
    print(f"  Record {i+1}: {record[' First_Name_of parent_guardian']} {record['Last Name of parent/guardian']}")
    print(f"    Child: {record['First Name']} {record['Last Name']}")
    print(f"    Child Email: {record['Email of Child (Data Subject)']}")
    print(f"    Parent Email: {record['Primary Email Address']}")
    print(f"    Phone: {record['Phone Number']}")
    print(f"    Address: {record['streetAddress']}, {record['city']}, {record['stateOrProvince']} {record['postalCode']}")
    print(f"    Request: {record['Request_type']}")
    print()

print("📋 All fields that the script fills are now included in the Excel file:")
print("  ✅ Parent Information: First Name, Last Name, Email")
print("  ✅ Child Information: First Name, Last Name, Email")
print("  ✅ Contact Information: Phone, Date of Birth, Address, City, State, ZIP, Country")
print("  ✅ Additional Details: School Name, Graduation Year, Educator Affiliation")
print("  ✅ Request Information: Request Type, Additional Details")
