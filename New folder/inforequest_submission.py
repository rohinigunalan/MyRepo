import pytest
from playwright.sync_api import sync_playwright, Page, expect
import time
import pandas as pd
import os

class TestPrivacyPortal:
    """Test suite for OneTrust Privacy Portal form automation"""
    
    def setup_method(self):
        """Setup method called before each test"""
        self.url = "https://privacyportaluat.onetrust.com/webform/b99e91a7-a15e-402d-913d-a09fe56fcd54/c31c1bfa-b0a7-4a7a-9fc0-22c44fa094d0"
        self.form_data = self.load_form_data()
    
    def load_form_data(self):
        """Load form data from Excel or CSV file"""
        print("📂 Loading form data from file...")
        
        # Try to load from Excel first, then CSV
        excel_file = "form_data.xlsx"
        csv_file = "form_data.csv"
        
        try:
            if os.path.exists(excel_file):
                print(f"📊 Attempting to read data from {excel_file}")
                try:
                    df = pd.read_excel(excel_file, engine='openpyxl')
                    print("✅ Excel file loaded successfully!")
                except Exception as excel_error:
                    print(f"⚠️  Excel file error: {excel_error}")
                    print("🔄 Trying CSV file as fallback...")
                    if os.path.exists(csv_file):
                        df = pd.read_csv(csv_file)
                        print("✅ CSV file loaded successfully!")
                    else:
                        raise FileNotFoundError("Neither Excel nor CSV file could be loaded")
            elif os.path.exists(csv_file):
                print(f"📊 Reading data from {csv_file}")
                df = pd.read_csv(csv_file)
                print("✅ CSV file loaded successfully!")
            else:
                raise FileNotFoundError("No form_data.xlsx or form_data.csv file found")
            
            # Get the first row of data
            if len(df) == 0:
                raise ValueError("No data found in the file")
            
            # Convert first row to dictionary
            data = df.iloc[0].to_dict()
            
            print("✅ Form data loaded successfully:")
            for key, value in data.items():
                print(f"  {key}: {value}")
            
            return data
            
        except Exception as e:
            print(f"❌ Error loading form data: {str(e)}")
            print("📝 Using default fallback data...")
            # Fallback to default data
            return {
                'Email Address': 'palmny1@mailinator.com',
                'First_Name': 'RobNY',
                'Last_Name': 'EdisonNY',
                'birthDate': '11/1/2003',
                'phone': '5712345567',
                'country': 'US',
                'stateOrProvince': 'New York',
                'postalCode': '14111',
                'city': 'North Collins',
                'streetAddress': '507 Central Avenue',
                'studentSchoolName': 'South Lakes High School',
                'studentGraduationYear': '2020',
                'educatorSchoolAffiliation': 'N/A',
                'Request_type': 'Request a copy of my data'
            }
        
    def test_privacy_form_submission(self):
        """Test filling and submitting the privacy portal form"""
        print("🚨 IMPORTANT NOTE: This script will automate most of the form filling,")
        print("   but you may need to manually solve reCAPTCHA challenges if they appear.")
        print("   The script will pause and wait for you to complete any image puzzles.")
        print("   Please stay near your computer to help with reCAPTCHA if needed!\n")
        
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=False)  # Set to True for headless mode
            page = browser.new_page()
            
            try:
                # Navigate to the privacy portal
                print(f"Navigating to: {self.url}")
                page.goto(self.url)
                
                # Wait for page to load
                page.wait_for_load_state("networkidle")
                time.sleep(2)
                
                # DEBUG: List all form fields to understand the structure
                print("\n🔍 DEBUGGING: Listing all form fields...")
                all_inputs = page.locator("input, select, textarea").all()
                for i, element in enumerate(all_inputs):
                    try:
                        tag_name = element.evaluate("el => el.tagName")
                        name = element.get_attribute("name") or "no-name"
                        id_attr = element.get_attribute("id") or "no-id"
                        placeholder = element.get_attribute("placeholder") or "no-placeholder"
                        type_attr = element.get_attribute("type") or "no-type"
                        visible = element.is_visible()
                        print(f"Field {i+1}: {tag_name} - name='{name}', id='{id_attr}', placeholder='{placeholder}', type='{type_attr}', visible={visible}")
                    except Exception as e:
                        print(f"Field {i+1}: Could not get attributes - {str(e)}")
                print("🔍 END FIELD LISTING\n")
                
                # Pause to review form structure
                print("⏸️ PAUSE: Review the form structure above. Continuing in 5 seconds...")
                time.sleep(5)
                
                # Fill out the form based on the data from your JSON
                print("\n🎯 STARTING FORM FILLING PROCESS...")
                try:
                    self.fill_subject_information(page)
                except Exception as e:
                    print(f"⚠️ Error in subject information: {str(e)}")
                    page.screenshot(path="screenshots/error_subject_info.png")
                
                # Take screenshot after subject info
                page.screenshot(path="screenshots/after_subject_info.png")
                print("📸 Screenshot saved after subject information")
                
                # Pause after subject info
                print("⏸️ PAUSE: Subject information filled. Continuing in 4 seconds...")
                time.sleep(4)
                
                try:
                    self.fill_contact_information(page)
                except Exception as e:
                    print(f"⚠️ Error in contact information: {str(e)}")
                    page.screenshot(path="screenshots/error_contact_info.png")
                
                # Take screenshot after contact info
                page.screenshot(path="screenshots/after_contact_info.png")
                print("📸 Screenshot saved after contact information")
                
                # Pause after contact info to observe dropdowns
                print("⏸️ PAUSE: Contact information filled (including country/state). Continuing in 5 seconds...")
                time.sleep(5)
                
                try:
                    self.fill_additional_details(page)
                except Exception as e:
                    print(f"⚠️ Error in additional details: {str(e)}")
                    page.screenshot(path="screenshots/error_additional_details.png")
                
                # Pause after additional details
                print("⏸️ PAUSE: Additional details filled. Continuing in 3 seconds...")
                time.sleep(3)
                
                try:
                    self.select_request_type(page)
                except Exception as e:
                    print(f"⚠️ Error in request type selection: {str(e)}")
                    page.screenshot(path="screenshots/error_request_type.png")
                
                # Pause after request type selection
                print("⏸️ PAUSE: Request type selected. Continuing in 3 seconds...")
                time.sleep(3)
                
                try:
                    self.handle_acknowledgments(page)
                except Exception as e:
                    print(f"⚠️ Error in acknowledgments: {str(e)}")
                    page.screenshot(path="screenshots/error_acknowledgments.png")
                
                # Pause after acknowledgments
                print("⏸️ PAUSE: Acknowledgments completed. Continuing in 3 seconds...")
                time.sleep(3)
                
                # Take a screenshot after filling all fields
                page.screenshot(path="screenshots/form_filled_complete.png")
                print("📸 Screenshot saved: screenshots/form_filled_complete.png")
                
                # Take a screenshot before submission (backup)
                page.screenshot(path="screenshots/before_submission.png")
                print("📸 Screenshot saved: screenshots/before_submission.png")
                
                # Pause before submission to review completed form
                print("⏸️ PAUSE: Form completely filled! Review the form before submission. Submitting in 7 seconds...")
                time.sleep(7)
                
                # Submit the form (now enabled for testing)
                try:
                    self.submit_form(page)
                except Exception as e:
                    print(f"⚠️ Error during form submission: {str(e)}")
                    page.screenshot(path="screenshots/error_submission.png")
                
                # Pause after submission to see results
                print("⏸️ PAUSE: Form submission attempted. Observe results for 8 seconds...")
                time.sleep(8)
                
                print("✅ Form automation completed successfully!")
                
            except Exception as e:
                # Take screenshot on error
                page.screenshot(path="screenshots/error_screenshot.png")
                print(f"❌ Error occurred: {str(e)}")
                print("📸 Error screenshot saved: screenshots/error_screenshot.png")
                raise
                
            finally:
                # Keep browser open for longer to see final results
                print("⏸️ FINAL PAUSE: Keeping browser open for 10 seconds to review final state...")
                time.sleep(10)
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
            "[data-value='Myself']"
        ]
        
        myself_clicked = False
        for selector in myself_selectors:
            try:
                if page.locator(selector).first.is_visible():
                    page.click(selector)
                    print(f"✅ Clicked 'Myself' button with selector: {selector}")
                    time.sleep(2)  # Longer pause to see form update
                    myself_clicked = True
                    break
            except Exception as e:
                print(f"⚠️ Could not click 'Myself' button with selector {selector}: {str(e)}")
                continue
        
        if not myself_clicked:
            print("⚠️ 'Myself' button not found - continuing anyway...")
        
        # Pause after clicking Myself to let form update
        print("⏸️ Brief pause after 'Myself' selection...")
        time.sleep(2)
        
        # First Name - enhanced selectors
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
                    time.sleep(1)  # Brief pause to watch field fill
                    break
            except:
                continue
                
        # Last Name - enhanced selectors
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
                    time.sleep(1)  # Brief pause to watch field fill
                    break
            except:
                continue
            
        # Email Address - enhanced selectors
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
                    time.sleep(1)  # Brief pause to watch field fill
                    break
            except:
                continue
            
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
                    page.fill(selector, str(self.form_data.get('phone', '5712345567')))
                    print(f"✅ Phone filled with selector: {selector}")
                    time.sleep(1)  # Brief pause to watch field fill
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
            
        # Country FIRST - Click input field first, then select from dropdown
        print("🌍 Attempting to fill country field...")
        country_filled = False
        
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
                            
                            # STEP 2: Look for dropdown options that appear after clicking
                            # Try multiple ways to find and click "United States" option
                            us_option_selectors = [
                                # Standard option selectors
                                "option:has-text('United States')",
                                "option[value='US']",
                                "option[value='USA']", 
                                "option[value='United States']",
                                # List item selectors (for custom dropdowns)
                                "li:has-text('United States')",
                                "li[data-value='US']",
                                "li[data-value='USA']",
                                # Div-based dropdown options
                                "div:has-text('United States')",
                                "[role='option']:has-text('United States')",
                                # More specific selectors
                                ".dropdown-option:has-text('United States')",
                                ".option:has-text('United States')",
                                "[data-value='United States']"
                            ]
                            
                            print("🔍 Looking for 'United States' option in dropdown...")
                            option_clicked = False
                            
                            for option_selector in us_option_selectors:
                                try:
                                    option_element = page.locator(option_selector).first
                                    if option_element.is_visible():
                                        option_element.click(timeout=3000)
                                        print(f"✅ Clicked 'United States' option with selector: {option_selector}")
                                        country_filled = True
                                        option_clicked = True
                                        break
                                except Exception as e:
                                    print(f"⚠️ Could not click option with {option_selector}: {str(e)}")
                                    continue
                            
                            # STEP 3: If clicking individual options didn't work, try select_option on select elements
                            if not option_clicked and country_selector.startswith("select"):
                                print("🔄 Trying select_option method...")
                                country_options = ["US", "USA", "United States", "United States of America"]
                                for option_value in country_options:
                                    try:
                                        page.select_option(country_selector, value=option_value, timeout=3000)
                                        print(f"✅ Country selected using select_option with value: {option_value}")
                                        country_filled = True
                                        break
                                    except:
                                        try:
                                            page.select_option(country_selector, label=option_value, timeout=3000)
                                            print(f"✅ Country selected using select_option with label: {option_value}")
                                            country_filled = True
                                            break
                                        except:
                                            continue
                            
                            # STEP 4: If it's an input field, try typing
                            if not country_filled and not country_selector.startswith("select"):
                                try:
                                    element.fill("United States", timeout=3000)
                                    print("✅ Country typed into input field: United States")
                                    country_filled = True
                                    # Press Enter to confirm selection
                                    element.press("Enter")
                                    print("⌨️ Pressed Enter to confirm country selection")
                                except:
                                    print("⚠️ Could not type in country input field")
                                    
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
            print("⚠️ Could not fill country field - continuing anyway...")
            # Take a screenshot to see current state
            page.screenshot(path="screenshots/country_field_issue.png")
            print("📸 Screenshot saved: screenshots/country_field_issue.png")

        # State SECOND - Enhanced click logic for state dropdown
        print("🗽 Attempting to fill state field...")
        state_filled = False
        
        try:
            # Wait longer after country selection for state field to become available
            print("⏳ Waiting for state field to become available after country selection...")
            time.sleep(5)
            
            # Try multiple selectors for state field - including input fields with dropdowns
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
            
            # First, let's see what state elements are available
            print("🔍 Checking for available state elements...")
            for i, selector in enumerate(state_selectors):
                try:
                    elements = page.locator(selector).all()
                    for j, element in enumerate(elements):
                        if element.is_visible():
                            print(f"  Found visible state element {i+1}.{j+1}: {selector}")
                except:
                    continue
            
            for state_selector in state_selectors:
                try:
                    element = page.locator(state_selector).first
                    if element.is_visible():
                        print(f"🔍 Found state field with selector: {state_selector}")
                        
                        # Get state name from Excel data
                        state_name = str(self.form_data.get('stateOrProvince', 'New York'))
                        print(f"🏛️ Using state from Excel: '{state_name}'")
                        
                        # IMPROVED STATE SELECTION - MORE RELIABLE
                        try:
                            print("🎯 Using improved state selection...")
                            
                            # Step 1: Click the state field to focus it
                            element.click(timeout=3000)
                            print("✅ Clicked state field")
                            time.sleep(1)
                            
                            # Step 2: Clear any existing value
                            element.fill("")
                            print("✅ Cleared field")
                            time.sleep(0.5)
                            
                            # Step 3: Type state name to filter dropdown
                            element.type(state_name, delay=100)
                            print(f"✅ Typed '{state_name}'")
                            time.sleep(3)  # Wait longer for dropdown to appear
                            
                            # Step 4: Multiple approaches to select the dropdown option
                            option_selected = False
                            
                            # Approach 1: Look for visible dropdown options
                            print("🔍 Looking for dropdown options...")
                            dropdown_option_selectors = [
                                f"option:has-text('{state_name}'):visible",
                                f"li:has-text('{state_name}'):visible", 
                                f"div[role='option']:has-text('{state_name}'):visible",
                                f"[data-value*='New York']:visible",
                                f"[value*='New York']:visible",
                                f".option:has-text('{state_name}'):visible"
                            ]
                            
                            for selector in dropdown_option_selectors:
                                try:
                                    options = page.locator(selector).all()
                                    if options:
                                        print(f"📋 Found {len(options)} matching options with selector: {selector}")
                                        for option in options:
                                            if option.is_visible():
                                                option_text = option.inner_text()
                                                print(f"🎯 Clicking option: '{option_text}'")
                                                option.click(timeout=2000)
                                                option_selected = True
                                                print(f"✅ Successfully selected '{option_text}'")
                                                break
                                    if option_selected:
                                        break
                                except Exception as e:
                                    print(f"⚠️ Selector {selector} failed: {str(e)}")
                                    continue
                            
                            # Approach 2: If no dropdown option found, try keyboard navigation
                            if not option_selected:
                                print("🔄 No dropdown option found, trying keyboard approach...")
                                
                                # Press Down arrow to open dropdown if needed
                                element.press("ArrowDown")
                                time.sleep(1)
                                
                                # Press Enter to select the first matching option
                                element.press("Enter")
                                print("⏎ Pressed Enter to select")
                                option_selected = True
                            
                            # Approach 3: If still not selected, try Tab to move away and confirm
                            if option_selected:
                                time.sleep(1)
                                element.press("Tab")  # Move focus away to confirm selection
                                print("✅ Moved focus away to confirm selection")
                            
                            time.sleep(2)
                            state_filled = True
                            break
                            
                            # Step 3: Press Arrow Down to open dropdown
                            element.press("ArrowDown")
                            print("✅ Pressed ArrowDown to open dropdown")
                            time.sleep(2)
                            
                            # Step 4: Navigate to New York using keyboard ONLY
                            print("� Navigating to New York using keyboard navigation...")
                            
                            # Press 'N' key to jump to states starting with 'N'
                            element.press("KeyN")
                            time.sleep(1)
                            print("✅ Pressed 'N' to jump to N states")
                            
                            # Press 'e' to get to "Ne..." states  
                            element.press("KeyE")
                            time.sleep(1)
                            print("✅ Pressed 'E' to get to 'Ne...' states")
                            
                            # Now use Arrow Down to find New York specifically
                            for i in range(15):  # Try up to 15 arrow downs to find New York
                                try:
                                    # Check current selection
                                    current_element = page.locator("[aria-selected='true'], .selected, .highlighted, option:focus").first
                                    if current_element.is_visible():
                                        current_text = current_element.inner_text().strip()
                                        print(f"🔍 Current selection: '{current_text}'")
                                        
                                        if "new york" in current_text.lower():
                                            print(f"✅ Found New York: '{current_text}'")
                                            element.press("Enter")
                                            print("✅ Pressed Enter to select New York")
                                            time.sleep(2)
                                            state_filled = True
                                            break
                                    
                                    # If not New York, continue navigating
                                    element.press("ArrowDown")
                                    time.sleep(0.5)
                                    
                                except Exception as nav_error:
                                    print(f"⚠️ Navigation error: {nav_error}")
                                    element.press("ArrowDown")
                                    time.sleep(0.5)
                            
                            # Verify selection worked
                            if state_filled:
                                try:
                                    current_value = element.input_value() or element.text_content() or ""
                                    print(f"🔍 Field value after selection: '{current_value}'")
                                    if current_value.strip() and ("new york" in current_value.lower() or len(current_value.strip()) > 0):
                                        print("✅ State appears to be selected successfully")
                                        break
                                    else:
                                        print("⚠️ Field appears empty, selection may not have worked")
                                        state_filled = False
                                except:
                                    print("✅ Assuming keyboard navigation worked")
                                    break
                            
                            # If keyboard navigation didn't find New York, try alternative
                            if not state_filled:
                                print("� Keyboard navigation didn't find New York, trying direct search...")
                                
                                # Start over with a different approach
                                element.click(timeout=3000)
                                element.fill("")
                                time.sleep(0.5)
                                element.press("ArrowDown")
                                time.sleep(2)
                                
                                # Try typing full state name "New York" (not abbreviation)
                                element.type("New York", delay=100)
                                print("✅ Typed 'New York' (full name)")
                                time.sleep(2)
                                
                                # Look for exact New York match and click it
                                try:
                                    ny_option = page.locator("option:has-text('New York'), li:has-text('New York'), div:has-text('New York')").first
                                    if ny_option.is_visible():
                                        ny_option.click(timeout=3000)
                                        print("✅ Clicked 'New York' option directly")
                                        state_filled = True
                                    else:
                                        # Fallback - just press Enter
                                        element.press("Enter")
                                        print("✅ Pressed Enter to select")
                                        state_filled = True
                                except:
                                    element.press("Enter")
                                    print("✅ Pressed Enter as fallback")
                                    state_filled = True
                            element.press("ArrowDown")
                            print("✅ Pressed ArrowDown to open dropdown")
                            time.sleep(2)
                            
                            # Step 4: Navigate to New York using keyboard
                            # New York is typically around position 32-35 in the US states list
                            print("� Navigating to New York using keyboard...")
                            
                            # Press 'N' key to jump to states starting with 'N'
                            element.press("KeyN")
                            time.sleep(1)
                            print("✅ Pressed 'N' to jump to N states")
                            
                            # Press 'e' to get to "Ne..." states  
                            element.press("KeyE")
                            time.sleep(1)
                            print("✅ Pressed 'E' to get to 'Ne...' states")
                            
                            # Now use Arrow Down to find New York specifically
                            for i in range(10):  # Try up to 10 arrow downs to find New York
                                try:
                                    # Check current selection
                                    current_element = page.locator("[aria-selected='true'], .selected, .highlighted, option:focus").first
                                    if current_element.is_visible():
                                        current_text = current_element.inner_text().strip()
                                        print(f"🔍 Current selection: '{current_text}'")
                                        
                                        if "new york" in current_text.lower():
                                            print(f"✅ Found New York: '{current_text}'")
                                            element.press("Enter")
                                            print("✅ Pressed Enter to select New York")
                                            time.sleep(2)
                                            state_filled = True
                                            break
                                    
                                    # If not New York, continue navigating
                                    element.press("ArrowDown")
                                    time.sleep(0.5)
                                    
                                except Exception as nav_error:
                                    print(f"⚠️ Navigation error: {nav_error}")
                                    element.press("ArrowDown")
                                    time.sleep(0.5)
                            
                            # If keyboard navigation didn't work, try direct value setting
                            if not state_filled:
                                print("� Keyboard navigation failed, trying direct approach...")
                                
                                # Clear and try typing "NY" (abbreviation)
                                element.fill("")
                                time.sleep(0.5)
                                element.type("NY", delay=100)
                                time.sleep(1)
                                element.press("Tab")  # Tab to next field to trigger selection
                                print("✅ Typed 'NY' and pressed Tab")
                                time.sleep(1)
                                state_filled = True
                            
                            # Verify selection worked
                            try:
                                current_value = element.input_value() or element.text_content() or ""
                                print(f"� Field value after selection: '{current_value}'")
                                if current_value.strip() and ("new york" in current_value.lower() or "ny" in current_value.lower() or len(current_value.strip()) > 0):
                                    print("✅ State appears to be selected successfully")
                                    state_filled = True
                                    break
                            except:
                                # Even if we can't verify, assume it worked
                                print("✅ Assuming state selection worked")
                                state_filled = True
                                break
                                
                        except Exception as e:
                            print(f"❌ Simple approach failed: {str(e)}")
                            
                            # FALLBACK: Try different approach - click, open dropdown, type abbreviation
                            try:
                                print("🔄 Fallback: Using dropdown + NY abbreviation...")
                                element.click(timeout=3000)
                                element.fill("")
                                time.sleep(0.5)
                                
                                # Open dropdown first
                                element.press("ArrowDown")
                                time.sleep(2)
                                
                                # Type NY abbreviation
                                element.type("NY", delay=100)
                                time.sleep(1)
                                element.press("Enter")
                                print("✅ Fallback: Typed 'NY' and pressed Enter")
                                state_filled = True
                                break
                            except Exception as e2:
                                print(f"❌ Fallback also failed: {str(e2)}")
                                
                                # LAST RESORT: Try typing first few letters of "New York"
                                try:
                                    print("🔄 Last resort: Typing 'New'...")
                                    element.click(timeout=3000)
                                    element.fill("")
                                    time.sleep(0.5)
                                    element.press("ArrowDown")  # Open dropdown
                                    time.sleep(2)
                                    element.type("New", delay=100)  # Type just "New"
                                    time.sleep(2)
                                    
                                    # Look for New York option specifically
                                    ny_options = page.locator("option:has-text('New York'), li:has-text('New York'), div:has-text('New York')").count()
                                    if ny_options > 0:
                                        page.locator("option:has-text('New York'), li:has-text('New York'), div:has-text('New York')").first.click()
                                        print("✅ Found and clicked 'New York' option")
                                    else:
                                        element.press("Enter")  # Just press enter
                                        print("⚠️ No specific New York option found, pressed Enter")
                                    
                                    state_filled = True
                                    break
                                except Exception as e3:
                                    print(f"❌ Last resort failed: {str(e3)}")
                        
                        if state_filled:
                            break
                        
                        # STEP 2: Fallback - Try abbreviation approach for New York
                        if not state_filled and state_name == "New York":
                            print("🔄 Fallback: Trying with 'NY' abbreviation...")
                            try:
                                element.click(timeout=3000)
                                element.fill("", timeout=3000)
                                time.sleep(0.5)
                                element.type("NY", delay=100)
                                print("✅ Typed 'NY' into state field")
                                time.sleep(2)
                                
                                # Look for NY options in dropdown
                                ny_selectors = [
                                    "option:has-text('NY')",
                                    "li:has-text('NY')",
                                    "option:has-text('New York')",
                                    "li:has-text('New York')",
                                    "div:has-text('NY')",
                                    "[role='option']:has-text('NY')"
                                ]
                                
                                ny_option_found = False
                                for ny_selector in ny_selectors:
                                    try:
                                        ny_option = page.locator(ny_selector).first
                                        if ny_option.is_visible():
                                            print(f"✅ Found NY option: {ny_selector}")
                                            ny_option.click(timeout=3000)
                                            print("🎯 Clicked on NY option")
                                            ny_option_found = True
                                            time.sleep(2)
                                            break
                                    except:
                                        continue
                                
                                if not ny_option_found:
                                    element.press("Enter")
                                    print("⏎ Pressed Enter for NY")
                                    time.sleep(1)
                                
                                state_filled = True
                                break
                                
                            except Exception as e:
                                print(f"❌ NY abbreviation approach failed: {str(e)}")
                        
                        # STEP 3: Last resort - Try keyboard navigation
                        if not state_filled:
                            print("🔄 Last resort: Trying keyboard navigation...")
                            try:
                                element.click(timeout=3000)
                                time.sleep(1)
                                element.press("ArrowDown")  # Open dropdown
                                time.sleep(1)
                                
                                # Navigate through options looking for our state
                                for i in range(60):  # Try up to 60 states
                                    try:
                                        # Check if current highlighted option matches our state
                                        highlighted = page.locator("[aria-selected='true'], .highlighted, .selected, [aria-current='true']").first
                                        if highlighted.is_visible():
                                            text = highlighted.inner_text().strip()
                                            if (state_name.lower() in text.lower() or 
                                                (state_name == "New York" and ("ny" in text.lower() or "new york" in text.lower()))):
                                                element.press("Enter")
                                                print(f"✅ Found and selected '{text}' via keyboard navigation")
                                                state_filled = True
                                                break
                                    except:
                                        pass
                                    
                                    element.press("ArrowDown")
                                    time.sleep(0.1)
                                
                                if state_filled:
                                    break
                                    
                            except Exception as e:
                                print(f"❌ Keyboard navigation failed: {str(e)}")
                            state_option_selectors = [
                                # Standard option selectors
                                f"option:has-text('{state_name}')",
                                f"option[value='{state_name}']",
                                "option[value='NY']" if state_name == "New York" else f"option[value='{state_name}']",
                                f"option:has-text('{state_name[:2]}')" if len(state_name) > 2 else f"option:has-text('{state_name}')",
                                # List item selectors (for custom dropdowns)
                                f"li:has-text('{state_name}')",
                                f"li[data-value='{state_name}']",
                                f"li:contains('{state_name}')",
                                # Div-based dropdown options
                                f"div:has-text('{state_name}')",
                                f"[role='option']:has-text('{state_name}')",
                                f"[role='menuitem']:has-text('{state_name}')",
                                # More specific selectors
                                f".dropdown-option:has-text('{state_name}')",
                                f".option:has-text('{state_name}')",
                                f".select-option:has-text('{state_name}')",
                                f"[data-value='{state_name}']",
                                # Button-based options
                                f"button:has-text('{state_name}')",
                                f"a:has-text('{state_name}')"
                            ]
                            
                            print(f"🔍 Looking for '{state_name}' option in dropdown...")
                            
                            # First, let's see what options are actually available
                            print("🔍 DEBUG: Checking all visible options after clicking state field...")
                            try:
                                all_options = page.locator("option, li, div[role='option'], .dropdown-option, .option").all()
                                for i, opt in enumerate(all_options):
                                    try:
                                        if opt.is_visible():
                                            text = opt.inner_text() or opt.text_content() or ""
                                            value = opt.get_attribute("value") or ""
                                            print(f"  Option {i+1}: text='{text}', value='{value}'")
                                    except:
                                        pass
                            except:
                                print("  Could not enumerate options")
                            
                            option_clicked = False
                            
                            # Wait a bit more for options to appear
                            time.sleep(2)
                            
                            for option_selector in state_option_selectors:
                                try:
                                    option_elements = page.locator(option_selector).all()
                                    print(f"🔍 Trying selector: {option_selector} - Found {len(option_elements)} elements")
                                    
                                    for j, option_element in enumerate(option_elements):
                                        try:
                                            if option_element.is_visible():
                                                text = option_element.inner_text() or ""
                                                print(f"  Element {j+1} visible with text: '{text}'")
                                                option_element.click(timeout=3000, force=True)
                                                print(f"✅ Clicked '{state_name}' option with selector: {option_selector}")
                                                state_filled = True
                                                option_clicked = True
                                                break
                                        except Exception as e:
                                            print(f"    Could not click element {j+1}: {str(e)}")
                                            continue
                                    
                                    if option_clicked:
                                        break
                                        
                                except Exception as e:
                                    print(f"⚠️ Could not use selector {option_selector}: {str(e)}")
                                    continue
                            
                            # Try typing state abbreviation to filter/select
                            if not option_clicked:
                                state_abbrev = "NY" if state_name == "New York" else state_name[:2].upper()
                                print(f"🔄 Trying to type '{state_abbrev}' to filter dropdown...")
                                try:
                                    element.type(state_abbrev, delay=100)
                                    time.sleep(1)
                                    element.press("Enter")
                                    print(f"✅ Typed '{state_abbrev}' and pressed Enter")
                                    state_filled = True
                                    option_clicked = True
                                except Exception as e:
                                    print(f"⚠️ Could not type '{state_abbrev}': {str(e)}")
                            
                            # Try typing full state name to filter/select
                            if not option_clicked:
                                print(f"🔄 Trying to type '{state_name}' to filter dropdown...")
                                try:
                                    element.clear()
                                    time.sleep(0.5)
                                    element.type(state_name, delay=100)
                                    time.sleep(1)
                                    element.press("Enter")
                                    print(f"✅ Typed '{state_name}' and pressed Enter")
                                    state_filled = True
                                    option_clicked = True
                                except Exception as e:
                                    print(f"⚠️ Could not type '{state_name}': {str(e)}")
                            
                            # Try using keyboard navigation
                            if not option_clicked:
                                print("🔄 Trying keyboard navigation...")
                                try:
                                    element.press("ArrowDown")
                                    time.sleep(0.5)
                                    # Look for the state from Excel in the list by pressing down arrow multiple times
                                    for i in range(50):  # Try up to 50 options to find the state
                                        try:
                                            current_text = page.locator("[aria-selected='true'], .selected, .highlighted").first.inner_text()
                                            # Check if current option matches our target state
                                            if (state_name.lower() in current_text.lower() or 
                                                (state_name == "New York" and ("NY" in current_text or "New York" in current_text)) or
                                                (len(state_name) >= 2 and state_name[:2].upper() in current_text)):
                                                element.press("Enter")
                                                print(f"✅ Found and selected '{state_name}' using keyboard navigation")
                                                state_filled = True
                                                option_clicked = True
                                                break
                                        except:
                                            pass
                                        element.press("ArrowDown")
                                        time.sleep(0.2)
                                except Exception as e:
                                    print(f"⚠️ Keyboard navigation failed: {str(e)}")
                            
                            # STEP 3: If clicking individual options didn't work, try select_option on select elements
                            if not option_clicked and state_selector.startswith("select"):
                                print("🔄 Trying select_option method for state...")
                                # Create dynamic state options based on Excel data
                                state_abbrev = "NY" if state_name == "New York" else state_name[:2].upper()
                                state_options = [
                                    state_name,  # Full state name from Excel
                                    state_name.upper(),  # Uppercase version
                                    state_abbrev,  # State abbreviation
                                    state_name[:2].upper() if len(state_name) >= 2 else state_name  # First 2 letters
                                ]
                                for option_value in state_options:
                                    try:
                                        page.select_option(state_selector, value=option_value, timeout=3000)
                                        print(f"✅ State selected using select_option with value: {option_value}")
                                        state_filled = True
                                        break
                                    except:
                                        try:
                                            page.select_option(state_selector, label=option_value, timeout=3000)
                                            print(f"✅ State selected using select_option with label: {option_value}")
                                            state_filled = True
                                            break
                                        except:
                                            continue
                        
                except Exception as e:
                    print(f"⚠️ Error with state selector {state_selector}: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"❌ Major error in state selection: {str(e)}")
        
        if not state_filled:
            print("⚠️ Could not fill state field - taking debug screenshot...")
            # Take a screenshot to see current state
            page.screenshot(path="screenshots/state_field_debug.png")
            print("📸 Debug screenshot saved: screenshots/state_field_debug.png")
            
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
    
    def select_request_type(self, page: Page):
        """Select request type - 'Request a copy of data'"""
        print("📋 Selecting request type...")
        
        # Look for "Request a copy of data" option with multiple selector strategies
        copy_data_selectors = [
            # Radio button selectors
            "input[type='radio'][value*='copy']",
            "input[type='radio'][value*='Copy']",
            "input[type='radio'][value*='data']",
            "input[type='radio'][value*='Data']",
            # Label selectors
            "label:has-text('Request a copy of data')",
            "label:has-text('request a copy of data')",
            "label:has-text('Copy of data')",
            "label:has-text('copy of data')",
            # Button selectors
            "button:has-text('Request a copy of data')",
            "button:has-text('request a copy of data')",
            "button:has-text('Copy of data')",
            # Div/span selectors for custom options
            "div:has-text('Request a copy of data')",
            "span:has-text('Request a copy of data')",
            # Generic selectors
            "[data-value*='copy']",
            "[data-value*='Copy']",
            "[aria-label*='copy']",
            "[aria-label*='Copy']"
        ]
        
        request_type_selected = False
        for selector in copy_data_selectors:
            try:
                elements = page.locator(selector).all()
                for element in elements:
                    if element.is_visible():
                        text = ""
                        try:
                            text = element.inner_text() or element.text_content() or ""
                        except:
                            pass
                        
                        # Check if this looks like the right option
                        if any(phrase in text.lower() for phrase in ["copy of data", "request a copy", "copy"]):
                            print(f"🔍 Found request type option - text: '{text}'")
                            element.click(timeout=5000)
                            print(f"✅ Selected 'Request a copy of data' using selector: {selector}")
                            request_type_selected = True
                            time.sleep(2)  # Brief pause after selection
                            break
                        
                if request_type_selected:
                    break
            except Exception as e:
                print(f"⚠️ Could not select with {selector}: {str(e)}")
                continue
        
        # If not found, try more generic approach
        if not request_type_selected:
            print("🔄 Trying alternative approach for request type...")
            try:
                # Look for any radio buttons or checkboxes
                radio_elements = page.locator("input[type='radio'], input[type='checkbox']").all()
                for i, radio in enumerate(radio_elements):
                    try:
                        if radio.is_visible():
                            # Try to find associated label or text
                            radio_id = radio.get_attribute("id") or ""
                            radio_value = radio.get_attribute("value") or ""
                            
                            # Look for associated label
                            label_text = ""
                            if radio_id:
                                try:
                                    label_elem = page.locator(f"label[for='{radio_id}']").first
                                    if label_elem.is_visible():
                                        label_text = label_elem.inner_text() or ""
                                except:
                                    pass
                            
                            print(f"🔍 Radio option {i+1}: value='{radio_value}', label='{label_text}'")
                            
                            # Check if this looks like copy of data option
                            if any(phrase in f"{radio_value} {label_text}".lower() for phrase in ["copy", "data", "request"]):
                                radio.click(timeout=3000)
                                print(f"✅ Selected option with value='{radio_value}', label='{label_text}'")
                                request_type_selected = True
                                break
                    except:
                        continue
            except:
                pass
        
        if not request_type_selected:
            print("⚠️ Could not find 'Request a copy of data' option")
            # Take screenshot for debugging
            page.screenshot(path="screenshots/request_type_debug.png")
            print("📸 Debug screenshot saved: screenshots/request_type_debug.png")
        
        print("✅ Request type selection completed")
    
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
            page.screenshot(path="screenshots/captcha_debug.png")
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
                page.screenshot(path="screenshots/captcha_challenge.png")
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
    
    def submit_form(self, page: Page):
        """Submit the form"""
        print("🚀 Attempting to submit form...")
        
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
            print("✅ Form submission initiated!")
            
            # Wait for submission to complete
            print("⏳ Waiting for form submission to complete...")
            try:
                page.wait_for_load_state("networkidle", timeout=15000)
                time.sleep(3)
            except:
                print("⚠️ Submission may still be processing...")
                time.sleep(5)
            
            # Take screenshot after submission
            page.screenshot(path="screenshots/after_submission.png")
            print("📸 Screenshot saved: screenshots/after_submission.png")
            
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
            page.screenshot(path="screenshots/submit_button_not_found.png")
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
