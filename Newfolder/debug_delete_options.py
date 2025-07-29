#!/usr/bin/env python3
"""
Debug script to check delete options handling
"""
import sys
import time
import pandas as pd
from playwright.sync_api import sync_playwright

# Check data
print("🔍 Checking Excel data...")
df = pd.read_csv('form_data.csv')
data = df.iloc[0].to_dict()

print(f"Request type: {data.get('Request_type')}")
print(f"Delete student: {data.get('delete_student')}")
print(f"Delete parent: {data.get('delete_parent')}")
print(f"Delete educator: {data.get('delete_educator')}")

print("\n🚀 Running abbreviated test to debug delete options...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=1000)
    page = browser.new_page()
    
    try:
        # Go to form
        page.goto("https://privacyportaluat.onetrust.com/webform/b99e91a7-a15e-402d-913d-a09fe56fcd54/c31c1bfa-b0a7-4a7a-9fc0-22c44fa094d0")
        page.wait_for_load_state('networkidle')
        
        # Click Myself
        page.click("button:has-text('Myself')")
        time.sleep(2)
        
        # Fill basic info quickly
        page.fill("input[name='emailAddress']", data['Email Address'])
        page.fill("input[name='firstName']", data['First_Name'])
        page.fill("input[name='lastName']", data['Last_Name'])
        
        # Select request type
        print("🔍 Looking for delete request option...")
        request_selectors = [
            "text=Request to delete my data",
            "text=request to delete my data",
            "button:has-text('Request to delete')",
            "div:has-text('Request to delete')",
            "span:has-text('Request to delete')"
        ]
        
        for selector in request_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.click(selector)
                    print(f"✅ Clicked delete request: {selector}")
                    break
            except:
                continue
        
        # Wait for delete sub-options to appear
        time.sleep(3)
        
        print("\n🔍 Looking for delete sub-options...")
        
        # Try to find all text on the page that contains relevant keywords
        page_text = page.inner_text("body")
        print("📄 Page contains these relevant lines:")
        for line in page_text.split('\n'):
            line = line.strip()
            if any(word in line.lower() for word in ['student', 'parent', 'educator']) and 'data' in line.lower():
                print(f"  → {line}")
        
        # Look for clickable elements with student/parent/educator
        print("\n🔍 Looking for clickable elements...")
        all_elements = page.locator("button, div, span, label, a").all()
        
        found_options = []
        for i, elem in enumerate(all_elements):
            try:
                if elem.is_visible():
                    text = elem.inner_text().strip()
                    if text and any(word in text.lower() for word in ['student', 'parent', 'educator']) and 'data' in text.lower():
                        tag = elem.evaluate("el => el.tagName")
                        classes = elem.get_attribute("class") or ""
                        clickable = elem.evaluate("el => getComputedStyle(el).cursor === 'pointer' || el.onclick !== null || el.getAttribute('role') === 'button'")
                        found_options.append({
                            'text': text,
                            'tag': tag,
                            'classes': classes,
                            'clickable': clickable,
                            'element': elem
                        })
                        print(f"  Option {len(found_options)}: {tag} - '{text}' (clickable: {clickable}) (classes: {classes})")
            except:
                continue
        
        # Try to click the student data option
        print(f"\n🎯 Trying to click student data option (should select: {data.get('delete_student')})")
        if data.get('delete_student', '').lower() == 'yes':
            for option in found_options:
                if 'student' in option['text'].lower():
                    try:
                        option['element'].click()
                        print(f"✅ Clicked: {option['text']}")
                        time.sleep(1)
                        break
                    except Exception as e:
                        print(f"⚠️ Click failed: {str(e)}")
                        try:
                            option['element'].click(force=True)
                            print(f"✅ Force-clicked: {option['text']}")
                            break
                        except:
                            continue
        
        time.sleep(5)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    finally:
        browser.close()

print("🏁 Debug completed!")
