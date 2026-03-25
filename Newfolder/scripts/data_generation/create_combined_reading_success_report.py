import pandas as pd
import os
from datetime import datetime

# Define the screenshots directory constant for organized output
SCREENSHOTS_DIR = "dsr/screenshots/Combined_Parent"

def create_combined_reading_success_report():
    """Create a report of successfully read data from combined Excel file"""
    
    # Create timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("📊 Creating Combined Data Reading Success Report...")
    print(f"🕒 Timestamp: {timestamp}")
    
    # Check for combined Excel file
    excel_file = "dsr/data/Combined/Combined_Parent_form_data.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"❌ No Combined Excel file found: {excel_file}")
        return None
    
    try:
        print(f"📂 Reading data from: {excel_file}")
        df = pd.read_excel(excel_file, engine='openpyxl', na_filter=False, keep_default_na=False, dtype=str)
        print(f"✅ Successfully loaded {len(df)} records")
        
        # Validate required column
        if 'Request_Category' not in df.columns:
            print("⚠️ Warning: 'Request_Category' column not found - adding default values")
            df['Request_Category'] = 'Unknown'
        
        # Create success report data
        success_data = []
        
        for index, row in df.iterrows():
            record_num = index + 1
            
            # Extract key information
            request_category = row.get('Request_Category', 'Unknown')
            parent_first = row.get('Parent First Name', '')
            parent_last = row.get('Parent Last Name', '')
            parent_email = row.get('Primary Email Address', '')
            
            child_first = row.get('Child First Name', '')
            child_last = row.get('Child Last Name', '')
            
            request_type = row.get('Which of the following types of requests would you like to make?', '')
            birth_date = row.get('Date of Birth', '')
            state = row.get('State', '')
            
            # Determine form type
            form_type = 'International' if 'international' in request_category.lower() else 'Domestic'
            
            # Create readable summary
            summary = f"Category: {request_category} | Parent: {parent_first} {parent_last} | Child: {child_first} {child_last} | Request: {request_type}"
            
            success_record = {
                'Record_Number': record_num,
                'Status': 'SUCCESS',
                'Request_Category': request_category,
                'Form_Type': form_type,
                'Parent_Name': f"{parent_first} {parent_last}",
                'Parent_Email': parent_email,
                'Child_Name': f"{child_first} {child_last}",
                'Birth_Date': birth_date,
                'State': state,
                'Request_Type': request_type,
                'Summary': summary,
                'Timestamp': timestamp,
                'Processing_Notes': f'Successfully processed {form_type.lower()} request'
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
        report_filename = f"{output_dir}/Combined_Data_Reading_Success_Report_{timestamp}.xlsx"
        
        # Create Excel writer with multiple sheets
        with pd.ExcelWriter(report_filename, engine='openpyxl') as writer:
            # Summary sheet
            category_counts = df['Request_Category'].value_counts()
            form_type_counts = success_df['Form_Type'].value_counts()
            
            summary_df = pd.DataFrame({
                'Metric': [
                    'Total Records Processed',
                    'Successful Records',
                    'Success Rate',
                    'International Records',
                    'Domestic Records',
                    'File Source',
                    'Processing Date',
                    'Report Generated'
                ],
                'Value': [
                    len(df),
                    len(success_data),
                    f"{(len(success_data)/len(df)*100):.1f}%",
                    form_type_counts.get('International', 0),
                    form_type_counts.get('Domestic', 0),
                    excel_file,
                    timestamp,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ]
            })
            
            # Write sheets
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            success_df.to_excel(writer, sheet_name='Success_Records', index=False)
            
            # Category breakdown sheet
            category_breakdown = []
            for category, count in category_counts.items():
                category_breakdown.append({
                    'Request_Category': category,
                    'Count': count,
                    'Percentage': f"{(count/len(df)*100):.1f}%"
                })
            
            category_df = pd.DataFrame(category_breakdown)
            category_df.to_excel(writer, sheet_name='Category_Breakdown', index=False)
            
            # Technical details sheet
            tech_df = pd.DataFrame({
                'Field': [
                    'Script Type',
                    'Request Categories',
                    'Data Source',
                    'Output Directory',
                    'Screenshots Directory',
                    'Processing Method',
                    'Record Format',
                    'Supported Types'
                ],
                'Details': [
                    'Combined International & Domestic Parent Automation',
                    ', '.join(category_counts.index.tolist()),
                    excel_file,
                    output_dir,
                    SCREENSHOTS_DIR,
                    'Playwright Browser Automation with Auto-Detection',
                    'Excel XLSX with Request_Category column',
                    'International Parent, Domestic Parent requests'
                ]
            })
            
            tech_df.to_excel(writer, sheet_name='Technical_Details', index=False)
            
            # Original input data
            df.to_excel(writer, sheet_name='Original_Input_Data', index=False)
        
        print(f"\n🎉 SUCCESS! Combined Data Reading Success Report generated:")
        print(f"📄 Report file: {report_filename}")
        print(f"📊 Records processed: {len(df)}")
        print(f"✅ Success records: {len(success_data)}")
        print(f"📈 Success rate: {(len(success_data)/len(df)*100):.1f}%")
        print(f"🌍 International records: {form_type_counts.get('International', 0)}")
        print(f"🇺🇸 Domestic records: {form_type_counts.get('Domestic', 0)}")
        print(f"📂 Report location: {os.path.abspath(report_filename)}")
        
        return report_filename
        
    except Exception as e:
        print(f"❌ Error creating combined success report: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Test the function directly
    report_file = create_combined_reading_success_report()
    if report_file:
        print(f"\n✅ Report generated successfully: {report_file}")
    else:
        print("\n❌ Failed to generate report")
