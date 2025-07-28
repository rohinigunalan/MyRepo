import pandas as pd

# Create the data dictionary
data = {
    'Email Address': 'palmny1@mailinator.com',
    'First_Name': 'RobNY',
    'Last_Name': 'EdisonNY',
    'birthDate': '11/1/2003',
    'phone': '5712345567',
    'country': 'US',
    'stateOrProvince': 'New York',
    'postalCode': '14111',
    'city': 'North Collins',
    'streetAddress': '507 Central Avenue',
    'studentSchoolName': 'South Lakes High School',
    'studentGraduationYear': '2020',
    'educatorSchoolAffiliation': 'N/A',
    'Request_type': 'Request a copy of my data'
}

# Create DataFrame with one row
df = pd.DataFrame([data])

# Save to Excel
df.to_excel('form_data.xlsx', index=False)
print("✅ Excel file 'form_data.xlsx' created successfully!")
print("\n📊 Data in the file:")
print(df)
