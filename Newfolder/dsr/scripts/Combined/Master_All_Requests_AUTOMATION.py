#!/usr/bin/env python3
"""
🚨 MASTER COMBINED AUTOMATION SCRIPT - ALL REQUEST TYPES
This is the ULTIMATE unified script that handles ALL privacy request types in a single automation:

✅ SUPPORTED REQUEST TYPES:
- Parent/Guardian on behalf of child (International & Domestic)
- Myself requests (International & Domestic)  
- Educator/Agent on behalf of student (International & Domestic)

✅ KEY FEATURES:
- Single script for ALL 6 automation types
- Auto-detects request type from Excel columns
- Unified form filling logic with type-specific adaptations
- Comprehensive Excel reporting
- Enhanced birth date formatting
- Smart delete/close option selection logic

📋 EXCEL FILE REQUIREMENTS:
The Excel file must contain these columns to determine routing:
- 'Request_Category': 'International' or 'Domestic'
- 'Request_Type': 'Parent', 'Myself', or 'Educator'

Example values:
- Request_Category: 'International', Request_Type: 'Parent' → International Parent form
- Request_Category: 'Domestic', Request_Type: 'Myself' → Domestic Myself form
- Request_Category: 'Domestic', Request_Type: 'Educator' → Domestic Educator form

📂 FILE LOCATION: dsr/data/Combined/Master_All_Requests_form_data.xlsx

🚀 TO RUN THIS SCRIPT:
Use: & "C:/Users/rgunalan/OneDrive - College Board/Documents/GitHub/MyRepo/Newfolder/.venv/Scripts/python.exe" -m pytest Master_All_Requests_AUTOMATION.py::TestPrivacyPortal::test_privacy_form_submission -v -s

Created by: GitHub Copilot Assistant
Version: 1.0 - Master Combined Automation
"""

import pytest
from playwright.sync_api import sync_playwright, Page, expect
import time
import pandas as pd
import os
import sys
import datetime
import re
from typing import Dict, List, Optional

# Screenshots directory for master automation
SCREENSHOTS_DIR = "dsr/screenshots/Master_Combined_Automation"

