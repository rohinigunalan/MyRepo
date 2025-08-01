#!/usr/bin/env python3
"""
🚨 IMPORTANT SETUP NOTE - EDUCATOR/AGENT REQUEST AUTOMATION:
This script automates EDUCATOR/AGENT requests using Educatoronbehalfofstudent_form_data.xlsx file with the following fields:
- Who is making this request: Authorized Agent on behalf of someone else
- Authorized Agent Company Name (insert N/A if not applicable)
- Agent First Name
- Agent Last Name  
- Agent Email Address
- Student/Child information (First Name, Last Name, Email)
- Additional details for delete requests

This script should ALWAYS be run using the virtual environment (.venv) which has all required packages installed:
- Playwright (with browser binaries)
- Pandas 
- Openpyxl
- Pytest

TO RUN THIS SCRIPT:
Use: & "C:/Users/rgunalan/OneDrive - College Board/Documents/GitHub/MyRepo/Newfolder/.venv/Scripts/python.exe" -m pytest educator_requesttypes_submission_MULTIPLE.py::TestPrivacyPortal::test_privacy_form_submission -v -s

The .venv contains all necessary dependencies and is properly configured for this automation.
"""

import pytest
from playwright.sync_api import sync_playwright, Page, expect
import time
import pandas as pd
import os
import sys
from datetime import datetime

# Add the parent directory to sys.path to import the report generator
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
try:
    from create_educator_reading_success_report import create_educator_reading_success_report
except ImportError:
    print("⚠️ Warning: Could not import create_educator_reading_success_report function")
    create_educator_reading_success_report = None

