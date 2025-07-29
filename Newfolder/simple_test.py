"""
Simple Playwright test to verify installation
"""
try:
    from playwright.sync_api import sync_playwright
    import time
    
    print("🚀 Starting simple Playwright test...")
    
    with sync_playwright() as p:
        print("✅ Playwright imported successfully")
        
        try:
            # Launch browser
            browser = p.chromium.launch(headless=False)
            print("✅ Browser launched successfully")
            
            # Create new page
            page = browser.new_page()
            print("✅ New page created")
            
            # Go to a simple website
            page.goto("https://example.com")
            print("✅ Navigated to example.com")
            
            # Get page title
            title = page.title()
            print(f"✅ Page title: {title}")
            
            # Take screenshot
            page.screenshot(path="screenshots/test_screenshot.png")
            print("✅ Screenshot taken: screenshots/test_screenshot.png")
            
            # Wait a bit to see the browser
            time.sleep(3)
            
            # Close browser
            browser.close()
            print("✅ Browser closed")
            
            print("\n🎉 Simple test completed successfully!")
            print("Playwright is working correctly!")
            
        except Exception as e:
            print(f"❌ Error during browser test: {str(e)}")
            
except ImportError as e:
    print(f"❌ Playwright not installed properly: {str(e)}")
    print("Please run: python -m pip install playwright")
    print("Then run: python -m playwright install")
    
except Exception as e:
    print(f"❌ Unexpected error: {str(e)}")
