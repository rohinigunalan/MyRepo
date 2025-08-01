#!/usr/bin/env python3
"""Fix the corrupted section in the main script"""

def fix_corrupted_script():
    file_path = 'dsr/scripts/International_educator_requesttypes_submission_MULTIPLE.py'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the corrupted section
    corrupted_pattern = '''        print("� Selecting request type based on Excel data...")
        request_type_from_excel = str(self.form_data.get('Request_type', '')).strip().lower()
        print(f"🎯 Request type from Excel: '{request_type_from_excel}'")
        
        # Map Excel request types to form options
        print("✅ Request type selection completed")
        time.sleep(2)
                    print(f"  Option {i+1}: Error reading - {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"⚠️ Error finding radio elements: {str(e)}")
            available_options = []'''
    
    fixed_content = '''        # Find all available radio button options on the form
        print("🔍 Finding available request type options on form...")
        available_options = []
        
        try:
            # Look for radio button elements
            radio_elements = page.locator("input[type='radio']").all()
            print(f"🔍 Found {len(radio_elements)} radio elements")
            
            for i, radio in enumerate(radio_elements):
                try:
                    if radio.is_visible():
                        value = radio.get_attribute("value") or ""
                        name = radio.get_attribute("name") or ""
                        element_id = radio.get_attribute("id") or ""
                        
                        # Try to find associated label text
                        label_text = ""
                        try:
                            # Try multiple ways to find the label
                            if element_id:
                                label_element = page.locator(f"label[for='{element_id}']").first
                                if label_element.is_visible():
                                    label_text = label_element.inner_text() or label_element.text_content() or ""
                            
                            # If no label found by ID, try to find parent container text
                            if not label_text:
                                parent = radio.locator("..").first
                                if parent.is_visible():
                                    label_text = parent.inner_text() or parent.text_content() or ""
                        except:
                            pass
                        
                        if value or label_text:
                            option = {
                                'element': radio,
                                'value': value,
                                'label': label_text,
                                'name': name
                            }
                            available_options.append(option)
                            print(f"  Option {i+1}: '{label_text}' (value: '{value}')")
                        
                except Exception as e:
                    print(f"  Option {i+1}: Error reading - {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"⚠️ Error finding radio elements: {str(e)}")
            available_options = []'''
    
    # Apply the fix
    new_content = content.replace(corrupted_pattern, fixed_content)
    
    # Write the fixed content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Fixed the corrupted section in the main script!")
    print("✅ The script should now be ready to run!")

if __name__ == "__main__":
    fix_corrupted_script()
