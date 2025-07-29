import pandas as pd
import os

def examine_educator_excel():
    """Examine the existing Educatoronbehalfofstudent_form_data.xlsx file"""
    
    excel_file = "dsr/data/Educatoronbehalfofstudent_form_data.xlsx"
    
    if os.path.exists(excel_file):
        print(f"📊 Found and examining: {excel_file}")
        
        try:
            # Read the Excel file
            df = pd.read_excel(excel_file, engine='openpyxl', na_filter=False, keep_default_na=False, dtype=str)
            
            print(f"✅ Successfully loaded Excel file!")
            print(f"📋 Total records: {len(df)}")
            print(f"📋 Total columns: {len(df.columns)}")
            
            print("\n🔍 COLUMN STRUCTURE:")
            for i, col in enumerate(df.columns):
                print(f"  {i+1}. '{col}'")
            
            print("\n📊 SAMPLE DATA (First few records):")
            for i, (index, row) in enumerate(df.iterrows()):
                if i >= 3:  # Show first 3 records
                    break
                    
                print(f"\n  Record {i+1}:")
                for col in df.columns:
                    value = row[col] if pd.notna(row[col]) and str(row[col]).strip() else "N/A"
                    print(f"    {col}: {value}")
            
            print(f"\n📋 DATA SUMMARY:")
            print(f"  - Found {len(df)} educator records")
            
            # Check key fields
            key_fields = [
                'Who is making this request',
                'Agent First Name', 
                'Agent Last Name',
                'Agent Email Address'
            ]
            
            print(f"\n🔑 KEY FIELD VERIFICATION:")
            for field in key_fields:
                if field in df.columns:
                    sample_values = df[field].unique()[:3]  # First 3 unique values
                    print(f"  ✅ '{field}' found - Sample values: {list(sample_values)}")
                else:
                    print(f"  ❌ '{field}' NOT found")
            
            # Check if there are any other columns that might contain student data
            print(f"\n📝 ALL AVAILABLE COLUMNS:")
            for col in df.columns:
                sample_val = df[col].iloc[0] if len(df) > 0 else "N/A"
                print(f"  • {col}: '{sample_val}'")
            
            return df
            
        except Exception as e:
            print(f"❌ Error reading Excel file: {str(e)}")
            return None
    else:
        print(f"❌ Excel file not found: {excel_file}")
        return None

if __name__ == "__main__":
    examine_educator_excel()
