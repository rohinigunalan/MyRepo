#!/usr/bin/env python3
"""
Run the dynamic request types automation test
Uses Request_type from Excel to dynamically select the appropriate form option
"""

import pandas as pd
import os
import sys

def main():
    """Main function to run the dynamic request types test"""
    
    print("🚀 Dynamic Request Types Automation Test")
    print("=" * 50)
    
    # Environment verification
    print("🔍 Environment Check:")
    print(f"📍 Python executable: {sys.executable}")
    if ".venv" in sys.executable:
        print("✅ Using virtual environment (.venv)")
    else:
        print("⚠️  WARNING: Not using virtual environment!")
        print("💡 This may cause 'No module named playwright' errors")
    
    # Read Excel data to show what request type will be used
    try:
        print("\n📊 Reading Excel data...")
        df = pd.read_excel("form_data.xlsx", engine='openpyxl')
        data = df.iloc[0].to_dict()
        
        request_type = str(data.get('Request_type', 'NOT FOUND')).strip()
        print(f"🎯 Request Type from Excel: '{request_type}'")
        
        # Show other key data
        print(f"📧 Email: {data.get('Email Address', 'NOT FOUND')}")
        print(f"👤 Name: {data.get('First_Name', '')} {data.get('Last_Name', '')}")
        print(f"🏛️ State: {data.get('stateOrProvince', 'NOT FOUND')}")
        
        print("\n" + "=" * 50)
        print("🚀 Starting dynamic request type automation...")
        print("=" * 50)
        
        # Import and run the test
        from myself_requesttypes_submission import TestPrivacyPortal
        
        test = TestPrivacyPortal()
        test.setup_method()
        test.test_privacy_form_submission()
        
        print("\n✅ Dynamic request type test completed!")
        print("📸 Check screenshots/ folder for results")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    print(f"\n🏁 Script completed with exit code: {exit_code}")