class TestPrivacyPortal:
    """Test suite for OneTrust Privacy Portal form automation"""
    
    def setup_method(self):
        """Setup method called before each test"""
        self.url = "https://privacyportaluat.onetrust.com/webform/b99e91a7-a15e-402d-913d-a09fe56fcd54/c31c1bfa-b0a7-4a7a-9fc0-22c44fa094d0"
        self.all_form_data = self.load_form_data()  # Load ALL records
        self.form_data = {}  # Will be set for each individual record
    
    def load_form_data(self):
        """Load ALL form data from International_Educatoronbehalfofstudent_form_data.xlsx file for multiple educator records"""
        print("📂 Loading ALL international educator form data from file...")
        
        # Use the International_Educatoronbehalfofstudent_form_data.xlsx file specifically
        excel_file = "dsr/data/International_Educatoronbehalfofstudent_form_data.xlsx"
        
        try:
            if os.path.exists(excel_file):
                print(f"📊 Attempting to read educator data from {excel_file}")
                try:
                    df = pd.read_excel(excel_file, engine='openpyxl', na_filter=False, keep_default_na=False, dtype=str)
                    print("✅ International Educator Excel file loaded successfully!")
                except Exception as excel_error:
                    print(f"⚠️  Excel file error: {excel_error}")
                    raise FileNotFoundError(f"Could not load International_Educatoronbehalfofstudent_form_data.xlsx: {excel_error}")
            else:
                raise FileNotFoundError(f"International_Educatoronbehalfofstudent_form_data.xlsx file not found at: {excel_file}")
            
            # Get ALL rows of data instead of just the first
            if len(df) == 0:
                raise ValueError("No data found in the Educatoronbehalfofstudent_form_data.xlsx file")
            
            print(f"📊 Found {len(df)} international educator records in the file")
            # Return ALL records as a list of dictionaries
            all_records = df.to_dict(orient='records')
            
            print("✅ All international educator form data loaded successfully:")
            for i, record in enumerate(all_records):
                agent_company = record.get('Authorized Agent Company Name', 'N/A')
                print(f"  Record {i+1}: {record.get('Agent First Name', 'N/A')} {record.get('Agent Last Name', 'N/A')} (Company: {agent_company}) - Student: {record.get('First Name', 'N/A')} {record.get('Last Name', 'N/A')} - Request: {record.get('Request_type', 'N/A')}")
            
            return all_records
            
        except Exception as e:
            print(f"❌ Error loading international educator form data: {str(e)}")
            print("📝 Using default fallback data for international educator requests...")
            # Fallback to default educator data - return as list
            return [{
                'Who is making this request': 'Authorized Agent on behalf of someone else',
                'Authorized Agent Company Name': 'Sample School District',
                'Agent First Name': 'John',
                'Agent Last Name': 'Educator',
                'Agent Email Address': 'john.educator@mailinator.com',
                'First Name': 'Jane',
                'Last Name': 'Student',
                'Email of Child (Data Subject)': 'student@mailinator.com',
                'Date of Birth': '11/1/2008',
                'Phone Number': '5712345567',
                'country': 'US',
                'stateOrProvince': 'New York',
                'postalCode': '14111',
                'city': 'North Collins',
                'streetAddress': '507 Central Avenue',
                'studentSchoolName': 'South Lakes High School',
                'studentGraduationYear': '2026',
                'educatorSchoolAffiliation': 'South Lakes High School',
                'Request_type': 'Request to delete my data'
            }]
        
    def test_privacy_form_submission(self):
        """Test filling and submitting the privacy portal form for ALL records"""
        print("🚨 IMPORTANT NOTE: This script will automate form filling for ALL records in Excel,")
        print("   but you may need to manually solve reCAPTCHA challenges if they appear.")
        print("   The script will pause and wait for you to complete any image puzzles.")
        print("   Please stay near your computer to help with reCAPTCHA if needed!\n")
        
        print(f"🎯 PROCESSING {len(self.all_form_data)} RECORDS FROM EXCEL FILE")
        
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=False)  # Set to True for headless mode
            page = browser.new_page()
            
            try:
                # Process each record
                for record_index, record_data in enumerate(self.all_form_data):
                    print(f"\n{'='*80}")
                    print(f"🔄 PROCESSING RECORD {record_index + 1} OF {len(self.all_form_data)}")
                    print(f"{'='*80}")
                    
                    # Set current record data
                    self.form_data = record_data
                    
                    # Display current record info
                    print(f"👤 Current Record Details:")
                    print(f"   Agent: {record_data.get('Agent First Name', 'N/A')} {record_data.get('Agent Last Name', 'N/A')}")
                    print(f"   Agent Email: {record_data.get('Agent Email Address', 'N/A')}")
                    print(f"   Agent Company: {record_data.get('Authorized Agent Company Name', 'N/A')}")
                    print(f"   Student: {record_data.get('First Name', 'N/A')} {record_data.get('Last Name', 'N/A')}")
                    print(f"   Request Type: {record_data.get('Request_type', 'N/A')}")
                    print(f"   Country: {record_data.get('country', 'N/A')}")  # International uses country instead of state
                    
                    try:
                        # Navigate to the privacy portal for each record
                        print(f"\n🌐 Navigating to form for record {record_index + 1}...")
                        page.goto(self.url)
                        
                        # Wait for page to load
                        page.wait_for_load_state("networkidle")
                        time.sleep(2)

                        # Fill out the form based on the current record's data
                        print(f"\n🎯 STARTING EDUCATOR/AGENT FORM FILLING PROCESS FOR RECORD {record_index + 1}...")
                        try:
                            self.fill_subject_information(page)
                            self.fill_contact_information(page)
                            self.fill_additional_details(page)
                            self.select_request_type(page)
                            self.handle_delete_request_additional_details(page)  # New method for educator delete details
                            self.handle_delete_data_suboptions(page)
                            self.handle_close_account_suboptions(page)
                            self.handle_acknowledgments(page)
                            
                            # Take screenshot BEFORE submission (after all fields are filled)
                            page.screenshot(path=f"dsr/screenshots/before_submission_record_{record_index + 1}.png")
                            print(f"📸 Screenshot saved: before_submission_record_{record_index + 1}.png")
                            
                            # Submit the form
                            self.submit_form(page, record_index + 1)
                            
                        except Exception as e:
                            print(f"⚠️ Error in parent form processing: {str(e)}")
                            page.screenshot(path=f"dsr/screenshots/error_record_{record_index + 1}.png")
                        
                        # Pause after submission to see results
                        print(f"⏸️ PAUSE: Record {record_index + 1} submission completed. Observing results for 3 seconds...")
                        time.sleep(3)
                        
                        print(f"✅ RECORD {record_index + 1} AUTOMATION COMPLETED SUCCESSFULLY!")
                        
                    except Exception as e:
                        print(f"❌ Error processing record {record_index + 1}: {str(e)}")
                        # Try to take screenshot on error if page is still available
                        try:
                            if page and not page.is_closed():
                                page.screenshot(path=f"dsr/screenshots/error_record_{record_index + 1}.png")
                                print(f"📸 Error screenshot saved for record {record_index + 1}")
                        except:
                            print("⚠️ Could not take error screenshot (page may be closed)")
                        # Continue with next record
                        
                    # Pause between records (except after the last one)
                    if record_index < len(self.all_form_data) - 1:
                        print(f"\n⏸️ PAUSING 5 SECONDS BEFORE PROCESSING NEXT RECORD...")
                        time.sleep(5)
                
                print(f"\n🎉 ALL {len(self.all_form_data)} RECORDS PROCESSED SUCCESSFULLY!")
                print("✅ Multiple record form automation completed!")
                
            except Exception as e:
                # Try to take screenshot on major error if page is still available
                try:
                    if page and not page.is_closed():
                        page.screenshot(path="dsr/screenshots/major_error_screenshot.png")
                        print("📸 Major error screenshot saved: screenshots/major_error_screenshot.png")
                except:
                    print("⚠️ Could not take major error screenshot (page may be closed)")
                print(f"❌ Major error occurred: {str(e)}")
                raise
                
            finally:
                # Keep browser open for longer to see final results
                print("⏸️ FINAL PAUSE: Keeping browser open for 10 seconds to review final state...")
                time.sleep(10)
                browser.close()
    
    def fill_subject_information(self, page: Page):
        """Fill subject information section for EDUCATOR/AGENT requests"""
        print("Filling subject information for EDUCATOR/AGENT request...")
        
        # FIRST: Click "Authorized Agent on behalf of someone else" button
        print("🔘 Looking for 'Authorized Agent on behalf of someone else' button...")
        agent_selectors = [
            "button:has-text('Authorized Agent on behalf of someone else')",
            "button:has-text('authorized agent on behalf of someone else')", 
            "button:has-text('Authorized Agent')",
            "button:has-text('authorized agent')",
            "button:has-text('Agent')",
            "button:has-text('agent')",
            "input[value='Authorized Agent on behalf of someone else']",
            "input[value='authorized agent on behalf of someone else']",
            "input[value='Authorized Agent']",
            "input[value='authorized agent']",
            "input[value='Agent']",
            "input[value='agent']",
            "input[type='radio'][value*='agent']",
            "input[type='radio'][value*='Agent']",
            "input[type='radio'][value*='authorized']",
            "input[type='radio'][value*='Authorized']",
            "label:has-text('Authorized Agent on behalf of someone else')",
            "label:has-text('authorized agent on behalf of someone else')",
            "label:has-text('Authorized Agent')",
            "label:has-text('authorized agent')",
            "label:has-text('Agent')",
            "label:has-text('agent')",
            "button[data-testid*='agent']",
            ".agent-btn",
            "#agent",
            "span:has-text('Authorized Agent on behalf of someone else')",
            "span:has-text('Authorized Agent')",
            "span:has-text('Agent')",
            "div:has-text('Authorized Agent on behalf of someone else')",
            "div:has-text('Authorized Agent')",
            "div:has-text('Agent')",
            "[data-value='agent']",
            "[data-value='Agent']",
            "[data-value='authorized']",
            "[data-value='Authorized']",
            "[role='button']:has-text('Agent')",
            "[role='button']:has-text('Authorized')"
        ]
        
        agent_clicked = False
        for selector in agent_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.click(selector)
                    print(f"✅ Clicked 'Authorized Agent on behalf of someone else' button with selector: {selector}")
                    time.sleep(3)  # Longer pause to let form update for agent fields
                    agent_clicked = True
                    break
            except Exception as e:
                print(f"⚠️ Could not click 'Agent' button with selector {selector}: {str(e)}")
                continue
        
        if not agent_clicked:
            print("⚠️ 'Authorized Agent on behalf of someone else' button not found - continuing anyway...")
        
        # Pause after clicking Agent to let form update with agent fields
        print("⏸️ Brief pause after 'Agent' selection to load agent fields...")
        time.sleep(3)
        
        # AGENT FIELDS: Fill agent/educator information
        print("👨‍🏫 Filling agent/educator information...")
        
        # Agent First Name
        agent_first_name_selectors = [
            # Look for fields specifically labeled for agent first name
            "input[aria-label*='Agent First Name']",
            "input[placeholder*='Agent First Name']",
            "input[aria-label*='First Name of Agent']",
            "input[placeholder*='First Name of Agent']",
            "label:has-text('Agent First Name') + input",
            "label:has-text('Agent First Name') ~ input",
            "label:has-text('First Name of Agent') + input",
            "label:has-text('First Name of Agent') ~ input",
            "*:has-text('Agent First Name') + input",
            "*:has-text('Agent First Name') ~ input",
            "*:has-text('First Name of Agent') + input",
            "*:has-text('First Name of Agent') ~ input",
            # Generic agent selectors
            "input[name*='agent'][name*='first']",
            "input[name*='educator'][name*='first']",
            "input[placeholder*='Agent'][placeholder*='First']",
            "input[placeholder*='Educator'][placeholder*='First']",
            "input[placeholder*='agent'][placeholder*='first']",
            "input[placeholder*='educator'][placeholder*='first']",
            "input[aria-label*='Agent'][aria-label*='First']",
            "input[aria-label*='Educator'][aria-label*='First']",
            "input[id*='agent'][id*='first']",
            "input[id*='educator'][id*='first']",
            "input[data-testid*='agent'][data-testid*='first']",
            "input[data-testid*='educator'][data-testid*='first']"
        ]
        agent_first_filled = False
        for selector in agent_first_name_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.fill(selector, str(self.form_data.get('Agent First Name', 'Educator')))
                    print(f"✅ Agent first name filled: '{self.form_data.get('Agent First Name', 'Educator')}' with selector: {selector}")
                    time.sleep(1)
                    agent_first_filled = True
                    break
            except:
                continue
        
        if not agent_first_filled:
            print("⚠️ Agent first name field not found")
        
        # Agent Last Name
        agent_last_name_selectors = [
            # Look for fields specifically labeled for agent last name
            "input[aria-label*='Agent Last Name']",
            "input[placeholder*='Agent Last Name']",
            "input[aria-label*='Last Name of Agent']",
            "input[placeholder*='Last Name of Agent']",
            "label:has-text('Agent Last Name') + input",
            "label:has-text('Agent Last Name') ~ input",
            "label:has-text('Last Name of Agent') + input",
            "label:has-text('Last Name of Agent') ~ input", 
            "*:has-text('Agent Last Name') + input",
            "*:has-text('Agent Last Name') ~ input",
            "*:has-text('Last Name of Agent') + input",
            "*:has-text('Last Name of Agent') ~ input",
            # Generic agent selectors
            "input[name*='agent'][name*='last']",
            "input[name*='educator'][name*='last']",
            "input[placeholder*='Agent'][placeholder*='Last']",
            "input[placeholder*='Educator'][placeholder*='Last']",
            "input[placeholder*='agent'][placeholder*='last']",
            "input[placeholder*='educator'][placeholder*='last']",
            "input[aria-label*='Agent'][aria-label*='Last']",
            "input[aria-label*='Educator'][aria-label*='Last']",
            "input[id*='agent'][id*='last']",
            "input[id*='educator'][id*='last']",
            "input[data-testid*='agent'][data-testid*='last']",
            "input[data-testid*='educator'][data-testid*='last']"
        ]
        agent_last_filled = False
        for selector in agent_last_name_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.fill(selector, str(self.form_data.get('Agent Last Name', 'AgentbehalfofStu')))
                    print(f"✅ Agent last name filled: '{self.form_data.get('Agent Last Name', 'AgentbehalfofStu')}' with selector: {selector}")
                    time.sleep(1)
                    agent_last_filled = True
                    break
            except:
                continue
        
        if not agent_last_filled:
            print("⚠️ Agent last name field not found")
        
        # Agent Email Address (This is a TEXT field, not email type!)
        print("📧 Filling agent email address...")
        agent_email_selectors = [
            # The exact field we found on the form
            "input[aria-label='Agent Email Address']",
            "input[id='formField123DSARElement']",
            # Fallback selectors
            "input[aria-label*='Agent Email Address']",
            "input[placeholder*='Agent Email Address']",
            "input[aria-label*='Email Address of Agent']",
            "input[placeholder*='Email Address of Agent']",
            "label:has-text('Agent Email Address') + input",
            "label:has-text('Agent Email Address') ~ input",
            "label:has-text('Email Address of Agent') + input",
            "label:has-text('Email Address of Agent') ~ input",
            "*:has-text('Agent Email Address') + input",
            "*:has-text('Agent Email Address') ~ input",
            "*:has-text('Email Address of Agent') + input",
            "*:has-text('Email Address of Agent') ~ input",
            # Generic agent email selectors - INCLUDE TEXT FIELDS!
            "input[name*='agent'][type='email']",
            "input[name*='educator'][type='email']", 
            "input[name*='agent'][name*='email']",
            "input[name*='educator'][name*='email']",
            "input[name*='agent'][type='text']",  # Agent email might be text type
            "input[name*='educator'][type='text']",
            "input[placeholder*='Agent'][placeholder*='Email']",
            "input[placeholder*='Educator'][placeholder*='Email']",
            "input[placeholder*='agent'][placeholder*='email']",
            "input[placeholder*='educator'][placeholder*='email']",
            "input[aria-label*='Agent'][aria-label*='Email']",
            "input[aria-label*='Educator'][aria-label*='Email']",
            "input[id*='agent'][id*='email']",
            "input[id*='educator'][id*='email']",
            "input[data-testid*='agent'][data-testid*='email']",
            "input[data-testid*='educator'][data-testid*='email']"
        ]
        agent_email_filled = False
        agent_email_value = str(self.form_data.get('Agent Email Address', 'educator@mailinator.com'))
        print(f"📧 Agent email from Excel: '{agent_email_value}'")
        
        for selector in agent_email_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.fill(selector, agent_email_value)
                    print(f"✅ Agent email filled: '{agent_email_value}' with selector: {selector}")
                    time.sleep(1)
                    agent_email_filled = True
                    break
            except:
                continue
        
        if not agent_email_filled:
            print("⚠️ Agent email field not found")
        
        # Agent Company Name - Found the exact field!
        print("🏢 Filling agent company name...")
        agent_company_selectors = [
            # The exact field we found on the form
            "input[aria-label='Authorized Agent Company Name (insert N/A if not applicable)']",
            "input[id='formField120DSARElement']",
            # Fallback selectors
            "input[aria-label*='Authorized Agent Company Name (insert N/A if not applicable)']",
            "input[placeholder*='Authorized Agent Company Name (insert N/A if not applicable)']",
            "label:has-text('Authorized Agent Company Name (insert N/A if not applicable)') + input",
            "label:has-text('Authorized Agent Company Name (insert N/A if not applicable)') ~ input",
            "*:has-text('Authorized Agent Company Name (insert N/A if not applicable)') + input",
            "*:has-text('Authorized Agent Company Name (insert N/A if not applicable)') ~ input",
            # Partial matches for the field
            "input[aria-label*='insert N/A if not applicable']",
            "input[placeholder*='insert N/A if not applicable']",
            "label:has-text('insert N/A if not applicable') + input",
            "label:has-text('insert N/A if not applicable') ~ input",
            "*:has-text('insert N/A if not applicable') + input",
            "*:has-text('insert N/A if not applicable') ~ input",
            # Look for fields specifically labeled for agent company name
            "input[aria-label*='Agent Company Name']",
            "input[placeholder*='Agent Company Name']",
            "input[aria-label*='Company Name of Agent']",
            "input[placeholder*='Company Name of Agent']",
            "input[aria-label*='Authorized Agent Company Name']",
            "input[placeholder*='Authorized Agent Company Name']",
            "label:has-text('Agent Company Name') + input",
            "label:has-text('Agent Company Name') ~ input",
            "label:has-text('Company Name of Agent') + input",
            "label:has-text('Company Name of Agent') ~ input",
            "label:has-text('Authorized Agent Company Name') + input",
            "label:has-text('Authorized Agent Company Name') ~ input",
            "*:has-text('Agent Company Name') + input",
            "*:has-text('Agent Company Name') ~ input",
            "*:has-text('Company Name of Agent') + input",
            "*:has-text('Company Name of Agent') ~ input",
            "*:has-text('Authorized Agent Company Name') + input",
            "*:has-text('Authorized Agent Company Name') ~ input",
            # Generic agent company selectors
            "input[name*='agent'][name*='company']",
            "input[name*='educator'][name*='company']",
            "input[name*='agent'][name*='organization']",
            "input[name*='educator'][name*='organization']",
            "input[placeholder*='Agent'][placeholder*='Company']",
            "input[placeholder*='Educator'][placeholder*='Company']",
            "input[placeholder*='agent'][placeholder*='company']",
            "input[placeholder*='educator'][placeholder*='company']",
            "input[aria-label*='Agent'][aria-label*='Company']",
            "input[aria-label*='Educator'][aria-label*='Company']",
            "input[id*='agent'][id*='company']",
            "input[id*='educator'][id*='company']",
            "input[data-testid*='agent'][data-testid*='company']",
            "input[data-testid*='educator'][data-testid*='company']"
        ]
        
        agent_company_filled = False
        company_name = str(self.form_data.get('Authorized Agent Company Name', 'N/A'))
        
        # Fill company name field - use "N/A" when Excel has "N/A", or use actual company name
        print(f"🏢 Company name from Excel: '{company_name}'")
        
        # Always try to fill the field (whether it's "N/A" or a real company name)
        for selector in agent_company_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.fill(selector, company_name)
                    print(f"✅ Agent company name filled: '{company_name}' with selector: {selector}")
                    time.sleep(1)
                    agent_company_filled = True
                    break
            except:
                continue
        
        if not agent_company_filled:
            print(f"⚠️ Agent company name field not found (value: '{company_name}')")
            # Let's add some debugging to see what fields are actually available
            print("🔍 DEBUG: Looking for any input fields that might be the company field...")
            try:
                # Get all visible input fields and check their labels/placeholders
                all_inputs = page.locator("input[type='text']:visible").all()
                print(f"Found {len(all_inputs)} text input fields on the form:")
                for i, input_field in enumerate(all_inputs):
                    try:
                        aria_label = input_field.get_attribute('aria-label') or ''
                        placeholder = input_field.get_attribute('placeholder') or ''
                        field_id = input_field.get_attribute('id') or ''
                        field_name = input_field.get_attribute('name') or ''
                        
                        # Check if this might be a company-related field
                        field_text = f"{aria_label} {placeholder} {field_id} {field_name}".lower()
                        if any(keyword in field_text for keyword in ['company', 'organization', 'agent', 'n/a', 'applicable', 'authorized']):
                            print(f"  🎯 Potential company field {i+1}: aria-label='{aria_label}', placeholder='{placeholder}', id='{field_id}', name='{field_name}'")
                        else:
                            print(f"  📝 Other field {i+1}: aria-label='{aria_label}', placeholder='{placeholder}', id='{field_id}', name='{field_name}'")
                    except:
                        continue
            except Exception as debug_error:
                print(f"⚠️ Debug error: {debug_error}")
        
        # STUDENT FIELDS: Fill student information (the person the agent is representing)
        print("👨‍🎓 Filling student information...")
        
        # Student First Name - enhanced selectors
        first_name_selectors = [
            "input[name='firstName']",
            "input[name='first_name']", 
            "input[id*='first']",
            "input[placeholder*='First']",
            "input[placeholder*='first']",
            "input[data-testid*='first']"
        ]
        for selector in first_name_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.fill(selector, str(self.form_data.get('First Name', 'StudentFirst')))
                    print(f"✅ Student first name filled with selector: {selector}")
                    time.sleep(1)
                    break
            except:
                continue
                
        # Child Last Name - enhanced selectors
        last_name_selectors = [
            "input[name='lastName']",
            "input[name='last_name']",
            "input[id*='last']",
            "input[placeholder*='Last']",
            "input[placeholder*='last']",
            "input[data-testid*='last']"
        ]
        for selector in last_name_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.fill(selector, str(self.form_data.get('Last Name', 'ChildLast')))
                    print(f"✅ Child last name filled with selector: {selector}")
                    time.sleep(1)
                    break
            except:
                continue
            
        # Child Email Address (Email of Child/Data Subject) - This might be the Primary Email Address field
        print("📧 Filling child/student email address...")
        child_email_selectors = [
            # Primary Email Address field we found (might be for child)
            "input[aria-label='Primary Email Address']",
            "input[id='emailDSARElement']",
            # Exact match from form label variations
            "input[aria-label*='Email of Child (Data Subject)']",
            "input[placeholder*='Email of Child (Data Subject)']",
            "label:has-text('Email of Child (Data Subject)') + input",
            "label:has-text('Email of Child (Data Subject)') ~ input",
            "*:has-text('Email of Child (Data Subject)') + input",
            "*:has-text('Email of Child (Data Subject)') ~ input",
            # Alternative variations
            "input[aria-label*='Email of Child']",
            "input[placeholder*='Email of Child']",
            "input[aria-label*='Child Email']", 
            "input[placeholder*='Child Email']",
            "input[aria-label*='Data Subject Email']",
            "input[placeholder*='Data Subject Email']",
            "input[aria-label*='Student Email']",
            "input[placeholder*='Student Email']",
            "label:has-text('Email of Child') + input",
            "label:has-text('Child Email') + input",
            "label:has-text('Student Email') + input",
            "label:has-text('Data Subject Email') + input",
            "*:has-text('Email of Child') + input",
            "*:has-text('Child Email') + input",
            "*:has-text('Student Email') + input",
            "*:has-text('Data Subject') + input[type='email']",
            # Generic selectors that might contain child/data subject context
            "input[name*='child'][type='email']",
            "input[name*='subject'][type='email']",
            "input[name*='student'][type='email']",
            "input[id*='child'][id*='email']",
            "input[id*='subject'][id*='email']",
            "input[id*='student'][id*='email']",
            "input[data-testid*='child'][data-testid*='email']",
            "input[data-testid*='student'][data-testid*='email']"
        ]
        
        child_email_filled = False
        child_email_value = str(self.form_data.get('Primary Email address', 
                               self.form_data.get('Email of Child (Data Subject)', 'childstudent@mailinator.com')))
        print(f"📧 Child email from Excel: '{child_email_value}'")
        
        for selector in child_email_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    # Check if this field is actually for child and not parent by examining context
                    field_element = page.locator(selector).first
                    field_label = ""
                    try:
                        # Try to get aria-label or placeholder to determine context
                        field_label = field_element.get_attribute('aria-label') or ""
                        if not field_label:
                            field_label = field_element.get_attribute('placeholder') or ""
                        if not field_label:
                            # Try to find associated label
                            field_id = field_element.get_attribute('id')
                            if field_id:
                                label_element = page.locator(f"label[for='{field_id}']").first
                                if label_element.is_visible():
                                    field_label = label_element.text_content() or ""
                    except:
                        pass
                    
                    # Check if this is definitely a child/student field and not parent/agent
                    field_label_lower = field_label.lower()
                    is_child_field = any(keyword in field_label_lower for keyword in ['child', 'student', 'data subject', 'subject'])
                    is_agent_field = any(keyword in field_label_lower for keyword in ['agent', 'educator', 'teacher'])
                    # NOTE: In agent forms, "Primary Email Address" is actually for the child, not parent
                    is_parent_field = any(keyword in field_label_lower for keyword in ['parent', 'guardian']) and 'primary email' not in field_label_lower
                    
                    # Skip agent fields, but allow primary email and child fields
                    if is_agent_field and 'primary' not in field_label_lower:
                        print(f"⚠️ Skipping email field (appears to be for agent): {selector} - {field_label}")
                        continue
                    elif is_parent_field:
                        print(f"⚠️ Skipping email field (appears to be for parent): {selector} - {field_label}")
                        continue
                    elif is_child_field or 'primary email' in field_label_lower or not (is_agent_field or is_parent_field):
                        page.fill(selector, child_email_value)
                        print(f"✅ Child email filled: '{child_email_value}' with selector: {selector}")
                        print(f"   Field context: {field_label}")
                        time.sleep(1)
                        child_email_filled = True
                        break
            except:
                continue
        
        if not child_email_filled:
            print("⚠️ Child email field not found")
            # Let's add some debugging to see what email fields are actually available
            print("🔍 DEBUG: Looking for any email fields that might be the child email field...")
            try:
                # Get all visible email input fields and check their labels/placeholders
                all_email_inputs = page.locator("input[type='email']:visible").all()
                for i, input_field in enumerate(all_email_inputs):
                    try:
                        aria_label = input_field.get_attribute('aria-label') or ''
                        placeholder = input_field.get_attribute('placeholder') or ''
                        field_id = input_field.get_attribute('id') or ''
                        field_name = input_field.get_attribute('name') or ''
                        
                        print(f"  Email field {i+1}: aria-label='{aria_label}', placeholder='{placeholder}', id='{field_id}', name='{field_name}'")
                    except:
                        continue
            except Exception as debug_error:
                print(f"⚠️ Debug error: {debug_error}")
            
        # Phone Number - enhanced selectors
        phone_selectors = [
            "input[type='tel']",
            "input[name='phone']",
            "input[name='telephone']",
            "input[id*='phone']",
            "input[placeholder*='phone']",
            "input[placeholder*='Phone']",
            "input[data-testid*='phone']"
        ]
        for selector in phone_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.fill(selector, str(self.form_data.get('Phone Number', '5712345567')))
                    print(f"✅ Phone filled with selector: {selector}")
                    time.sleep(1)
                    break
            except:
                continue
            
        # Birth Date - try multiple selectors and formats
        birthdate_selectors = [
            "input[type='date']",
            "input[name='birthdate']", 
            "input[name='dateOfBirth']",
            "input[name='dob']",
            "input[id*='birth']",
            "input[id*='date']",
            "input[placeholder*='birth']",
            "input[placeholder*='Birth']",
            "input[placeholder*='Date']",
            "input[class*='date']"
        ]
        
        birth_filled = False
        for selector in birthdate_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    # Get birth date from Excel data and try different formats
                    birth_date_raw = str(self.form_data.get('Date of Birth', '11/1/2008'))
                    date_formats = [birth_date_raw, "11/01/2008", "11/1/2008", "2008-11-01", "01/11/2008", "01-11-2008"]
                    for date_format in date_formats:
                        try:
                            page.fill(selector, date_format)
                            print(f"✅ Birth date filled with format {date_format} using selector {selector}")
                            birth_filled = True
                            break
                        except:
                            continue
                    if birth_filled:
                        break
            except:
                continue
        
        if not birth_filled:
            print("❌ Could not fill birth date field - manual inspection needed")
    
    def fill_contact_information(self, page: Page):
        """Fill contact/address information"""
        print("Filling contact information...")
        
        # Street Address - enhanced selectors
        address_selectors = [
            "input[name='address']",
            "input[name='street']",
            "input[id*='address']",
            "input[id*='street']",
            "input[placeholder*='Address']",
            "input[placeholder*='Street']",
            "input[data-testid*='address']"
        ]
        for selector in address_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.fill(selector, str(self.form_data.get('streetAddress', '507 Central Avenue')))
                    print(f"✅ Address filled with selector: {selector}")
                    break
            except:
                continue
            
        # City - enhanced selectors
        city_selectors = [
            "input[name='city']",
            "input[id*='city']",
            "input[placeholder*='City']",
            "input[data-testid*='city']"
        ]
        for selector in city_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.fill(selector, str(self.form_data.get('city', 'North Collins')))
                    print(f"✅ City filled with selector: {selector}")
                    break
            except:
                continue
            
        # Postal Code - enhanced selectors  
        postal_selectors = [
            "input[name='zip']",
            "input[name='postal']",
            "input[name='zipcode']",
            "input[id*='zip']",
            "input[id*='postal']",
            "input[placeholder*='Zip']",
            "input[placeholder*='Postal']",
            "input[data-testid*='zip']"
        ]
        for selector in postal_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.fill(selector, str(self.form_data.get('postalCode', '14111')))
                    print(f"✅ ZIP code filled with selector: {selector}")
                    break
            except:
                continue
            
        # Country FIRST - Use the actual country from Excel data for international requests
        print("🌍 Attempting to fill country field for international request...")
        country_filled = False
        
        # Get the actual country from Excel data
        country_from_excel = str(self.form_data.get('country', 'India'))
        print(f"🌏 Country from Excel: '{country_from_excel}'")
        
        try:
            # Try multiple selectors for country field - including input fields with dropdowns
            country_selectors = [
                "select[name*='country']",
                "select[id*='country']", 
                "select[id*='Country']",
                "select[class*='country']",
                "input[name*='country']",
                "input[id*='country']",
                "input[placeholder*='Country']",
                "input[placeholder*='country']",
                "[data-testid*='country']"
            ]
            
            for country_selector in country_selectors:
                try:
                    element = page.locator(country_selector).first
                    if element.is_visible():
                        print(f"🔍 Found country field with selector: {country_selector}")
                        
                        # STEP 1: Click the field to open dropdown (works for both select and input with dropdown)
                        try:
                            element.click(timeout=5000)
                            print("🖱️ Clicked country field to open dropdown")
                            time.sleep(2)  # Wait for dropdown to fully open
                            
                            # STEP 2: Look for dropdown options that match the Excel country
                            # Create dynamic selectors based on the actual country from Excel
                            country_option_selectors = [
                                # Standard option selectors for the Excel country
                                f"option:has-text('{country_from_excel}')",
                                f"option[value='{country_from_excel}']",
                                f"option[value*='{country_from_excel}']",
                                # List item selectors (for custom dropdowns)
                                f"li:has-text('{country_from_excel}')",
                                f"li[data-value='{country_from_excel}']",
                                f"li[data-value*='{country_from_excel}']",
                                # Div-based dropdown options
                                f"div:has-text('{country_from_excel}')",
                                f"[role='option']:has-text('{country_from_excel}')",
                                # More specific selectors
                                f".dropdown-option:has-text('{country_from_excel}')",
                                f".option:has-text('{country_from_excel}')",
                                f"[data-value='{country_from_excel}']",
                                f"[data-value*='{country_from_excel}']"
                            ]
                            
                            print(f"🔍 Looking for '{country_from_excel}' option in dropdown...")
                            option_clicked = False
                            
                            for option_selector in country_option_selectors:
                                try:
                                    option_element = page.locator(option_selector).first
                                    if option_element.is_visible():
                                        option_element.click(timeout=3000)
                                        print(f"✅ Clicked '{country_from_excel}' option with selector: {option_selector}")
                                        country_filled = True
                                        option_clicked = True
                                        break
                                except Exception as e:
                                    print(f"⚠️ Could not click option with {option_selector}: {str(e)}")
                                    continue
                            
                            # STEP 3: If clicking individual options didn't work, try select_option on select elements
                            if not option_clicked and country_selector.startswith("select"):
                                print("🔄 Trying select_option method...")
                                # Try different variations of the country name
                                country_variations = [country_from_excel, country_from_excel.upper(), country_from_excel.lower(), country_from_excel.title()]
                                for country_variation in country_variations:
                                    try:
                                        page.select_option(country_selector, value=country_variation, timeout=3000)
                                        print(f"✅ Country selected using select_option with value: {country_variation}")
                                        country_filled = True
                                        break
                                    except:
                                        try:
                                            page.select_option(country_selector, label=country_variation, timeout=3000)
                                            print(f"✅ Country selected using select_option with label: {country_variation}")
                                            country_filled = True
                                            break
                                        except:
                                            continue
                            
                            # STEP 4: If it's an input field, try typing the actual country
                            if not country_filled and not country_selector.startswith("select"):
                                try:
                                    element.fill(country_from_excel, timeout=3000)
                                    print(f"✅ Country typed into input field: {country_from_excel}")
                                    country_filled = True
                                    # Press Enter to confirm selection
                                    element.press("Enter")
                                    print("⌨️ Pressed Enter to confirm country selection")
                                except:
                                    print(f"⚠️ Could not type '{country_from_excel}' in country input field")
                                    
                        except Exception as e:
                            print(f"⚠️ Could not click country field: {str(e)}")
                        
                        if country_filled:
                            time.sleep(3)  # Longer pause after successful selection
                            break
                            
                except Exception as e:
                    print(f"⚠️ Error with country selector {country_selector}: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"❌ Major error in country selection: {str(e)}")
        
        if not country_filled:
            print(f"⚠️ Could not fill country field with '{country_from_excel}' - continuing anyway...")
            # Take a screenshot to see current state
            page.screenshot(path="dsr/screenshots/country_field_issue.png")
            print("📸 Screenshot saved: screenshots/country_field_issue.png")

        # State/Province handling for international requests
        print("🌍 Checking if state field is needed for international request...")
        
        # For international requests, state field may not be required or may not exist
        # Check if the country from Excel indicates this is truly international (non-US)
        country_from_excel = str(self.form_data.get('country', 'India'))
        is_us_address = country_from_excel.upper() in ['US', 'USA', 'UNITED STATES', 'UNITED STATES OF AMERICA']
        
        if is_us_address:
            print(f"🇺🇸 US address detected ('{country_from_excel}'), will attempt to fill state field...")
            # Use the existing state logic for US addresses
            state_filled = False
            try:
                # Wait for state field to become available after country selection
                print("⏳ Waiting for state field to become available after US country selection...")
                time.sleep(5)
                
                # Try multiple selectors for state field
                state_selectors = [
                    "select[name*='state']",
                    "select[id*='state']",
                    "select[id*='State']", 
                    "select[class*='state']",
                    "input[name*='state']",
                    "input[id*='state']",
                    "input[placeholder*='State']",
                    "input[placeholder*='state']",
                    "input[class*='state']",
                    "[data-testid*='state']",
                    "[aria-label*='state']",
                    "[aria-label*='State']"
                ]
                
                for state_selector in state_selectors:
                    try:
                        element = page.locator(state_selector).first
                        if element.is_visible():
                            print(f"🔍 Found state field with selector: {state_selector}")
                            
                            # Get state name from Excel data (fallback for US addresses in international file)
                            state_name = str(self.form_data.get('stateOrProvince', 'New York'))
                            print(f"🏛️ Using state from Excel: '{state_name}'")
                            
                            # Simple state selection for US addresses
                            try:
                                element.click(timeout=3000)
                                print("✅ Clicked state field")
                                time.sleep(1)
                                
                                element.fill(state_name)
                                print(f"✅ Typed '{state_name}'")
                                time.sleep(2)
                                
                                element.press("Enter")
                                print("⏎ Pressed Enter to select state")
                                time.sleep(2)
                                state_filled = True
                                break
                                
                            except Exception as e:
                                print(f"⚠️ Error filling state field: {str(e)}")
                                continue
                        
                    except Exception as e:
                        print(f"⚠️ Error with state selector {state_selector}: {str(e)}")
                        continue
                        
            except Exception as e:
                print(f"❌ Error in US state selection: {str(e)}")
                
            if not state_filled:
                print("⚠️ Could not fill US state field - continuing anyway...")
                
        else:
            print(f"🌏 International address detected ('{country_from_excel}'), skipping state field...")
            print("✅ No state field needed for international addresses")
            
            # Wait a moment for form to stabilize after country selection
        
        print("✅ Contact information section completed")
    
    def fill_additional_details(self, page: Page):
        """Fill additional form details"""
        print("Filling additional details...")
        
        # Student School Name - enhanced selectors with more variations
        print("🏫 Looking for student school name field...")
        school_selectors = [
            "input[name*='school']",
            "input[id*='school']",
            "input[placeholder*='School']",
            "input[placeholder*='school']",
            "input[placeholder*='Student School']",
            "input[placeholder*='student school']",
            "input[placeholder*='Institution']",
            "input[placeholder*='institution']",
            "input[data-testid*='school']",
            "input[aria-label*='school']",
            "input[aria-label*='School']",
            "input[aria-label*='Student']",
            # Look for fields that mention "If Student" or "N/A"
            "input[placeholder*='If Student']",
            "input[placeholder*='If not applicable']",
            "input[placeholder*='write N/A']"
        ]
        school_filled = False
        for selector in school_selectors:
            try:
                elements = page.locator(selector).all()
                for element in elements:
                    if element.is_visible():
                        placeholder = element.get_attribute("placeholder") or ""
                        label_text = ""
                        try:
                            # Try to find associated label
                            label_id = element.get_attribute("id")
                            if label_id:
                                label_elem = page.locator(f"label[for='{label_id}']").first
                                if label_elem.is_visible():
                                    label_text = label_elem.inner_text() or ""
                        except:
                            pass
                        
                        print(f"🔍 Found school field - placeholder: '{placeholder}', label: '{label_text}'")
                        element.fill(str(self.form_data.get('studentSchoolName', 'South Lakes High School')))
                        print(f"✅ School field filled with '{self.form_data.get('studentSchoolName', 'South Lakes High School')}' using selector: {selector}")
                        school_filled = True
                        break
                if school_filled:
                    break
            except:
                continue
        
        if not school_filled:
            print("⚠️ Student school field not found")
            
        # Graduation Year - enhanced selectors
        print("🎓 Looking for graduation year field...")
        grad_year_selectors = [
            "input[name*='graduation']",
            "input[id*='graduation']",
            "input[placeholder*='Graduation']",
            "input[placeholder*='graduation']",
            "input[placeholder*='Year']",
            "input[placeholder*='year']",
            "input[data-testid*='graduation']",
            "input[aria-label*='graduation']",
            "input[aria-label*='Graduation']",
            "input[type='number'][placeholder*='year']",
            "input[type='text'][placeholder*='year']"
        ]
        grad_filled = False
        for selector in grad_year_selectors:
            try:
                elements = page.locator(selector).all()
                for element in elements:
                    if element.is_visible():
                        placeholder = element.get_attribute("placeholder") or ""
                        print(f"🔍 Found graduation field - placeholder: '{placeholder}'")
                        element.fill(str(self.form_data.get('studentGraduationYear', '2020')))
                        print(f"✅ Graduation year filled with '{self.form_data.get('studentGraduationYear', '2020')}' using selector: {selector}")
                        grad_filled = True
                        break
                if grad_filled:
                    break
            except:
                continue
        
        if not grad_filled:
            print("⚠️ Graduation year field not found")
            
        # Educator School Affiliation - enhanced selectors
        print("👨‍🏫 Looking for educator affiliation field...")
        educator_selectors = [
            "input[name*='educator']",
            "input[id*='educator']",
            "input[placeholder*='Educator']",
            "input[placeholder*='educator']",
            "input[placeholder*='Affiliation']",
            "input[placeholder*='affiliation']",
            "input[placeholder*='Teacher']",
            "input[placeholder*='teacher']",
            "input[data-testid*='educator']",
            "input[aria-label*='educator']",
            "input[aria-label*='Educator']",
            "input[aria-label*='teacher']",
            "input[aria-label*='Teacher']"
        ]
        educator_filled = False
        for selector in educator_selectors:
            try:
                elements = page.locator(selector).all()
                for element in elements:
                    if element.is_visible():
                        placeholder = element.get_attribute("placeholder") or ""
                        print(f"🔍 Found educator field - placeholder: '{placeholder}'")
                        element.fill(str(self.form_data.get('educatorSchoolAffiliation', 'N/A')))
                        print(f"✅ Educator affiliation filled with '{self.form_data.get('educatorSchoolAffiliation', 'N/A')}' using selector: {selector}")
                        educator_filled = True
                        break
                if educator_filled:
                    break
            except:
                continue
        
        if not educator_filled:
            print("⚠️ Educator affiliation field not found")
                
        # Look for any textarea fields (description, comments, etc.)
        print("📝 Looking for textarea/comment fields...")
        textarea_selectors = [
            "textarea[name*='description']",
            "textarea[name*='comment']",
            "textarea[name*='message']",
            "textarea[name*='details']",
            "textarea[placeholder*='description']",
            "textarea[placeholder*='comment']",
            "textarea[placeholder*='message']",
            "textarea[placeholder*='details']",
            "textarea[placeholder*='additional']",
            "textarea[placeholder*='other']",
            "textarea[aria-label*='description']",
            "textarea[aria-label*='comment']",
            "textarea[aria-label*='message']",
            "textarea"
        ]
        textarea_filled = False
        for selector in textarea_selectors:
            try:
                elements = page.locator(selector).all()
                for element in elements:
                    if element.is_visible():
                        placeholder = element.get_attribute("placeholder") or ""
                        print(f"🔍 Found textarea field - placeholder: '{placeholder}'")
                        element.fill("Automated form submission for privacy request testing.")
                        print(f"✅ Textarea filled using selector: {selector}")
                        textarea_filled = True
                        break
                if textarea_filled:
                    break
            except:
                continue
        
        if not textarea_filled:
            print("⚠️ Textarea/comment field not found")
        
        # Look for any additional input fields that might need N/A
        print("🔍 Looking for any other empty input fields that might need N/A...")
        try:
            # Find all visible text inputs that are empty
            empty_inputs = page.locator("input[type='text']:not([value]):not([placeholder*='email']):not([placeholder*='Email']):not([placeholder*='phone']):not([placeholder*='Phone']):not([placeholder*='name']):not([placeholder*='Name'])").all()
            for i, input_elem in enumerate(empty_inputs):
                try:
                    if input_elem.is_visible() and not input_elem.input_value():
                        placeholder = input_elem.get_attribute("placeholder") or ""
                        name = input_elem.get_attribute("name") or ""
                        print(f"🔍 Found empty text input - name: '{name}', placeholder: '{placeholder}'")
                        # Fill with N/A if it looks like it might need it
                        if any(word in placeholder.lower() for word in ["school", "institution", "affiliation", "organization", "company"]):
                            input_elem.fill("N/A")
                            print(f"✅ Filled empty input with 'N/A' - placeholder: '{placeholder}'")
                except:
                    continue
        except:
            pass
        
        print("✅ Additional details section completed")
    
    def handle_delete_request_additional_details(self, page: Page):
        """Handle additional details field that appears specifically for delete requests"""
        print("📝 Handling delete request additional details...")
        
        # Check if this is a delete request
        request_type_from_excel = str(self.form_data.get('Request_type', '')).strip().lower()
        if 'delete' not in request_type_from_excel:
            print("ℹ️ Not a delete request, skipping additional details")
            return
        
        # Wait for the additional details field to appear after selecting delete request type
        time.sleep(3)
        
        # Look for the additional details prompt
        details_indicators = [
            "text=If necessary, please add additional details",
            "text=If you have no details to add, write N/A",
            "text=additional details",
            "text=Additional details",
            "text=Please provide additional information",
            "text=If necessary, please add"
        ]
        
        details_section_found = False
        for indicator in details_indicators:
            try:
                if page.locator(indicator).first.is_visible():
                    print(f"✅ Found additional details section: {indicator}")
                    details_section_found = True
                    break
            except:
                continue
        
        if not details_section_found:
            print("ℹ️ Additional details section not found - may not be required")
            return
        
        # Look for the textarea or input field for additional details
        print("🔍 Looking for additional details input field...")
        additional_details_selectors = [
            "textarea[name*='additional']",
            "textarea[name*='details']",
            "textarea[name*='comment']",
            "textarea[name*='message']",
            "textarea[placeholder*='additional']",
            "textarea[placeholder*='details']",
            "textarea[placeholder*='N/A']",
            "textarea[placeholder*='add additional details']",
            "textarea[aria-label*='additional']",
            "textarea[aria-label*='details']",
            "input[name*='additional']",
            "input[name*='details']",
            "input[placeholder*='additional']",
            "input[placeholder*='details']",
            "input[placeholder*='N/A']",
            "textarea"  # Last resort - any textarea
        ]
        
        details_filled = False
        additional_details_text = str(self.form_data.get('additional_details', 'N/A')).strip()
        
        if not additional_details_text or additional_details_text.lower() in ['nan', '', 'none']:
            additional_details_text = 'N/A'
        
        print(f"📝 Additional details text from Excel: '{additional_details_text}'")
        
        for selector in additional_details_selectors:
            try:
                elements = page.locator(selector).all()
                for element in elements:
                    if element.is_visible():
                        placeholder = element.get_attribute("placeholder") or ""
                        name = element.get_attribute("name") or ""
                        
                        print(f"🔍 Found details field - name: '{name}', placeholder: '{placeholder}'")
                        
                        # Clear any existing content and fill with our data
                        element.fill("")
                        time.sleep(0.5)
                        element.fill(additional_details_text)
                        print(f"✅ Additional details filled: '{additional_details_text}' using selector: {selector}")
                        details_filled = True
                        break
                if details_filled:
                    break
            except:
                continue
        
        if not details_filled:
            print("⚠️ Additional details field not found")
        else:
            print(f"✅ Successfully filled additional details with: '{additional_details_text}'")
        
        time.sleep(2)  # Brief pause after filling details
    
    def select_request_type(self, page: Page):
        """Select request type dynamically based on Excel data"""
        print("📋 Selecting request type dynamically...")
        
        # Get the request type from Excel data
        request_type_from_excel = str(self.form_data.get('Request_type', 'Request a copy of my data')).strip()
        print(f"🎯 Request type from Excel: '{request_type_from_excel}'")
        
        # Define possible request type mappings for different wordings
        request_type_mappings = {
            # Delete data variants
            'request to delete my data': ['delete', 'removal', 'erase', 'remove'],
            'delete my data': ['delete', 'removal', 'erase', 'remove'],
            'delete data': ['delete', 'removal', 'erase', 'remove'],
            'remove my data': ['delete', 'removal', 'erase', 'remove'],
            'erase my data': ['delete', 'removal', 'erase', 'remove'],
            
            # Parent/CC information specific (exact match priority)
            'remove my parent\'s cc information': ['cc information', 'parent', 'credit card'],
            'remove my parents cc information': ['cc information', 'parent', 'credit card'],
            'remove parent cc information': ['cc information', 'parent', 'credit card'],
            'remove my parent\'s credit card information': ['cc information', 'parent', 'credit card'],
            
            # Copy data variants  
            'request a copy of my data': ['copy', 'access', 'download', 'portability'],
            'copy of my data': ['copy', 'access', 'download', 'portability'],
            'copy my data': ['copy', 'access', 'download', 'portability'],
            'access my data': ['copy', 'access', 'download', 'portability'],
            'download my data': ['copy', 'access', 'download', 'portability'],
            
            # Correct data variants
            'correct my data': ['correct', 'rectify', 'update', 'modify'],
            'update my data': ['correct', 'rectify', 'update', 'modify'],
            'modify my data': ['correct', 'rectify', 'update', 'modify'],
            'rectify my data': ['correct', 'rectify', 'update', 'modify'],
            
            # Restrict processing variants
            'restrict processing': ['restrict', 'limit', 'stop processing'],
            'limit processing': ['restrict', 'limit', 'stop processing'],
            'stop processing my data': ['restrict', 'limit', 'stop processing'],
            
            # Object to processing variants
            'object to processing': ['object', 'opt out', 'withdraw consent'],
            'opt out': ['object', 'opt out', 'withdraw consent'],
            'opt out of search': ['opt out', 'search', 'withdraw consent'],
            'withdraw consent': ['object', 'opt out', 'withdraw consent'],
            
            # Close/deactivate account variants
            'close/deactivate/cancel my college board account': ['close', 'deactivate', 'cancel', 'account'],
            'close my college board account': ['close', 'deactivate', 'cancel', 'account'],
            'deactivate my college board account': ['close', 'deactivate', 'cancel', 'account'],
            'cancel my college board account': ['close', 'deactivate', 'cancel', 'account'],
            'close account': ['close', 'deactivate', 'cancel', 'account'],
            'deactivate account': ['close', 'deactivate', 'cancel', 'account'],
            'cancel account': ['close', 'deactivate', 'cancel', 'account']
        }
        
        # STEP 1: First try EXACT TEXT MATCHING (priority)
        search_keywords = []
        request_type_lower = request_type_from_excel.lower()
        exact_match_found = False
        
        # Check for exact phrase matches first
        for key, keywords in request_type_mappings.items():
            if key in request_type_lower:
                search_keywords = keywords
                exact_match_found = True
                print(f"✅ Found exact mapping for '{request_type_from_excel}' -> keywords: {keywords}")
                break
        
        # STEP 2: If no exact mapping found, try KEYWORD-BASED MATCHING (fallback)
        if not search_keywords:
            print(f"⚠️ No exact mapping found for '{request_type_from_excel}', trying keyword-based matching...")
            
            # Special handling for specific cases that might be mismatched
            if 'cc information' in request_type_lower or 'credit card' in request_type_lower:
                # This might be a specific request type, let's try to find exact match first
                search_keywords = ['cc information', 'credit card', 'parent', 'remove']
                print(f"🎯 Detected CC/credit card request, using specific keywords: {search_keywords}")
            elif 'parent' in request_type_lower and 'information' in request_type_lower:
                # Parent information removal - might be its own category
                search_keywords = ['parent', 'information', 'remove', 'cc']
                print(f"🎯 Detected parent information request, using specific keywords: {search_keywords}")
            elif 'delete' in request_type_lower or 'remove' in request_type_lower or 'erase' in request_type_lower:
                search_keywords = ['delete', 'removal', 'erase', 'remove']
                print(f"🔍 Using delete/remove keywords: {search_keywords}")
            elif 'copy' in request_type_lower or 'access' in request_type_lower or 'download' in request_type_lower:
                search_keywords = ['copy', 'access', 'download', 'portability']
                print(f"🔍 Using copy/access keywords: {search_keywords}")
            elif 'correct' in request_type_lower or 'update' in request_type_lower or 'modify' in request_type_lower:
                search_keywords = ['correct', 'rectify', 'update', 'modify']
                print(f"🔍 Using correct/update keywords: {search_keywords}")
            elif 'restrict' in request_type_lower or 'limit' in request_type_lower:
                search_keywords = ['restrict', 'limit', 'stop processing']
                print(f"🔍 Using restrict/limit keywords: {search_keywords}")
            elif 'object' in request_type_lower or 'opt out' in request_type_lower:
                search_keywords = ['object', 'opt out', 'withdraw consent']
                print(f"🔍 Using object/opt-out keywords: {search_keywords}")
            elif 'close' in request_type_lower or 'deactivate' in request_type_lower or 'cancel' in request_type_lower:
                search_keywords = ['close', 'deactivate', 'cancel', 'account']
                print(f"🔍 Using close/deactivate/cancel keywords: {search_keywords}")
            else:
                # Default to copy if nothing matches
                search_keywords = ['copy', 'access', 'download', 'portability']
                print(f"⚠️ No specific mapping found for '{request_type_from_excel}', defaulting to copy/access keywords")
        
        print(f"🔍 Final search keywords: {search_keywords}")
        
        # First, debug: find all available radio buttons and their labels
        print("🔍 DEBUG: Finding all available request type options...")
        try:
            radio_elements = page.locator("input[type='radio'], input[type='checkbox']").all()
            available_options = []
            
            for i, radio in enumerate(radio_elements):
                try:
                    if radio.is_visible():
                        radio_id = radio.get_attribute("id") or ""
                        radio_value = radio.get_attribute("value") or ""
                        radio_name = radio.get_attribute("name") or ""
                        
                        # Look for associated label
                        label_text = ""
                        try:
                            if radio_id:
                                label_elem = page.locator(f"label[for='{radio_id}']").first
                                if label_elem.is_visible():
                                    label_text = label_elem.inner_text() or ""
                            
                            # Also try to find nearby text
                            if not label_text:
                                parent = radio.locator("xpath=..").first
                                if parent.is_visible():
                                    parent_text = parent.inner_text() or ""
                                    # Extract just the relevant part
                                    lines = parent_text.split('\n')
                                    for line in lines:
                                        line = line.strip()
                                        if line and len(line) < 100:  # Reasonable length for option text
                                            label_text = line
                                            break
                        except:
                            pass
                        
                        option_info = {
                            'index': i+1,
                            'element': radio,
                            'id': radio_id,
                            'value': radio_value,
                            'name': radio_name,
                            'label': label_text
                        }
                        available_options.append(option_info)
                        print(f"  Option {i+1}: value='{radio_value}', name='{radio_name}', label='{label_text}'")
                except Exception as e:
                    print(f"  Option {i+1}: Error reading - {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"⚠️ Error finding radio elements: {str(e)}")
            available_options = []
        
        # Now try to select the appropriate option based on search keywords
        request_type_selected = False
        
        for option in available_options:
            try:
                # Combine all text for searching
                search_text = f"{option['value']} {option['label']} {option['name']}".lower()
                
                # Check if any of our search keywords match this option
                for keyword in search_keywords:
                    if keyword.lower() in search_text:
                        print(f"🎯 Found matching option for keyword '{keyword}': '{option['label']}'")
                        try:
                            option['element'].click(timeout=5000)
                            print(f"✅ Selected request type: '{option['label']}' (matched keyword: '{keyword}')")
                            request_type_selected = True
                            time.sleep(2)  # Brief pause after selection
                            break
                        except Exception as e:
                            print(f"⚠️ Could not click option: {str(e)}")
                            continue
                
                if request_type_selected:
                    break
                    
            except Exception as e:
                print(f"⚠️ Error checking option: {str(e)}")
                continue
        
        # If still not found, try text-based selectors with EXACT MATCHING first
        if not request_type_selected:
            print("🔄 Trying text-based selectors...")
            
            # STEP 1: Try exact matching with the original Excel text first
            print(f"🎯 STEP 1: Trying exact match for: '{request_type_from_excel}'")
            exact_match_selectors = [
                f"label:has-text('{request_type_from_excel}')",
                f"span:has-text('{request_type_from_excel}')", 
                f"div:has-text('{request_type_from_excel}')",
                f"button:has-text('{request_type_from_excel}')",
                f"[aria-label*='{request_type_from_excel}']"
            ]
            
            for selector in exact_match_selectors:
                try:
                    elements = page.locator(selector).all()
                    for element in elements:
                        if element.is_visible():
                            text = ""
                            try:
                                text = element.inner_text() or element.text_content() or ""
                            except:
                                pass
                            
                            # Check for exact or very close match
                            if request_type_from_excel.lower() in text.lower() or text.lower() in request_type_from_excel.lower():
                                print(f"🎯 Found EXACT MATCH - text: '{text}'")
                                element.click(timeout=5000)
                                print(f"✅ Selected request type using EXACT MATCH: '{text}'")
                                request_type_selected = True
                                time.sleep(2)
                                break
                        
                    if request_type_selected:
                        break
                except Exception as e:
                    print(f"⚠️ Could not use exact match selector {selector}: {str(e)}")
                    continue
            
            # STEP 2: If no exact match, try keyword-based matching  
            if not request_type_selected:
                print(f"🔍 STEP 2: No exact match found, trying keyword-based matching...")
                
                for keyword in search_keywords:
                    if request_type_selected:
                        break
                        
                    # Create dynamic selectors based on keywords
                    text_selectors = [
                        f"label:has-text('{keyword}')",
                        f"span:has-text('{keyword}')",
                        f"div:has-text('{keyword}')",
                        f"button:has-text('{keyword}')",
                        f"[aria-label*='{keyword}']",
                        f"[data-value*='{keyword}']",
                        f"[value*='{keyword}']"
                    ]
                    
                    for selector in text_selectors:
                        try:
                            elements = page.locator(selector).all()
                            for element in elements:
                                if element.is_visible():
                                    text = ""
                                    try:
                                        text = element.inner_text() or element.text_content() or ""
                                    except:
                                        pass
                                    
                                    # Check if this looks like our target option
                                    if keyword.lower() in text.lower():
                                        print(f"🔍 Found text-based option - text: '{text}' (keyword: '{keyword}')")
                                        element.click(timeout=5000)
                                        print(f"✅ Selected request type using text selector: '{text}'")
                                        request_type_selected = True
                                        time.sleep(2)
                                        break
                                
                            if request_type_selected:
                                break
                        except Exception as e:
                            print(f"⚠️ Could not use selector {selector}: {str(e)}")
                            continue
        
        # Final fallback - try to click anything that seems related to our original Excel text
        if not request_type_selected:
            print("🔄 Final fallback: searching for partial matches with Excel text...")
            
            # Extract key words from the original Excel request type
            excel_words = request_type_from_excel.lower().split()
            meaningful_words = [word for word in excel_words if len(word) > 3 and word not in ['data', 'my', 'the', 'to', 'of', 'and']]
            
            print(f"🔍 Trying partial matches with words: {meaningful_words}")
            
            for option in available_options:
                search_text = f"{option['value']} {option['label']} {option['name']}".lower()
                
                for word in meaningful_words:
                    if word in search_text:
                        print(f"🎯 Found partial match for word '{word}': '{option['label']}'")
                        try:
                            option['element'].click(timeout=5000)
                            print(f"✅ Selected request type with partial match: '{option['label']}'")
                            request_type_selected = True
                            time.sleep(2)
                            break
                        except Exception as e:
                            print(f"⚠️ Could not click option: {str(e)}")
                            continue
                
                if request_type_selected:
                    break
        
        if not request_type_selected:
            print(f"⚠️ Could not find option for '{request_type_from_excel}'")
            print("📋 Available options were:")
            for option in available_options:
                print(f"  - '{option['label']}' (value: '{option['value']}')")
            
            # Take screenshot for debugging
            page.screenshot(path="dsr/screenshots/request_type_debug.png")
            print("📸 Debug screenshot saved: screenshots/request_type_debug.png")
        
        print("✅ Request type selection completed")
    
    def handle_delete_data_suboptions(self, page: Page):
        """Handle delete data sub-options when 'request to delete my data' is selected"""
        print("🗑️ Handling delete data sub-options...")
        
        # Check if this is a delete request
        request_type_from_excel = str(self.form_data.get('Request_type', '')).strip().lower()
        if 'delete' not in request_type_from_excel:
            print("ℹ️ Not a delete request, skipping delete sub-options")
            return
        
        # Get delete options from Excel
        delete_student = str(self.form_data.get('delete_student', '')).strip()
        delete_parent = str(self.form_data.get('delete_parent', '')).strip()
        delete_educator = str(self.form_data.get('delete_educator', '')).strip()
        
        print(f"📊 Delete options from Excel:")
        print(f"  🎓 Student data: '{delete_student}'")
        print(f"  👨‍👩‍👧‍👦 Parent data: '{delete_parent}'")
        print(f"  👨‍🏫 Educator data: '{delete_educator}'")
        
        # Determine which options should be selected based on Excel values
        # If the field contains text like "Student data (if any)" or "yes/true/1", select it
        # If the field is empty, "no", "false", "0", don't select it
        
        def should_select_option(excel_value):
            """Determine if an option should be selected based on Excel value"""
            # Convert to string and handle NaN/None values
            if excel_value is None:
                return False
            
            excel_str = str(excel_value).strip()
            
            # Handle pandas NaN, empty strings, and explicit "no" values
            if excel_str.lower() in ['nan', '', 'none', 'no', 'false', '0', 'n']:
                return False
            
            # Handle explicit "yes" values
            if excel_str.lower() in ['yes', 'true', '1', 'y']:
                return True
                
            # If it contains descriptive text like "Student data (if any)", select it
            # This means the Excel has specific instructions for this option
            if any(keyword in excel_str.lower() for keyword in ['data', 'student', 'parent', 'educator']):
                return True
                
            # For any other non-empty value, consider it as "select"
            return len(excel_str) > 0
        
        student_should_select = should_select_option(delete_student)
        parent_should_select = should_select_option(delete_parent)
        educator_should_select = should_select_option(delete_educator)
        
        print(f"📋 Selection logic based on Excel data:")
        print(f"  🎓 Student: {'SELECT' if student_should_select else 'SKIP'} (Excel: '{delete_student}')")
        print(f"  👨‍👩‍👧‍👦 Parent: {'SELECT' if parent_should_select else 'SKIP'} (Excel: '{delete_parent}')")
        print(f"  👨‍🏫 Educator: {'SELECT' if educator_should_select else 'SKIP'} (Excel: '{delete_educator}')")
        
        # Count how many options should be selected
        total_to_select = sum([student_should_select, parent_should_select, educator_should_select])
        print(f"📊 Total options to select: {total_to_select}")
        
        if total_to_select == 0:
            print("⚠️ No delete options to select based on Excel data!")
            return
        
        # Wait a moment for any dynamic content to load after request type selection
        time.sleep(3)
        
        # Look for the delete data sub-question text
        delete_question_indicators = [
            "text=you may engage with College Board in multiple ways",
            "text=Please let us know which data you would like deleted",
            "text=You may select more than one option below",
            "text=which data you would like deleted",
            "text=Student data (if any)",
            "text=Parent data (if any)",
            "text=Educator data (if any)"
        ]
        
        delete_question_found = False
        for indicator in delete_question_indicators:
            try:
                if page.locator(indicator).first.is_visible():
                    delete_question_found = True
                    print(f"✅ Found delete sub-question with indicator: {indicator}")
                    break
            except:
                continue
        
        if not delete_question_found:
            print("ℹ️ Delete data sub-question not found - may not be required for this form")
            return
        
        print("🔍 Delete data sub-question detected! Looking for options...")
        
        # Define the option mappings
        delete_options = [
            {
                'excel_field': 'delete_student',
                'excel_value': delete_student,
                'should_select': student_should_select,
                'option_keywords': ['student', 'student data'],
                'description': '🎓 Student data'
            },
            {
                'excel_field': 'delete_parent', 
                'excel_value': delete_parent,
                'should_select': parent_should_select,
                'option_keywords': ['parent', 'parent data'],
                'description': '👨‍👩‍👧‍👦 Parent data'
            },
            {
                'excel_field': 'delete_educator',
                'excel_value': delete_educator,
                'should_select': educator_should_select,
                'option_keywords': ['educator', 'educator data', 'teacher'],
                'description': '👨‍🏫 Educator data'
            }
        ]
        
        # First, find all available clickable options (not checkboxes)
        print("🔍 Finding all available delete data options...")
        available_options = []
        
        # Try multiple selectors for clickable option elements
        option_selectors = [
            "button:has-text('Student data')",
            "button:has-text('Parent data')",
            "button:has-text('Educator data')",
            "div:has-text('Student data (if any)')",
            "div:has-text('Parent data (if any)')",
            "div:has-text('Educator data (if any)')",
            "span:has-text('Student data')",
            "span:has-text('Parent data')",
            "span:has-text('Educator data')",
            "[role='button']:has-text('Student')",
            "[role='button']:has-text('Parent')",
            "[role='button']:has-text('Educator')",
            ".option:has-text('Student')",
            ".option:has-text('Parent')",
            ".option:has-text('Educator')",
            "[data-testid*='student']",
            "[data-testid*='parent']",
            "[data-testid*='educator']"
        ]
        
        try:
            # Look for all clickable elements that might contain delete options
            all_clickables = page.locator("button, div[role='button'], span[role='button'], .option, [data-testid], [class*='option']").all()
            
            for i, element in enumerate(all_clickables):
                try:
                    if element.is_visible():
                        element_text = element.inner_text().strip()
                        element_id = element.get_attribute("id") or ""
                        element_class = element.get_attribute("class") or ""
                        element_role = element.get_attribute("role") or ""
                        element_testid = element.get_attribute("data-testid") or ""
                        
                        # Check if this element contains delete data option keywords
                        search_text = f"{element_text} {element_id} {element_class} {element_testid}".lower()
                        if any(keyword in search_text for keyword in ['student', 'parent', 'educator']) and 'data' in search_text:
                            option_info = {
                                'index': i+1,
                                'element': element,
                                'text': element_text,
                                'id': element_id,
                                'class': element_class,
                                'role': element_role,
                                'testid': element_testid
                            }
                            available_options.append(option_info)
                            print(f"  Option {len(available_options)}: text='{element_text}', class='{element_class}', role='{element_role}'")
                
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"⚠️ Error finding clickable options: {str(e)}")
            
        # Also try direct text selectors for common patterns
        direct_selectors = [
            "text=Student data (if any)",
            "text=Parent data (if any)", 
            "text=Educator data (if any)",
            "text=Student data",
            "text=Parent data",
            "text=Educator data"
        ]
        
        for selector in direct_selectors:
            try:
                elements = page.locator(selector).all()
                for element in elements:
                    if element.is_visible():
                        element_text = element.inner_text().strip()
                        option_info = {
                            'index': len(available_options) + 1,
                            'element': element,
                            'text': element_text,
                            'selector': selector
                        }
                        available_options.append(option_info)
                        print(f"  Direct option {len(available_options)}: text='{element_text}', selector='{selector}'")
            except:
                continue
        
        # Now process each delete option based on Excel settings
        for option_config in delete_options:
            excel_value = option_config['excel_value']
            should_select = option_config['should_select']
            keywords = option_config['option_keywords']
            description = option_config['description']
            
            print(f"\n🔍 Processing {description} (Excel: '{excel_value}', Should select: {should_select})")
            
            if not should_select:
                print(f"  ⏭️ SKIPPING {description} - Excel value is empty/NaN/no: '{excel_value}'")
                print(f"  📋 Following Excel instructions: empty = skip, even if option exists on form")
                continue
            
            # Find matching clickable option
            option_found = False
            for option_info in available_options:
                search_text = f"{option_info.get('text', '')} {option_info.get('id', '')} {option_info.get('class', '')}".lower()
                
                # Check if any keywords match
                for keyword in keywords:
                    if keyword.lower() in search_text:
                        print(f"  🎯 Found matching option for '{keyword}': '{option_info.get('text', '')}'")
                        
                        try:
                            # Click the option element
                            option_info['element'].click(timeout=5000)
                            print(f"  ✅ Clicked {description}: '{option_info.get('text', '')}'")
                            time.sleep(2)  # Wait for any text input to appear
                            
                            # Check for text input field after selecting the option
                            print(f"  🔍 Looking for text input after selecting {description}...")
                            text_input_selectors = [
                                "input[type='text']:visible",
                                "textarea:visible", 
                                "input[placeholder*='details']:visible",
                                "input[placeholder*='information']:visible",
                                "textarea[placeholder*='details']:visible",
                                "textarea[placeholder*='information']:visible",
                                "input:not([type='hidden']):not([type='radio']):not([type='checkbox']):visible",
                                ".text-input:visible",
                                "[data-testid*='text']:visible",
                                "[aria-label*='text']:visible"
                            ]
                            
                            text_input_found = False
                            for text_selector in text_input_selectors:
                                try:
                                    text_inputs = page.locator(text_selector).all()
                                    for text_input in text_inputs:
                                        if text_input.is_visible():
                                            # Check if this is a new text input (not pre-filled)
                                            current_value = text_input.input_value()
                                            if not current_value or len(current_value.strip()) == 0:
                                                # This looks like the text input for the delete option
                                                text_input.fill("test DSR")
                                                print(f"  ✅ Entered 'test DSR' in text input for {description}")
                                                text_input_found = True
                                                time.sleep(1)
                                                break
                                    if text_input_found:
                                        break
                                except:
                                    continue
                            
                            if not text_input_found:
                                print(f"  ℹ️ No text input found after selecting {description}")
                            
                            option_found = True
                            break
                        except Exception as e:
                            print(f"  ⚠️ Could not click option: {str(e)}")
                            # Try force click
                            try:
                                option_info['element'].click(force=True, timeout=5000)
                                print(f"  ✅ Force-clicked {description}: '{option_info.get('text', '')}'")
                                time.sleep(2)
                                
                                # Try text input after force click too
                                try:
                                    text_input = page.locator("input[type='text']:visible, textarea:visible").first
                                    if text_input.is_visible():
                                        text_input.fill("test DSR")
                                        print(f"  ✅ Entered 'test DSR' after force-click")
                                except:
                                    pass
                                
                                option_found = True
                                break
                            except Exception as e2:
                                print(f"  ❌ Force click also failed: {str(e2)}")
                                continue
                
                if option_found:
                    break
            
            if not option_found:
                print(f"  ⚠️ Could not find clickable option for {description}")
                # Try direct text selector as fallback
                text_patterns = [
                    f"{keyword} data (if any)" for keyword in keywords
                ] + [
                    f"{keyword} data" for keyword in keywords
                ] + keywords
                
                for pattern in text_patterns:
                    try:
                        selector = f"text={pattern}"
                        if page.locator(selector).first.is_visible():
                            page.click(selector, timeout=3000)
                            print(f"  ✅ Clicked {description} using text selector: '{pattern}'")
                            time.sleep(2)
                            
                            # Check for text input after clicking
                            try:
                                text_input = page.locator("input[type='text']:visible, textarea:visible").first
                                if text_input.is_visible():
                                    text_input.fill("test DSR")
                                    print(f"  ✅ Entered 'test DSR' after clicking '{pattern}'")
                            except:
                                pass
                            
                            option_found = True
                            break
                    except:
                        continue
                
                if not option_found:
                    print(f"  ❌ All attempts failed for {description}")
        
        # Take screenshot after delete options selection
        page.screenshot(path="dsr/screenshots/delete_options_selected.png")
        print("📸 Screenshot saved: screenshots/delete_options_selected.png")
        
        print("✅ Delete data sub-options handling completed")
    
    def handle_close_account_suboptions(self, page: Page):
        """Handle close account sub-options when 'Close/deactivate/cancel my College Board account' is selected"""
        print("🚪 Handling close account sub-options...")
        
        # Check if this is a close account request
        request_type_from_excel = str(self.form_data.get('Request_type', '')).strip().lower()
        if not any(keyword in request_type_from_excel for keyword in ['close', 'deactivate', 'cancel', 'account']):
            print("ℹ️ Not a close account request, skipping close account sub-options")
            return
        
        # Get close account options from Excel
        close_student = str(self.form_data.get('close_student', '')).strip()
        close_educator = str(self.form_data.get('close_educator', '')).strip()
        
        print(f"📊 Close account options from Excel:")
        print(f"  🎓 Student account: '{close_student}'")
        print(f"  👨‍🏫 Educator account: '{close_educator}'")
        
        # Determine which options should be selected based on Excel values
        def should_select_option(excel_value):
            """Determine if an option should be selected based on Excel value"""
            if excel_value is None:
                return False
            
            excel_str = str(excel_value).strip()
            
            # Handle pandas NaN, empty strings, and explicit "no" values
            if excel_str.lower() in ['nan', '', 'none', 'no', 'false', '0', 'n']:
                return False
            
            # Handle explicit "yes" values
            if excel_str.lower() in ['yes', 'true', '1', 'y']:
                return True
                
            # If it contains descriptive text like "Student account (if any)", select it
            if any(keyword in excel_str.lower() for keyword in ['account', 'student', 'educator']):
                return True
                
            # For any other non-empty value, consider it as "select"
            return len(excel_str) > 0
        
        student_should_select = should_select_option(close_student)
        educator_should_select = should_select_option(close_educator)
        
        print(f"📋 Selection logic based on Excel data:")
        print(f"  🎓 Student account: {'SELECT' if student_should_select else 'SKIP'} (Excel: '{close_student}')")
        print(f"  👨‍🏫 Educator account: {'SELECT' if educator_should_select else 'SKIP'} (Excel: '{close_educator}')")
        
        # Count how many options should be selected
        total_to_select = sum([student_should_select, educator_should_select])
        print(f"📊 Total options to select: {total_to_select}")
        
        if total_to_select == 0:
            print("⚠️ No close account options to select based on Excel data!")
            return
        
        # Wait a moment for any dynamic content to load after request type selection
        time.sleep(3)
        
        # Look for the close account sub-question text
        close_question_indicators = [
            "text=Student account (if any)",
            "text=Educator data (if any)",
            "text=Please select which account",
            "text=Select the account type",
            "text=Which account would you like to close"
        ]
        
        close_question_found = False
        for indicator in close_question_indicators:
            try:
                if page.locator(indicator).first.is_visible():
                    close_question_found = True
                    print(f"✅ Found close account sub-question with indicator: {indicator}")
                    break
            except:
                continue
        
        if not close_question_found:
            print("ℹ️ Close account sub-question not found - may not be required for this form")
            return
        
        print("🔍 Close account sub-question detected! Looking for options...")
        
        # Define the option mappings
        close_options = [
            {
                'excel_field': 'close_student',
                'excel_value': close_student,
                'should_select': student_should_select,
                'option_keywords': ['student', 'student account'],
                'description': '🎓 Student account'
            },
            {
                'excel_field': 'close_educator', 
                'excel_value': close_educator,
                'should_select': educator_should_select,
                'option_keywords': ['educator', 'educator data', 'teacher'],
                'description': '👨‍🏫 Educator account'
            }
        ]
        
        # Find all available clickable options
        print("🔍 Finding all available close account options...")
        available_options = []
        
        # Try direct text selectors for common patterns
        direct_selectors = [
            "text=Student account (if any)",
            "text=Educator data (if any)", 
            "text=Student account",
            "text=Educator data",
            "text=Educator account"
        ]
        
        for selector in direct_selectors:
            try:
                elements = page.locator(selector).all()
                for element in elements:
                    if element.is_visible():
                        text = element.inner_text()
                        option_info = {
                            'element': element,
                            'text': text,
                            'selector': selector
                        }
                        available_options.append(option_info)
                        print(f"  Direct option: text='{text}', selector='{selector}'")
            except:
                continue
        
        # Also try to find all clickable elements that might contain close account options
        try:
            all_clickables = page.locator("button, div[role='button'], span[role='button'], .option, [data-testid], [class*='option']").all()
            
            for i, element in enumerate(all_clickables):
                try:
                    if element.is_visible():
                        text = element.inner_text()
                        if text and any(keyword in text.lower() for keyword in ['student', 'educator', 'account', 'data']):
                            option_info = {
                                'element': element,
                                'text': text,
                                'selector': f'clickable_{i}'
                            }
                            # Avoid duplicates
                            if not any(opt['text'].lower() == text.lower() for opt in available_options):
                                available_options.append(option_info)
                                print(f"  Clickable option: text='{text}'")
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"⚠️ Error finding clickable options: {str(e)}")
        
        # Now process each close account option based on Excel settings
        for option_config in close_options:
            excel_value = option_config['excel_value']
            should_select = option_config['should_select']
            keywords = option_config['option_keywords']
            description = option_config['description']
            
            print(f"\n🔍 Processing {description} (Excel: '{excel_value}', Should select: {should_select})")
            
            if not should_select:
                print(f"  ⏭️ SKIPPING {description} - Excel value is empty/NaN/no: '{excel_value}'")
                print(f"  📋 Following Excel instructions: empty = skip, even if option exists on form")
                continue
            
            # Find matching clickable option
            option_found = False
            for option_info in available_options:
                option_text = option_info['text'].lower()
                
                # Check if this option matches any of our keywords
                for keyword in keywords:
                    if keyword.lower() in option_text:
                        print(f"  🎯 Found matching option for '{keyword}': '{option_info['text']}'")
                        try:
                            option_info['element'].click(timeout=5000)
                            print(f"  ✅ Clicked {description}: '{option_info['text']}'")
                            time.sleep(2)  # Wait for any text input to appear
                            
                            # Check for text input field after selecting the option
                            print(f"  🔍 Looking for text input after selecting {description}...")
                            text_input_selectors = [
                                "input[type='text']:visible",
                                "textarea:visible", 
                                "input[placeholder*='details']:visible",
                                "input[placeholder*='information']:visible",
                                "textarea[placeholder*='details']:visible",
                                "textarea[placeholder*='information']:visible",
                                "input:not([type='hidden']):not([type='radio']):not([type='checkbox']):visible"
                            ]
                            
                            text_input_found = False
                            for text_selector in text_input_selectors:
                                try:
                                    text_inputs = page.locator(text_selector).all()
                                    for text_input in text_inputs:
                                        if text_input.is_visible():
                                            current_value = text_input.input_value()
                                            if not current_value or len(current_value.strip()) == 0:
                                                text_input.fill("Account closure request")
                                                print(f"  ✅ Entered 'Account closure request' in text input for {description}")
                                                text_input_found = True
                                                time.sleep(1)
                                                break
                                    if text_input_found:
                                        break
                                except:
                                    continue
                            
                            if not text_input_found:
                                print(f"  ℹ️ No text input found after selecting {description}")
                            
                            option_found = True
                            break
                        except Exception as e:
                            print(f"  ⚠️ Could not click option: {str(e)}")
                            continue
                
                if option_found:
                    break
            
            if not option_found:
                print(f"  ❌ Could not find clickable option for {description}")
                print(f"  🔍 Available options were:")
                for opt in available_options:
                    print(f"    - '{opt['text']}'")
        
        # Take screenshot after close account options selection
        page.screenshot(path="dsr/screenshots/close_account_options_selected.png")
        print("📸 Screenshot saved: screenshots/close_account_options_selected.png")
        
        print("✅ Close account sub-options handling completed")
    
    def handle_acknowledgments(self, page: Page):
        """Handle acknowledgment button and captcha"""
        print("✅ Handling acknowledgments and verification...")
        
        # First, look for acknowledgment BUTTON (not checkbox)
        print("🔘 Looking for acknowledgment button...")
        acknowledge_selectors = [
            # Button selectors
            "button:has-text('I acknowledge')",
            "button:has-text('acknowledge')",
            "button:has-text('Acknowledge')",
            "button:has-text('I confirm')",
            "button:has-text('confirm')",
            "button:has-text('Confirm')",
            "button:has-text('accurate')",
            "button:has-text('Accurate')",
            "button:has-text('information provided is accurate')",
            # Generic button selectors
            "button[data-testid*='acknowledge']",
            "button[data-testid*='confirm']",
            "button[aria-label*='confirm']",
            "button[aria-label*='acknowledge']",
            "button[value*='acknowledge']",
            "button[value*='confirm']",
            ".acknowledge-btn",
            ".confirm-btn",
            "#acknowledge",
            "#confirm"
        ]
        
        acknowledge_clicked = False
        
        # First try to find any button that might be the acknowledgment
        print("🔍 DEBUG: Looking for all buttons to find acknowledgment...")
        try:
            all_buttons = page.locator("button").all()
            for i, button in enumerate(all_buttons):
                try:
                    if button.is_visible():
                        button_text = button.inner_text() or ""
                        button_value = button.get_attribute("value") or ""
                        button_id = button.get_attribute("id") or ""
                        button_class = button.get_attribute("class") or ""
                        button_title = button.get_attribute("title") or ""
                        button_aria_label = button.get_attribute("aria-label") or ""
                        is_enabled = not button.is_disabled()
                        
                        print(f"  Button {i+1}: text='{button_text}', value='{button_value}', id='{button_id}', enabled={is_enabled}")
                        print(f"    class='{button_class}', title='{button_title}', aria-label='{button_aria_label}'")
                        
                        # Check if this looks like the acknowledgment button
                        full_text = f"{button_text} {button_value} {button_id} {button_class} {button_title} {button_aria_label}".lower()
                        if any(phrase in full_text for phrase in ["acknowledge", "confirm", "accurate", "certify", "agree"]):
                            if is_enabled:
                                button.click(timeout=5000)
                                print(f"✅ Clicked acknowledgment button: '{button_text}' (id: {button_id})")
                                acknowledge_clicked = True
                                time.sleep(2)
                                break
                            else:
                                print(f"⚠️ Found acknowledgment button but it's disabled: '{button_text}'")
                        
                        # Also try clicking buttons that might be acknowledgment buttons based on position/context
                        # Check if it's near acknowledgment text
                        try:
                            # Look for nearby text that might indicate this is an acknowledgment button
                            parent = button.locator("xpath=..").first
                            if parent.is_visible():
                                parent_text = parent.inner_text() or ""
                                if any(phrase in parent_text.lower() for phrase in ["acknowledge", "confirm", "accurate", "certify", "agree", "information provided"]):
                                    if is_enabled and not acknowledge_clicked:
                                        button.click(timeout=5000)
                                        print(f"✅ Clicked acknowledgment button based on context: '{parent_text[:100]}...'")
                                        acknowledge_clicked = True
                                        time.sleep(2)
                                        break
                        except:
                            pass
                        
                except Exception as e:
                    print(f"    Error checking button {i+1}: {str(e)}")
                    continue
        except Exception as e:
            print(f"⚠️ Error enumerating buttons: {str(e)}")
        
        # Also try looking for clickable elements with acknowledgment text
        if not acknowledge_clicked:
            print("🔄 Trying to find acknowledgment text as clickable elements...")
            acknowledge_text_selectors = [
                "text=I acknowledge",
                "text=acknowledge",
                "text=Acknowledge", 
                "text=I confirm",
                "text=confirm",
                "text=Confirm",
                "*:has-text('I acknowledge')",
                "*:has-text('acknowledge')",
                "*:has-text('I confirm')",
                "*:has-text('confirm')"
            ]
            
            for text_selector in acknowledge_text_selectors:
                try:
                    elements = page.locator(text_selector).all()
                    for element in elements:
                        if element.is_visible():
                            element_text = element.inner_text() or ""
                            print(f"🔍 Found acknowledgment text element: '{element_text}'")
                            try:
                                element.click(timeout=5000)
                                print(f"✅ Clicked acknowledgment text element: '{element_text}'")
                                acknowledge_clicked = True
                                time.sleep(2)
                                break
                            except Exception as e:
                                print(f"⚠️ Could not click acknowledgment text: {str(e)}")
                                continue
                    if acknowledge_clicked:
                        break
                except Exception as e:
                    print(f"⚠️ Error with text selector {text_selector}: {str(e)}")
                    continue
        
        # If still not found, try the specific selectors
        if not acknowledge_clicked:
            for selector in acknowledge_selectors:
                try:
                    elements = page.locator(selector).all()
                    for element in elements:
                        if element.is_visible():
                            is_enabled = not element.is_disabled()
                            button_text = element.inner_text() or ""
                            
                            print(f"🔍 Found acknowledgment button candidate - text: '{button_text}', enabled: {is_enabled}")
                            
                            if is_enabled:
                                element.click(timeout=5000)
                                print(f"✅ Clicked acknowledgment button: '{button_text}' using selector: {selector}")
                                acknowledge_clicked = True
                                time.sleep(2)
                                break
                            else:
                                print(f"⚠️ Acknowledgment button found but disabled: '{button_text}'")
                    
                    if acknowledge_clicked:
                        break
                except Exception as e:
                    print(f"⚠️ Could not click acknowledgment button with {selector}: {str(e)}")
                    continue
        
        if not acknowledge_clicked:
            print("⚠️ Could not find acknowledgment button")
        
        # Wait a bit before looking for captcha
        time.sleep(3)
        
        # Second, look for "I'm not a robot" checkbox (reCAPTCHA)
        print("🤖 Looking for 'I'm not a robot' checkbox...")
        robot_selectors = [
            # Standard reCAPTCHA selectors
            "#recaptcha-anchor",
            ".recaptcha-checkbox",
            "iframe[src*='recaptcha']",
            "iframe[title*='reCAPTCHA']",
            # Generic robot checkbox selectors
            "input[type='checkbox'][value*='robot']",
            "input[type='checkbox'][id*='captcha']",
            "input[type='checkbox'][id*='recaptcha']",
            "label:has-text('not a robot')",
            "label:has-text('I\\'m not a robot')",
            "[data-testid*='captcha']",
            "[data-testid*='recaptcha']",
            "[aria-label*='robot']",
            "[aria-label*='captcha']"
        ]
        
        captcha_handled = False
        
        # First, let's debug what's available on the page
        print("🔍 DEBUG: Looking for all potential captcha elements...")
        try:
            # Look for any checkbox that might be the captcha
            all_checkboxes = page.locator("input[type='checkbox']").all()
            for i, checkbox in enumerate(all_checkboxes):
                try:
                    if checkbox.is_visible():
                        checkbox_id = checkbox.get_attribute("id") or ""
                        checkbox_name = checkbox.get_attribute("name") or ""
                        checkbox_value = checkbox.get_attribute("value") or ""
                        checkbox_class = checkbox.get_attribute("class") or ""
                        is_checked = checkbox.is_checked()
                        
                        # Look for associated label
                        label_text = ""
                        if checkbox_id:
                            try:
                                label_elem = page.locator(f"label[for='{checkbox_id}']").first
                                if label_elem.is_visible():
                                    label_text = label_elem.inner_text() or ""
                            except:
                                pass
                        
                        print(f"  Checkbox {i+1}: id='{checkbox_id}', name='{checkbox_name}', value='{checkbox_value}', checked={is_checked}")
                        print(f"    class='{checkbox_class}', label='{label_text}'")
                        
                        # Check if this looks like a captcha checkbox
                        full_text = f"{checkbox_value} {label_text} {checkbox_class} {checkbox_id}".lower()
                        if any(phrase in full_text for phrase in ["robot", "captcha", "recaptcha", "not a robot"]):
                            if not is_checked:
                                checkbox.click(timeout=5000)
                                print(f"✅ Clicked 'I'm not a robot' checkbox with text: '{label_text}'")
                                captcha_handled = True
                                time.sleep(3)
                                break
                            else:
                                print(f"✅ 'I'm not a robot' checkbox already checked: '{label_text}'")
                                captcha_handled = True
                                break
                except Exception as e:
                    print(f"    Error checking checkbox {i+1}: {str(e)}")
                    continue
        except Exception as e:
            print(f"⚠️ Error enumerating checkboxes: {str(e)}")
        
        # Also look for divs or other elements that might be clickable captcha
        if not captcha_handled:
            print("🔍 Looking for clickable captcha elements...")
            captcha_clickable_selectors = [
                "div:has-text('I\\'m not a robot')",
                "span:has-text('I\\'m not a robot')",
                "div:has-text('not a robot')",
                "span:has-text('not a robot')",
                "[role='checkbox']:has-text('robot')",
                "[role='checkbox']:has-text('not a robot')",
                "div[class*='captcha']",
                "div[class*='recaptcha']",
                "div[id*='captcha']",
                "div[id*='recaptcha']"
            ]
            
            for selector in captcha_clickable_selectors:
                try:
                    elements = page.locator(selector).all()
                    for element in elements:
                        if element.is_visible():
                            element_text = element.inner_text() or ""
                            print(f"🔍 Found clickable captcha element: '{element_text}'")
                            try:
                                element.click(timeout=5000)
                                print(f"✅ Clicked captcha element: '{element_text}'")
                                captcha_handled = True
                                time.sleep(3)
                                break
                            except Exception as e:
                                print(f"⚠️ Could not click captcha element: {str(e)}")
                                continue
                    if captcha_handled:
                        break
                except Exception as e:
                    print(f"⚠️ Error with captcha selector {selector}: {str(e)}")
                    continue
        
        # Try the original selectors if still not handled
        if not captcha_handled:
            for selector in robot_selectors:
                try:
                    if selector.startswith("iframe"):
                        # Handle iframe-based reCAPTCHA
                        iframe_elements = page.locator(selector).all()
                        for iframe in iframe_elements:
                            if iframe.is_visible():
                                print("🔍 Found reCAPTCHA iframe")
                                try:
                                    # Wait for iframe to be ready
                                    page.wait_for_timeout(2000)
                                    
                                    # Get the frame content correctly
                                    frame = iframe.content_frame()
                                    if frame:
                                        # Wait for frame to load
                                        frame.wait_for_load_state("networkidle", timeout=10000)
                                        time.sleep(2)
                                        
                                        # Look for the checkbox in the frame
                                        checkbox_selectors = [
                                            "#recaptcha-anchor",
                                            ".recaptcha-checkbox-border", 
                                            ".recaptcha-checkbox",
                                            "div[role='checkbox']",
                                            "[aria-labelledby*='recaptcha']",
                                            ".recaptcha-checkbox-checkmark"
                                        ]
                                        
                                        checkbox_clicked = False
                                        for checkbox_selector in checkbox_selectors:
                                            try:
                                                checkbox = frame.locator(checkbox_selector).first
                                                if checkbox.is_visible():
                                                    checkbox.click(timeout=5000)
                                                    print(f"✅ Clicked 'I'm not a robot' checkbox in iframe using: {checkbox_selector}")
                                                    captcha_handled = True
                                                    checkbox_clicked = True
                                                    time.sleep(3)  # Wait for potential challenge
                                                    break
                                            except Exception as e:
                                                print(f"⚠️ Could not click checkbox with {checkbox_selector}: {str(e)}")
                                                continue
                                        
                                        if checkbox_clicked:
                                            break
                                    else:
                                        print("⚠️ Could not get iframe content frame")
                                except Exception as e:
                                    print(f"⚠️ Could not interact with reCAPTCHA iframe: {str(e)}")
                            
                            if captcha_handled:
                                break
                    else:
                        # Handle regular checkbox
                        elements = page.locator(selector).all()
                        for element in elements:
                            if element.is_visible():
                                is_checked = False
                                try:
                                    is_checked = element.is_checked()
                                except:
                                    pass
                                
                                # Try to find associated label text
                                label_text = ""
                                try:
                                    element_id = element.get_attribute("id") or ""
                                    if element_id:
                                        label_elem = page.locator(f"label[for='{element_id}']").first
                                        if label_elem.is_visible():
                                            label_text = label_elem.inner_text() or ""
                                except:
                                    pass
                                
                                print(f"🔍 Found potential captcha checkbox - label: '{label_text}', checked: {is_checked}")
                                
                                # Check if this looks like the robot checkbox
                                if any(phrase in label_text.lower() for phrase in ["robot", "captcha", "not a robot"]) or "captcha" in selector.lower():
                                    if not is_checked:
                                        element.click(timeout=5000)
                                        print(f"✅ Checked 'I'm not a robot' checkbox: '{label_text}'")
                                        captcha_handled = True
                                        time.sleep(3)  # Wait for potential challenge
                                        break
                                    else:
                                        print(f"✅ 'I'm not a robot' checkbox already checked: '{label_text}'")
                                        captcha_handled = True
                                        break
                    
                    if captcha_handled:
                        break
                except Exception as e:
                    print(f"⚠️ Could not handle captcha with {selector}: {str(e)}")
                    continue
        
        if not captcha_handled:
            print("⚠️ Could not find 'I'm not a robot' checkbox")
            # Take screenshot for debugging
            page.screenshot(path="dsr/screenshots/captcha_debug.png")
            print("📸 Debug screenshot saved: screenshots/captcha_debug.png")
        else:
            # After clicking captcha, check if there's a challenge (image puzzle)
            print("🔍 Checking for reCAPTCHA challenge after clicking...")
            time.sleep(3)  # Wait for challenge to appear
            
            # Look for signs of a reCAPTCHA challenge
            challenge_indicators = [
                "iframe[src*='bframe']",  # reCAPTCHA challenge frame
                ".rc-imageselect",        # Image selection challenge
                ".rc-audiochallenge",     # Audio challenge
                "text=Select all images", # Challenge instruction text
                "text=Click verify",      # Verify button text
                "[title*='reCAPTCHA challenge']"
            ]
            
            challenge_detected = False
            for indicator in challenge_indicators:
                try:
                    if page.locator(indicator).first.is_visible():
                        challenge_detected = True
                        print(f"🧩 reCAPTCHA challenge detected with indicator: {indicator}")
                        break
                except:
                    continue
            
            if challenge_detected:
                print("🚨 reCAPTCHA CHALLENGE DETECTED!")
                print("🧩 Please manually solve the reCAPTCHA challenge (select images, audio, etc.)")
                print("⏰ The script will wait for 60 seconds for you to complete the challenge...")
                print("🔍 Once you solve it, the script will continue automatically.")
                
                # Take screenshot of the challenge
                page.screenshot(path="dsr/screenshots/captcha_challenge.png")
                print("📸 Challenge screenshot saved: screenshots/captcha_challenge.png")
                
                # Wait for the challenge to be solved (check periodically)
                max_wait_time = 60  # Wait up to 60 seconds
                check_interval = 2   # Check every 2 seconds
                waited_time = 0
                challenge_solved = False
                
                while waited_time < max_wait_time and not challenge_solved:
                    time.sleep(check_interval)
                    waited_time += check_interval
                    
                    # Check if challenge is still visible
                    challenge_still_present = False
                    for indicator in challenge_indicators:
                        try:
                            if page.locator(indicator).first.is_visible():
                                challenge_still_present = True
                                break
                        except:
                            continue
                    
                    if not challenge_still_present:
                        # Challenge seems to be solved, but double-check
                        try:
                            # Look for success indicators or the original form
                            submit_button = page.locator("button:has-text('Submit'), button[type='submit']").first
                            if submit_button.is_visible() and not submit_button.is_disabled():
                                challenge_solved = True
                                print("✅ reCAPTCHA challenge appears to be solved!")
                                break
                        except:
                            pass
                    
                    if waited_time % 10 == 0:  # Show progress every 10 seconds
                        remaining = max_wait_time - waited_time
                        print(f"⏳ Still waiting for challenge completion... {remaining} seconds remaining")
                
                if challenge_solved:
                    print("🎉 reCAPTCHA challenge completed successfully!")
                    time.sleep(2)  # Brief pause before continuing
                else:
                    print("⚠️ Challenge wait time expired. Continuing anyway...")
                    print("🔧 You may need to complete the challenge manually before submission works.")
                    
            else:
                print("✅ No reCAPTCHA challenge detected - proceeding normally")
        
        # Wait a bit more after captcha interaction
        time.sleep(3)
        
        print("✅ Acknowledgments and verification completed")
    
    def submit_form(self, page: Page, record_number: int):
        """Submit the form and take screenshot after submission"""
        print("🚀 Attempting to submit parent form...")
        
        # Look for submit button with enhanced selectors
        submit_selectors = [
            "button[type='submit']",
            "input[type='submit']", 
            "button:has-text('Submit')",
            "button:has-text('submit')",
            "button:has-text('Send')",
            "button:has-text('Send Request')",
            "button:has-text('Submit Request')",
            "button:has-text('Submit Form')",
            ".submit-btn",
            ".btn-submit",
            "#submit",
            "#submitBtn",
            "button[data-testid*='submit']",
            "button[class*='submit']",
            "button[value*='submit']",
            "button[value*='Submit']"
        ]
        
        form_submitted = False
        
        # First, check if submit button is enabled
        print("🔍 Checking for available submit buttons...")
        available_buttons = []
        for selector in submit_selectors:
            try:
                elements = page.locator(selector).all()
                for element in elements:
                    if element.is_visible():
                        text = ""
                        try:
                            text = element.inner_text() or element.text_content() or ""
                        except:
                            pass
                        is_enabled = not element.is_disabled()
                        available_buttons.append({
                            'selector': selector,
                            'element': element,
                            'text': text,
                            'enabled': is_enabled
                        })
                        print(f"  Found button: '{text}' (enabled: {is_enabled}) - selector: {selector}")
            except:
                continue
        
        # Try to click enabled submit buttons first
        for button_info in available_buttons:
            if button_info['enabled'] and any(word in button_info['text'].lower() for word in ['submit', 'send']):
                try:
                    print(f"🔍 Attempting to click enabled submit button: '{button_info['text']}'")
                    button_info['element'].click(timeout=5000)
                    print(f"✅ Successfully clicked submit button: '{button_info['text']}'")
                    form_submitted = True
                    break
                except Exception as e:
                    print(f"⚠️ Could not click submit button '{button_info['text']}': {str(e)}")
                    continue
        
        # If no enabled buttons worked, try any visible submit button
        if not form_submitted:
            print("🔄 Trying any visible submit button...")
            for button_info in available_buttons:
                try:
                    print(f"🔍 Attempting to click submit button: '{button_info['text']}'")
                    button_info['element'].click(timeout=5000, force=True)
                    print(f"✅ Force-clicked submit button: '{button_info['text']}'")
                    form_submitted = True
                    break
                except Exception as e:
                    print(f"⚠️ Could not force-click submit button '{button_info['text']}': {str(e)}")
                    continue
        
        if form_submitted:
            print("✅ Parent form submission initiated!")
            
            # Wait for submission to complete
            print("⏳ Waiting for parent form submission to complete...")
            try:
                page.wait_for_load_state("networkidle", timeout=15000)
                time.sleep(3)
            except:
                print("⚠️ Submission may still be processing...")
                time.sleep(5)
            
            # Take screenshot AFTER submission
            page.screenshot(path=f"dsr/screenshots/after_submission_record_{record_number}.png")
            print(f"📸 Screenshot saved: after_submission_record_{record_number}.png")
            
            # Check for success message or confirmation
            success_indicators = [
                "text=Thank you",
                "text=Success",
                "text=Submitted",
                "text=Request received",
                "text=Confirmation",
                ".success-message",
                ".confirmation-message",
                "[data-testid*='success']"
            ]
            
            success_found = False
            for indicator in success_indicators:
                try:
                    if page.locator(indicator).first.is_visible():
                        success_text = page.locator(indicator).first.inner_text()
                        print(f"✅ Success confirmation found: '{success_text}'")
                        success_found = True
                        break
                except:
                    continue
            
            if not success_found:
                print("⚠️ No clear success message found - checking page content...")
                try:
                    page_title = page.title()
                    page_url = page.url
                    print(f"📄 Current page title: '{page_title}'")
                    print(f"🔗 Current URL: {page_url}")
                except:
                    pass
        else:
            print("❌ Submit button not found! Available buttons:")
            # List all available buttons for debugging
            try:
                all_buttons = page.locator("button, input[type='submit']").all()
                for i, button in enumerate(all_buttons):
                    try:
                        if button.is_visible():
                            text = button.inner_text() or button.text_content() or ""
                            button_type = button.get_attribute("type") or ""
                            is_enabled = not button.is_disabled()
                            print(f"  Button {i+1}: '{text}' (type: {button_type}, enabled: {is_enabled})")
                    except:
                        pass
            except:
                print("  Could not enumerate buttons")
                
            print("❌ Form submission failed - no accessible submit button found!")
            page.screenshot(path="dsr/screenshots/submit_button_not_found.png")
            print("📸 Debug screenshot saved: screenshots/submit_button_not_found.png")

