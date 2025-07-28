import sys
print("Python is working!")
print(f"Python version: {sys.version}")

try:
    import playwright
    print(f"Playwright version: {playwright.__version__}")
except Exception as e:
    print(f"Playwright error: {e}")

try:
    from playwright.sync_api import sync_playwright
    print("Playwright sync_api imported successfully!")
    
    with sync_playwright() as p:
        print("Playwright context created!")
        browser = p.chromium.launch(headless=False)
        print("Browser launched!")
        browser.close()
        print("Browser closed!")
        
except Exception as e:
    print(f"Browser test failed: {e}")
    print("You may need to run: playwright install")

print("Test completed!")
