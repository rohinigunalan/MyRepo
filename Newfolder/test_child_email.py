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
            
            # Fill some basic fields to see if more email fields appear
            print(f"\n📝 Filling basic fields to trigger more form sections...")
            
            # Fill agent first name
            try:
                agent_first_selectors = ["input[aria-label*='Agent First Name']", "input[placeholder*='Agent First Name']"]
                for selector in agent_first_selectors:
                    if page.locator(selector).first.is_visible():
                        page.fill(selector, first_record.get('Agent First Name', 'TestAgent'))
                        print(f"✅ Filled agent first name")
                        time.sleep(1)
                        break
            except:
                pass
            
            # Fill agent last name
            try:
                agent_last_selectors = ["input[aria-label*='Agent Last Name']", "input[placeholder*='Agent Last Name']"]
                for selector in agent_last_selectors:
                    if page.locator(selector).first.is_visible():
                        page.fill(selector, first_record.get('Agent Last Name', 'TestAgent'))
                        print(f"✅ Filled agent last name")
                        time.sleep(1)
                        break
            except:
                pass
                
            # Fill student first name
            try:
                student_first_selectors = ["input[id*='first']", "input[placeholder*='First']"]
                for selector in student_first_selectors:
                    if page.locator(selector).first.is_visible():
                        page.fill(selector, first_record.get('First Name', 'TestStudent'))
                        print(f"✅ Filled student first name")
                        time.sleep(1)
                        break
            except:
                pass
                
            # Fill student last name
            try:
                student_last_selectors = ["input[id*='last']", "input[placeholder*='Last']"]
                for selector in student_last_selectors:
                    if page.locator(selector).first.is_visible():
                        page.fill(selector, first_record.get('Last Name', 'TestStudent'))
                        print(f"✅ Filled student last name")
                        time.sleep(1)
                        break
            except:
                pass
            
            # Look for email fields again after filling basic info
            print(f"\n📧 Looking for email fields again after filling basic info...")
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
                            print(f"    ❓ Field type unclear - checking if we should fill as primary email")
                            # If this is the "Primary Email Address" field, it might be for the agent
                            if 'primary' in field_text and not is_child_field:
                                try:
                                    agent_email = first_record.get('Agent Email Address', 'agent@mailinator.com')
                                    input_field.fill(agent_email)
                                    print(f"    ✅ Filled as agent email: {agent_email}")
                                except Exception as fill_error:
                                    print(f"    ❌ Could not fill: {fill_error}")
                        
                    except Exception as field_error:
                        print(f"  Error examining field {i+1}: {field_error}")
                        
            except Exception as e:
                print(f"❌ Error finding email fields: {e}")
            
            # Scroll down to see if there are more fields
            print(f"\n📜 Scrolling down to look for additional fields...")
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            
            # Look for email fields again after scrolling
            try:
                all_email_inputs = page.locator("input[type='email']").all()
                print(f"After scrolling, found {len(all_email_inputs)} total email fields (visible and hidden):")
                
                for i, input_field in enumerate(all_email_inputs):
                    try:
                        is_visible = input_field.is_visible()
                        aria_label = input_field.get_attribute('aria-label') or ''
                        placeholder = input_field.get_attribute('placeholder') or ''
                        field_id = input_field.get_attribute('id') or ''
                        
                        print(f"  Email field {i+1} (visible: {is_visible}): aria-label='{aria_label}', id='{field_id}'")
                        
                    except Exception as field_error:
                        print(f"  Error examining field {i+1}: {field_error}")
                        
            except Exception as e:
                print(f"❌ Error finding all email fields: {e}")
            
            # Take a screenshot to see the current state
            page.screenshot(path="dsr/screenshots/child_email_debug.png")
            print(f"\n📸 Screenshot saved: dsr/screenshots/child_email_debug.png")
            
            print(f"\n⏸️ Pausing for 10 seconds to review...")
            time.sleep(10)
            
        finally:
            browser.close()

if __name__ == "__main__":
    test_child_email_field()
