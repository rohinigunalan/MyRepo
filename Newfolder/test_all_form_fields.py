#!/usr/bin/env python3
"""
Quick test script to examine all form fields after clicking agent button
"""
import pandas as pd
import os
import time
from playwright.sync_api import sync_playwright, Page

def test_all_form_fields():
    """Test to see all form fields after agent selection"""
    
    # Load Excel data
    excel_file = "dsr/data/Educatoronbehalfofstudent_form_data.xlsx"
    df = pd.read_excel(excel_file, engine='openpyxl', na_filter=False, keep_default_na=False, dtype=str)
    first_record = df.iloc[0].to_dict()
    
    print(f"🔍 Testing all form fields for first record:")
    print(f"   Agent Email from Excel: '{first_record.get('Agent Email Address', 'N/A')}'")
    print(f"   Child Email from Excel: '{first_record.get('Email of Child (Data Subject)', 'N/A')}'")
    print(f"   Company Name from Excel: '{first_record.get('Authorized Agent Company Name', 'N/A')}'")
    
    url = "https://privacyportaluat.onetrust.com/webform/b99e91a7-a15e-402d-913d-a09fe56fcd54/c31c1bfa-b0a7-4a7a-9fc0-22c44fa094d0"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # Navigate to form
            print(f"\n🌐 Navigating to form...")
            page.goto(url)
            page.wait_for_load_state("networkidle")
            time.sleep(3)
            
            # First click the agent button
            print(f"\n🔘 Clicking 'Authorized Agent on behalf of someone else' button...")
            agent_selectors = [
                "span:has-text('Authorized Agent on behalf of someone else')",
                "button:has-text('Authorized Agent on behalf of someone else')",
                "label:has-text('Authorized Agent on behalf of someone else')"
            ]
            
            for selector in agent_selectors:
                try:
                    if page.locator(selector).first.is_visible():
                        page.click(selector)
                        print(f"✅ Clicked agent button with: {selector}")
                        time.sleep(5)  # Wait longer for form to fully update
                        break
                except:
                    continue
            
            # Now examine ALL form fields
            print(f"\n📋 Examining ALL form fields after agent selection...")
            
            # 1. Email fields
            print(f"\n📧 EMAIL FIELDS:")
            try:
                all_email_inputs = page.locator("input[type='email']:visible").all()
                print(f"Found {len(all_email_inputs)} email fields:")
                
                for i, input_field in enumerate(all_email_inputs):
                    try:
                        aria_label = input_field.get_attribute('aria-label') or ''
                        placeholder = input_field.get_attribute('placeholder') or ''
                        field_id = input_field.get_attribute('id') or ''
                        field_name = input_field.get_attribute('name') or ''
                        
                        print(f"  📧 Email field {i+1}:")
                        print(f"     aria-label: '{aria_label}'")
                        print(f"     placeholder: '{placeholder}'")  
                        print(f"     id: '{field_id}'")
                        print(f"     name: '{field_name}'")
                        
                        # Identify field type
                        field_text = f"{aria_label} {placeholder} {field_id} {field_name}".lower()
                        if 'agent' in field_text:
                            print(f"     🎯 AGENT EMAIL FIELD!")
                        elif any(keyword in field_text for keyword in ['child', 'student', 'data subject', 'subject']):
                            print(f"     🎯 CHILD EMAIL FIELD!")
                        else:
                            print(f"     ❓ Unknown email field type")
                        print()
                        
                    except Exception as field_error:
                        print(f"  Error examining email field {i+1}: {field_error}")
                        
            except Exception as e:
                print(f"❌ Error finding email fields: {e}")
            
            # 2. Text input fields (for company name, names, etc.)
            print(f"\n📝 TEXT INPUT FIELDS:")
            try:
                all_text_inputs = page.locator("input[type='text']:visible").all()
                print(f"Found {len(all_text_inputs)} text input fields:")
                
                for i, input_field in enumerate(all_text_inputs):
                    try:
                        aria_label = input_field.get_attribute('aria-label') or ''
                        placeholder = input_field.get_attribute('placeholder') or ''
                        field_id = input_field.get_attribute('id') or ''
                        field_name = input_field.get_attribute('name') or ''
                        
                        print(f"  📝 Text field {i+1}:")
                        print(f"     aria-label: '{aria_label}'")
                        print(f"     placeholder: '{placeholder}'")  
                        print(f"     id: '{field_id}'")
                        print(f"     name: '{field_name}'")
                        
                        # Identify field type
                        field_text = f"{aria_label} {placeholder} {field_id} {field_name}".lower()
                        if any(keyword in field_text for keyword in ['company', 'organization']):
                            print(f"     🎯 COMPANY FIELD!")
                        elif 'agent' in field_text and ('first' in field_text or 'last' in field_text):
                            print(f"     🎯 AGENT NAME FIELD!")
                        elif any(keyword in field_text for keyword in ['first', 'last']) and 'agent' not in field_text:
                            print(f"     🎯 STUDENT NAME FIELD!")
                        elif 'n/a' in field_text or 'applicable' in field_text:
                            print(f"     🎯 POTENTIAL COMPANY FIELD (with N/A instruction)!")
                        else:
                            print(f"     ❓ Other text field")
                        print()
                        
                    except Exception as field_error:
                        print(f"  Error examining text field {i+1}: {field_error}")
                        
            except Exception as e:
                print(f"❌ Error finding text fields: {e}")
            
            # Take a screenshot to see the current state
            page.screenshot(path="dsr/screenshots/all_fields_debug.png")
            print(f"\n📸 Screenshot saved: dsr/screenshots/all_fields_debug.png")
            
            print(f"\n⏸️ Pausing for 15 seconds to review...")
            time.sleep(15)
            
        finally:
            browser.close()

if __name__ == "__main__":
    test_all_form_fields()
