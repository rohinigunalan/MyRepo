import pytest
from playwright.sync_api import sync_playwright, Page, expect
import time
import pandas as pd
import os

# This is a backup of the working script as of July 28, 2025
# Original: myself_requesttypes_submission.py
# Purpose: OneTrust Privacy Portal form automation

class TestPrivacyPortal:
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

if __name__ == "__main__":
    print("\nRunning form fill test...")
    test = TestPrivacyPortal()
    test.setup_method()
    test.test_privacy_form_submission()
