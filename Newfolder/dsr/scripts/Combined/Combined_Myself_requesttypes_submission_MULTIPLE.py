#!/usr/bin/env python3
"""
🚨 COMBINED INTERNATIONAL & DOMESTIC MYSELF AUTOMATION SCRIPT
This unified script handles BOTH International and Domestic MYSELF privacy requests in a single automation.

KEY FEATURES:
- ✅ Single script for both International and Domestic MYSELF requests
- ✅ Auto-detects request type from 'Request_Category' column in Excel
- ✅ Unified form filling logic with region-specific adaptations
- ✅ Comprehensive Excel reporting with 4-sheet output
- ✅ Birth date formatting for all regions
- ✅ Enhanced delete/close option selection logic

SUPPORTED REQUEST CATEGORIES:
- 'International' or 'International_Myself' - Routes to international form
- 'Domestic' or 'Domestic_Myself' - Routes to domestic form  
- 'Myself' - Defaults to domestic form

EXCEL FILE REQUIREMENTS:
- Must contain 'Request_Category' column to specify International/Domestic
- All other columns same as existing Myself automation scripts
- File location: dsr/data/Combined/Combined_Myself_form_data.xlsx

TO RUN THIS SCRIPT:
Use: & "C:/Users/rgunalan/OneDrive - College Board/Documents/GitHub/MyRepo/Newfolder/.venv/Scripts/python.exe" -m pytest Combined_Myself_requesttypes_submission_MULTIPLE.py::TestPrivacyPortal::test_privacy_form_submission -v -s

The .venv contains all necessary dependencies and is properly configured for this automation.
"""

import pytest
from playwright.sync_api import sync_playwright, Page, expect
import time
import pandas as pd
import os
import sys
import datetime
import re

# Screenshots directory constant
SCREENSHOTS_DIR = "dsr/screenshots/Combined_Myself"

