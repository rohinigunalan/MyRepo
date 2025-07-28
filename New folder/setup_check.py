#!/usr/bin/env python3
"""
Setup verification script for Playwright
"""
import sys
import subprocess
import os

def check_playwright_installation():
    """Check if Playwright is properly installed"""
    try:
        import playwright
        print("✅ Playwright package is installed")
        print(f"   Version: {playwright.__version__}")
        return True
    except ImportError:
        print("❌ Playwright package not found")
        return False

def install_browsers():
    """Install Playwright browsers"""
    try:
        print("🔄 Installing Playwright browsers...")
        # Use the virtual environment python
        python_path = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")
        if os.path.exists(python_path):
            result = subprocess.run([python_path, "-m", "playwright", "install"], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print("✅ Playwright browsers installed successfully")
                return True
            else:
                print(f"❌ Browser installation failed: {result.stderr}")
                return False
        else:
            print(f"❌ Python executable not found at: {python_path}")
            return False
    except Exception as e:
        print(f"❌ Error installing browsers: {str(e)}")
        return False

def test_basic_playwright():
    """Test basic Playwright functionality"""
    try:
        from playwright.sync_api import sync_playwright
        print("🔄 Testing basic Playwright functionality...")
        
        with sync_playwright() as p:
            # Try to launch a browser
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://example.com")
            title = page.title()
            print(f"✅ Successfully loaded page: {title}")
            browser.close()
            return True
    except Exception as e:
        print(f"❌ Playwright test failed: {str(e)}")
        return False

def main():
    print("🔍 Playwright Setup Verification")
    print("=" * 50)
    
    # Check installation
    if not check_playwright_installation():
        print("Please install Playwright first: pip install playwright")
        return 1
    
    # Install browsers
    if not install_browsers():
        print("Browser installation failed. Try running manually:")
        print("python -m playwright install")
        return 1
    
    # Test functionality
    if not test_basic_playwright():
        print("Basic test failed. Check your installation.")
        return 1
    
    print("\n🎉 Setup verification completed successfully!")
    print("\nNext steps:")
    print("1. Run: python run_test.py")
    print("2. Or run: python inforequest_submission.py")
    print("3. Or run: pytest inforequest_submission.py -v")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
