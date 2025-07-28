#!/usr/bin/env python3

# Test if Playwright is working
try:
    from playwright.sync_api import sync_playwright
    print("✅ Playwright imported successfully!")
    
    # Test basic Playwright functionality
    with sync_playwright() as p:
        print("✅ Playwright sync_playwright context works!")
        browser = p.chromium.launch(headless=True)
        print("✅ Chromium browser launched!")
        page = browser.new_page()
        print("✅ New page created!")
        page.goto("https://example.com")
        print(f"✅ Page loaded: {page.title()}")
        browser.close()
        print("✅ Browser closed!")
    
    print("\n🎉 Playwright is fully working and ready to use!")
    
except ImportError as e:
    print(f"❌ Playwright import failed: {e}")
except Exception as e:
    print(f"❌ Playwright test failed: {e}")
    print("💡 You may need to run: playwright install")
