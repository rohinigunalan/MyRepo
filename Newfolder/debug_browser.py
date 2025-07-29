#!/usr/bin/env python3
"""
Diagnostic script to check Playwright browser installation
"""

print("🔍 Checking Playwright installation...")

try:
    from playwright.sync_api import sync_playwright
    print("✅ Playwright imported successfully!")
    
    print("\n🌐 Testing browser launch...")
    
    with sync_playwright() as p:
        print("✅ Playwright context created!")
        
        try:
            print("🚀 Attempting to launch Chromium browser...")
            browser = p.chromium.launch(headless=False)  # Visible browser
            print("✅ Browser launched successfully!")
            
            page = browser.new_page()
            print("✅ New page created!")
            
            print("🔗 Navigating to test page...")
            page.goto("https://example.com")
            print(f"✅ Page loaded: {page.title()}")
            
            print("⏳ Browser will stay open for 10 seconds so you can see it...")
            import time
            time.sleep(10)
            
            browser.close()
            print("✅ Browser closed successfully!")
            
            print("\n🎉 All tests passed! Playwright is working correctly.")
            print("📝 Ready to run privacy portal automation!")
            
        except Exception as browser_error:
            print(f"❌ Browser launch failed: {browser_error}")
            print("\n💡 Possible solutions:")
            print("1. Run: playwright install")
            print("2. Or run: python -m playwright install chromium")
            print("3. Check if you have sufficient permissions")
            print("4. Try running as administrator")
            
except ImportError as e:
    print(f"❌ Playwright import failed: {e}")
    print("💡 Try: pip install playwright")
except Exception as e:
    print(f"❌ Unexpected error: {e}")

print("\n🏁 Diagnostic completed!")
