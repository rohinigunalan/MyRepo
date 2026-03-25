#!/usr/bin/env python3
"""
Simple script to run the privacy portal test
Usage: python run_test.py
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inforequest_submission import TestPrivacyPortal, test_inspect_form_elements

def main():
    print("🚀 Starting Privacy Portal Test Automation")
    print("=" * 50)
    
    try:
        # Option 1: Inspect form elements first
        print("1. Inspecting form elements...")
        test_inspect_form_elements()
        
        print("\n" + "=" * 50)
        print("2. Running form automation test...")
        
        # Option 2: Run the actual test
        test = TestPrivacyPortal()
        test.setup_method()
        test.test_privacy_form_submission()
        
        print("✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
