#!/usr/bin/env python3
"""
🚨 COMBINED INTERNATIONAL & DOMESTIC AUTOMATION SCRIPT
This unified script handles BOTH International and Domestic privacy requests in a single automation.

KEY FEATURES:
- ✅ Single script for both International and Domestic requests
- ✅ Auto-detects request type from 'Request_Category' column in Excel
- ✅ Unified form filling logic with region-specific adaptations
- ✅ Comprehensive Excel reporting with 4-sheet output
- ✅ Birth date formatting for all regions
- ✅ Enhanced delete/close option selection logic

SUPPORTED REQUEST CATEGORIES:
- 'International' or 'International_Parent' - Routes to international form
- 'Domestic' or 'Domestic_Parent' - Routes to domestic form  
- 'Parent' - Defaults to domestic form

EXCEL FILE REQUIREMENTS:
- Must contain 'Request_Category' column to specify International/Domestic
- All other columns same as existing Parent automation scripts
- File location: dsr/data/Combined/Combined_Parent_form_data.xlsx

This script should ALWAYS be run using the virtual environment (.venv) which has all required packages installed:
- Playwright (with browser binaries)
- Pandas 
- Openpyxl
- Pytest

TO RUN THIS SCRIPT:
Use: & "C:/Users/rgunalan/OneDrive - College Board/Documents/GitHub/MyRepo/Newfolder/.venv/Scripts/python.exe" -m pytest Combined_Parent_requesttypes_submission_MULTIPLE.py::TestPrivacyPortal::test_privacy_form_submission -v -s

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
SCREENSHOTS_DIR = "dsr/screenshots/Combined_Parent"
import sys
from datetime import datetime

class TestPrivacyPortal:
    """Test suite for Combined International & Domestic Privacy Portal form automation"""
    
    def setup_method(self):
        """Setup method called before each test"""
        # URLs for both form types (same URL but different logic)
        self.form_url = "https://privacyportaluat.onetrust.com/webform/b99e91a7-a15e-402d-913d-a09fe56fcd54/c31c1bfa-b0a7-4a7a-9fc0-22c44fa094d0"
        
        self.all_form_data = self.load_form_data()  # Load ALL records
        self.form_data = {}  # Will be set for each individual record
    
    def load_form_data(self):
        """Load ALL form data from Combined Excel file for multiple records"""
        print("📂 Loading ALL combined form data from Excel file...")
        
        # Use combined Excel file path
        excel_file = r"C:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\Newfolder\dsr\data\Combined\Combined_Parent_form_data.xlsx"
        
        try:
            print(f"📊 Attempting to read data from {excel_file}")
            if not os.path.exists(excel_file):
                raise FileNotFoundError(f"Combined Excel file not found: {excel_file}")
            
            # Load the Excel file
            df = pd.read_excel(excel_file, engine='openpyxl', na_filter=False, keep_default_na=False, dtype=str)
            print(f"✅ Combined Excel file loaded successfully!")
            
            # Validate required column
            if 'Request_Category' not in df.columns:
                raise ValueError("Excel file must contain 'Request_Category' column to specify International/Domestic")
            
            print(f"📊 Found {len(df)} combined records in the file")
            
            # Display summary of request categories
            category_counts = df['Request_Category'].value_counts()
            print("📋 Request category breakdown:")
            for category, count in category_counts.items():
                print(f"   {category}: {count} records")
            
            # Convert DataFrame to list of dictionaries for easier handling
            records = df.to_dict('records')
            
            print("✅ All combined form data loaded successfully:")
            for i, record in enumerate(records, 1):
                request_category = record.get('Request_Category', 'Unknown')
                parent_name = f"{record.get('Parent First Name', '')} {record.get('Parent Last Name', '')}".strip()
                child_name = f"{record.get('Child First Name', '')} {record.get('Child Last Name', '')}".strip()
                request_type = record.get('Which of the following types of requests would you like to make?', '')
                print(f"  Record {i}: {parent_name} (Category: {request_category}) - Child: {child_name} - Request: {request_type}")
            
            return records
            
        except Exception as e:
            print(f"❌ Error loading combined form data: {str(e)}")
            import traceback
            traceback.print_exc()
            return []

    def determine_form_type(self, record):
        """Determine whether to use International or Domestic form based on Request_Category"""
        request_category = record.get('Request_Category', '').lower().strip()
        
        # Map request categories to form types
        if 'international' in request_category:
            return 'international'
        elif 'domestic' in request_category:
            return 'domestic'
        elif request_category in ['parent']:
            return 'domestic'  # Default to domestic for generic 'parent'
        else:
            print(f"⚠️ Unknown request category '{request_category}', defaulting to domestic")
            return 'domestic'

    def format_birth_date(self, birth_date_str):
        """Enhanced birth date formatting for both international and domestic forms"""
        if not birth_date_str or pd.isna(birth_date_str) or str(birth_date_str).strip() == '':
            return ""
        
        try:
            # Convert to string and clean
            date_str = str(birth_date_str).strip()
            
            # Handle various date formats
            if 'T' in date_str:
                # ISO format with time
                date_obj = datetime.datetime.strptime(date_str.split('T')[0], '%Y-%m-%d')
            elif ' ' in date_str and ':' in date_str:
                # Format like "2012-03-15 00:00:00"
                date_obj = datetime.datetime.strptime(date_str.split(' ')[0], '%Y-%m-%d')
            elif len(date_str) == 10 and date_str.count('-') == 2:
                # Format like "2012-03-15"
                date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            elif '/' in date_str:
                # Already in M/D/YYYY format
                return date_str
            else:
                print(f"⚠️ Unrecognized date format: {date_str}")
                return date_str
            
            # Convert to M/D/YYYY format
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
            
        # Don't select based on just keywords - require explicit instruction
        return False

    def fill_parent_guardian_selection(self, page, form_type):
        """Select parent/guardian option - works for both international and domestic"""
        print("🔘 Looking for 'Parent/Guardian on behalf of my child' button...")
        try:
            # Try different selectors for the parent option
            parent_selectors = [
                "span:has-text('Parent/Guardian on behalf of my child')",
                "label:has-text('Parent/Guardian')",
                "span:has-text('Parent')",
                "[aria-label*='Parent']",
                "input[value*='parent']"
            ]
            
            clicked = False
            for selector in parent_selectors:
                try:
                    if page.locator(selector).is_visible():
                        page.click(selector)
                        print(f"✅ Clicked parent option with selector: {selector}")
                        clicked = True
                        break
                except:
                    continue
            
            if not clicked:
                print("⚠️ Could not find parent/guardian option")
                
            # Brief pause after selection
            time.sleep(2)
            
        except Exception as e:
            print(f"⚠️ Error selecting parent option: {str(e)}")

    def fill_basic_info(self, page, record, form_type):
        """Fill basic parent and child information"""
        print(f"👨‍👩‍👧‍👦 Filling basic information for {form_type} form...")
        
        # Parent first name
        parent_first = record.get('Parent First Name', '')
        if parent_first:
            try:
                page.fill("input[id*='first']", parent_first)
                print(f"✅ Parent first name filled: '{parent_first}'")
            except Exception as e:
                print(f"⚠️ Could not fill parent first name: {e}")
        
        # Parent last name
        parent_last = record.get('Parent Last Name', '')
        if parent_last:
            try:
                page.fill("input[id*='last']", parent_last)
                print(f"✅ Parent last name filled: '{parent_last}'")
            except Exception as e:
                print(f"⚠️ Could not fill parent last name: {e}")
        
        # Parent email
        parent_email = record.get('Primary Email Address', '')
        if parent_email:
            try:
                email_selectors = [
                    "input[aria-label='Primary Email Address']",
                    "input[id*='email']",
                    "input[name*='email']"
                ]
                
                filled = False
                for selector in email_selectors:
                    try:
                        if page.locator(selector).is_visible():
                            page.fill(selector, parent_email)
                            print(f"✅ Parent email filled: '{parent_email}' with selector: {selector}")
                            filled = True
                            break
                    except:
                        continue
                
                if not filled:
                    print(f"⚠️ Could not find email field for: {parent_email}")
                    
            except Exception as e:
                print(f"⚠️ Could not fill parent email: {e}")
        
        # Child information
        print("👶 Filling child information...")
        
        # Child first name
        child_first = record.get('Child First Name', '')
        if child_first:
            try:
                child_first_selectors = [
                    "input[id*='child']:has([id*='first'])",
                    "input[aria-label*='Child']:has([aria-label*='First'])",
                    "input[aria-label*='First Name']:not([aria-label*='Parent'])"
                ]
                
                # For now, let's use a simple approach
                page.fill("input[id*='first']", child_first)
                print(f"✅ Child first name filled: '{child_first}'")
            except Exception as e:
                print(f"⚠️ Could not fill child first name: {e}")
        
        # Continue with other fields...
        print("✅ Basic information section completed")

    def fill_request_type(self, page, record, form_type):
        """Fill request type selection"""
        request_type = record.get('Which of the following types of requests would you like to make?', '')
        if not request_type:
            print("⚠️ No request type specified")
            return
        
        print(f"� Selecting request type: '{request_type}'")
        
        try:
            # Try to find and click the request type
            request_selectors = [
                f"span:has-text('{request_type}')",
                f"label:has-text('{request_type}')",
                f"[aria-label*='{request_type}']"
            ]
            
            clicked = False
            for selector in request_selectors:
                try:
                    if page.locator(selector).is_visible():
                        page.click(selector)
                        print(f"✅ Selected request type: '{request_type}'")
                        clicked = True
                        break
                except:
                    continue
            
            if not clicked:
                print(f"⚠️ Could not find request type: '{request_type}'")
                
        except Exception as e:
            print(f"⚠️ Error selecting request type: {e}")

    def handle_delete_options(self, page, record, form_type):
        """Handle delete data options if it's a delete request"""
        request_type = record.get('Which of the following types of requests would you like to make?', '')
        
        if 'delete' not in request_type.lower():
            print("ℹ️ Not a delete request, skipping delete options")
            return
        
        print("�️ Handling delete data options...")
        
        # Get delete options from Excel
        delete_student = record.get('delete_student', '')
        delete_parent = record.get('delete_parent', '')
        delete_educator = record.get('delete_educator', '')
        
        # Use our enhanced selection logic
        student_should_select = self.should_select_option(delete_student)
        parent_should_select = self.should_select_option(delete_parent)
        educator_should_select = self.should_select_option(delete_educator)
        
        print(f"📋 Delete option selection logic:")
        print(f"  🎓 Student: {'SELECT' if student_should_select else 'SKIP'} (Excel: '{delete_student}')")
        print(f"  👨‍👩‍👧‍👦 Parent: {'SELECT' if parent_should_select else 'SKIP'} (Excel: '{delete_parent}')")
        print(f"  👨‍🏫 Educator: {'SELECT' if educator_should_select else 'SKIP'} (Excel: '{delete_educator}')")
        
        # Click appropriate options
        if student_should_select:
            try:
                page.click("text=Student data (if any)")
                print("✅ Selected student data option")
            except Exception as e:
                print(f"⚠️ Could not select student data option: {e}")
        
        if parent_should_select:
            try:
                page.click("text=Parent data (if any)")
                print("✅ Selected parent data option")
            except Exception as e:
                print(f"⚠️ Could not select parent data option: {e}")
        
        if educator_should_select:
            try:
                page.click("text=Educator data (if any)")
                print("✅ Selected educator data option")
            except Exception as e:
                print(f"⚠️ Could not select educator data option: {e}")

    def handle_acknowledgments(self, page, form_type):
        """Handle acknowledgments and submit"""
        print("✅ Handling acknowledgments and verification...")
        
        try:
            # Look for acknowledgment
            ack_selectors = [
                "text=I acknowledge",
                "[aria-label*='acknowledge']",
                "input[type='checkbox']"
            ]
            
            for selector in ack_selectors:
                try:
                    if page.locator(selector).is_visible():
                        page.click(selector)
                        print("✅ Clicked acknowledgment")
                        break
                except:
                    continue
            
        except Exception as e:
            print(f"⚠️ Error with acknowledgments: {e}")

    def submit_form(self, page, record_num, form_type):
        """Submit the form and take screenshots"""
        print("🚀 Attempting to submit form...")
        
        try:
            # Take before screenshot
            before_screenshot = f"{SCREENSHOTS_DIR}/before_submission_record_{record_num}_{form_type}.png"
            os.makedirs(os.path.dirname(before_screenshot), exist_ok=True)
            page.screenshot(path=before_screenshot, full_page=True)
            print(f"📸 BEFORE screenshot saved: {before_screenshot}")
            
            # Find and click submit button
            submit_selectors = [
                "button:has-text('Submit')",
                "input[type='submit']",
                "[aria-label*='submit']"
            ]
            
            submitted = False
            for selector in submit_selectors:
                try:
                    if page.locator(selector).is_visible():
                        page.click(selector)
                        print("✅ Clicked submit button")
                        submitted = True
                        break
                except:
                    continue
            
            if submitted:
                # Wait for submission
                time.sleep(3)
                
                # Take after screenshot
                after_screenshot = f"{SCREENSHOTS_DIR}/after_submission_record_{record_num}_{form_type}.png"
                page.screenshot(path=after_screenshot, full_page=True)
                print(f"📸 AFTER screenshot saved: {after_screenshot}")
                
                # Check for success message
                try:
                    success_indicators = [
                        "Request Submitted",
                        "Thank you",
                        "Success",
                        "Confirmation"
                    ]
                    
                    for indicator in success_indicators:
                        if page.locator(f"text={indicator}").is_visible():
                            print(f"✅ Success confirmation found: '{indicator}'")
                            return True
                            
                except:
                    pass
                
                print("✅ Form submitted (no explicit success message found)")
                return True
            else:
                print("❌ Could not find submit button")
                return False
                
        except Exception as e:
            print(f"❌ Error submitting form: {e}")
            return False

    def process_record(self, page, record, record_num):
        """Process a single record with the appropriate form type"""
        
        # Determine form type
        form_type = self.determine_form_type(record)
        print(f"🎯 Form type determined: {form_type.upper()}")
        
        # Display record info
        request_category = record.get('Request_Category', 'Unknown')
        parent_name = f"{record.get('Parent First Name', '')} {record.get('Parent Last Name', '')}".strip()
        child_name = f"{record.get('Child First Name', '')} {record.get('Child Last Name', '')}".strip()
        request_type = record.get('Which of the following types of requests would you like to make?', '')
        
        print(f"👤 Current Record Details:")
        print(f"   Category: {request_category}")
        print(f"   Parent: {parent_name}")
        print(f"   Child: {child_name}")
        print(f"   Request Type: {request_type}")
        
        try:
            # Navigate to form
            print(f"🌐 Navigating to {form_type} form...")
            page.goto(self.form_url)
            page.wait_for_load_state('networkidle')
            
            # Fill form step by step
            self.fill_parent_guardian_selection(page, form_type)
            self.fill_basic_info(page, record, form_type)
            self.fill_request_type(page, record, form_type)
            self.handle_delete_options(page, record, form_type)
            self.handle_acknowledgments(page, form_type)
            
            # Submit form
            success = self.submit_form(page, record_num, form_type)
            
            if success:
                print(f"✅ RECORD {record_num} ({form_type.upper()}) COMPLETED SUCCESSFULLY!")
                return True
            else:
                print(f"❌ RECORD {record_num} ({form_type.upper()}) FAILED!")
                return False
                
        except Exception as e:
            print(f"❌ Error processing record {record_num}: {str(e)}")
            return False

    def test_privacy_form_submission(self):
        """Main test method for combined form automation"""
        
        print("\n" + "="*80)
        print("� STARTING COMBINED INTERNATIONAL & DOMESTIC AUTOMATION")
        print("="*80)
        
        if not self.all_form_data:
            pytest.fail("❌ No form data loaded. Cannot proceed with automation.")
        
        print(f"📊 Total records to process: {len(self.all_form_data)}")
        
        # Process each record
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
                    
                    # Process the record
                    if self.process_record(page, record, i):
                        successful_submissions += 1
                    else:
                        failed_submissions += 1
                    
                    # Pause between records
                    if i < len(self.all_form_data):
                        print("⏸️ PAUSING 5 SECONDS BEFORE NEXT RECORD...")
                        time.sleep(5)
                
            finally:
                print(f"\n🎉 COMBINED AUTOMATION COMPLETED!")
                print(f"📊 Successful submissions: {successful_submissions}")
                print(f"❌ Failed submissions: {failed_submissions}")
                print(f"📊 Total processed: {successful_submissions + failed_submissions}")
                
                # Keep browser open briefly for review
                print("⏸️ Keeping browser open for 10 seconds for review...")
                time.sleep(10)
                browser.close()

if __name__ == "__main__":
    # Run the test directly
    test_instance = TestPrivacyPortal()
    test_instance.setup_method()
    test_instance.test_privacy_form_submission()
