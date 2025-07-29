#!/usr/bin/env python3
"""
Quick test script to focus on child email field identification
"""
import pandas as pd
import os
import time
from playwright.sync_api import sync_playwright, Page

def test_child_email_field():
    """Test just the child email field identification"""
    
    # Load Excel data
    excel_file = "dsr/data/Educatoronbehalfofstudent_form_data.xlsx"
    df = pd.read_excel(excel_file, engine='openpyxl', na_filter=False, keep_default_na=False, dtype=str)
    first_record = df.iloc[0].to_dict()
    
    print(f"🔍 Testing child email field for first record:")
    print(f"   Child Email from Excel: '{first_record.get('Email of Child (Data Subject)', 'N/A')}'")
    print(f"   Student Name: {first_record.get('First Name', 'N/A')} {first_record.get('Last Name', 'N/A')}")
    
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
                        time.sleep(3)
                        break
                except:
                    continue
            
            # Now look for all email fields
            print(f"\n📧 Looking for all email fields on the form...")
            try:
                all_email_inputs = page.locator("input[type='email']:visible").all()
                print(f"Found {len(all_email_inputs)} email fields:")
                
                for i, input_field in enumerate(all_email_inputs):
                    try:
                        aria_label = input_field.get_attribute('aria-label') or ''
                        placeholder = input_field.get_attribute('placeholder') or ''
                        field_id = input_field.get_attribute('id') or ''
                        field_name = input_field.get_attribute('name') or ''
                        
                        print(f"  Email field {i+1}:")
                        print(f"    aria-label: '{aria_label}'")
                        print(f"    placeholder: '{placeholder}'")  
                        print(f"    id: '{field_id}'")
                        print(f"    name: '{field_name}'")
                        print()
                        
                        # Try to identify if this is the child email field
                        field_text = f"{aria_label} {placeholder} {field_id} {field_name}".lower()
                        is_child_field = any(keyword in field_text for keyword in ['child', 'student', 'data subject', 'subject'])
                        is_agent_field = any(keyword in field_text for keyword in ['agent', 'educator', 'teacher'])
                        
                        if is_child_field:
                            print(f"    🎯 This appears to be a CHILD email field!")
                            # Try to fill it
                            try:
                                child_email = first_record.get('Email of Child (Data Subject)', 'test@mailinator.com')
                                input_field.fill(child_email)
                                print(f"    ✅ Successfully filled with: {child_email}")
                            except Exception as fill_error:
                                print(f"    ❌ Could not fill: {fill_error}")
                        elif is_agent_field:
                            print(f"    🚫 This appears to be an AGENT email field - skipping")
                        else:
                            print(f"    ❓ Field type unclear")
                        
                    except Exception as field_error:
                        print(f"  Error examining field {i+1}: {field_error}")
                        
            except Exception as e:
                print(f"❌ Error finding email fields: {e}")
            
            # Take a screenshot to see the current state
            page.screenshot(path="dsr/screenshots/child_email_debug.png")
            print(f"\n📸 Screenshot saved: dsr/screenshots/child_email_debug.png")
            
            print(f"\n⏸️ Pausing for 10 seconds to review...")
            time.sleep(10)
            
        finally:
            browser.close()

if __name__ == "__main__":
    test_child_email_field()