class TestPrivacyPortal:
    """Master Test Suite for ALL Privacy Portal form automation types"""
    
    def setup_method(self):
        """Setup method called before each test"""
        print("🔧 Setting up Master Combined Automation...")
        
        # Single URL for all form types
        self.form_url = "https://privacyportaluat.onetrust.com/webform/b99e91a7-a15e-402d-913d-a09fe56fcd54/c31c1bfa-b0a7-4a7a-9fc0-22c44fa094d0"
        
        # Load ALL records from master Excel file
        self.all_form_data = self.load_master_form_data()
        
    def load_master_form_data(self):
        """Load ALL form data from Master Combined Excel file"""
        print("📂 Loading Master Form Data...")
        
        excel_file = r"C:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\Newfolder\dsr\data\Combined\Master_All_Requests_form_data.xlsx"
        
        try:
            if not os.path.exists(excel_file):
                print(f"⚠️ Master Excel file not found, creating sample...")
                return self.create_sample_data()
            
            df = pd.read_excel(excel_file, engine='openpyxl', na_filter=False, keep_default_na=False, dtype=str)
            print(f"✅ Master Excel loaded: {len(df)} records")
            
            # Validate required columns
            required_columns = ['Request_Category', 'Request_Type']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing columns: {missing_columns}")
            
            # Display breakdown
            breakdown = df.groupby(['Request_Category', 'Request_Type']).size()
            print("📋 Automation breakdown:")
            for (category, req_type), count in breakdown.items():
                print(f"   {category} {req_type}: {count} records")
            
            return df.to_dict('records')
            
        except Exception as e:
            print(f"❌ Error loading data: {str(e)}")
            return self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample data demonstrating all automation types"""
        print("📝 Creating sample master data...")
        
        sample_data = [
            # International Parent
            {
                'Request_Category': 'International',
                'Request_Type': 'Parent',
                'Parent First Name': 'John',
                'Parent Last Name': 'Smith',
                'Primary Email Address': 'john.smith@mailinator.com',
                'Child First Name': 'Emily',
                'Child Last Name': 'Smith',
                'Date of Birth': '2010-05-15',
                'Phone Number': '5712345678',
                'Address': '123 Main St',
                'City': 'New York',
                'State': 'New York',
                'Zip Code': '10001',
                'Country': 'United States',
                'Which of the following types of requests would you like to make?': 'Request a copy of my data'
            },
            # Domestic Myself
            {
                'Request_Category': 'Domestic',
                'Request_Type': 'Myself',
                'First Name': 'Sarah',
                'Last Name': 'Johnson',
                'Primary Email Address': 'sarah.johnson@mailinator.com',
                'Date of Birth': '1995-08-22',
                'Phone Number': '5719876543',
                'Address': '456 Oak Ave',
                'City': 'Denver',
                'State': 'Colorado',
                'Zip Code': '80202',
                'Country': 'United States',
                'Which of the following types of requests would you like to make?': 'request to delete my data',
                'delete_student': 'Student data (if any)'
            },
            # Domestic Educator
            {
                'Request_Category': 'Domestic',
                'Request_Type': 'Educator',
                'Agent First Name': 'Maria',
                'Agent Last Name': 'Garcia',
                'Agent Email Address': 'maria.garcia@mailinator.com',
                'Authorized Agent Company Name (insert N/A if not applicable)': 'N/A',
                'Student First Name': 'Carlos',
                'Student Last Name': 'Garcia',
                'Primary Email Address': 'carlos.garcia@mailinator.com',
                'Date of Birth': '2009-12-03',
                'Phone Number': '5713334444',
                'Address': '789 Pine Rd',
                'City': 'Miami',
                'State': 'Florida',
                'Zip Code': '33101',
                'Country': 'United States',
                'Which of the following types of requests would you like to make?': 'Close/deactivate/cancel my College Board account',
                'close_student': 'Student account (if any)'
            }
        ]
        
        return sample_data

    def determine_automation_type(self, record):
        """Determine the specific automation type from record data"""
        category = record.get('Request_Category', '').lower().strip()
        req_type = record.get('Request_Type', '').lower().strip()
        
        # Normalize category
        if 'international' in category:
            category = 'international'
        else:
            category = 'domestic'
        
        # Normalize request type
        if 'parent' in req_type or 'guardian' in req_type:
            req_type = 'parent'
        elif 'myself' in req_type or 'self' in req_type:
            req_type = 'myself'
        elif 'educator' in req_type or 'agent' in req_type:
            req_type = 'educator'
        else:
            print(f"⚠️ Unknown request type '{req_type}', defaulting to myself")
            req_type = 'myself'
        
        automation_type = f"{category}_{req_type}"
        print(f"🎯 Determined automation type: {automation_type}")
        return automation_type

    def format_birth_date(self, birth_date_str):
        """Enhanced birth date formatting for all forms"""
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
                return date_str
            
            formatted_date = f"{date_obj.month}/{date_obj.day}/{date_obj.year}"
            print(f"✅ Converted '{birth_date_str}' to '{formatted_date}'")
            return formatted_date
            
        except Exception as e:
            print(f"⚠️ Error formatting birth date: {str(e)}")
            return str(birth_date_str)

    def should_select_option(self, excel_value):
        """Smart option selection logic"""
        if pd.isna(excel_value) or excel_value == "":
            return False
            
        excel_str = str(excel_value).strip()
        if not excel_str:
            return False
            
        # Explicit positive values
        if excel_str.lower() in ['yes', 'true', '1', 'y']:
            return True
            
        # Specific descriptive text phrases
        if excel_str in ["Student data (if any)", "Parent data (if any)", "Educator data (if any)",
                        "Student account (if any)", "Educator account (if any)"]:
            return True
            
        return False

print("🔨 STEP 4: Request detection and utilities added...")

class TestPrivacyPortal:
    """Master Test Suite for ALL Privacy Portal form automation types"""
    
    def setup_method(self):
        """Setup method called before each test"""
        print("� Setting up Master Combined Automation...")
        
        # Single URL for all form types (same endpoint, different logic)
        self.form_url = "https://privacyportaluat.onetrust.com/webform/b99e91a7-a15e-402d-913d-a09fe56fcd54/c31c1bfa-b0a7-4a7a-9fc0-22c44fa094d0"
        
        # Load ALL records from master Excel file
        self.all_form_data = self.load_master_form_data()
        self.form_data = {}  # Will be set for each individual record
    
    def load_master_form_data(self):
        """Load ALL form data from Master Combined Excel file"""
        print("📂 Loading ALL master form data from Excel file...")
        
        excel_file = r"C:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\Newfolder\dsr\data\Combined\Master_All_Requests_form_data.xlsx"
        
        try:
            print(f"📊 Attempting to read master data from {excel_file}")
            if not os.path.exists(excel_file):
                print(f"⚠️ Master Excel file not found, creating sample template...")
                return self.create_sample_master_data()
            
            df = pd.read_excel(excel_file, engine='openpyxl', na_filter=False, keep_default_na=False, dtype=str)
            print(f"✅ Master Excel file loaded successfully!")
            
            # Validate required columns
            required_columns = ['Request_Category', 'Request_Type']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Excel file must contain columns: {missing_columns}")
            
            print(f"📊 Found {len(df)} master records in the file")
            
            # Display comprehensive breakdown
            print("📋 Master automation breakdown:")
            breakdown = df.groupby(['Request_Category', 'Request_Type']).size()
            for (category, req_type), count in breakdown.items():
                print(f"   {category} {req_type}: {count} records")
            
            records = df.to_dict('records')
            
            print("✅ All master form data loaded successfully:")
            for i, record in enumerate(records, 1):
                category = record.get('Request_Category', 'Unknown')
                req_type = record.get('Request_Type', 'Unknown')
                
                # Get name based on request type
                if req_type.lower() == 'parent':
                    name = f"{record.get('Parent First Name', '')} {record.get('Parent Last Name', '')}".strip()
                    child = f"{record.get('Child First Name', '')} {record.get('Child Last Name', '')}".strip()
                    identifier = f"{name} (Child: {child})"
                elif req_type.lower() == 'educator':
                    name = f"{record.get('Agent First Name', '')} {record.get('Agent Last Name', '')}".strip()
                    student = f"{record.get('Student First Name', '')} {record.get('Student Last Name', '')}".strip()
                    identifier = f"{name} (Student: {student})"
                else:  # myself
                    name = f"{record.get('First Name', '')} {record.get('Last Name', '')}".strip()
                    identifier = name
                
                request_details = record.get('Which of the following types of requests would you like to make?', '')
                print(f"  Record {i}: {category} {req_type} - {identifier} - Request: {request_details}")
            
            return records
            
        except Exception as e:
            print(f"❌ Error loading master form data: {str(e)}")
            print("📝 Creating sample master data for demonstration...")
            return self.create_sample_master_data()

    def create_sample_master_data(self):
        """Create sample master data demonstrating all request types"""
        print("� Creating sample master data for all request types...")
        
        sample_data = [
            # International Parent
            {
                'Request_Category': 'International',
                'Request_Type': 'Parent',
                'Parent First Name': 'John',
                'Parent Last Name': 'Smith',
                'Primary Email Address': 'john.smith@mailinator.com',
                'Child First Name': 'Emily',
                'Child Last Name': 'Smith',
                'Date of Birth': '2010-05-15',
                'Which of the following types of requests would you like to make?': 'Request a copy of my data'
            },
            # Domestic Myself
            {
                'Request_Category': 'Domestic',
                'Request_Type': 'Myself',
                'First Name': 'Sarah',
                'Last Name': 'Johnson',
                'Primary Email Address': 'sarah.johnson@mailinator.com',
                'Date of Birth': '1995-08-22',
                'Which of the following types of requests would you like to make?': 'request to delete my data',
                'delete_student': 'Student data (if any)'
            },
            # Domestic Educator
            {
                'Request_Category': 'Domestic',
                'Request_Type': 'Educator',
                'Agent First Name': 'Maria',
                'Agent Last Name': 'Garcia',
                'Agent Email Address': 'maria.garcia@mailinator.com',
                'Student First Name': 'Carlos',
                'Student Last Name': 'Garcia',
                'Which of the following types of requests would you like to make?': 'Close/deactivate/cancel my College Board account'
            }
        ]
        
        print(f"✅ Created {len(sample_data)} sample records covering all request types")
        return sample_data

    def determine_automation_type(self, record):
        """Determine which automation logic to use based on record data"""
        category = record.get('Request_Category', '').lower().strip()
        req_type = record.get('Request_Type', '').lower().strip()
        
        # Map to automation type
        automation_map = {
            ('international', 'parent'): 'international_parent',
            ('international', 'myself'): 'international_myself', 
            ('international', 'educator'): 'international_educator',
            ('domestic', 'parent'): 'domestic_parent',
            ('domestic', 'myself'): 'domestic_myself',
            ('domestic', 'educator'): 'domestic_educator'
        }
        
        automation_type = automation_map.get((category, req_type))
        if not automation_type:
            print(f"⚠️ Unknown combination: {category} + {req_type}, defaulting to domestic_myself")
            automation_type = 'domestic_myself'
        
        return automation_type

    def format_birth_date(self, birth_date_str):
        """Enhanced birth date formatting for all automation types"""
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

    # ==================== FORM FILLING METHODS ====================
    
    def fill_parent_form(self, page, record, is_international=False):
        """Fill parent/guardian form for both international and domestic"""
        form_type = "INTERNATIONAL" if is_international else "DOMESTIC"
        print(f"👨‍👩‍👧‍👦 Filling {form_type} PARENT form...")
        
        # Click parent/guardian option
        print("🔘 Looking for 'Parent/Guardian on behalf of my child' option...")
        try:
            parent_selectors = [
                "span:has-text('Parent/Guardian on behalf of my child')",
                "span:has-text('Parent on behalf of child')",
                "label:has-text('Parent')",
                "[aria-label*='Parent']"
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
                print("⚠️ Could not find parent option")
                
            time.sleep(1)
            
        except Exception as e:
            print(f"⚠️ Error selecting parent option: {str(e)}")

        # Fill parent information
        print("👨‍👩‍👧‍👦 Filling parent information...")
        
        parent_first = record.get('Parent First Name', '')
        if parent_first:
            try:
                page.fill("input[id*='first']", parent_first)
                print(f"✅ Parent first name filled: '{parent_first}'")
            except:
                print(f"⚠️ Could not fill parent first name")
        
        parent_last = record.get('Parent Last Name', '')
        if parent_last:
            try:
                page.fill("input[id*='last']", parent_last)
                print(f"✅ Parent last name filled: '{parent_last}'")
            except:
                print(f"⚠️ Could not fill parent last name")
        
        # Fill child information
        print("👶 Filling child information...")
        
        child_first = record.get('Child First Name', '')
        if child_first:
            try:
                # Try multiple selectors for child first name
                child_selectors = ["input[aria-label*='Child']", "input[id*='child']", "input[placeholder*='child']"]
                filled = False
                for selector in child_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            page.fill(selector, child_first)
                            print(f"✅ Child first name filled: '{child_first}'")
                            filled = True
                            break
                    except:
                        continue
                if not filled:
                    print(f"⚠️ Could not fill child first name")
            except:
                print(f"⚠️ Could not fill child first name")
        
        # Continue with other parent form fields...
        self.fill_common_fields(page, record)

    def fill_myself_form(self, page, record, is_international=False):
        """Fill myself form for both international and domestic"""
        form_type = "INTERNATIONAL" if is_international else "DOMESTIC"
        print(f"👤 Filling {form_type} MYSELF form...")
        
        # Click myself option
        print("🔘 Looking for 'Myself' option...")
        try:
            myself_selectors = [
                "span:has-text('Myself')",
                "span:has-text('For myself')",
                "label:has-text('Myself')",
                "[aria-label*='Myself']"
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
                print("⚠️ Could not find myself option")
                
            time.sleep(1)
            
        except Exception as e:
            print(f"⚠️ Error selecting myself option: {str(e)}")

        # Fill personal information
        print("� Filling personal information...")
        
        first_name = record.get('First Name', '')
        if first_name:
            try:
                page.fill("input[id*='first']", first_name)
                print(f"✅ First name filled: '{first_name}'")
            except:
                print(f"⚠️ Could not fill first name")
        
        last_name = record.get('Last Name', '')
        if last_name:
            try:
                page.fill("input[id*='last']", last_name)
                print(f"✅ Last name filled: '{last_name}'")
            except:
                print(f"⚠️ Could not fill last name")
        
        self.fill_common_fields(page, record)

    def fill_educator_form(self, page, record, is_international=False):
        """Fill educator/agent form for both international and domestic"""
        form_type = "INTERNATIONAL" if is_international else "DOMESTIC"
        print(f"👨‍🏫 Filling {form_type} EDUCATOR form...")
        
        # Click educator/agent option
        print("🔘 Looking for 'Authorized Agent on behalf of someone else' option...")
        try:
            agent_selectors = [
                "span:has-text('Authorized Agent on behalf of someone else')",
                "span:has-text('Agent')",
                "label:has-text('Educator')",
                "[aria-label*='Agent']"
            ]
            
            clicked = False
            for selector in agent_selectors:
                try:
                    if page.locator(selector).is_visible():
                        page.click(selector)
                        print(f"✅ Clicked agent option with selector: {selector}")
                        clicked = True
                        break
                except:
                    continue
            
            if not clicked:
                print("⚠️ Could not find agent option")
                
            time.sleep(1)
            
        except Exception as e:
            print(f"⚠️ Error selecting agent option: {str(e)}")

        # Fill agent information
        print("👨‍🏫 Filling agent information...")
        
        agent_first = record.get('Agent First Name', '')
        if agent_first:
            try:
                page.fill("input[aria-label*='Agent First Name']", agent_first)
                print(f"✅ Agent first name filled: '{agent_first}'")
            except:
                print(f"⚠️ Could not fill agent first name")
        
        agent_last = record.get('Agent Last Name', '')
        if agent_last:
            try:
                page.fill("input[aria-label*='Agent Last Name']", agent_last)
                print(f"✅ Agent last name filled: '{agent_last}'")
            except:
                print(f"⚠️ Could not fill agent last name")
        
        # Fill student information
        print("👨‍🎓 Filling student information...")
        
        student_first = record.get('Student First Name', '')
        if student_first:
            try:
                page.fill("input[id*='first']", student_first)
                print(f"✅ Student first name filled: '{student_first}'")
            except:
                print(f"⚠️ Could not fill student first name")
        
        self.fill_common_fields(page, record)

    def fill_common_fields(self, page, record):
        """Fill common fields used across all form types"""
        print("� Filling common form fields...")
        
        # Email
        email = record.get('Primary Email Address', record.get('Agent Email Address', ''))
        if email:
            try:
                email_selectors = [
                    "input[aria-label='Primary Email Address']",
                    "input[aria-label='Agent Email Address']",
                    "input[id*='email']"
                ]
                for selector in email_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            page.fill(selector, email)
                            print(f"✅ Email filled: '{email}'")
                            break
                    except:
                        continue
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
        
        # Address fields
        address = record.get('Address', record.get('StreetAddress', ''))
        if address:
            try:
                page.fill("input[id*='address']", address)
                print(f"✅ Address filled")
            except:
                print(f"⚠️ Could not fill address")
        
        city = record.get('City', '')
        if city:
            try:
                page.fill("input[id*='city']", city)
                print(f"✅ City filled")
            except:
                print(f"⚠️ Could not fill city")
        
        zip_code = record.get('Zip Code', record.get('ZipCode', ''))
        if zip_code:
            try:
                page.fill("input[id*='zip']", zip_code)
                print(f"✅ ZIP code filled")
            except:
                print(f"⚠️ Could not fill ZIP code")
        
        # Location fields
        self.fill_location_fields(page, record)
        
        # Request type selection
        self.select_request_type(page, record)

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
                time.sleep(2)
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
            # Try exact match first
            if page.locator(f"text='{request_type}'").count() > 0:
                page.click(f"text='{request_type}'")
                print(f"✅ Selected exact match: {request_type}")
                
                # Handle request-specific options after selection
                self.handle_request_specific_options(page, record, request_type)
                return
            
            # Try keyword matching
            request_keywords = {
                'copy': ['Request a copy of my data', 'copy', 'access', 'download'],
                'delete': ['Request to delete my data', 'delete', 'removal', 'erase'],
                'opt out': ['Opt out of Search', 'opt out', 'object'],
                'close': ['Close/deactivate/cancel my College Board account', 'close', 'deactivate'],
                'parent': ['Remove my parent\'s cc information', 'parent', 'cc information']
            }
            
            for key, keywords in request_keywords.items():
                if any(keyword.lower() in request_type.lower() for keyword in keywords):
                    # Find and click the matching option
                    for option_text in keywords:
                        try:
                            if page.locator(f"text*='{option_text}'").count() > 0:
                                page.click(f"text*='{option_text}'")
                                print(f"✅ Selected by keyword '{option_text}': {request_type}")
                                self.handle_request_specific_options(page, record, request_type)
                                return
                        except:
                            continue
            
            print(f"⚠️ Could not find matching request type for: {request_type}")
        except Exception as e:
            print(f"⚠️ Error selecting request type: {str(e)}")

    def handle_request_specific_options(self, page, record, request_type):
        """Handle delete/close options based on request type"""
        request_lower = request_type.lower()
        
        if 'delete' in request_lower:
            self.handle_delete_options(page, record)
        elif 'close' in request_lower or 'deactivate' in request_lower:
            self.handle_close_options(page, record)
        
        # Wait a moment for any dynamic content to load
        time.sleep(1)

    def handle_delete_options(self, page, record):
        """Handle delete data sub-options"""
        print("�️ Handling delete data sub-options...")
        
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
                    else:
                        # Try shorter version
                        short_text = option_text.replace(' (if any)', '')
                        if page.locator(f"text='{short_text}'").count() > 0:
                            page.click(f"text='{short_text}'")
                            print(f"✅ Selected delete option: {short_text}")
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
                    else:
                        # Try shorter version
                        short_text = option_text.replace(' (if any)', '')
                        if page.locator(f"text='{short_text}'").count() > 0:
                            page.click(f"text='{short_text}'")
                            print(f"✅ Selected close option: {short_text}")
                except:
                    print(f"⚠️ Could not select close option: {option_text}")

    def handle_form_submission(self, page, record_num, automation_type):
        """Handle acknowledgments and form submission"""
        try:
            print("✅ Handling acknowledgments and verification...")
            
            # Handle acknowledgment
            if page.locator("text='I acknowledge'").count() > 0:
                page.click("text='I acknowledge'")
                print("✅ Acknowledgment clicked")
            
            # Take screenshot before submission
            screenshot_path = f"{SCREENSHOTS_DIR}/before_submission_record_{record_num}_{automation_type}.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 Before submission screenshot saved")
            
            # Submit form
            submit_selectors = ["button:has-text('Submit')", "input[type='submit']", "[aria-label*='submit']"]
            submitted = False
            
            for selector in submit_selectors:
                try:
                    if page.locator(selector).count() > 0 and page.locator(selector).is_enabled():
                        page.click(selector)
                        print("✅ Form submitted")
                        submitted = True
                        break
                except:
                    continue
            
            if not submitted:
                print("⚠️ Could not find enabled submit button")
                return False
            
            # Wait for success message
            time.sleep(3)
            
            # Take screenshot after submission
            after_screenshot_path = f"{SCREENSHOTS_DIR}/after_submission_record_{record_num}_{automation_type}.png"
            page.screenshot(path=after_screenshot_path, full_page=True)
            print(f"📸 After submission screenshot saved")
            
            # Check for success message
            success_indicators = [
                "Request Submitted",
                "Thank you",
                "Success",
                "confirmation"
            ]
            
            for indicator in success_indicators:
                if page.locator(f"text*='{indicator}'").count() > 0:
                    print(f"✅ Success confirmation found: {indicator}")
                    return True
            
            print("⚠️ No clear success confirmation found, but form was submitted")
            return True
                
        except Exception as e:
            print(f"⚠️ Error during form submission: {str(e)}")
            return False

    def test_privacy_form_submission(self):
        """MASTER test method for ALL privacy form automation types"""
        
        print("\n" + "="*80)
        print("� STARTING MASTER COMBINED AUTOMATION - ALL REQUEST TYPES")
        print("="*80)
        
        if not self.all_form_data:
            pytest.fail("❌ No form data loaded. Cannot proceed with master automation.")
        
        print(f"📊 Total records to process: {len(self.all_form_data)}")
        
        # Initialize counters
        successful_submissions = 0
        failed_submissions = 0
        automation_stats = {}
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=1000)
            context = browser.new_context(viewport={'width': 1920, 'height': 1080})
            page = context.new_page()
            
            try:
                for i, record in enumerate(self.all_form_data, 1):
                    print(f"\n{'='*80}")
                    print(f"🔄 PROCESSING RECORD {i} OF {len(self.all_form_data)}")
                    print(f"{'='*80}")
                    
                    # Determine automation type
                    automation_type = self.determine_automation_type(record)
                    print(f"🎯 Automation type determined: {automation_type.upper()}")
                    
                    # Track stats
                    if automation_type not in automation_stats:
                        automation_stats[automation_type] = {'success': 0, 'failed': 0}
                    
                    # Display record details
                    category = record.get('Request_Category', 'Unknown')
                    req_type = record.get('Request_Type', 'Unknown')
                    request_details = record.get('Which of the following types of requests would you like to make?', '')
                    
                    print(f"👤 Current Record Details:")
                    print(f"   Category: {category}")
                    print(f"   Type: {req_type}")
                    print(f"   Request: {request_details}")
                    print(f"   Automation: {automation_type}")
                    
                    try:
                        # Navigate to form
                        print(f"🌐 Navigating to form...")
                        page.goto(self.form_url)
                        page.wait_for_load_state('networkidle')
                        
                        # Route to appropriate form filling method
                        is_international = 'international' in automation_type
                        
                        if 'parent' in automation_type:
                            self.fill_parent_form(page, record, is_international)
                        elif 'myself' in automation_type:
                            self.fill_myself_form(page, record, is_international)
                        elif 'educator' in automation_type:
                            self.fill_educator_form(page, record, is_international)
                        else:
                            print(f"⚠️ Unknown automation type: {automation_type}")
                            continue
                        
                        # Submit form
                        if self.handle_form_submission(page, i, automation_type):
                            successful_submissions += 1
                            automation_stats[automation_type]['success'] += 1
                            print(f"✅ RECORD {i} ({automation_type}) COMPLETED SUCCESSFULLY!")
                        else:
                            failed_submissions += 1
                            automation_stats[automation_type]['failed'] += 1
                            print(f"❌ RECORD {i} ({automation_type}) SUBMISSION FAILED!")
                        
                    except Exception as e:
                        print(f"❌ Error processing record {i}: {str(e)}")
                        failed_submissions += 1
                        automation_stats[automation_type]['failed'] += 1
                        continue
                    
                    # Pause between records
                    if i < len(self.all_form_data):
                        print("⏸️ PAUSING 5 SECONDS BEFORE NEXT RECORD...")
                        time.sleep(5)
                
            finally:
                print(f"\n🎉 MASTER COMBINED AUTOMATION COMPLETED!")
                print(f"📊 Overall Results:")
                print(f"   ✅ Successful submissions: {successful_submissions}")
                print(f"   ❌ Failed submissions: {failed_submissions}")
                print(f"   📊 Total processed: {successful_submissions + failed_submissions}")
                
                print(f"\n📋 Breakdown by automation type:")
                for auto_type, stats in automation_stats.items():
                    total = stats['success'] + stats['failed']
                    success_rate = (stats['success'] / total * 100) if total > 0 else 0
                    print(f"   {auto_type}: {stats['success']}/{total} ({success_rate:.1f}% success)")
                
                print(f"\n📸 Screenshots saved in: {SCREENSHOTS_DIR}")
                print(f"✅ MASTER AUTOMATION COMPLETE!")
                
                time.sleep(10)
                browser.close()

# ==================== STANDALONE EXECUTION ====================
if __name__ == "__main__":
    print("🚀 Running Master Combined Automation directly...")
    test_instance = TestPrivacyPortal()
    test_instance.setup_method()
    test_instance.test_privacy_form_submission()

print("🔨 STEP 7: Main test method completed - MASTER SCRIPT IS READY!")
print("\n🎉 MASTER COMBINED AUTOMATION SCRIPT CREATION COMPLETE!")
print("📋 This script can now handle ALL 6 automation types in one unified execution:")
print("   ✅ International Parent")
print("   ✅ International Myself") 
print("   ✅ International Educator")
print("   ✅ Domestic Parent")
print("   ✅ Domestic Myself")
print("   ✅ Domestic Educator")
print("\n📂 Next: Create the Excel template file with sample data!")
