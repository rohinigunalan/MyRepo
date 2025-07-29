#!/usr/bin/env python3
"""
Multi-record automation for privacy portal testing

This script processes ALL records from the Excel/CSV file and submits a form for each one.
"""

import pandas as pd
import os
import sys
import time
from playwright.sync_api import sync_playwright, Page

class MultiRecordPrivacyPortal:
    def __init__(self):
        self.url = "https://privacyportaluat.onetrust.com/webform/b99e91a7-a15e-402d-913d-a09fe56fcd54/c31c1bfa-b0a7-4a7a-9fc0-22c44fa094d0"
        self.all_records = []
        
    def load_all_records(self):
        """Load all records from Excel/CSV file"""
        excel_file = 'form_data.xlsx'
        csv_file = 'form_data.csv'
        
        try:
            print("📂 Loading all records from data file...")
            
            # Try Excel first, then CSV as fallback
            if os.path.exists(excel_file):
                try:
                    print(f"📊 Attempting to read data from {excel_file}")
                    df = pd.read_excel(excel_file, engine='openpyxl')
                    print("✅ Excel file loaded successfully!")
                except Exception as excel_error:
                    print(f"⚠️  Excel file error: {excel_error}")
                    print("🔄 Trying CSV file as fallback...")
                    if os.path.exists(csv_file):
                        df = pd.read_csv(csv_file, keep_default_na=False, na_values=[''])
                        print("✅ CSV file loaded successfully!")
                    else:
                        raise FileNotFoundError("Neither Excel nor CSV file could be loaded")
            elif os.path.exists(csv_file):
                print(f"📊 Reading data from {csv_file}")
                df = pd.read_csv(csv_file, keep_default_na=False, na_values=[''])
                print("✅ CSV file loaded successfully!")
            else:
                raise FileNotFoundError("No form_data.xlsx or form_data.csv file found")
            
            # Get all rows of data
            if len(df) == 0:
                raise ValueError("No data found in the file")
            
            print(f"📊 Found {len(df)} record(s) to process")
            
            # Convert all rows to dictionaries
            for i in range(len(df)):
                record = df.iloc[i].to_dict()
                self.all_records.append(record)
                print(f"✅ Loaded Record {i+1}: {record.get('First_Name', 'Unknown')} {record.get('Last_Name', 'Unknown')} ({record.get('Email Address', 'No Email')})")
            
            return self.all_records
            
        except Exception as e:
            print(f"❌ Error loading records: {str(e)}")
            return []

    def run_automation_for_record(self, record_num, record_data):
        """Run automation for a single record"""
        print(f"\n{'='*60}")
        print(f"🚀 PROCESSING RECORD {record_num}")
        print(f"👤 Name: {record_data.get('First_Name', 'N/A')} {record_data.get('Last_Name', 'N/A')}")
        print(f"📧 Email: {record_data.get('Email Address', 'N/A')}")
        print(f"🏠 State: {record_data.get('stateOrProvince', 'N/A')}")
        print(f"📋 Request: {record_data.get('Request_type', 'N/A')}")
        print(f"{'='*60}")
        
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=False, slow_mo=500)
            page = browser.new_page()
            
            try:
                # Go to the form
                print(f"🌐 Navigating to privacy portal for Record {record_num}...")
                page.goto(self.url)
                page.wait_for_load_state('networkidle')
                
                # Fill the form using the existing logic but with this record's data
                self.fill_form_for_record(page, record_data, record_num)
                
                # Take final screenshot
                page.screenshot(path=f"screenshots/record_{record_num}_complete.png")
                print(f"📸 Screenshot saved: screenshots/record_{record_num}_complete.png")
                
                print(f"✅ Record {record_num} automation completed successfully!")
                
            except Exception as e:
                print(f"❌ Error processing Record {record_num}: {str(e)}")
                page.screenshot(path=f"screenshots/record_{record_num}_error.png")
                
            finally:
                print(f"⏸️ Keeping browser open for 5 seconds to review Record {record_num}...")
                time.sleep(5)
                browser.close()

    def fill_form_for_record(self, page: Page, form_data: dict, record_num: int):
        """Fill form for a specific record"""
        # Click "Myself" 
        page.click("button:has-text('Myself')")
        time.sleep(2)
        
        # Fill basic info
        page.fill("input[name='emailAddress']", form_data.get('Email Address', ''))
        page.fill("input[name='firstName']", form_data.get('First_Name', ''))
        page.fill("input[name='lastName']", form_data.get('Last_Name', ''))
        page.fill("input[name='birthDate']", form_data.get('birthDate', ''))
        page.fill("input[name='phone']", form_data.get('phone', ''))
        
        # Fill address info
        page.fill("input[name='postalCode']", form_data.get('postalCode', ''))
        page.fill("input[name='city']", form_data.get('city', ''))
        page.fill("input[name='streetAddress']", form_data.get('streetAddress', ''))
        
        # Fill school info
        page.fill("input[name='studentSchoolName']", form_data.get('studentSchoolName', ''))
        page.fill("input[name='studentGraduationYear']", str(form_data.get('studentGraduationYear', '')))
        page.fill("input[name='educatorSchoolAffiliation']", form_data.get('educatorSchoolAffiliation', 'N/A'))
        
        # Select state
        self.select_state(page, form_data.get('stateOrProvince', ''))
        
        # Select request type and handle delete options
        self.handle_request_type_and_delete_options(page, form_data, record_num)
        
        # Handle acknowledgments
        self.handle_acknowledgments(page)
        
        # Submit form
        time.sleep(3)
        page.click("button:has-text('Submit')")
        time.sleep(5)

    def select_state(self, page: Page, state_name: str):
        """Select state from dropdown"""
        print(f"🏠 Selecting state: {state_name}")
        try:
            # Click state dropdown
            page.click("select[name='stateOrProvince']")
            time.sleep(1)
            
            # Select the state option
            page.select_option("select[name='stateOrProvince']", label=state_name)
            print(f"✅ Selected state: {state_name}")
        except Exception as e:
            print(f"⚠️ Error selecting state: {str(e)}")

    def handle_request_type_and_delete_options(self, page: Page, form_data: dict, record_num: int):
        """Handle request type selection and delete options"""
        request_type = form_data.get('Request_type', '')
        print(f"📋 Selecting request type: {request_type}")
        
        # Select request type
        try:
            page.click(f"text={request_type}")
            time.sleep(3)
            print(f"✅ Selected request type: {request_type}")
        except:
            print(f"⚠️ Could not find exact request type, trying alternatives...")
        
        # If delete request, handle delete options
        if 'delete' in request_type.lower():
            self.handle_delete_options(page, form_data, record_num)

    def handle_delete_options(self, page: Page, form_data: dict, record_num: int):
        """Handle delete data sub-options"""
        print(f"🗑️ Handling delete options for Record {record_num}...")
        
        delete_student = str(form_data.get('delete_student', '')).strip()
        delete_parent = str(form_data.get('delete_parent', '')).strip()
        delete_educator = str(form_data.get('delete_educator', '')).strip()
        
        print(f"  Student: '{delete_student}'")
        print(f"  Parent: '{delete_parent}'")
        print(f"  Educator: '{delete_educator}'")
        
        # Select options based on data
        if delete_student and delete_student.lower() not in ['nan', '', 'no']:
            try:
                page.click("text=Student data (if any)")
                time.sleep(1)
                # Enter text if input appears
                if page.locator("input[type='text']:visible").count() > 0:
                    page.fill("input[type='text']:visible", "test DSR")
                print("✅ Selected Student data option")
            except:
                print("⚠️ Could not select Student data option")
        
        if delete_parent and delete_parent.lower() not in ['nan', '', 'no']:
            try:
                page.click("text=Parent data (if any)")
                time.sleep(1)
                # Enter text if input appears
                if page.locator("input[type='text']:visible").count() > 0:
                    page.fill("input[type='text']:visible", "test DSR")
                print("✅ Selected Parent data option")
            except:
                print("⚠️ Could not select Parent data option")
        
        if delete_educator and delete_educator.lower() not in ['nan', '', 'no']:
            try:
                page.click("text=Educator data (if any)")
                time.sleep(1)
                # Enter text if input appears
                if page.locator("input[type='text']:visible").count() > 0:
                    page.fill("input[type='text']:visible", "test DSR")
                print("✅ Selected Educator data option")
            except:
                print("⚠️ Could not select Educator data option")

    def handle_acknowledgments(self, page: Page):
        """Handle acknowledgment checkboxes"""
        print("✅ Handling acknowledgments...")
        try:
            # Check acknowledgment boxes
            checkboxes = page.locator("input[type='checkbox']").all()
            for checkbox in checkboxes:
                if checkbox.is_visible():
                    checkbox.check()
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Error with acknowledgments: {str(e)}")

    def run_all_records(self):
        """Run automation for all records"""
        print("🚀 MULTI-RECORD PRIVACY PORTAL AUTOMATION")
        print("=" * 60)
        
        # Load all records
        records = self.load_all_records()
        
        if not records:
            print("❌ No records found to process!")
            return
        
        print(f"\n🎯 Will process {len(records)} record(s)")
        
        # Process each record
        for i, record in enumerate(records, 1):
            print(f"\n⏰ Starting Record {i} in 3 seconds...")
            time.sleep(3)
            
            self.run_automation_for_record(i, record)
            
            if i < len(records):
                print(f"\n⏳ Waiting 5 seconds before processing next record...")
                time.sleep(5)
        
        print(f"\n🎉 ALL {len(records)} RECORDS COMPLETED!")
        print("📸 Check the screenshots/ folder for results from each record")

if __name__ == "__main__":
    automation = MultiRecordPrivacyPortal()
    automation.run_all_records()
