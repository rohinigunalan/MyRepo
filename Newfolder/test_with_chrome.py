#!/usr/bin/env python3
"""
Test using system Chrome browser instead of Playwright's
"""

print("🔍 TESTING WITH SYSTEM CHROME")
print("=" * 40)

try:
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        # Try to use system Chrome instead of Playwright's Chromium
        print("Attempting to launch with system Chrome...")
        
        # Common Chrome paths on Windows
        chrome_paths = [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe")
        ]
        
        import os
        chrome_path = None
        for path in chrome_paths:
            if os.path.exists(path):
                chrome_path = path
                break
        
        if chrome_path:
            print(f"Found Chrome at: {chrome_path}")
            browser = p.chromium.launch(
                executable_path=chrome_path,
                headless=False
            )
            print("✅ Browser launched successfully!")
            
            page = browser.new_page()
            page.goto("https://www.google.com")
            print("✅ Navigated to Google - Browser should be visible!")
            
            # Wait so you can see it
            import time
            time.sleep(3)
            
            browser.close()
            print("✅ Test completed!")
            
        else:
            print("❌ Chrome not found in common locations")
            print("Trying default Playwright chromium...")
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto("https://www.google.com")
            print("✅ Default browser worked!")
            import time
            time.sleep(3)
            browser.close()
            
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("🏁 Test complete!")
