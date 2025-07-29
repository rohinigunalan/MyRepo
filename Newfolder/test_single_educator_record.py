#!/usr/bin/env python3
"""
Test script to verify educator automation with a single record.
Tests the fixed company name and agent email fields.
"""

import pandas as pd
import time
from playwright.sync_api import sync_playwright

def test_single_educator_record():
    """Test educator automation with just the first record"""
    
    print("🧪 TESTING SINGLE EDUCATOR RECORD...")
    print("📂 Loading educator data...")
    
    # Load Excel data
    try:
        df = pd.read_excel('dsr/data/Educatoronbehalfofstudent_form_data.xlsx')
        print(f"✅ Loaded {len(df)} records from Excel")
        
        # Use just the first record
        first_record = df.iloc[0]
        print(f"\n👤 Testing Record 1:")
        print(f"   Agent: {first_record.get('Agent First Name', 'N/A')} {first_record.get('Agent Last Name', 'N/A')}")
        print(f"   Company: {first_record.get('Authorized Agent Company Name', 'N/A')}")
        print(f"   Agent Email: {first_record.get('Agent Email Address', 'N/A')}")
        print(f"   Child Email: {first_record.get('Email of Child (Data Subject)', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Error loading Excel: {str(e)}")
        return
    
    # Test with Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        
        try:
            print("\n🌐 Navigating to form...")
            page.goto("https://prod.privacy-portal.college-board.org/privacy/dsr", wait_until="networkidle", timeout=30000)
            
            print("🔘 Clicking 'Authorized Agent on behalf of someone else'...")
            page.click("span:has-text('Authorized Agent on behalf of someone else')")
            
            print("⏸️ Waiting for agent fields to load...")
            time.sleep(2)
            
            # Test Company Name Field
            print("\n🏢 Testing Company Name Field...")
            company_name = str(first_record.get('Authorized Agent Company Name', 'N/A'))
            print(f"🏢 Company from Excel: '{company_name}'")
            
            try:
                page.fill("input[id='formField120DSARElement']", company_name)
                print("✅ Company name filled using exact ID selector!")
            except Exception as e:
                print(f"❌ Company field error: {str(e)}")
            
            # Test Agent Email Field
            print("\n📧 Testing Agent Email Field...")
            agent_email = str(first_record.get('Agent Email Address', 'agent@mailinator.com'))
            print(f"📧 Agent email from Excel: '{agent_email}'")
            
            try:
                page.fill("input[id='formField123DSARElement']", agent_email)
                print("✅ Agent email filled using exact ID selector!")
            except Exception as e:
                print(f"❌ Agent email field error: {str(e)}")
            
            # Test Agent Name Fields
            print("\n👨‍🏫 Testing Agent Name Fields...")
            agent_first = str(first_record.get('Agent First Name', 'TestAgent'))
            agent_last = str(first_record.get('Agent Last Name', 'TestLast'))
            
            try:
                page.fill("input[id='formField121DSARElement']", agent_first)
                print(f"✅ Agent first name '{agent_first}' filled!")
            except Exception as e:
                print(f"❌ Agent first name error: {str(e)}")
            
            try:
                page.fill("input[id='formField122DSARElement']", agent_last)
                print(f"✅ Agent last name '{agent_last}' filled!")
            except Exception as e:
                print(f"❌ Agent last name error: {str(e)}")
            
            # Test Primary Email Field (Child Email)
            print("\n👶 Testing Primary Email Field (Child Email)...")
            child_email = str(first_record.get('Email of Child (Data Subject)', 'child@mailinator.com'))
            print(f"👶 Child email from Excel: '{child_email}'")
            
            try:
                page.fill("input[id='emailDSARElement']", child_email)
                print("✅ Primary Email (Child) filled using exact ID selector!")
            except Exception as e:
                print(f"❌ Primary email field error: {str(e)}")
            
            print("\n📸 Taking final screenshot...")
            page.screenshot(path="dsr/screenshots/single_record_test.png")
            
            print("\n⏸️ Pausing for 10 seconds to review form...")
            time.sleep(10)
            
            print("✅ Single record test completed successfully!")
            
        except Exception as e:
            print(f"❌ Test error: {str(e)}")
            try:
                page.screenshot(path="dsr/screenshots/single_record_test_error.png")
            except:
                pass
        
        finally:
            browser.close()

if __name__ == "__main__":
    test_single_educator_record()
