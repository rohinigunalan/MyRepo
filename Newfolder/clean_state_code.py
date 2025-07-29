# Simple state selection code to replace the broken section

state_selection_code = '''
            # Simple state selection approach
            state_filled = False
            state_name = str(self.form_data.get('stateOrProvince', 'New York'))
            print(f"🏛️ Target state from Excel: '{state_name}'")
            
            for state_selector in state_selectors:
                try:
                    element = page.locator(state_selector).first
                    if element.is_visible():
                        print(f"🔍 Found state field: {state_selector}")
                        
                        # Simple approach: Click, clear, type, enter
                        element.click(timeout=3000)
                        time.sleep(1)
                        
                        element.fill("")
                        time.sleep(0.5)
                        
                        element.type(state_name, delay=100)
                        print(f"✅ Typed '{state_name}'")
                        
                        element.press("Enter")
                        print(f"⏎ Pressed Enter")
                        time.sleep(2)
                        
                        state_filled = True
                        break
                        
                except Exception as e:
                    print(f"❌ Error with {state_selector}: {str(e)}")
                    continue
'''

print("Clean state selection code ready for replacement")
print(state_selection_code)
