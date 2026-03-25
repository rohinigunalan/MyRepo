#!/usr/bin/env python3
"""
Install Playwright browsers
"""

import subprocess
import sys

print("🔧 Installing Playwright browsers...")
print("=" * 40)

try:
    # Install browsers
    print("Installing Playwright browsers...")
    result = subprocess.run([sys.executable, "-m", "playwright", "install"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Browsers installed successfully!")
        print(result.stdout)
    else:
        print("⚠️  Installation had issues:")
        print(result.stderr)
        
    # Try to install just Chromium
    print("\nInstalling Chromium specifically...")
    result2 = subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], 
                           capture_output=True, text=True)
    
    if result2.returncode == 0:
        print("✅ Chromium installed successfully!")
    else:
        print("⚠️  Chromium installation issues:")
        print(result2.stderr)
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n🧪 Testing browser after installation...")
try:
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        print("✅ Browser test successful! You should see a browser window.")
        
        page = browser.new_page()
        page.goto("https://www.google.com")
        print("✅ Navigation successful!")
        
        # Wait 3 seconds so you can see it
        page.wait_for_timeout(3000)
        
        browser.close()
        print("✅ Browser closed")
        
except Exception as e:
    print(f"❌ Browser test failed: {e}")

print("\n🏁 Installation and test complete!")
