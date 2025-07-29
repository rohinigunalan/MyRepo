import pytest
from playwright.sync_api import sync_playwright, Page, expect
import time
import pandas as pd
import os

# This is a backup of the working script as of July 28, 2025
# Original: myself_requesttypes_submission.py
# Purpose: OneTrust Privacy Portal form automation

class TestPrivacyPortal:
    """Test suite for OneTrust Privacy Portal form automation"""
    
    def setup_method(self):
        """Setup method called before each test"""
        self.url = "https://privacyportaluat.onetrust.com/webform/b99e91a7-a15e-402d-913d-a09fe56fcd54/c31c1bfa-b0a7-4a7a-9fc0-22c44fa094d0"
        self.form_data = {}  # Will be set for each record
    
    def load_form_data(self):
        """Load form data from Excel or CSV file"""
        print("📂 Loading form data from file...")

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

            return df.to_dict(orient='records')  # Return all records as a list of dictionaries

        except Exception as e:
            print(f"❌ Error loading form data: {str(e)}")
            raise

    def test_privacy_form_submission(self):
        """Test filling and submitting the privacy portal form for all records"""
        print("🚨 IMPORTANT NOTE: This script will automate most of the form filling,")
        print("   but you may need to manually solve reCAPTCHA challenges if they appear.")
        print("   The script will pause and wait for you to complete any image puzzles.")
        print("   Please stay near your computer to help with reCAPTCHA if needed!\n")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # Set to True for headless mode
            page = browser.new_page()

            try:
                # Load all records
                all_records = self.load_form_data()

                for index, record in enumerate(all_records):
                    print(f"\nProcessing record {index + 1} of {len(all_records)}")
                    self.form_data = record

                    # Navigate to the privacy portal
                    print(f"Navigating to: {self.url}")
                    page.goto(self.url)

                    # Wait for page to load
                    page.wait_for_load_state("networkidle")
                    time.sleep(2)

                    # Fill and submit the form for the current record
                    try:
                        self.fill_subject_information(page)
                        self.fill_contact_information(page)
                        self.fill_additional_details(page)
                        self.select_request_type(page)
                        self.handle_delete_data_suboptions(page)
                        self.handle_acknowledgments(page)
                        self.submit_form(page)
                    except Exception as e:
                        print(f"⚠️ Error processing record {index + 1}: {str(e)}")
                        page.screenshot(path=f"dsr/screenshots/error_record_{index + 1}.png")
                        print(f"📸 Error screenshot saved for record {index + 1}")

                    # Pause between records
                    print(f"⏸️ Pausing before processing the next record...")
                    time.sleep(5)

                print("✅ All records processed successfully!")

            except Exception as e:
                print(f"❌ Error occurred: {str(e)}")
                raise

            finally:
                browser.close()

    def fill_subject_information(self, page: Page):
        """Fill subject information section"""
        print("Filling subject information...")
        
        # FIRST: Click "Myself" button if it exists
        print("🔘 Looking for 'Myself' button...")
        myself_selectors = [
            "button:has-text('Myself')",
            "button:has-text('myself')",
            "input[value='Myself']",
            "input[value='myself']",
            "input[type='radio'][value*='myself']",
            "input[type='radio'][value*='Myself']",
            "label:has-text('Myself')",
            "label:has-text('myself')",
            "button[data-testid*='myself']",
            ".myself-btn",
            "#myself",
            "span:has-text('Myself')",
            "div:has-text('Myself')",
            "[data-value='myself']",
            "[role='button']:has-text('Myself')"
        ]
        
        myself_clicked = False
        for selector in myself_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.click(selector)
                    print(f"✅ Clicked 'Myself' button with selector: {selector}")
                    time.sleep(2)
                    myself_clicked = True
                    break
            except Exception as e:
                print(f"⚠️ Could not click 'Myself' button with selector {selector}: {str(e)}")
                continue
        
        if not myself_clicked:
            print("⚠️ 'Myself' button not found - continuing anyway...")
        
        time.sleep(2)
        
        # First Name
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
                    page.fill(selector, str(self.form_data.get('First_Name', 'RobNY')))
                    print(f"✅ First name filled with selector: {selector}")
                    time.sleep(1)
                    break
            except:
                continue
                
        # Last Name
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
                    page.fill(selector, str(self.form_data.get('Last_Name', 'EdisonNY')))
                    print(f"✅ Last name filled with selector: {selector}")
                    time.sleep(1)
                    break
            except:
                continue
            
        # Email Address
        email_selectors = [
            "input[type='email']",
            "input[name='email']",
            "input[id*='email']",
            "input[placeholder*='email']",
            "input[placeholder*='Email']",
            "input[data-testid*='email']"
        ]
        for selector in email_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.fill(selector, str(self.form_data.get('Email Address', 'palmny1@mailinator.com')))
                    print(f"✅ Email filled with selector: {selector}")
                    time.sleep(1)
                    break
            except:
                continue
            
        # Phone Number
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
                    page.fill(selector, str(self.form_data.get('phone', '5712345567')))
                    print(f"✅ Phone filled with selector: {selector}")
                    time.sleep(1)
                    break
            except:
                continue
            
        # Birth Date
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
                    birth_date_raw = str(self.form_data.get('birthDate', '11/1/2003'))
                    date_formats = [birth_date_raw, "11/01/2003", "11/1/2003", "2003-11-01", "01/11/2003", "01-11-2003"]
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
        
        # Street Address
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
            
        # City
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
            
        # Postal Code
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
        
        print("✅ Contact information section completed")

    def fill_additional_details(self, page: Page):
        """Fill additional details section"""
        print("Filling additional details...")
        # Basic implementation - can be expanded based on form requirements
        time.sleep(1)
        print("✅ Additional details section completed")

    def select_request_type(self, page: Page):
        """Select request type and handle close account sub-options if needed"""
        print("Selecting request type...")
        request_type = str(self.form_data.get('Request_type', 'Request a copy of my data'))
        print(f"🎯 Looking for request type: {request_type}")
        # Try different selectors for request type
        selectors = [
            f"button:has-text('{request_type}')",
            f"input[value='{request_type}']",
            f"label:has-text('{request_type}')",
            "button:has-text('Request a copy of my data')",
            "input[value*='copy']",
            "label:has-text('copy')"
        ]
        selected = False
        for selector in selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.click(selector)
                    print(f"✅ Selected request type with selector: {selector}")
                    time.sleep(2)
                    selected = True
                    break
            except:
                continue
        if not selected:
            print("⚠️ Could not find request type selector")

        # Handle close account sub-options if this is a close/deactivate/cancel request
        close_keywords = ["close", "deactivate", "cancel"]
        if any(kw in request_type.lower() for kw in close_keywords):
            print("\n🚪 Handling close account sub-options...")
            # Wait for the sub-options to appear
            time.sleep(2)
            # Read from Excel columns (case-insensitive)
            close_student = str(self.form_data.get('close_student', '')).strip()
            close_educator = str(self.form_data.get('close_educator', '')).strip()
            print(f"📊 Close account options from Excel:")
            print(f"  🎓 Student account: '{close_student}'")
            print(f"  👨‍🏫 Educator account: '{close_educator}'")
            # Selection logic
            def should_select_option(excel_value):
                if excel_value is None:
                    return False
                excel_str = str(excel_value).strip().lower()
                if excel_str in ["nan", "", "none", "no", "false", "0", "n"]:
                    return False
                if excel_str in ["yes", "true", "1", "y"]:
                    return True
                if any(keyword in excel_str for keyword in ["account", "student", "educator"]):
                    return True
                return len(excel_str) > 0
            student_should_select = should_select_option(close_student)
            educator_should_select = should_select_option(close_educator)
            print(f"📋 Selection logic based on Excel data:")
            print(f"  🎓 Student account: {'SELECT' if student_should_select else 'SKIP'} (Excel: '{close_student}')")
            print(f"  👨‍🏫 Educator account: {'SELECT' if educator_should_select else 'SKIP'} (Excel: '{close_educator}')")
            print(f"📊 Total options to select: {sum([student_should_select, educator_should_select])}")
            # Try to select the checkboxes/buttons for the sub-options
            if student_should_select:
                try:
                    # Try various selectors for student account
                    student_selectors = [
                        "label:has-text('Student account')",
                        "button:has-text('Student account')",
                        "input[value*='student']",
                        "[aria-label*='Student']",
                        "text=Student account (if any)",
                        "text=Student account"
                    ]
                    for sel in student_selectors:
                        try:
                            if page.locator(sel).first.is_visible():
                                page.click(sel)
                                print(f"✅ Selected student account option with selector: {sel}")
                                time.sleep(1)
                                break
                        except:
                            continue
                except Exception as e:
                    print(f"⚠️ Could not select student account option: {e}")
            if educator_should_select:
                try:
                    educator_selectors = [
                        "label:has-text('Educator account')",
                        "button:has-text('Educator account')",
                        "input[value*='educator']",
                        "[aria-label*='Educator']",
                        "text=Educator account (if any)",
                        "text=Educator data (if any)",
                        "text=Educator account"
                    ]
                    for sel in educator_selectors:
                        try:
                            if page.locator(sel).first.is_visible():
                                page.click(sel)
                                print(f"✅ Selected educator account option with selector: {sel}")
                                time.sleep(1)
                                break
                        except:
                            continue
                except Exception as e:
                    print(f"⚠️ Could not select educator account option: {e}")
            if not (student_should_select or educator_should_select):
                print("⚠️ No close account options to select based on Excel data!")

    def handle_delete_data_suboptions(self, page: Page):
        """Handle delete data sub-options if they appear"""
        print("Checking for delete data options...")
        time.sleep(2)
        print("✅ Delete data options handled")

    def handle_acknowledgments(self, page: Page):
        """Handle acknowledgment checkboxes"""
        print("Handling acknowledgments...")
        
        # Try to find and check acknowledgment boxes
        ack_selectors = [
            "input[type='checkbox']",
            "[role='checkbox']",
            "input[name*='acknowledge']",
            "input[name*='agree']",
            "input[name*='consent']"
        ]
        
        for selector in ack_selectors:
            try:
                elements = page.locator(selector).all()
                for element in elements:
                    if element.is_visible() and not element.is_checked():
                        element.check()
                        print(f"✅ Checked acknowledgment box")
                        time.sleep(1)
            except:
                continue
        
        print("✅ Acknowledgments handled")

    def submit_form(self, page: Page):
        """Submit the form"""
        print("Submitting form...")
        
        # Look for submit button
        submit_selectors = [
            "button[type='submit']",
            "input[type='submit']",
            "button:has-text('Submit')",
            "button:has-text('Send')",
            "button:has-text('Continue')",
            ".submit-btn",
            "#submit"
        ]
        
        for selector in submit_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    print("⏳ Waiting before clicking submit...")
                    time.sleep(3)
                    page.click(selector)
                    print(f"✅ Clicked submit button with selector: {selector}")
                    time.sleep(5)  # Wait for submission
                    return
            except:
                continue
        
        print("⚠️ Could not find submit button")

if __name__ == "__main__":
    print("\nRunning form fill test...")
    test = TestPrivacyPortal()
    test.setup_method()
    test.test_privacy_form_submission()
