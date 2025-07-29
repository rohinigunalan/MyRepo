import pandas as pd

# Simple test to create Excel file with verified data
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

# Create DataFrame and save
df = pd.DataFrame([data])
df.to_excel('form_data.xlsx', index=False)

print("✅ Excel file recreated with 'New York'")
print("State value:", df.iloc[0]['stateOrProvince'])
print("State type:", type(df.iloc[0]['stateOrProvince']))

# Test loading
test_df = pd.read_excel('form_data.xlsx')
form_data = test_df.iloc[0].to_dict()
test_state = str(form_data.get('stateOrProvince', 'New York'))
print(f"Loaded state: '{test_state}'")
