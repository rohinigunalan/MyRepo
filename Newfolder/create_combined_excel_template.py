import pandas as pd
import os

def create_combined_excel_template():
    """Create a combined Excel template with both International and Domestic records"""
    
    # Sample data combining both international and domestic records
    sample_data = [
        {
            'Request_Category': 'International',
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
            'Which of the following types of requests would you like to make?': 'Request a copy of my data',
            'Request_Notes': 'International parent request for data copy'
        },
        {
            'Request_Category': 'Domestic',
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
            'delete_educator': '',
            'Request_Notes': 'Domestic parent request for data deletion'
        },
        {
            'Request_Category': 'International',
            'Parent First Name': 'Maria',
            'Parent Last Name': 'Garcia',
            'Primary Email Address': 'maria.garcia@mailinator.com',
            'Child First Name': 'Carlos',
            'Child Last Name': 'Garcia',
            'Date of Birth': '2009-12-03',
            'Phone Number': '5713334444',
            'Address': '789 Pine Road',
            'City': 'Miami',
            'State': 'Florida',
            'Zip Code': '33101',
            'Country': 'United States',
            'Which of the following types of requests would you like to make?': 'Opt out of search',
            'Request_Notes': 'International parent opt-out request'
        },
        {
            'Request_Category': 'Domestic',
            'Parent First Name': 'David',
            'Parent Last Name': 'Brown',
            'Primary Email Address': 'david.brown@mailinator.com',
            'Child First Name': 'Jessica',
            'Child Last Name': 'Brown',
            'Date of Birth': '2011-04-18',
            'Phone Number': '5715556666',
            'Address': '321 Elm Street',
            'City': 'Austin',
            'State': 'Texas',
            'Zip Code': '78701',
            'Country': 'United States',
            'Which of the following types of requests would you like to make?': 'Close/deactivate/cancel my College Board account',
            'close_student': 'Student account (if any)',
            'close_educator': '',
            'Request_Notes': 'Domestic parent account closure request'
        }
    ]
    
    # Create DataFrame
    df = pd.DataFrame(sample_data)
    
    # Create output directory if it doesn't exist
    output_dir = "dsr/data/Combined"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to Excel file
    excel_file = f"{output_dir}/Combined_Parent_form_data.xlsx"
    df.to_excel(excel_file, index=False, engine='openpyxl')
    
    print(f"✅ Combined Excel template created: {excel_file}")
    print(f"📊 Records created: {len(df)}")
    print("📋 Request category breakdown:")
    category_counts = df['Request_Category'].value_counts()
    for category, count in category_counts.items():
        print(f"   {category}: {count} records")
    
    return excel_file

if __name__ == "__main__":
    create_combined_excel_template()
