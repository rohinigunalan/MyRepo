#!/usr/bin/env python3
"""
Test ONLY the Excel data loading to see if the issue is in the loading or elsewhere
"""

import pandas as pd
import os
import sys

# Add the scripts directory to path so we can import the class
sys.path.append(r'c:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\Newfolder\dsr\scripts')

# Import the test class
from Domestic_Parent_requesttypes_submission_MULTIPLE import TestPrivacyPortal

def test_excel_loading():
    """Test ONLY the Excel loading functionality"""
    print("🧪 TESTING EXCEL DATA LOADING...")
    
    # Create an instance of the test class
    test_instance = TestPrivacyPortal()
    
    # Call setup_method to load the data
    test_instance.setup_method()
    
    print(f"📊 Total records loaded: {len(test_instance.all_form_data)}")
    
    # Check if we have enough records (should be 24)
    if len(test_instance.all_form_data) >= 20:
        print("✅ Sufficient records found - no fallback needed")
        
        # Show records 20-24
        print("\n" + "="*80)
        print("🎯 RECORDS 20-24 FROM SCRIPT:")
        print("="*80)
        
        start_index = 19  # Record 20 (0-based)
        for i in range(start_index, min(start_index + 5, len(test_instance.all_form_data))):
            record = test_instance.all_form_data[i]
            record_num = i + 1
            print(f"\n📋 RECORD {record_num} (as loaded by script):")
            print(f"   Parent First: '{record.get(' First_Name_of parent_guardian', 'N/A')}'")
            print(f"   Parent Last: '{record.get('Last Name of parent/guardian', 'N/A')}'")
            print(f"   Child First: '{record.get('First Name', 'N/A')}'")
            print(f"   Child Last: '{record.get('Last Name', 'N/A')}'")
            print(f"   Child Email: '{record.get('Email of Child (Data Subject)', 'N/A')}'")
            print(f"   Birth Date: '{record.get(' Date of Birth', 'N/A')}'")
            print(f"   Phone Number: '{record.get('Phone Number', 'N/A')}'")
            
    else:
        print(f"❌ NOT ENOUGH RECORDS: Only {len(test_instance.all_form_data)} found, script needs 20")
        print("🔧 Script will enter FALLBACK MODE and create fake data")

if __name__ == "__main__":
    test_excel_loading()
