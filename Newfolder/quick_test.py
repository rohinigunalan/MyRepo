#!/usr/bin/env python3
"""
Simple test to verify Playwright and run state selection
"""

import time
import os

print("🚀 Starting simple test...")

try:
    # Test imports
    from playwright.sync_api import sync_playwright
    import pandas as pd
    print("✅ All imports successful!")
    
    # Test Excel data loading
    if os.path.exists("form_data.xlsx"):
        df = pd.read_excel("form_data.xlsx")
        data = df.iloc[0].to_dict()
        state_name = str(data.get('stateOrProvince', 'New York'))
        print(f"✅ Excel data loaded - State: {state_name}")
    else:
        print("⚠️ No Excel file found, using default state: New York")
        state_name = "New York"
    
    # Test browser launch
    with sync_playwright() as p:
        print("🌐 Testing browser launch...")
        browser = p.chromium.launch(headless=False)  # Visible browser
        page = browser.new_page()
        
        print("🔗 Testing navigation...")
        page.goto("https://example.com")
        print(f"✅ Page loaded: {page.title()}")
        
        print("⏳ Keeping browser open for 5 seconds...")
        time.sleep(5)
        
        browser.close()
        print("✅ Browser test completed!")
    
    print("🎉 All tests passed! Your environment is ready.")
    print(f"📝 Ready to test state selection with: '{state_name}'")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("💡 If browser fails, run: playwright install")

print("🏁 Test completed!")
