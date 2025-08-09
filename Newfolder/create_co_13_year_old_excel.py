import pandas as pd
from datetime import datetime
import os

# Create Excel data for 13-year-old Colorado student
data = {
    'Record_ID': [1],
    'First_Name': ['Sophia'],
    'Last_Name': ['Martinez'],
    'Middle_Initial': ['A'],
    'Email': ['sophia.martinez13@mailinator.com'],
    'Phone': ['7205551357'],
    'Birth_Date': ['03/15/2012'],  # 13 years old
    'Address': ['2468 Pine Ridge Circle, Apt 7B'],
    'City': ['Thornton'],
    'State': ['Colorado'],
    'ZIP_Code': ['80241'],
    'Country': ['United States'],
    'Gender': ['Female'],
    'Student_School': ['Thornton Middle School'],
    'Graduation_Year': ['2030'],
    'Educator_Affiliation': ['N/A'],
    'Request_Type': ['Close/deactivate/cancel my College Board account'],
    'Student_Account_Close': ['Student account (if any)'],
    'Educator_Account_Close': [''],
    'Parent_First_Name': ['Maria'],
    'Parent_Last_Name': ['Martinez'],
    'Parent_Email': ['maria.martinez.parent@mailinator.com'],
    'AI_Code': ['013579'],
    'Expected_Graduation': ['06/15/2030'],
    'Device_Type_Primary': ['Mobile'],
    'Device_Type_Alt': ['International'],
    'Text_Msg_Allowed': ['Y'],
    'Newsletter_Subscription': ['Y'],
    'CC_Selected': ['Y'],
    'Student_Search_OptIn': ['N'],
    'Sunday_Test_Taker': ['N'],
    'Deceased': ['N'],
    'Active': ['Y'],
    'ZIP4': ['2468'],
    'Area_Code': ['720'],
    'Phone_Local': ['5551357'],
    'Alt_Phone_Country': ['44'],
    'Alt_Phone_Intl': ['7890123456'],
    'Notes': ['13-year-old student test case for Colorado']
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel with multiple sheets
output_file = 'CO_13_Year_Old_Student_Data.xlsx'

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # Main data sheet
    df.to_excel(writer, sheet_name='Student_Data', index=False)
    
    # API Payload sheet with JSON structure
    api_data = {
        'Field': [
            'requestName',
            'channel.type',
            'channel.orgId',
            'personInfo.matchInd',
            'personInfo.genderCd',
            'personInfo.firstNm',
            'personInfo.lastNm',
            'personInfo.middleInitial',
            'personInfo.birthDt',
            'personInfo.hsGradDt',
            'personInfo.aiCd',
            'homeAddress.streetAddr1',
            'homeAddress.streetAddr2',
            'homeAddress.city',
            'homeAddress.zip5',
            'homeAddress.zip4',
            'homeAddress.stateCd',
            'homeAddress.countryIsoCd',
            'personalEmail.emailAddress',
            'homePhone.ndc',
            'homePhone.cc',
            'homePhone.local',
            'altPhone.cc',
            'altPhone.intlPhone',
            'personParent.firstNm',
            'personParent.lastNm',
            'personParent.emailAddr',
            'callerAppId',
            'aiDomainCd'
        ],
        'Value': [
            'createPersonInfo',
            'C',
            '0',
            'Y',
            'F',
            'Sophia',
            'Martinez',
            'A',
            '2012-03-15',
            '2030-06-15',
            '013579',
            '2468 Pine Ridge Circle',
            'Apt 7B',
            'Thornton',
            '80241',
            '2468',
            'CO',
            'US',
            'sophia.martinez13@mailinator.com',
            '720',
            '1',
            '5551357',
            '44',
            '7890123456',
            'Maria',
            'Martinez',
            'maria.martinez.parent@mailinator.com',
            '303',
            'SAT'
        ],
        'Description': [
            'API request type',
            'Channel type',
            'Organization ID',
            'Match indicator',
            'Gender code (F=Female)',
            'First name',
            'Last name',
            'Middle initial',
            'Birth date (13 years old)',
            'High school graduation date',
            'AI code',
            'Street address line 1',
            'Street address line 2',
            'City',
            'ZIP code (5 digits)',
            'ZIP code (4 digits)',
            'State code',
            'Country ISO code',
            'Email address',
            'Area code',
            'Country code',
            'Local phone number',
            'Alt phone country code',
            'International phone number',
            'Parent first name',
            'Parent last name',
            'Parent email address',
            'Caller application ID',
            'AI domain code'
        ]
    }
    
    api_df = pd.DataFrame(api_data)
    api_df.to_excel(writer, sheet_name='API_Mapping', index=False)
    
    # Summary sheet
    summary_data = {
        'Category': [
            'Student Information',
            'Student Information',
            'Student Information',
            'Student Information',
            'Contact Information',
            'Contact Information',
            'Contact Information',
            'Contact Information',
            'Address Information',
            'Address Information',
            'Address Information',
            'Address Information',
            'Parent Information',
            'Parent Information',
            'Parent Information',
            'Technical Information',
            'Technical Information',
            'Test Case Information'
        ],
        'Field': [
            'Full Name',
            'Age',
            'Birth Date',
            'Expected Graduation',
            'Email',
            'Phone',
            'Alt Phone',
            'Text Messages',
            'Street Address',
            'City, State',
            'ZIP Code',
            'Country',
            'Parent Name',
            'Parent Email',
            'Newsletter Subscription',
            'AI Code',
            'API Domain',
            'Test Purpose'
        ],
        'Value': [
            'Sophia A. Martinez',
            '13 years old',
            'March 15, 2012',
            'June 15, 2030',
            'sophia.martinez13@mailinator.com',
            '(720) 555-1357',
            '+44 7890123456',
            'Allowed',
            '2468 Pine Ridge Circle, Apt 7B',
            'Thornton, CO',
            '80241-2468',
            'United States',
            'Maria Martinez',
            'maria.martinez.parent@mailinator.com',
            'Yes',
            '013579',
            'SAT',
            'Test 13-year-old student data for API validation'
        ]
    }
    
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_excel(writer, sheet_name='Summary', index=False)

print(f"✅ Excel file created: {output_file}")
print("\n📊 File contains 3 sheets:")
print("   1. Student_Data - Main data in Excel format")
print("   2. API_Mapping - Field mapping for API payload")
print("   3. Summary - Human-readable summary")
print(f"\n👤 Student: Sophia Martinez (Age 13)")
print(f"📍 Location: Thornton, Colorado")
print(f"🎂 Birth Date: March 15, 2012")
print(f"🎓 Expected Graduation: June 15, 2030")
print(f"📧 Email: sophia.martinez13@mailinator.com")
print(f"👨‍👩‍👧 Parent: Maria Martinez")

# Display the main data
print(f"\n📋 Main Excel Data Preview:")
print(df.to_string(index=False))
