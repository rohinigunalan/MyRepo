#!/usr/bin/env python3
"""
🎯 MASTER EXCEL TEMPLATE CREATOR
Creates comprehensive Excel template for Master_All_Requests_AUTOMATION.py

This script creates a sample Excel file with all required columns
and sample data for testing all 6 automation types.
"""

import pandas as pd
import os
from datetime import datetime, timedelta
import random

def create_master_template():
    """Create comprehensive Excel template with sample data for all automation types"""
    
    print("🎯 Creating Master Excel Template for Combined Automation...")
    
    # Define all required columns
    columns = [
        # ROUTING COLUMNS (Required for automation type detection)
        'Request_Category',  # International/Domestic
        'Request_Type',      # Parent/Myself/Educator
        
        # COMMON PERSONAL INFO
        'First name',
        'Last name', 
        'Email',
        'Date of birth',
        'Phone number',
        'Address line 1',
        'Address line 2',
        'City',
        'State',
        'ZIP code',
        'Country',
        
        # REQUEST DETAILS
        'Which of the following types of requests would you like to make?',
        'What option do you want us to take with the data we find?',
        'If we find data, would you like us to close the account?',
        
        # INTERNATIONAL SPECIFIC
        'What country are you in?',
        'What is your relationship to the person whose information you are requesting?',
        'What is the name of the person whose information you are requesting?',
        'What is the date of birth of the person whose information you are requesting?',
        'Confirm that this person is deceased',
        
        # EDUCATOR SPECIFIC  
        'What is your role?',
        'What is the name of your school or educational institution?',
        'What is the address of your school or educational institution?',
        'What is the city of your school or educational institution?',
        'What is the state of your school or educational institution?',
        'What is the ZIP code of your school or educational institution?',
        'What is the country of your school or educational institution?',
        'Name of the student whose information you are requesting',
        'Date of birth of the student whose information you are requesting',
        
        # ADDITIONAL FIELDS
        'Additional details'
    ]
    
    # Sample data for different automation types
    sample_records = [
        # INTERNATIONAL PARENT
        {
            'Request_Category': 'International',
            'Request_Type': 'Parent',
            'First name': 'Maria',
            'Last name': 'Rodriguez',
            'Email': 'maria.rodriguez@example.com',
            'Date of birth': '1985-06-15 00:00:00',
            'Phone number': '+1-555-0101',
            'Address line 1': '123 Elm Street',
            'Address line 2': 'Apt 4B',
            'City': 'Toronto',
            'State': 'Ontario',
            'ZIP code': 'M5V 3A8',
            'Country': 'Canada',
            'What country are you in?': 'Canada',
            'Which of the following types of requests would you like to make?': 'Access my information',
            'What option do you want us to take with the data we find?': 'Send me a copy of my data',
            'If we find data, would you like us to close the account?': 'No',
            'What is your relationship to the person whose information you are requesting?': 'Parent',
            'What is the name of the person whose information you are requesting?': 'Sofia Rodriguez',
            'What is the date of birth of the person whose information you are requesting?': '2010-08-22 00:00:00',
            'Confirm that this person is deceased': 'No',
            'Additional details': 'Requesting access to my child\'s College Board account data'
        },
        
        # INTERNATIONAL MYSELF
        {
            'Request_Category': 'International',
            'Request_Type': 'Myself',
            'First name': 'Jean',
            'Last name': 'Dubois',
            'Email': 'jean.dubois@example.com',
            'Date of birth': '1998-12-03 00:00:00',
            'Phone number': '+33-1-42-86-83-12',
            'Address line 1': '45 Rue de la Paix',
            'Address line 2': '',
            'City': 'Paris',
            'State': 'Île-de-France',
            'ZIP code': '75002',
            'Country': 'France',
            'What country are you in?': 'France',
            'Which of the following types of requests would you like to make?': 'Delete my information',
            'What option do you want us to take with the data we find?': 'Delete my data',
            'If we find data, would you like us to close the account?': 'Yes',
            'Additional details': 'Please delete all my College Board account information'
        },
        
        # INTERNATIONAL EDUCATOR
        {
            'Request_Category': 'International',
            'Request_Type': 'Educator',
            'First name': 'Dr. Emma',
            'Last name': 'Thompson',
            'Email': 'emma.thompson@oxfordschool.uk',
            'Date of birth': '1975-04-18 00:00:00',
            'Phone number': '+44-20-7946-0958',
            'Address line 1': '221B Baker Street',
            'Address line 2': '',
            'City': 'London',
            'State': 'Greater London',
            'ZIP code': 'NW1 6XE',
            'Country': 'United Kingdom',
            'What country are you in?': 'United Kingdom',
            'Which of the following types of requests would you like to make?': 'Access information on behalf of a student',
            'What option do you want us to take with the data we find?': 'Send me a copy of the data',
            'If we find data, would you like us to close the account?': 'No',
            'What is your role?': 'Guidance Counselor',
            'What is the name of your school or educational institution?': 'Oxford International School',
            'What is the address of your school or educational institution?': '221B Baker Street',
            'What is the city of your school or educational institution?': 'London',
            'What is the state of your school or educational institution?': 'Greater London',
            'What is the ZIP code of your school or educational institution?': 'NW1 6XE',
            'What is the country of your school or educational institution?': 'United Kingdom',
            'Name of the student whose information you are requesting': 'James Wilson',
            'Date of birth of the student whose information you are requesting': '2006-09-14 00:00:00',
            'Additional details': 'Requesting student information for college guidance purposes'
        },
        
        # DOMESTIC PARENT
        {
            'Request_Category': 'Domestic',
            'Request_Type': 'Parent',
            'First name': 'Jennifer',
            'Last name': 'Smith',
            'Email': 'jennifer.smith@example.com',
            'Date of birth': '1980-11-25 00:00:00',
            'Phone number': '(555) 123-4567',
            'Address line 1': '456 Oak Avenue',
            'Address line 2': '',
            'City': 'Denver',
            'State': 'Colorado',
            'ZIP code': '80202',
            'Country': 'United States',
            'Which of the following types of requests would you like to make?': 'Access my information',
            'What option do you want us to take with the data we find?': 'Send me a copy of my data',
            'If we find data, would you like us to close the account?': 'No',
            'Additional details': 'Need to access my child\'s SAT score information'
        },
        
        # DOMESTIC MYSELF
        {
            'Request_Category': 'Domestic',
            'Request_Type': 'Myself',
            'First name': 'Michael',
            'Last name': 'Johnson',
            'Email': 'michael.johnson@example.com',
            'Date of birth': '2000-07-09 00:00:00',
            'Phone number': '(555) 987-6543',
            'Address line 1': '789 Pine Road',
            'Address line 2': 'Unit 12',
            'City': 'Austin',
            'State': 'Texas',
            'ZIP code': '73301',
            'Country': 'United States',
            'Which of the following types of requests would you like to make?': 'Correct my information',
            'What option do you want us to take with the data we find?': 'Correct my data',
            'If we find data, would you like us to close the account?': 'No',
            'Additional details': 'Need to update incorrect address in my College Board profile'
        },
        
        # DOMESTIC EDUCATOR
        {
            'Request_Category': 'Domestic',
            'Request_Type': 'Educator',
            'First name': 'Sarah',
            'Last name': 'Wilson',
            'Email': 'sarah.wilson@springfieldhs.edu',
            'Date of birth': '1972-02-14 00:00:00',
            'Phone number': '(555) 246-8135',
            'Address line 1': '321 Education Blvd',
            'Address line 2': '',
            'City': 'Springfield',
            'State': 'Illinois',
            'ZIP code': '62701',
            'Country': 'United States',
            'Which of the following types of requests would you like to make?': 'Access information on behalf of a student',
            'What option do you want us to take with the data we find?': 'Send me a copy of the data',
            'If we find data, would you like us to close the account?': 'No',
            'What is your role?': 'High School Counselor',
            'What is the name of your school or educational institution?': 'Springfield High School',
            'What is the address of your school or educational institution?': '321 Education Blvd',
            'What is the city of your school or educational institution?': 'Springfield',
            'What is the state of your school or educational institution?': 'Illinois',
            'What is the ZIP code of your school or educational institution?': '62701',
            'What is the country of your school or educational institution?': 'United States',
            'Name of the student whose information you are requesting': 'Alex Thompson',
            'Date of birth of the student whose information you are requesting': '2005-03-28 00:00:00',
            'Additional details': 'Requesting AP score information for transcript purposes'
        }
    ]
    
    # Create DataFrame
    df = pd.DataFrame(sample_records)
    
    # Ensure all columns are present (fill missing with empty strings)
    for col in columns:
        if col not in df.columns:
            df[col] = ''
    
    # Reorder columns
    df = df[columns]
    
    # Save to Excel
    output_path = "dsr/scripts/Combined/MASTER_TEMPLATE.xlsx"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df.to_excel(output_path, index=False, sheet_name='Master_Template')
    
    print(f"✅ Master Excel template created: {output_path}")
    print(f"📊 Template contains {len(sample_records)} sample records")
    print(f"📋 Template includes {len(columns)} columns")
    print("\n🎯 Sample records included:")
    for i, record in enumerate(sample_records, 1):
        category = record['Request_Category']
        req_type = record['Request_Type']
        print(f"   {i}. {category} {req_type} - {record['First name']} {record['Last name']}")
    
    print(f"\n📁 Use this template with Master_All_Requests_AUTOMATION.py")
    print(f"   ✅ All automation types covered")
    print(f"   ✅ All required fields included")
    print(f"   ✅ Sample data ready for testing")
    
    return output_path

if __name__ == "__main__":
    create_master_template()
