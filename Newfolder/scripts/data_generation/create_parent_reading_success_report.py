import pandas as pd
import os
from datetime import datetime

# Define the screenshots directory constant for organized output
SCREENSHOTS_DIR = "dsr/screenshots/Domestic_Parent_onbehalfofstudent"

def create_parent_reading_success_report():
    """Create a report of successfully read data from parent Excel files (domestic or international)"""
    
    # Create timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("📊 Creating Parent Data Reading Success Report...")
    print(f"🕒 Timestamp: {timestamp}")
    
    # Check for both domestic and international Excel files
    domestic_file = "dsr/data/Domestic_Parent_form_data.xlsx"
    international_file = "dsr/data/International_Parent_form_data.xlsx"
    legacy_domestic_file = "dsr/data/Parent_form_data.xlsx"
    
    excel_file = None
    file_type = ""
    
    # Priority: Check for domestic file first, then international, then legacy
    if os.path.exists(domestic_file):
        excel_file = domestic_file
        file_type = "Domestic"
        print(f"📂 Found Domestic parent file: {excel_file}")
    elif os.path.exists(international_file):
        excel_file = international_file
        file_type = "International"
        print(f"📂 Found International parent file: {excel_file}")
    elif os.path.exists(legacy_domestic_file):
        excel_file = legacy_domestic_file
        file_type = "Legacy_Domestic"
        print(f"📂 Found Legacy Domestic parent file: {excel_file}")
    else:
        print(f"❌ No Excel file found:")
        print(f"   - Domestic: {domestic_file}")
        print(f"   - International: {international_file}")
        print(f"   - Legacy Domestic: {legacy_domestic_file}")
        return None
    
    try:
        if os.path.exists(excel_file):
            print(f"📂 Reading data from: {excel_file}")
            df = pd.read_excel(excel_file, engine='openpyxl', na_filter=False, keep_default_na=False, dtype=str)
            print(f"✅ Successfully loaded {len(df)} records")
        else:
            print(f"❌ Excel file not found: {excel_file}")
            return
        
        # Process each record and extract key data
        success_data = []
        
        for index, row in df.iterrows():
            try:
                # Extract key parent information
                parent_first_name = str(row.get(' First_Name_of parent_guardian', '')).strip()
                parent_last_name = str(row.get('Last Name of parent/guardian', '')).strip()
                parent_email = str(row.get('Primary Email Address', '')).strip()
                
                # Extract child information
                child_first_name = str(row.get('First Name', '')).strip()
                child_last_name = str(row.get('Last Name', '')).strip()
                child_email = str(row.get('Email of Child (Data Subject)', '')).strip()
                
                # Extract request information
                request_type = str(row.get('Request_type', '')).strip()
                
                # Extract contact information
                phone = str(row.get('phone', '')).strip()
                state = str(row.get('stateOrProvince', '')).strip()
                
                # Determine status based on data completeness
                if parent_first_name and parent_last_name and child_first_name and child_last_name and request_type:
                    status = "SUCCESS"
                elif parent_first_name or parent_last_name or child_first_name or child_last_name:
                    status = "PARTIAL"
                else:
                    status = "EMPTY"
                
                # Create success record
                success_record = {
                    'Record_Number': index + 1,
                    'Parent_First_Name_READ': parent_first_name,
                    'Parent_Last_Name_READ': parent_last_name,
                    'Parent_Email_READ': parent_email,
                    'Child_First_Name_READ': child_first_name,
                    'Child_Last_Name_READ': child_last_name,
                    'Child_Email_READ': child_email,
                    'Privacy_Request_Type_READ': request_type,
                    'Phone_READ': phone,
                    'State_READ': state,
                    'Data_Read_Status': status,
                    'File_Type': file_type,
                    'Timestamp': timestamp
                }
                
                success_data.append(success_record)
                
                # Print progress for successful records
                if status == "SUCCESS":
                    print(f"🔍 Processing Record {index + 1}...")
                    print(f"  ✅ Parent: {success_record['Parent_First_Name_READ']} {success_record['Parent_Last_Name_READ']}")
                    print(f"  ✅ Child: {success_record['Child_First_Name_READ']} {success_record['Child_Last_Name_READ']}")
                    print(f"  ✅ Child Email: {success_record['Child_Email_READ']}")
                    print(f"  ✅ Request: {success_record['Privacy_Request_Type_READ']}")
                    print(f"  ✅ Status: {success_record['Data_Read_Status']}")
                
            except Exception as e:
                print(f"⚠️ Error processing record {index + 1}: {str(e)}")
                # Still add a record with error status
                success_data.append({
                    'Record_Number': index + 1,
                    'Parent_First_Name_READ': 'ERROR',
                    'Parent_Last_Name_READ': 'ERROR',
                    'Parent_Email_READ': 'ERROR', 
                    'Child_First_Name_READ': 'ERROR',
                    'Child_Last_Name_READ': 'ERROR',
                    'Child_Email_READ': 'ERROR',
                    'Privacy_Request_Type_READ': 'ERROR',
                    'Phone_READ': 'ERROR',
                    'State_READ': 'ERROR',
                    'Data_Read_Status': 'ERROR',
                    'File_Type': file_type,
                    'Timestamp': timestamp
                })
        
        # Create DataFrame from success data
        success_df = pd.DataFrame(success_data)
        
        # Ensure screenshots directory exists
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        
        # Create the report filename with timestamp
        report_filename = f"{SCREENSHOTS_DIR}/Parent_Data_Reading_Success_Report_{timestamp}.xlsx"
        
        # Save to Excel with multiple sheets for different views
        with pd.ExcelWriter(report_filename, engine='openpyxl') as writer:
            # Main report sheet
            success_df.to_excel(writer, sheet_name='Parent_Reading_Report', index=False)
            
            # Summary sheet
            summary_data = {
                'Report_Info': [
                    'Total Records',
                    'Successfully Read Records',
                    'Partial Records',
                    'Empty Records',
                    'Error Records',
                    'Parent Email Working',
                    'Child Email Working',
                    'Request Type Working',
                    'Phone Working',
                    'State Working',
                    'Report Generated'
                ],
                'Count': [
                    len(success_df),
                    len(success_df[success_df['Data_Read_Status'] == 'SUCCESS']),
                    len(success_df[success_df['Data_Read_Status'] == 'PARTIAL']),
                    len(success_df[success_df['Data_Read_Status'] == 'EMPTY']),
                    len(success_df[success_df['Data_Read_Status'] == 'ERROR']),
                    len(success_df[success_df['Parent_Email_READ'] != '']),
                    len(success_df[success_df['Child_Email_READ'] != '']),
                    len(success_df[success_df['Privacy_Request_Type_READ'] != '']),
                    len(success_df[success_df['Phone_READ'] != '']),
                    len(success_df[success_df['State_READ'] != '']),
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Field mapping sheet for reference
            field_mapping_data = {
                'Excel_Column_Name': [
                    ' First_Name_of parent_guardian',
                    'Last Name of parent/guardian', 
                    'Primary Email Address',
                    'First Name',
                    'Last Name',
                    'Email of Child (Data Subject)',
                    'Request_type',
                    'phone',
                    'stateOrProvince'
                ],
                'Report_Column_Name': [
                    'Parent_First_Name_READ',
                    'Parent_Last_Name_READ',
                    'Parent_Email_READ',
                    'Child_First_Name_READ', 
                    'Child_Last_Name_READ',
                    'Child_Email_READ',
                    'Privacy_Request_Type_READ',
                    'Phone_READ',
                    'State_READ'
                ],
                'Field_Type': [
                    'Parent Information',
                    'Parent Information',
                    'Parent Contact',
                    'Child Information',
                    'Child Information', 
                    'Child Contact',
                    'Request Type',
                    'Contact Information',
                    'Location Information'
                ]
            }
            field_mapping_df = pd.DataFrame(field_mapping_data)
            field_mapping_df.to_excel(writer, sheet_name='Field_Mapping', index=False)
            
            # Recent fixes documentation
            recent_fixes_data = {
                'Issue_Date': [
                    '2025-08-04',
                    '2025-08-04',
                    '2025-08-04',
                    '2025-08-04'
                ],
                'Issue_Description': [
                    'Updated file path to use Domestic_Parent_form_data.xlsx',
                    'Added organized screenshot directory structure',
                    'Implemented Record 20 starting position',
                    'Added full page screenshot capability'
                ],
                'Fix_Applied': [
                    'Changed excel_file path to dsr/data/Domestic_Parent_form_data.xlsx',
                    'Added SCREENSHOTS_DIR constant for organized output',
                    'Implemented start_record = 19 logic with safety checks',
                    'Added full_page=True parameter to screenshots'
                ],
                'Status': [
                    'FIXED',
                    'FIXED', 
                    'FIXED',
                    'FIXED'
                ]
            }
            recent_fixes_df = pd.DataFrame(recent_fixes_data)
            recent_fixes_df.to_excel(writer, sheet_name='Recent_Fixes', index=False)
        
        # Calculate summary statistics
        total_records = len(success_df)
        successful_records = len(success_df[success_df['Data_Read_Status'] == 'SUCCESS'])
        parent_email_working = len(success_df[success_df['Parent_Email_READ'] != ''])
        child_email_working = len(success_df[success_df['Child_Email_READ'] != ''])
        
        print(f"\n🎉 SUCCESS! Parent Data Reading Success Report created:")
        print(f"📁 File: {report_filename}")
        print(f"📊 Total Records: {total_records}")
        print(f"✅ Successfully Read: {successful_records}")
        print(f"✅ Parent Email Working: {parent_email_working}")
        print(f"✅ Child Email Working: {child_email_working}")
        print(f"📋 Report includes 4 sheets:")
        print(f"   1. Parent_Reading_Report - Detailed data for each record")
        print(f"   2. Summary - Overall statistics")
        print(f"   3. Field_Mapping - Column mapping information with field IDs")
        print(f"   4. Recent_Fixes - Documentation of issues resolved")
        
        return report_filename
        
    except Exception as e:
        print(f"❌ Error creating report: {str(e)}")
        return None

if __name__ == "__main__":
    # Test the report generation
    create_parent_reading_success_report()
