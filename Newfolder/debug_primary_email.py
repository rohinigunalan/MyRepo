#!/usr/bin/env python3
"""
Debug script to specifically test the Primary Email Address field filling.
"""

import pandas as pd
import time
from playwright.sync_api import sync_playwright

def debug_primary_email_field():
    """Debug the Primary Email Address field specifically"""
    
    print("🔍 DEBUGGING PRIMARY EMAIL ADDRESS FIELD...")
    
    # Load Excel data to get the email value
    try:
        df = pd.read_excel('dsr/data/Educatoronbehalfofstudent_form_data.xlsx')
        first_record = df.iloc[0]
        child_email = str(first_record.get('Email of Child (Data Subject)', 'test@mailinator.com'))
        print(f"📧 Child email from Excel: '{child_email}'")
    except Exception as e:
        print(f"❌ Error loading Excel: {str(e)}")
        child_email = 'test@mailinator.com'
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        
        try:
            print("\n🌐 Navigating to form...")
            page.goto("https://privacyportaluat.onetrust.com/webform/b99e91a7-a15e-402d-913d-a09fe56fcd54/c31c1bfa-b0a7-4a7a-9fc0-22c44fa094d0", wait_until="networkidle", timeout=30000)
            
            print("🔘 Clicking 'Authorized Agent on behalf of someone else'...")
            page.click("span:has-text('Authorized Agent on behalf of someone else')")
            
            print("⏸️ Waiting for fields to load...")
            time.sleep(3)
            
            print("\n🔍 ANALYZING PRIMARY EMAIL ADDRESS FIELD...")
            
            # Find the Primary Email Address field specifically
            primary_email_selectors = [
                "input[aria-label='Primary Email Address']",
                "input[id='emailDSARElement']",
                "input[placeholder*='Primary Email']"
            ]
            
            for selector in primary_email_selectors:
                try:
                    element = page.locator(selector)
                    if element.count() > 0 and element.first.is_visible():
                        print(f"\n✅ Found Primary Email field with selector: {selector}")
                        
                        # Get all field attributes
                        attrs = {}
                        attrs['aria-label'] = element.first.get_attribute('aria-label') or ''
                        attrs['placeholder'] = element.first.get_attribute('placeholder') or ''
                        attrs['id'] = element.first.get_attribute('id') or ''
                        attrs['name'] = element.first.get_attribute('name') or ''
                        attrs['type'] = element.first.get_attribute('type') or ''
                        attrs['class'] = element.first.get_attribute('class') or ''
                        
                        print("📋 Field Attributes:")
                        for key, value in attrs.items():
                            if value:
                                print(f"   {key}: '{value}'")
                        
                        # Check for associated label
                        try:
                            field_id = attrs['id']
                            if field_id:
                                label_element = page.locator(f"label[for='{field_id}']")
                                if label_element.count() > 0:
                                    label_text = label_element.first.text_content() or ""
                                    print(f"   Label text: '{label_text}'")
                        except:
                            print("   No associated label found")
                        
                        # Test the logic that determines if this is a child field
                        field_label = attrs['aria-label']
                        field_label_lower = field_label.lower()
                        
                        is_child_field = any(keyword in field_label_lower for keyword in ['child', 'student', 'data subject', 'subject'])
                        is_agent_field = any(keyword in field_label_lower for keyword in ['agent', 'educator', 'teacher'])
                        is_parent_field = any(keyword in field_label_lower for keyword in ['parent', 'guardian']) and 'primary email' not in field_label_lower
                        is_primary_email = 'primary email' in field_label_lower
                        
                        print(f"\n🧪 LOGIC TEST RESULTS:")
                        print(f"   is_child_field: {is_child_field}")
                        print(f"   is_agent_field: {is_agent_field}")
                        print(f"   is_parent_field: {is_parent_field}")
                        print(f"   is_primary_email: {is_primary_email}")
                        
                        # Determine if field should be filled based on current logic
                        should_fill = (is_child_field or is_primary_email or not (is_agent_field or is_parent_field))
                        print(f"   should_fill: {should_fill}")
                        
                        if should_fill:
                            print(f"\n✅ ATTEMPTING TO FILL PRIMARY EMAIL FIELD...")
                            element.first.fill(child_email)
                            print(f"✅ Successfully filled with: '{child_email}'")
                            
                            # Verify the value was set
                            time.sleep(1)
                            current_value = element.first.input_value()
                            print(f"🔍 Current field value: '{current_value}'")
                            
                            if current_value == child_email:
                                print("✅ PRIMARY EMAIL FIELD FILLED SUCCESSFULLY!")
                            else:
                                print("❌ PRIMARY EMAIL FIELD VALUE MISMATCH!")
                        else:
                            print(f"❌ Field would be skipped by current logic")
                        
                        break
                        
                except Exception as e:
                    print(f"❌ Error with selector {selector}: {str(e)}")
                    continue
            
            print("\n📸 Taking screenshot...")
            page.screenshot(path="dsr/screenshots/primary_email_debug.png")
            
            print("\n⏸️ Pausing for 10 seconds to review...")
            time.sleep(10)
            
        except Exception as e:
            print(f"❌ Debug error: {str(e)}")
            try:
                page.screenshot(path="dsr/screenshots/primary_email_debug_error.png")
            except:
                pass
        
        finally:
            browser.close()

if __name__ == "__main__":
    debug_primary_email_field()
