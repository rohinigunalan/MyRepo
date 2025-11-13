import pandas as pd
import os
from datetime import datetime

# Define the screenshots directory constant for organized output
SCREENSHOTS_DIR = "dsr/screenshots/Domestic_Educator_onbehalfofstudent"

def create_educator_reading_success_report():
    """Create a report of successfully read data from educator Excel files"""
    
    # Create timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("📊 Creating Educator Data Reading Success Report...")
    print(f"🕒 Timestamp: {timestamp}")
    
    # Check for educator Excel file
    excel_file = "dsr/data/Domestic_Educatoronbehalfofstudent_form_data.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"❌ No Educator Excel file found: {excel_file}")
        return None
    
    try:
        print(f"📂 Reading data from: {excel_file}")
        df = pd.read_excel(excel_file, engine='openpyxl', na_filter=False, keep_default_na=False, dtype=str)
        print(f"✅ Successfully loaded {len(df)} records")
        
        # Create success report data
        success_data = []
        
        for index, row in df.iterrows():
            record_num = index + 1
            
            # Extract key information
            agent_first = row.get('Agent First Name', '')
            agent_last = row.get('Agent Last Name', '')
            agent_email = row.get('Agent Email Address', '')
            agent_company = row.get('Authorized Agent Company Name (insert N/A if not applicable)', '')
            
            student_first = row.get('Student First Name', '')
            student_last = row.get('Student Last Name', '')
            student_email = row.get('Primary Email Address', '')
            
            request_type = row.get('Which of the following types of requests would you like to make?', '')
            birth_date = row.get('Date of Birth', '')
            state = row.get('State', '')
            
            # Create readable summary
            summary = f"Agent: {agent_first} {agent_last} | Student: {student_first} {student_last} | Request: {request_type}"
            
            success_record = {
                'Record_Number': record_num,
                'Status': 'SUCCESS',
                'Agent_Name': f"{agent_first} {agent_last}",
                'Agent_Email': agent_email,
                'Agent_Company': agent_company,
                'Student_Name': f"{student_first} {student_last}",
                'Student_Email': student_email,
                'Birth_Date': birth_date,
                'State': state,
                'Request_Type': request_type,
                'Summary': summary,
                'Timestamp': timestamp,
                'Processing_Notes': 'Successfully processed educator/agent request'
            }
            
            # Add all original columns for complete record
            for col in df.columns:
                if col not in success_record:
                    success_record[f'Original_{col}'] = row.get(col, '')
            
            success_data.append(success_record)
        
        # Create success report DataFrame
        success_df = pd.DataFrame(success_data)
        
        # Create output directory
        output_dir = "dsr/reports"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate report filename
        report_filename = f"{output_dir}/Educator_Data_Reading_Success_Report_{timestamp}.xlsx"
        
        # Create Excel writer with multiple sheets
        with pd.ExcelWriter(report_filename, engine='openpyxl') as writer:
            # Summary sheet
            summary_df = pd.DataFrame({
                'Metric': [
                    'Total Records Processed',
                    'Successful Records',
                    'Success Rate',
                    'File Source',
                    'Processing Date',
                    'Report Generated'
                ],
                'Value': [
                    len(df),
                    len(success_data),
                    f"{(len(success_data)/len(df)*100):.1f}%",
                    excel_file,
                    timestamp,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ]
            })
            
            # Write sheets
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            success_df.to_excel(writer, sheet_name='Success_Records', index=False)
            
            # Technical details sheet
            tech_df = pd.DataFrame({
                'Field': [
                    'Script Type',
                    'Request Category',
                    'Data Source',
                    'Output Directory',
                    'Screenshots Directory',
                    'Processing Method',
                    'Record Format'
                ],
                'Details': [
                    'Domestic Educator/Agent Automation',
                    'Authorized Agent on behalf of Student',
                    excel_file,
                    output_dir,
                    SCREENSHOTS_DIR,
                    'Playwright Browser Automation',
                    'Excel XLSX with agent and student data'
                ]
            })
            
            tech_df.to_excel(writer, sheet_name='Technical_Details', index=False)
            
            # Original input data
            df.to_excel(writer, sheet_name='Original_Input_Data', index=False)
        
        print(f"\n🎉 SUCCESS! Educator Data Reading Success Report generated:")
        print(f"📄 Report file: {report_filename}")
        print(f"📊 Records processed: {len(df)}")
        print(f"✅ Success records: {len(success_data)}")
        print(f"📈 Success rate: {(len(success_data)/len(df)*100):.1f}%")
        print(f"📂 Report location: {os.path.abspath(report_filename)}")
        
        return report_filename
        
    except Exception as e:
        print(f"❌ Error creating educator success report: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Test the function directly
    report_file = create_educator_reading_success_report()
    if report_file:
        print(f"\n✅ Report generated successfully: {report_file}")
    else:
        print("\n❌ Failed to generate report")