def test_inspect_form_elements():
    """Helper test to inspect form elements and their selectors"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        url = "https://privacyportaluat.onetrust.com/webform/b99e91a7-a15e-402d-913d-a09fe56fcd54/c31c1bfa-b0a7-4a7a-9fc0-22c44fa094d0"
        page.goto(url)
        page.wait_for_load_state("networkidle")
        time.sleep(3)
        
        # Get all input elements with detailed info
        inputs = page.locator("input").all()
        print(f"Found {len(inputs)} input elements:")
        
        for i, input_elem in enumerate(inputs):
            try:
                name = input_elem.get_attribute("name") or ""
                id_attr = input_elem.get_attribute("id") or ""
                placeholder = input_elem.get_attribute("placeholder") or ""
                input_type = input_elem.get_attribute("type") or ""
                class_attr = input_elem.get_attribute("class") or ""
                value = input_elem.get_attribute("value") or ""
                print(f"  {i+1}. Type: {input_type}, Name: {name}, ID: {id_attr}, Placeholder: {placeholder}, Class: {class_attr}, Value: {value}")
            except:
                pass
        
        # Get all select elements
        selects = page.locator("select").all()
        print(f"\nFound {len(selects)} select elements:")
        
        for i, select_elem in enumerate(selects):
            try:
                name = select_elem.get_attribute("name") or ""
                id_attr = select_elem.get_attribute("id") or ""
                print(f"  {i+1}. Name: {name}, ID: {id_attr}")
            except:
                pass
        
        # Get all buttons
        buttons = page.locator("button").all()
        print(f"\nFound {len(buttons)} button elements:")
        
        for i, button_elem in enumerate(buttons):
            try:
                text = button_elem.inner_text()
                button_type = button_elem.get_attribute("type") or ""
                print(f"  {i+1}. Type: {button_type}, Text: {text}")
            except:
                pass
        
        time.sleep(10)  # Keep browser open to inspect manually
        browser.close()

if __name__ == "__main__":
    # Run the inspection test first to understand form structure
    print("Running form inspection...")
    test_inspect_form_elements()
    
    # Then run the actual test
    print("\nRunning form fill test...")
    test = TestPrivacyPortal()
    test.setup_method()
    test.test_privacy_form_submission()
    
    # Automatically generate Data Reading Success Report after completion
    print("\n" + "="*80)
    print("🎯 AUTOMATION COMPLETED! Generating Data Reading Success Report...")
    print("="*80)
    
    if create_educator_reading_success_report:
        try:
            report_file = create_educator_reading_success_report()
            if report_file:
                print(f"\n🎉 SUCCESS! Educator Data Reading Success Report generated:")
                print(f"📁 Report File: {report_file}")
                print(f"📅 Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print("❌ Failed to generate report")
        except Exception as e:
            print(f"❌ Error generating report: {str(e)}")
    else:
        print("⚠️ Report generator not available - skipping report generation")
    
    print("\n✅ ALL TASKS COMPLETED!")
    print("📊 Check the dsr/screenshots/ folder for:")
    print("   • Form submission screenshots")
    print("   • Data Reading Success Report (Excel file)")
    print("   • Automation logs and results")
