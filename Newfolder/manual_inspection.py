from playwright.sync_api import sync_playwright
import time

def manual_form_inspection():
    """Open the form and pause for manual inspection and filling"""
    with sync_playwright() as p:
        # Launch browser in non-headless mode
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        
        # Navigate to the privacy portal
        url = "https://privacyportaluat.onetrust.com/webform/b99e91a7-a15e-402d-913d-a09fe56fcd54/c31c1bfa-b0a7-4a7a-9fc0-22c44fa094d0"
        print(f"🌐 Opening: {url}")
        page.goto(url)
        
        # Wait for page to load
        page.wait_for_load_state("networkidle")
        time.sleep(3)
        
        print("\n" + "="*80)
        print("🔍 MANUAL INSPECTION MODE")
        print("="*80)
        print("1. The browser is now open with the privacy portal form")
        print("2. Please fill out the form manually with your data")
        print("3. I'll list all form elements below for reference")
        print("4. The browser will stay open for 5 minutes")
        print("5. Take screenshots as you go if needed")
        print("="*80 + "\n")
        
        # List all form elements for reference
        print("📋 FORM ELEMENTS DETECTED:")
        print("-" * 50)
        
        try:
            # Get all inputs
            inputs = page.locator("input").all()
            print(f"\n📝 INPUT FIELDS ({len(inputs)} found):")
            for i, element in enumerate(inputs):
                try:
                    name = element.get_attribute("name") or "no-name"
                    id_attr = element.get_attribute("id") or "no-id" 
                    placeholder = element.get_attribute("placeholder") or "no-placeholder"
                    input_type = element.get_attribute("type") or "text"
                    visible = element.is_visible()
                    print(f"  {i+1:2d}. Type: {input_type:10} | Name: {name:15} | ID: {id_attr:15} | Placeholder: {placeholder:20} | Visible: {visible}")
                except Exception as e:
                    print(f"  {i+1:2d}. Error reading input: {str(e)}")
            
            # Get all selects
            selects = page.locator("select").all()
            print(f"\n📋 SELECT DROPDOWNS ({len(selects)} found):")
            for i, element in enumerate(selects):
                try:
                    name = element.get_attribute("name") or "no-name"
                    id_attr = element.get_attribute("id") or "no-id"
                    visible = element.is_visible()
                    
                    # Get options
                    options = element.locator("option").all()
                    option_values = []
                    for opt in options[:5]:  # Show first 5 options
                        try:
                            value = opt.get_attribute("value") or ""
                            text = opt.inner_text() or ""
                            if value or text:
                                option_values.append(f"{value}={text}")
                        except:
                            pass
                    
                    print(f"  {i+1:2d}. Name: {name:15} | ID: {id_attr:15} | Visible: {visible}")
                    if option_values:
                        print(f"      Options: {', '.join(option_values[:3])}{'...' if len(option_values) > 3 else ''}")
                        
                except Exception as e:
                    print(f"  {i+1:2d}. Error reading select: {str(e)}")
            
            # Get all textareas
            textareas = page.locator("textarea").all()
            if textareas:
                print(f"\n📄 TEXTAREA FIELDS ({len(textareas)} found):")
                for i, element in enumerate(textareas):
                    try:
                        name = element.get_attribute("name") or "no-name"
                        id_attr = element.get_attribute("id") or "no-id"
                        placeholder = element.get_attribute("placeholder") or "no-placeholder"
                        visible = element.is_visible()
                        print(f"  {i+1:2d}. Name: {name:15} | ID: {id_attr:15} | Placeholder: {placeholder:20} | Visible: {visible}")
                    except Exception as e:
                        print(f"  {i+1:2d}. Error reading textarea: {str(e)}")
            
            # Get all buttons
            buttons = page.locator("button").all()
            if buttons:
                print(f"\n🔘 BUTTONS ({len(buttons)} found):")
                for i, element in enumerate(buttons):
                    try:
                        text = element.inner_text() or "no-text"
                        button_type = element.get_attribute("type") or "button"
                        visible = element.is_visible()
                        print(f"  {i+1:2d}. Type: {button_type:10} | Text: {text:20} | Visible: {visible}")
                    except Exception as e:
                        print(f"  {i+1:2d}. Error reading button: {str(e)}")
                        
        except Exception as e:
            print(f"❌ Error during element inspection: {str(e)}")
        
        print("\n" + "="*80)
        print("⏰ KEEPING BROWSER OPEN FOR 5 MINUTES")
        print("You can now:")
        print("- Fill the form manually")
        print("- Note which fields work/don't work") 
        print("- Take screenshots")
        print("- Test dropdown interactions")
        print("="*80)
        
        # Keep browser open for 5 minutes
        countdown = 300  # 5 minutes
        while countdown > 0:
            minutes = countdown // 60
            seconds = countdown % 60
            print(f"\r⏱️  Time remaining: {minutes:02d}:{seconds:02d} ", end="", flush=True)
            time.sleep(1)
            countdown -= 1
        
        print("\n\n🏁 Session completed. Browser will close in 5 seconds...")
        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    manual_form_inspection()
