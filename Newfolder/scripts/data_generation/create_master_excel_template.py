import pandas as pd
import os

def create_master_excel_template():
    """Create the Master Excel template for all automation types"""
    print("📊 Creating Master Excel template with all automation types...")
    
    # Sample data covering all 6 automation combinations
    master_data = [
        # International Parent
        {
            'Request_Category': 'International',
            'Request_Type': 'Parent',
            'Parent First Name': 'John',
            'Parent Last Name': 'Smith',
            'Primary Email Address': 'john.smith@mailinator.com',
            'Child First Name': 'Emily',
            'Child Last Name': 'Smith',
            'Date of Birth': '2010-05-15',
            'Phone Number': '5712345678',
            'Address': '123 Main Street',
            'City': 'New York',
            'State': 'New York',
            'Zip Code': '10001',
            'Country': 'United States',
            'Which of the following types of requests would you like to make?': 'Request a copy of my data'
        },
        # Domestic Parent
        {
            'Request_Category': 'Domestic',
            'Request_Type': 'Parent',
            'Parent First Name': 'Sarah',
            'Parent Last Name': 'Johnson',
            'Primary Email Address': 'sarah.johnson@mailinator.com',
            'Child First Name': 'Michael',
            'Child Last Name': 'Johnson',
            'Date of Birth': '2012-08-22',
            'Phone Number': '5719876543',
            'Address': '456 Oak Avenue',
            'City': 'Denver',
            'State': 'Colorado',
            'Zip Code': '80202',
            'Country': 'United States',
            'Which of the following types of requests would you like to make?': 'request to delete my data',
            'delete_student': 'Student data (if any)',
            'delete_parent': 'Parent data (if any)',
            'delete_educator': ''
        },
        # International Myself
        {
            'Request_Category': 'International',
            'Request_Type': 'Myself',
            'First Name': 'Maria',
            'Last Name': 'Garcia',
            'Primary Email Address': 'maria.garcia@mailinator.com',
            'Date of Birth': '1995-12-03',
            'Phone Number': '5713334444',
            'Address': '789 Pine Road',
            'City': 'Miami',
            'State': 'Florida',
            'Zip Code': '33101',
            'Country': 'United States',
            'Which of the following types of requests would you like to make?': 'Opt out of search'
        },
        # Domestic Myself
        {
            'Request_Category': 'Domestic',
            'Request_Type': 'Myself',
            'First Name': 'David',
            'Last Name': 'Brown',
            'Primary Email Address': 'david.brown@mailinator.com',
            'Date of Birth': '1988-04-18',
            'Phone Number': '5715556666',
            'Address': '321 Elm Street',
            'City': 'Austin',
            'State': 'Texas',
            'Zip Code': '78701',
            'Country': 'United States',
            'Which of the following types of requests would you like to make?': 'Close/deactivate/cancel my College Board account',
            'close_student': 'Student account (if any)',
            'close_educator': ''
        },
        # International Educator
        {
            'Request_Category': 'International',
            'Request_Type': 'Educator',
            'Agent First Name': 'Lisa',
            'Agent Last Name': 'Wilson',
            'Agent Email Address': 'lisa.wilson@mailinator.com',
            'Authorized Agent Company Name (insert N/A if not applicable)': 'Wilson Education Services',
            'Student First Name': 'James',
            'Student Last Name': 'Wilson',
            'Primary Email Address': 'james.wilson@mailinator.com',
            'Date of Birth': '2008-11-12',
            'Phone Number': '5717778888',
            'Address': '654 Maple Drive',
            'City': 'Seattle',
            'State': 'Washington',
            'Zip Code': '98101',
            'Country': 'United States',
            'Which of the following types of requests would you like to make?': 'Request a copy of my data'
        },
        # Domestic Educator
        {
            'Request_Category': 'Domestic',
            'Request_Type': 'Educator',
            'Agent First Name': 'Robert',
            'Agent Last Name': 'Davis',
            'Agent Email Address': 'robert.davis@mailinator.com',
            'Authorized Agent Company Name (insert N/A if not applicable)': 'N/A',
            'Student First Name': 'Sophia',
            'Student Last Name': 'Davis',
            'Primary Email Address': 'sophia.davis@mailinator.com',
            'Date of Birth': '2009-07-25',
            'Phone Number': '5719990000',
            'Address': '987 Birch Lane',
            'City': 'Phoenix',
            'State': 'Arizona',
            'Zip Code': '85001',
            'Country': 'United States',
            'Which of the following types of requests would you like to make?': 'request to delete my data',
            'delete_student': '',
            'delete_parent': 'Parent data (if any)',
            'delete_educator': 'Educator data (if any)'
        }
    ]
    
    # Create DataFrame
    df = pd.DataFrame(master_data)
    
    # Create output directory
    output_dir = "dsr/data/Combined"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to Excel file
    excel_file = f"{output_dir}/Master_All_Requests_form_data.xlsx"
    df.to_excel(excel_file, index=False, engine='openpyxl')
    
    print(f"✅ Master Excel template created: {excel_file}")
    print(f"📊 Total records: {len(df)}")
    print("📋 Automation type breakdown:")
    breakdown = df.groupby(['Request_Category', 'Request_Type']).size()
    for (category, req_type), count in breakdown.items():
        print(f"   {category} {req_type}: {count} record(s)")
    
    print(f"\n🎯 Ready to run master automation with:")
    print(f"   📂 Excel file: {excel_file}")
    print(f"   🚀 Script: Master_All_Requests_AUTOMATION.py")
    
    return excel_file

if __name__ == "__main__":
    create_master_excel_template()
