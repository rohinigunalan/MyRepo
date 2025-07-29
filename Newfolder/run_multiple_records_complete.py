import pytest
from playwright.sync_api import sync_playwright, Page, expect
import time
import pandas as pd
import os

class TestPrivacyPortalMultiple:
    """Test suite for OneTrust Privacy Portal form automation - Multiple Records"""
    
    def setup_method(self):
        """Setup method called before each test"""
        self.url = "https://privacyportaluat.onetrust.com/webform/b99e91a7-a15e-402d-913d-a09fe56fcd54/c31c1bfa-b0a7-4a7a-9fc0-22c44fa094d0"
        self.form_data = {}  # Will be set for each record

    def load_all_form_data(self):
        """Load ALL form data from Excel or CSV file"""
        print("📂 Loading ALL form data from file...")

        excel_file = "dsr/data/form_data.xlsx"
        csv_file = "form_data.csv"

        try:
            if os.path.exists(excel_file):
                print(f"📊 Attempting to read data from {excel_file}")
                df = pd.read_excel(excel_file, engine='openpyxl', na_filter=False, keep_default_na=False, dtype=str)
                print("✅ Excel file loaded successfully!")
            elif os.path.exists(csv_file):
                print(f"📊 Reading data from {csv_file}")
                df = pd.read_csv(csv_file, keep_default_na=False, na_values=[''])
                print("✅ CSV file loaded successfully!")
            else:
                raise FileNotFoundError("No form_data.xlsx or form_data.csv file found")

            if len(df) == 0:
                raise ValueError("No data found in the file")

            print(f"📊 Found {len(df)} records in the file")
            return df.to_dict(orient='records')  # Return all records as list of dictionaries

        except Exception as e:
            print(f"❌ Error loading form data: {str(e)}")
            print("📝 Using default fallback data...")
            return [{
                'Email Address': 'test1@mailinator.com',
                'First_Name': 'Test1',
                'Last_Name': 'User1',
                'birthDate': '11/1/2003',
                'phone': '5712345567',
                'country': 'US',
                'stateOrProvince': 'New York',
                'postalCode': '14111',
                'city': 'North Collins',
                'streetAddress': '507 Central Avenue',
                'studentSchoolName': 'N/A',
                'studentGraduationYear': 'N/A',
                'educatorSchoolAffiliation': 'N/A',
                'Request_type': 'Request a copy of my data'
            }]

    def test_multiple_privacy_form_submissions(self):
        """Test filling and submitting the privacy portal form for ALL records"""
        print("🚨 IMPORTANT NOTE: This script will automate form filling for ALL records in the Excel file.")
        print("   You may need to manually solve reCAPTCHA challenges if they appear.")
        print("   Please stay near your computer to help with reCAPTCHA if needed!\n")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            try:
                # Load all records
                all_records = self.load_all_form_data()
                print(f"\n🎯 Processing {len(all_records)} records from Excel file...")

                for index, record in enumerate(all_records):
                    print(f"\n{'='*60}")
                    print(f"🔄 PROCESSING RECORD {index + 1} of {len(all_records)}")
                    print(f"{'='*60}")
                    
                    # Set current record data
                    self.form_data = record
                    
                    # Display current record info
                    print(f"👤 Current Record Details:")
                    print(f"   Name: {record.get('First_Name', 'N/A')} {record.get('Last_Name', 'N/A')}")
                    print(f"   Email: {record.get('Email Address', 'N/A')}")
                    print(f"   Request Type: {record.get('Request_type', 'N/A')}")
                    print(f"   State: {record.get('stateOrProvince', 'N/A')}")

                    try:
                        # Navigate to the privacy portal for each record
                        print(f"\n🌐 Navigating to form for record {index + 1}...")
                        page.goto(self.url)
                        page.wait_for_load_state("networkidle")
                        time.sleep(3)

                        # Fill and submit the form for the current record
                        print(f"\n🎯 Starting form automation for record {index + 1}...")
                        
                        self.fill_subject_information(page)
                        self.fill_contact_information(page)
                        self.fill_additional_details(page)
                        self.select_request_type(page)
                        self.handle_delete_data_suboptions(page)
                        self.handle_acknowledgments(page)
                        
                        # Take screenshot before submission
                        screenshot_path = f"dsr/screenshots/record_{index + 1}_before_submit.png"
                        try:
                            page.screenshot(path=screenshot_path)
                            print(f"📸 Screenshot saved: {screenshot_path}")
                        except:
                            print("⚠️ Could not save before-submit screenshot")
                        
                        # Submit form
                        submission_success = self.submit_form(page)
                        
                        # Take screenshot after submission
                        if submission_success:
                            screenshot_path = f"dsr/screenshots/record_{index + 1}_after_submit.png"
                            try:
                                page.screenshot(path=screenshot_path)
                                print(f"📸 Screenshot saved: {screenshot_path}")
                            except:
                                print("⚠️ Could not save after-submit screenshot")
                        
                        print(f"✅ Record {index + 1} processed successfully!")

                    except Exception as e:
                        print(f"❌ Error processing record {index + 1}: {str(e)}")
                        try:
                            error_screenshot = f"dsr/screenshots/error_record_{index + 1}.png"
                            page.screenshot(path=error_screenshot)
                            print(f"📸 Error screenshot saved: {error_screenshot}")
                        except:
                            print("⚠️ Could not save error screenshot")
                        
                        # Continue with next record instead of stopping
                        print(f"⏭️ Continuing with next record...")

                    # Pause between records
                    if index < len(all_records) - 1:  # Don't pause after last record
                        print(f"\n⏸️ Pausing 5 seconds before processing next record...")
                        time.sleep(5)

                print(f"\n🎉 ALL {len(all_records)} RECORDS PROCESSED!")
                print("✅ Multiple record automation completed successfully!")

            except Exception as e:
                print(f"❌ Major error occurred: {str(e)}")
                raise

            finally:
                print("\n⏸️ Keeping browser open for 10 seconds to review final state...")
                time.sleep(10)
                browser.close()

    def fill_subject_information(self, page: Page):
        """Fill subject information section"""
        print("📝 Filling subject information...")
        
        # Click "Myself" button
        myself_selectors = [
            "span:has-text('Myself')",
            "button:has-text('Myself')",
            "label:has-text('Myself')",
            "div:has-text('Myself')",
            "[data-value='myself']"
        ]
        
        for selector in myself_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.click(selector)
                    print(f"✅ Clicked 'Myself' button")
                    time.sleep(2)
                    break
            except:
                continue
        
        # Fill First Name
        first_name_selectors = ["input[id*='first']", "input[name*='firstName']", "input[placeholder*='First']"]
        for selector in first_name_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.fill(selector, str(self.form_data.get('First_Name', 'Test')))
                    print(f"✅ First name filled")
                    break
            except:
                continue
                
        # Fill Last Name
        last_name_selectors = ["input[id*='last']", "input[name*='lastName']", "input[placeholder*='Last']"]
        for selector in last_name_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.fill(selector, str(self.form_data.get('Last_Name', 'User')))
                    print(f"✅ Last name filled")
                    break
            except:
                continue
            
        # Fill Email
        email_selectors = ["input[type='email']", "input[id*='email']", "input[name*='email']"]
        for selector in email_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.fill(selector, str(self.form_data.get('Email Address', 'test@mailinator.com')))
                    print(f"✅ Email filled")
                    break
            except:
                continue
            
        # Fill Phone
        phone_selectors = ["input[id*='phone']", "input[name*='phone']", "input[type='tel']"]
        for selector in phone_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.fill(selector, str(self.form_data.get('phone', '5712345567')))
                    print(f"✅ Phone filled")
                    break
            except:
                continue
            
        # Fill Birth Date
        birthdate_selectors = ["input[id*='date']", "input[id*='birth']", "input[type='date']"]
        for selector in birthdate_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    birth_date = str(self.form_data.get('birthDate', '11/1/2003'))
                    page.fill(selector, birth_date)
                    print(f"✅ Birth date filled")
                    break
            except:
                continue

    def fill_contact_information(self, page: Page):
        """Fill contact information section"""
        print("📍 Filling contact information...")
        
        # Fill Address
        address_selectors = ["input[id*='address']", "input[name*='address']", "input[placeholder*='Address']"]
        for selector in address_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.fill(selector, str(self.form_data.get('streetAddress', '123 Main St')))
                    print(f"✅ Address filled")
                    break
            except:
                continue
            
        # Fill City
        city_selectors = ["input[id*='city']", "input[name*='city']", "input[placeholder*='City']"]
        for selector in city_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.fill(selector, str(self.form_data.get('city', 'New York')))
                    print(f"✅ City filled")
                    break
            except:
                continue
            
        # Fill ZIP
        zip_selectors = ["input[id*='zip']", "input[name*='zip']", "input[placeholder*='Zip']"]
        for selector in zip_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.fill(selector, str(self.form_data.get('postalCode', '10001')))
                    print(f"✅ ZIP code filled")
                    break
            except:
                continue
        
        # Fill Country (enhanced)
        print("🌍 Filling country field...")
        country_selectors = ["input[id*='country']", "select[id*='country']"]
        for selector in country_selectors:
            try:
                element = page.locator(selector).first
                if element.is_visible():
                    element.click()
                    time.sleep(2)
                    # Try to select United States
                    us_option_selectors = [
                        "[role='option']:has-text('United States')",
                        "option:has-text('United States')",
                        "li:has-text('United States')"
                    ]
                    for us_selector in us_option_selectors:
                        try:
                            page.locator(us_selector).first.click()
                            print(f"✅ Country (United States) selected")
                            time.sleep(3)
                            break
                        except:
                            continue
                    break
            except:
                continue
        
        # Fill State (enhanced)
        print("🗽 Filling state field...")
        state_selectors = ["input[id*='state']", "select[id*='state']"]
        state_name = str(self.form_data.get('stateOrProvince', 'New York'))
        
        for selector in state_selectors:
            try:
                element = page.locator(selector).first
                if element.is_visible():
                    element.click()
                    time.sleep(1)
                    element.fill("")
                    element.type(state_name, delay=100)
                    time.sleep(2)
                    element.press("Enter")
                    print(f"✅ State ({state_name}) filled")
                    time.sleep(2)
                    break
            except:
                continue

    def fill_additional_details(self, page: Page):
        """Fill additional details section"""
        print("📋 Filling additional details...")
        
        # Student School
        school_selectors = ["input[aria-label*='School']", "input[placeholder*='School']", "input[id*='school']"]
        for selector in school_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.fill(selector, str(self.form_data.get('studentSchoolName', 'N/A')))
                    print(f"✅ Student school filled")
                    break
            except:
                continue
        
        # Graduation Year
        grad_selectors = ["input[aria-label*='Graduation']", "input[placeholder*='Graduation']", "input[id*='graduation']"]
        for selector in grad_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.fill(selector, str(self.form_data.get('studentGraduationYear', 'N/A')))
                    print(f"✅ Graduation year filled")
                    break
            except:
                continue
        
        # Educator Affiliation
        educator_selectors = ["input[aria-label*='Educator']", "input[placeholder*='Educator']", "input[id*='educator']"]
        for selector in educator_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.fill(selector, str(self.form_data.get('educatorSchoolAffiliation', 'N/A')))
                    print(f"✅ Educator affiliation filled")
                    break
            except:
                continue

    def select_request_type(self, page: Page):
        """Select request type based on Excel data"""
        print("🎯 Selecting request type...")
        
        request_type = str(self.form_data.get('Request_type', 'Request a copy of my data')).lower()
        print(f"📋 Looking for: {request_type}")
        
        # Enhanced request type selection
        if 'delete' in request_type or 'remove' in request_type:
            # Look for delete-specific text
            delete_selectors = [
                "text=Request to delete my data",
                "button:has-text('delete')",
                "label:has-text('delete')",
                "span:has-text('delete')",
                "*:has-text('Request to delete my data')",
                "*:has-text('delete my data')"
            ]
            
            for selector in delete_selectors:
                try:
                    if page.locator(selector).first.is_visible():
                        page.click(selector)
                        print(f"✅ Selected delete request type")
                        time.sleep(3)
                        return
                except:
                    continue
                    
        elif 'copy' in request_type or 'access' in request_type:
            # Look for copy/access-specific text
            copy_selectors = [
                "text=Request a copy of my data",
                "button:has-text('copy')",
                "label:has-text('copy')",
                "span:has-text('copy')",
                "*:has-text('Request a copy of my data')",
                "*:has-text('copy of my data')"
            ]
            
            for selector in copy_selectors:
                try:
                    if page.locator(selector).first.is_visible():
                        page.click(selector)
                        print(f"✅ Selected copy request type")
                        time.sleep(3)
                        return
                except:
                    continue
        
        # Fallback - try any radio button or clickable element with relevant text
        fallback_selectors = [
            "input[type='radio']",
            "button[role='radio']",
            "[role='button']",
            "label"
        ]
        
        for selector in fallback_selectors:
            try:
                elements = page.locator(selector).all()
                for element in elements:
                    if element.is_visible():
                        text = element.text_content().lower()
                        if any(word in text for word in ['delete', 'copy', 'access', 'request']):
                            element.click()
                            print(f"✅ Selected request type (fallback): {text[:50]}")
                            time.sleep(3)
                            return
            except:
                continue
        
        print("⚠️ Could not find matching request type")

    def handle_delete_data_suboptions(self, page: Page):
        """Handle delete data sub-options if applicable"""
        print("🗑️ Handling delete data options...")
        
        request_type = str(self.form_data.get('Request_type', '')).lower()
        if 'delete' not in request_type:
            print("ℹ️ Not a delete request, skipping sub-options")
            return
        
        # Get delete options from Excel
        delete_student = str(self.form_data.get('delete_student', '')).strip()
        delete_parent = str(self.form_data.get('delete_parent', '')).strip()
        delete_educator = str(self.form_data.get('delete_educator', '')).strip()
        
        print(f"📊 Delete options: Student='{delete_student}', Parent='{delete_parent}', Educator='{delete_educator}'")
        
        # Helper function to determine if option should be selected
        def should_select(value):
            return value and value.lower() not in ['', 'nan', 'none', 'no', 'false', '0']
        
        # Select student data if specified
        if should_select(delete_student):
            try:
                page.locator("text=Student data").first.click()
                print("✅ Selected Student data option")
                time.sleep(1)
                # Fill any text input that appears
                text_inputs = page.locator("input[type='text']:visible").all()
                for input_elem in text_inputs[-2:]:  # Get last 2 inputs (likely the new ones)
                    try:
                        input_elem.fill("test DSR")
                        break
                    except:
                        continue
            except:
                print("⚠️ Could not select Student data option")
        
        # Select parent data if specified
        if should_select(delete_parent):
            try:
                page.locator("text=Parent data").first.click()
                print("✅ Selected Parent data option")
                time.sleep(1)
                # Fill any text input that appears
                text_inputs = page.locator("input[type='text']:visible").all()
                for input_elem in text_inputs[-2:]:  # Get last 2 inputs
                    try:
                        input_elem.fill("test DSR")
                        break
                    except:
                        continue
            except:
                print("⚠️ Could not select Parent data option")
        
        # Skip educator if not specified or empty
        if should_select(delete_educator):
            try:
                page.locator("text=Educator data").first.click()
                print("✅ Selected Educator data option")
                time.sleep(1)
            except:
                print("⚠️ Could not select Educator data option")
        else:
            print("⏭️ Skipping Educator data (empty in Excel)")

    def handle_acknowledgments(self, page: Page):
        """Handle acknowledgment and captcha"""
        print("✅ Handling acknowledgments...")
        
        # Look for acknowledgment button/text
        ack_selectors = [
            "text=I acknowledge",
            "button:has-text('acknowledge')",
            "label:has-text('acknowledge')",
            "*:has-text('I acknowledge')"
        ]
        
        for selector in ack_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.click(selector)
                    print("✅ Clicked acknowledgment")
                    time.sleep(2)
                    break
            except:
                continue
        
        # Look for captcha
        captcha_selectors = [
            "#recaptcha-anchor",
            ".recaptcha-checkbox",
            "iframe[src*='recaptcha']"
        ]
        
        for selector in captcha_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.click(selector)
                    print("✅ Clicked reCAPTCHA")
                    print("⏰ Waiting 10 seconds for manual CAPTCHA solving if needed...")
                    time.sleep(10)
                    break
            except:
                continue

    def submit_form(self, page: Page):
        """Submit the form"""
        print("🚀 Submitting form...")
        
        # Enhanced submit button detection
        submit_selectors = [
            "button:has-text('Submit')",
            "button[type='submit']",
            "input[type='submit']",
            "#dsar-webform-submit-button",
            "button[id*='submit']",
            "button[class*='submit']",
            ".submit-btn",
            "*:has-text('Submit'):not(label)"
        ]
        
        for selector in submit_selectors:
            try:
                element = page.locator(selector).first
                if element.is_visible():
                    # Check if button is enabled
                    is_enabled = element.is_enabled()
                    print(f"🔍 Found submit button (enabled: {is_enabled})")
                    
                    if is_enabled:
                        print("⏳ Waiting 3 seconds before submission...")
                        time.sleep(3)
                        element.click()
                        print("✅ Form submitted successfully!")
                        time.sleep(5)  # Wait for submission to complete
                        return True
                    else:
                        print("⚠️ Submit button found but disabled")
            except Exception as e:
                print(f"⚠️ Error with selector {selector}: {str(e)}")
                continue
        
        print("❌ Could not find enabled submit button")
        return False

if __name__ == "__main__":
    print("🚀 Starting Multiple Record Privacy Portal Automation...")
    print("📋 This will process ALL records from the Excel file automatically")
    
    test = TestPrivacyPortalMultiple()
    test.setup_method()
    test.test_multiple_privacy_form_submissions()
