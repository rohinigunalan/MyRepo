import pandas as pd
import os

print("🎯 Creating Master Excel Template...")

# Sample data for testing all 6 automation types
data = [
    # International Parent
    {
        'Request_Category': 'International',
        'Request_Type': 'Parent', 
        'First name': 'Maria',
        'Last name': 'Rodriguez',
        'Email': 'maria.rodriguez@example.com',
        'Date of birth': '1985-06-15 00:00:00',
        'Phone number': '+1-555-0101',
        'Address line 1': '123 Elm Street',
        'City': 'Toronto',
        'State': 'Ontario',
        'Country': 'Canada',
        'What country are you in?': 'Canada',
        'Which of the following types of requests would you like to make?': 'Access my information',
        'What option do you want us to take with the data we find?': 'Send me a copy of my data',
        'If we find data, would you like us to close the account?': 'No',
        'What is your relationship to the person whose information you are requesting?': 'Parent',
        'What is the name of the person whose information you are requesting?': 'Sofia Rodriguez',
        'What is the date of birth of the person whose information you are requesting?': '2010-08-22 00:00:00',
        'Additional details': 'Test International Parent automation'
    },
    # International Myself
    {
        'Request_Category': 'International',
        'Request_Type': 'Myself',
        'First name': 'Jean',
        'Last name': 'Dubois',
        'Email': 'jean.dubois@example.com',
        'Date of birth': '1998-12-03 00:00:00',
        'Phone number': '+33-1-42-86-83-12',
        'Address line 1': '45 Rue de la Paix',
        'City': 'Paris',
        'State': 'Île-de-France',
        'Country': 'France',
        'What country are you in?': 'France',
        'Which of the following types of requests would you like to make?': 'Delete my information',
        'What option do you want us to take with the data we find?': 'Delete my data',
        'If we find data, would you like us to close the account?': 'Yes',
        'Additional details': 'Test International Myself automation'
    },
    # International Educator
    {
        'Request_Category': 'International',
        'Request_Type': 'Educator',
        'First name': 'Dr. Emma',
        'Last name': 'Thompson',
        'Email': 'emma.thompson@school.uk',
        'Date of birth': '1975-04-18 00:00:00',
        'Phone number': '+44-20-7946-0958',
        'Address line 1': '221B Baker Street',
        'City': 'London',
        'State': 'Greater London',
        'Country': 'United Kingdom',
        'What country are you in?': 'United Kingdom',
        'Which of the following types of requests would you like to make?': 'Access information on behalf of a student',
        'What option do you want us to take with the data we find?': 'Send me a copy of the data',
        'If we find data, would you like us to close the account?': 'No',
        'What is your role?': 'Guidance Counselor',
        'What is the name of your school or educational institution?': 'Oxford International School',
        'Name of the student whose information you are requesting': 'James Wilson',
        'Date of birth of the student whose information you are requesting': '2006-09-14 00:00:00',
        'Additional details': 'Test International Educator automation'
    },
    # Domestic Parent
    {
        'Request_Category': 'Domestic',
        'Request_Type': 'Parent',
        'First name': 'Jennifer',
        'Last name': 'Smith',
        'Email': 'jennifer.smith@example.com',
        'Date of birth': '1980-11-25 00:00:00',
        'Phone number': '(555) 123-4567',
        'Address line 1': '456 Oak Avenue',
        'City': 'Denver',
        'State': 'Colorado',
        'ZIP code': '80202',
        'Country': 'United States',
        'Which of the following types of requests would you like to make?': 'Access my information',
        'What option do you want us to take with the data we find?': 'Send me a copy of my data',
        'If we find data, would you like us to close the account?': 'No',
        'Additional details': 'Test Domestic Parent automation'
    },
    # Domestic Myself
    {
        'Request_Category': 'Domestic',
        'Request_Type': 'Myself',
        'First name': 'Michael',
        'Last name': 'Johnson',
        'Email': 'michael.johnson@example.com',
        'Date of birth': '2000-07-09 00:00:00',
        'Phone number': '(555) 987-6543',
        'Address line 1': '789 Pine Road',
        'City': 'Austin',
        'State': 'Texas',
        'ZIP code': '73301',
        'Country': 'United States',
        'Which of the following types of requests would you like to make?': 'Correct my information',
        'What option do you want us to take with the data we find?': 'Correct my data',
        'If we find data, would you like us to close the account?': 'No',
        'Additional details': 'Test Domestic Myself automation'
    },
    # Domestic Educator
    {
        'Request_Category': 'Domestic',
        'Request_Type': 'Educator',
        'First name': 'Sarah',
        'Last name': 'Wilson',
        'Email': 'sarah.wilson@school.edu',
        'Date of birth': '1972-02-14 00:00:00',
        'Phone number': '(555) 246-8135',
        'Address line 1': '321 Education Blvd',
        'City': 'Springfield',
        'State': 'Illinois',
        'ZIP code': '62701',
        'Country': 'United States',
        'Which of the following types of requests would you like to make?': 'Access information on behalf of a student',
        'What option do you want us to take with the data we find?': 'Send me a copy of the data',
        'If we find data, would you like us to close the account?': 'No',
        'What is your role?': 'High School Counselor',
        'What is the name of your school or educational institution?': 'Springfield High School',
        'Name of the student whose information you are requesting': 'Alex Thompson',
        'Date of birth of the student whose information you are requesting': '2005-03-28 00:00:00',
        'Additional details': 'Test Domestic Educator automation'
    }
]

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel
output_path = 'dsr/scripts/Combined/MASTER_TEMPLATE.xlsx'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_excel(output_path, index=False, sheet_name='Test_Data')

print(f"✅ Excel template created: {output_path}")
print(f"📊 Contains {len(data)} sample records for testing:")
for i, record in enumerate(data, 1):
    category = record['Request_Category']
    req_type = record['Request_Type']
    name = f"{record['First name']} {record['Last name']}"
    print(f"   {i}. {category} {req_type} - {name}")

print("\n🎯 Template ready for Master_All_Requests_AUTOMATION.py!")