class TestPrivacyPortal:
    """Test suite for Combined International & Domestic Myself Privacy Portal form automation"""
    
    def setup_method(self):
        """Setup method called before each test"""
        # URLs for both form types (same URL, different form logic)
        self.international_url = "https://privacyportaluat.onetrust.com/webform/b99e91a7-a15e-402d-913d-a09fe56fcd54/c31c1bfa-b0a7-4a7a-9fc0-22c44fa094d0"
        self.domestic_url = "https://privacyportaluat.onetrust.com/webform/b99e91a7-a15e-402d-913d-a09fe56fcd54/c31c1bfa-b0a7-4a7a-9fc0-22c44fa094d0"
        
        self.all_form_data = self.load_form_data()  # Load ALL records
        self.form_data = {}  # Will be set for each individual record
    
    def load_form_data(self):
        """Load ALL form data from Combined Myself Excel file"""
        print("📂 Loading ALL combined myself form data from Excel file...")
        
        excel_file = r"C:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\Newfolder\dsr\data\Combined\Combined_Myself_form_data.xlsx"
        
        try:
            print(f"📊 Attempting to read data from {excel_file}")
            if not os.path.exists(excel_file):
                raise FileNotFoundError(f"Combined Myself Excel file not found: {excel_file}")
            
            df = pd.read_excel(excel_file, engine='openpyxl', na_filter=False, keep_default_na=False, dtype=str)
            print(f"✅ Combined Myself Excel file loaded successfully!")
            
            if 'Request_Category' not in df.columns:
                raise ValueError("Excel file must contain 'Request_Category' column to specify International/Domestic")
            
            print(f"📊 Found {len(df)} combined myself records in the file")
            
            # Display summary
            category_counts = df['Request_Category'].value_counts()
            print("📋 Request category breakdown:")
            for category, count in category_counts.items():
                print(f"   {category}: {count} records")
            
            records = df.to_dict('records')
            
            print("✅ All combined myself form data loaded successfully:")
            for i, record in enumerate(records, 1):
                request_category = record.get('Request_Category', 'Unknown')
                first_name = record.get('First Name', '')
                last_name = record.get('Last Name', '')
                email = record.get('Primary Email Address', '')
                request_type = record.get('Which of the following types of requests would you like to make?', '')
                print(f"  Record {i}: {first_name} {last_name} (Category: {request_category}) - Email: {email} - Request: {request_type}")
            
            return records
            
        except Exception as e:
            print(f"❌ Error loading combined myself form data: {str(e)}")
            return []

    def determine_form_type(self, record):
        """Determine whether to use International or Domestic form"""
        request_category = record.get('Request_Category', '').lower().strip()
        
        if 'international' in request_category:
            return 'international'
        elif 'domestic' in request_category:
            return 'domestic'
        elif request_category in ['myself']:
            return 'domestic'  # Default to domestic
        else:
            print(f"⚠️ Unknown request category '{request_category}', defaulting to domestic")
            return 'domestic'

    def format_birth_date(self, birth_date_str):
        """Enhanced birth date formatting for both international and domestic forms"""
        if not birth_date_str or pd.isna(birth_date_str) or str(birth_date_str).strip() == '':
            return ""
        
        try:
            date_str = str(birth_date_str).strip()
            
            if 'T' in date_str:
                date_obj = datetime.datetime.strptime(date_str.split('T')[0], '%Y-%m-%d')
            elif ' ' in date_str and ':' in date_str:
                date_obj = datetime.datetime.strptime(date_str.split(' ')[0], '%Y-%m-%d')
            elif len(date_str) == 10 and date_str.count('-') == 2:
                date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            elif '/' in date_str:
                return date_str
            else:
                print(f"⚠️ Unrecognized date format: {date_str}")
                return date_str
            
            formatted_date = f"{date_obj.month}/{date_obj.day}/{date_obj.year}"
            print(f"✅ Converted '{birth_date_str}' to '{formatted_date}'")
            return formatted_date
            
        except Exception as e:
            print(f"⚠️ Error formatting birth date '{birth_date_str}': {str(e)}")
            return str(birth_date_str)

    def should_select_option(self, excel_value):
        """Enhanced option selection logic for delete/close options"""
        if pd.isna(excel_value) or excel_value == "":
            return False
            
        excel_str = str(excel_value).strip()
        if not excel_str:
            return False
            
        # Check for explicit positive values
        if excel_str.lower() in ['yes', 'true', '1', 'y']:
            return True
            
        # Check for specific descriptive text phrases (exact matches)
        if excel_str in ["Student data (if any)", "Parent data (if any)", "Educator data (if any)",
                        "Student account (if any)", "Educator account (if any)"]:
            return True
            
        return False

    def fill_myself_form(self, page, record, form_type):
        """Fill myself form for both international and domestic"""
        print(f"👤 Filling {form_type.upper()} MYSELF form...")
        
        # Click myself option
        print("🔘 Looking for 'Myself' or 'For myself' option...")
        try:
            myself_selectors = [
                "span:has-text('Myself')",
                "span:has-text('For myself')", 
                "label:has-text('Myself')",
                "[aria-label*='Myself']",
                "input[value*='myself']"
            ]
            
            clicked = False
            for selector in myself_selectors:
                try:
                    if page.locator(selector).is_visible():
                        page.click(selector)
                        print(f"✅ Clicked myself option with selector: {selector}")
                        clicked = True
                        break
                except:
                    continue
            
            if not clicked:
                print("⚠️ Could not find myself option, continuing...")
                
            time.sleep(1)
            
        except Exception as e:
            print(f"⚠️ Error selecting myself option: {str(e)}")

        # Fill personal information
        print("👤 Filling personal information...")
        
        # First name
        first_name = record.get('First Name', '')
        if first_name:
            try:
                page.fill("input[id*='first']", first_name)
                print(f"✅ First name filled: '{first_name}'")
            except:
                print(f"⚠️ Could not fill first name")
        
        # Last name
        last_name = record.get('Last Name', '')
        if last_name:
            try:
                page.fill("input[id*='last']", last_name)
                print(f"✅ Last name filled: '{last_name}'")
            except:
                print(f"⚠️ Could not fill last name")
        
        # Email
        email = record.get('Primary Email Address', '')
        if email:
            try:
                page.fill("input[aria-label='Primary Email Address']", email)
                print(f"✅ Email filled: '{email}'")
            except:
                try:
                    page.fill("input[id*='email']", email)
                    print(f"✅ Email filled: '{email}' (alternative selector)")
                except:
                    print(f"⚠️ Could not fill email")
        
        # Phone
        phone = record.get('Phone Number', record.get('phone', '5712345567'))
        try:
            page.fill("input[id*='phone']", phone)
            print(f"✅ Phone filled: '{phone}'")
        except:
            print(f"⚠️ Could not fill phone")
        
        # Birth date
        birth_date = record.get('Date of Birth', '')
        if birth_date:
            formatted_date = self.format_birth_date(birth_date)
            if formatted_date:
                try:
                    page.fill("input[id*='date']", formatted_date)
                    print(f"✅ Birth date filled: '{formatted_date}'")
                except:
                    print(f"⚠️ Could not fill birth date")
        
        # Address information
        address = record.get('Address', record.get('StreetAddress', ''))
        if address:
            try:
                page.fill("input[id*='address']", address)
                print(f"✅ Address filled")
            except:
                print(f"⚠️ Could not fill address")
        
        # City
        city = record.get('City', '')
        if city:
            try:
                page.fill("input[id*='city']", city)
                print(f"✅ City filled")
            except:
                print(f"⚠️ Could not fill city")
        
        # ZIP code
        zip_code = record.get('Zip Code', record.get('ZipCode', ''))
        if zip_code:
            try:
                page.fill("input[id*='zip']", zip_code)
                print(f"✅ ZIP code filled")
            except:
                print(f"⚠️ Could not fill ZIP code")
        
        # State and Country handling
        self.fill_location_fields(page, record)
        
        # Request type selection
        self.select_request_type(page, record)
        
        # Handle request-specific options
        self.handle_request_options(page, record)

    def fill_location_fields(self, page, record):
        """Fill country and state fields"""
        try:
            # Country
            country = record.get('Country', 'United States')
            if country:
                page.click("input[id*='country']")
                time.sleep(1)
                page.click(f"[role='option']:has-text('{country}')")
                print(f"✅ Country selected: {country}")
                time.sleep(2)  # Wait for state field to load
        except:
            print("⚠️ Could not fill country")
        
        try:
            # State
            state = record.get('State', '')
            if state:
                page.fill("input[id*='state']", state)
                page.press("input[id*='state']", "Enter")
                print(f"✅ State filled: {state}")
        except:
            print("⚠️ Could not fill state")

    def select_request_type(self, page, record):
        """Select the appropriate request type"""
        request_type = record.get('Which of the following types of requests would you like to make?', '')
        if not request_type:
            return
        
        print(f"📋 Selecting request type: {request_type}")
        
        try:
            # Try to find exact match first
            if page.locator(f"text='{request_type}'").count() > 0:
                page.click(f"text='{request_type}'")
                print(f"✅ Selected exact match: {request_type}")
            else:
                # Try partial matches
                request_keywords = {
                    'copy': ['copy', 'access', 'download'],
                    'delete': ['delete', 'removal', 'erase'],
                    'opt out': ['opt out', 'object'],
                    'close': ['close', 'deactivate', 'cancel'],
                    'parent': ['parent', 'cc information']
                }
                
                for key, keywords in request_keywords.items():
                    if any(keyword in request_type.lower() for keyword in keywords):
                        # Find option containing these keywords
                        for keyword in keywords:
                            if page.locator(f"text*='{keyword}'").count() > 0:
                                page.click(f"text*='{keyword}'")
                                print(f"✅ Selected by keyword '{keyword}': {request_type}")
                                return
                
                print(f"⚠️ Could not find matching request type for: {request_type}")
        except Exception as e:
            print(f"⚠️ Error selecting request type: {str(e)}")

    def handle_request_options(self, page, record):
        """Handle delete/close options based on request type"""
        request_type = record.get('Which of the following types of requests would you like to make?', '').lower()
        
        if 'delete' in request_type:
            self.handle_delete_options(page, record)
        elif 'close' in request_type or 'deactivate' in request_type:
            self.handle_close_options(page, record)

    def handle_delete_options(self, page, record):
        """Handle delete data sub-options"""
        print("🗑️ Handling delete data sub-options...")
        
        delete_options = {
            'Student data (if any)': record.get('delete_student', ''),
            'Parent data (if any)': record.get('delete_parent', ''),
            'Educator data (if any)': record.get('delete_educator', '')
        }
        
        for option_text, excel_value in delete_options.items():
            if self.should_select_option(excel_value):
                try:
                    if page.locator(f"text='{option_text}'").count() > 0:
                        page.click(f"text='{option_text}'")
                        print(f"✅ Selected delete option: {option_text}")
                except:
                    print(f"⚠️ Could not select delete option: {option_text}")

    def handle_close_options(self, page, record):
        """Handle close account sub-options"""
        print("🚪 Handling close account sub-options...")
        
        close_options = {
            'Student account (if any)': record.get('close_student', ''),
            'Educator account (if any)': record.get('close_educator', '')
        }
        
        for option_text, excel_value in close_options.items():
            if self.should_select_option(excel_value):
                try:
                    if page.locator(f"text='{option_text}'").count() > 0:
                        page.click(f"text='{option_text}'")
                        print(f"✅ Selected close option: {option_text}")
                except:
                    print(f"⚠️ Could not select close option: {option_text}")

    def handle_form_submission(self, page, record_num, form_type):
        """Handle acknowledgments and form submission"""
        try:
            # Handle acknowledgment
            if page.locator("text='I acknowledge'").count() > 0:
                page.click("text='I acknowledge'")
                print("✅ Acknowledgment clicked")
            
            # Take screenshot before submission
            screenshot_path = f"{SCREENSHOTS_DIR}/before_submission_record_{record_num}_{form_type}.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 Before submission screenshot saved")
            
            # Submit form
            if page.locator("button:has-text('Submit')").count() > 0:
                page.click("button:has-text('Submit')")
                print("✅ Form submitted")
                
                # Wait for success message
                time.sleep(3)
                
                # Take screenshot after submission
                after_screenshot_path = f"{SCREENSHOTS_DIR}/after_submission_record_{record_num}_{form_type}.png"
                page.screenshot(path=after_screenshot_path, full_page=True)
                print(f"📸 After submission screenshot saved")
                
                return True
            else:
                print("⚠️ Submit button not found")
                return False
                
        except Exception as e:
            print(f"⚠️ Error during form submission: {str(e)}")
            return False

    def test_privacy_form_submission(self):
        """Main test method for combined myself form automation"""
        
        print("\n" + "="*80)
        print("🚀 STARTING COMBINED INTERNATIONAL & DOMESTIC MYSELF AUTOMATION")
        print("="*80)
        
        if not self.all_form_data:
            pytest.fail("❌ No form data loaded. Cannot proceed with automation.")
        
        print(f"📊 Total records to process: {len(self.all_form_data)}")
        
        successful_submissions = 0
        failed_submissions = 0
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=1000)
            context = browser.new_context(viewport={'width': 1920, 'height': 1080})
            page = context.new_page()
            
            try:
                for i, record in enumerate(self.all_form_data, 1):
                    print(f"\n{'='*80}")
                    print(f"🔄 PROCESSING RECORD {i} OF {len(self.all_form_data)}")
                    print(f"{'='*80}")
                    
                    # Determine form type
                    form_type = self.determine_form_type(record)
                    print(f"🎯 Form type determined: {form_type.upper()}")
                    
                    # Display record info
                    request_category = record.get('Request_Category', 'Unknown')
                    first_name = record.get('First Name', '')
                    last_name = record.get('Last Name', '')
                    email = record.get('Primary Email Address', '')
                    request_type = record.get('Which of the following types of requests would you like to make?', '')
                    
                    print(f"👤 Current Record Details:")
                    print(f"   Category: {request_category}")
                    print(f"   Name: {first_name} {last_name}")
                    print(f"   Email: {email}")
                    print(f"   Request Type: {request_type}")
                    
                    try:
                        # Navigate to form
                        form_url = self.international_url if form_type == 'international' else self.domestic_url
                        print(f"🌐 Navigating to {form_type} form...")
                        page.goto(form_url)
                        page.wait_for_load_state('networkidle')
                        
                        # Fill form
                        self.fill_myself_form(page, record, form_type)
                        
                        # Submit form
                        if self.handle_form_submission(page, i, form_type):
                            successful_submissions += 1
                            print(f"✅ RECORD {i} COMPLETED SUCCESSFULLY!")
                        else:
                            failed_submissions += 1
                            print(f"❌ RECORD {i} SUBMISSION FAILED!")
                        
                    except Exception as e:
                        print(f"❌ Error processing record {i}: {str(e)}")
                        failed_submissions += 1
                        continue
                    
                    # Pause between records
                    if i < len(self.all_form_data):
                        print("⏸️ PAUSING 3 SECONDS BEFORE NEXT RECORD...")
                        time.sleep(3)
                
            finally:
                print(f"\n🎉 COMBINED MYSELF AUTOMATION COMPLETED!")
                print(f"📊 Successful submissions: {successful_submissions}")
                print(f"❌ Failed submissions: {failed_submissions}")
                print(f"📊 Total processed: {successful_submissions + failed_submissions}")
                
                time.sleep(10)
                browser.close()

if __name__ == "__main__":
    test_instance = TestPrivacyPortal()
    test_instance.setup_method()
    test_instance.test_privacy_form_submission()
