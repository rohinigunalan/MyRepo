#!/usr/bin/env python3
"""
Quick test for Primary Email Address field in educator forms
"""

import pandas as pd
import time
from playwright.sync_api import sync_playwright

def test_primary_email_field():
    """Test that Primary Email Address field gets filled for child email"""
    
    print("🧪 TESTING PRIMARY EMAIL ADDRESS FIELD...")
    
    # Load Excel data
    try:
        df = pd.read_excel('dsr/data/Educatoronbehalfofstudent_form_data.xlsx')
        first_record = df.iloc[0]
        child_email = str(first_record.get('Email of Child (Data Subject)', 'childstudent@mailinator.com'))
        print(f"📧 Child email from Excel: '{child_email}'")
        
    except Exception as e:
        print(f"❌ Error loading Excel: {str(e)}")
        return
    
    # Test with Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        
        try:
            print("🌐 Navigating to form...")
            page.goto("https://prod.privacy-portal.college-board.org/privacy/dsr", wait_until="networkidle", timeout=30000)
            
            print("🔘 Clicking 'Authorized Agent on behalf of someone else'...")
            page.click("span:has-text('Authorized Agent on behalf of someone else')")
            
            print("⏸️ Waiting for agent fields to load...")
            time.sleep(3)
            
            # Test Primary Email Address field
            print(f"\n📧 Testing Primary Email Address field with: '{child_email}'")
            try:
                # Check the field label first
                primary_email_field = page.locator("input[id='emailDSARElement']")
                if primary_email_field.is_visible():
                    # Get the label
                    try:
                        label = page.locator("label[for='emailDSARElement']").text_content()
                        print(f"📋 Field label: '{label}'")
                    except:
                        print("📋 Field label: Could not retrieve")
                    
                    # Fill the field
                    primary_email_field.fill(child_email)
                    print(f"✅ PRIMARY EMAIL ADDRESS FILLED SUCCESSFULLY: '{child_email}'")
                    
                    # Take screenshot
                    page.screenshot(path="dsr/screenshots/primary_email_test.png")
                    print("📸 Screenshot saved: primary_email_test.png")
                    
                else:
                    print("❌ Primary Email Address field not visible")
            except Exception as e:
                print(f"❌ Error filling Primary Email Address: {str(e)}")
            
            print("\n⏸️ Pausing for 5 seconds to review...")
            time.sleep(5)
            
        except Exception as e:
            print(f"❌ Test error: {str(e)}")
        
        finally:
            browser.close()

if __name__ == "__main__":
    test_primary_email_field()
