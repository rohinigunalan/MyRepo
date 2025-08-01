#!/usr/bin/env python3
"""
Minimal test script to verify phone field fixes work correctly
"""

import pytest
from playwright.sync_api import sync_playwright, Page
import time
import pandas as pd
import os
import re

class PhoneFieldTest:
    """Minimal test to verify phone field behavior"""
    
    def __init__(self):
        self.url = "https://privacyportaluat.onetrust.com/webform/b99e91a7-a15e-402d-913d-a09fe56fcd54/c31c1bfa-b0a7-4a7a-9fc0-22c44fa094d0"
        self.load_excel_data()
    
    def load_excel_data(self):
        """Load the Excel data to check phone validation"""
        try:
            excel_path = 'dsr/data/International_Educatoronbehalfofstudent_form_data.xlsx'
            df = pd.read_excel(excel_path, na_filter=False, keep_default_na=False, dtype=str)
            self.all_records = df.to_dict(orient='records')
            print(f"✅ Loaded {len(self.all_records)} records from Excel")
            
            # Show phone data for first few records
            for i, record in enumerate(self.all_records[:3]):
                phone = str(record.get('Phone Number', '')).strip()
                print(f"   Record {i+1} phone: '{phone}'")
                
        except Exception as e:
            print(f"❌ Error loading Excel: {e}")
            self.all_records = []
    
    def clear_phone_fields(self, page: Page):
        """🔧 Clear any pre-filled phone fields to prevent browser auto-fill issues"""
        print("🧹 Clearing any pre-filled phone fields...")
        
        phone_selectors = [
            "input[type='tel']",
            "input[name*='phone']", 
            "input[id*='phone']",
            "input[placeholder*='phone']",
            "input[placeholder*='Phone']",
            "input[data-testid*='phone']"
        ]
        
        cleared_count = 0
        for selector in phone_selectors:
            try:
                elements = page.locator(selector).all()
                for element in elements:
                    if element.is_visible():
                        current_value = element.input_value() or ""
                        if current_value:
                            print(f"📞 Found pre-filled phone field with value: '{current_value}'")
                        element.clear()
                        cleared_count += 1
                        print(f"✅ Cleared phone field: {selector}")
            except:
                continue
        
        print(f"🧹 Cleared {cleared_count} phone fields")
    
    def validate_phone_data(self, record_index):
        """Validate phone data same way as main script"""
        record = self.all_records[record_index]
        phone_from_excel = str(record.get('Phone Number', '')).strip()
        
        print(f"📞 Phone validation for record {record_index + 1}:")
        print(f"   Raw value: '{phone_from_excel}'")
        
        # Same validation logic as main script
        if not phone_from_excel or phone_from_excel.lower() in ['', 'nan', 'none', 'null', 'n/a', 'na']:
            print(f"   ✅ VALIDATION RESULT: Phone will be SKIPPED (empty/invalid)")
            return False
        else:
            # Additional validation for actual phone numbers
            phone_digits_only = re.sub(r'[^\d]', '', phone_from_excel)
            
            is_valid_phone = (
                len(phone_digits_only) >= 7 and 
                len(phone_digits_only) <= 15 and
                not any(word in phone_from_excel.lower() for word in ['account', 'closure', 'close', 'delete', 'request', 'data', 'subject', 'test'])
            )
            
            if is_valid_phone:
                print(f"   ✅ VALIDATION RESULT: Valid phone will be USED: '{phone_from_excel}'")
                return True
            else:
                print(f"   ⚠️ VALIDATION RESULT: Invalid phone will be SKIPPED: '{phone_from_excel}'")
                return False
    
    def check_phone_fields_on_page(self, page: Page):
        """Check if any phone fields are filled on the page"""
        print("🔍 Checking if any phone fields are filled on the page...")
        
        phone_selectors = [
            "input[type='tel']",
            "input[name*='phone']", 
            "input[id*='phone']",
            "input[placeholder*='phone']",
            "input[placeholder*='Phone']"
        ]
        
        filled_phones = []
        for selector in phone_selectors:
            try:
                elements = page.locator(selector).all()
                for element in elements:
                    if element.is_visible():
                        value = element.input_value() or ""
                        if value.strip():
                            filled_phones.append(f"Selector: {selector}, Value: '{value}'")
                            print(f"📞 FOUND FILLED PHONE FIELD: {selector} = '{value}'")
            except:
                continue
        
        if not filled_phones:
            print("✅ NO phone fields are filled - this is CORRECT based on Excel data")
        else:
            print(f"⚠️ FOUND {len(filled_phones)} filled phone fields:")
            for phone in filled_phones:
                print(f"   {phone}")
            print("🔍 This suggests browser auto-fill or form JavaScript is filling fields")
        
        return filled_phones
    
    def test_phone_behavior(self):
        """Test phone field behavior with our fixes"""
        print("🚀 TESTING PHONE FIELD BEHAVIOR")
        print("="*60)
        
        if not self.all_records:
            print("❌ No Excel data available")
            return
        
        with sync_playwright() as p:
            # Launch browser with anti-autofill settings
            browser = p.chromium.launch(
                headless=False,
                args=[
                    '--disable-blink-features=AutofillShowTypePredictions',
                    '--disable-autofill',
                    '--disable-autofill-keyboard-accessory-view',
                    '--disable-full-form-autofill-ios',
                    '--incognito'
                ]
            )
            context = browser.new_context(
                ignore_https_errors=True,
                extra_http_headers={'Accept-Language': 'en-US,en;q=0.9'}
            )
            page = context.new_page()
            
            try:
                # Test with record 4 (index 3) like the main script
                record_index = 3
                
                print(f"\\n🎯 TESTING RECORD {record_index + 1}")
                
                # Validate phone data
                should_fill_phone = self.validate_phone_data(record_index)
                
                # Navigate to form
                print(f"\\n🌐 Navigating to privacy portal...")
                page.goto(self.url)
                page.wait_for_load_state("networkidle")
                time.sleep(2)
                
                # Clear phone fields immediately
                self.clear_phone_fields(page)
                
                # Check initial state
                print(f"\\n📋 INITIAL STATE CHECK:")
                initial_filled = self.check_phone_fields_on_page(page)
                
                # Take screenshot
                page.screenshot(path="dsr/screenshots/phone_test_initial.png")
                print("📸 Screenshot saved: phone_test_initial.png")
                
                # Select "Authorized Agent on behalf of someone else" to trigger form changes
                print(f"\\n🔘 Selecting agent option...")
                try:
                    agent_button = page.locator("button:has-text('Authorized Agent on behalf of someone else')").first
                    if agent_button.is_visible():
                        agent_button.click()
                        print("✅ Clicked agent button")
                        time.sleep(3)
                        
                        # Clear phone fields again after form changes
                        self.clear_phone_fields(page)
                        
                        # Check state after agent selection
                        print(f"\\n📋 AFTER AGENT SELECTION CHECK:")
                        after_agent_filled = self.check_phone_fields_on_page(page)
                        
                        # Take another screenshot
                        page.screenshot(path="dsr/screenshots/phone_test_after_agent.png")
                        print("📸 Screenshot saved: phone_test_after_agent.png")
                        
                except Exception as e:
                    print(f"⚠️ Could not click agent button: {e}")
                
                # Try to select a delete request type to trigger sub-options
                print(f"\\n🗑️ Trying to select delete request type...")
                try:
                    delete_button = page.locator("label:has-text('delete'), span:has-text('delete'), div:has-text('delete')").first
                    if delete_button.is_visible():
                        delete_button.click()
                        print("✅ Clicked delete option")
                        time.sleep(3)
                        
                        # Clear phone fields again after request type selection
                        self.clear_phone_fields(page)
                        
                        # Check state after delete selection
                        print(f"\\n📋 AFTER DELETE SELECTION CHECK:")
                        after_delete_filled = self.check_phone_fields_on_page(page)
                        
                        # Take final screenshot
                        page.screenshot(path="dsr/screenshots/phone_test_after_delete.png")
                        print("📸 Screenshot saved: phone_test_after_delete.png")
                        
                except Exception as e:
                    print(f"⚠️ Could not select delete option: {e}")
                
                # Final summary
                print(f"\\n🎯 PHONE FIELD TEST SUMMARY:")
                print(f"   Excel phone data valid: {should_fill_phone}")
                print(f"   Initial filled phones: {len(initial_filled)}")
                print(f"   Expected behavior: Phone fields should remain EMPTY")
                if any([initial_filled, after_agent_filled if 'after_agent_filled' in locals() else [], after_delete_filled if 'after_delete_filled' in locals() else []]):
                    print(f"   ⚠️ ISSUE: Phone fields are being filled from somewhere other than our script")
                    print(f"   🔧 This confirms browser auto-fill or form JavaScript is the cause")
                else:
                    print(f"   ✅ SUCCESS: Phone fields remain empty as expected")
                
                # Keep browser open for manual inspection
                print(f"\\n⏸️ Keeping browser open for 15 seconds for manual inspection...")
                time.sleep(15)
                
            finally:
                browser.close()

if __name__ == "__main__":
    test = PhoneFieldTest()
    test.test_phone_behavior()
