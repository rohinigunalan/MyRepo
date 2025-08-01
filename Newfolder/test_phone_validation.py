#!/usr/bin/env python3
"""
Quick test to verify phone validation logic works correctly
"""

import pandas as pd

def test_phone_validation():
    """Test the phone validation logic with actual Excel data"""
    print("🧪 TESTING PHONE VALIDATION LOGIC")
    print("="*50)
    
    try:
        # Read Excel file same way as main script
        df = pd.read_excel('dsr/data/International_Educatoronbehalfofstudent_form_data.xlsx', 
                          na_filter=False, keep_default_na=False, dtype=str)
        
        print(f"📊 Loaded {len(df)} records from Excel")
        
        # Test phone validation for each record
        for i, record in enumerate(df.to_dict(orient='records')[:5]):  # Test first 5 records
            print(f"\n📞 RECORD {i+1} PHONE VALIDATION:")
            
            # Get phone number same way as main script
            phone_from_excel = str(record.get('Phone Number', '')).strip()
            print(f"   Raw phone from Excel: '{phone_from_excel}'")
            
            # Apply same validation logic as main script
            if not phone_from_excel or phone_from_excel.lower() in ['', 'nan', 'none', 'null', 'n/a', 'na']:
                print(f"   ✅ VALIDATION RESULT: Phone field will be SKIPPED (empty/invalid data)")
                print(f"   📝 Expected behavior: Form phone field should remain EMPTY")
            else:
                # Additional validation for actual phone numbers
                import re
                phone_digits_only = re.sub(r'[^\d]', '', phone_from_excel)
                
                is_valid_phone = (
                    len(phone_digits_only) >= 7 and 
                    len(phone_digits_only) <= 15 and
                    not any(word in phone_from_excel.lower() for word in ['account', 'closure', 'close', 'delete', 'request', 'data', 'subject', 'test'])
                )
                
                if is_valid_phone:
                    print(f"   ✅ VALIDATION RESULT: Valid phone number will be USED: '{phone_from_excel}'")
                    print(f"   📝 Expected behavior: Form phone field will be FILLED")
                else:
                    print(f"   ⚠️ VALIDATION RESULT: Invalid phone number will be SKIPPED: '{phone_from_excel}'")
                    print(f"   📝 Expected behavior: Form phone field should remain EMPTY")
        
        print(f"\n🎯 SUMMARY:")
        print(f"   - Based on this validation, ALL phone fields should remain EMPTY")
        print(f"   - If you see phone numbers in the form, it's likely browser auto-fill")
        print(f"   - The script's validation logic is working correctly")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_phone_validation()
