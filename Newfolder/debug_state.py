import pandas as pd
import os

print("=== DEBUGGING STATE SELECTION ISSUE ===")

# Check if Excel file exists
if os.path.exists('form_data.xlsx'):
    print("✅ Excel file exists")
    
    # Load the Excel file
    df = pd.read_excel('form_data.xlsx')
    print("📊 Excel data:")
    print(df.to_string())
    
    # Check the specific state value
    state_value = df.iloc[0]['stateOrProvince']
    print(f"\n🏛️ State value: '{state_value}'")
    print(f"🏛️ State type: {type(state_value)}")
    print(f"🏛️ State repr: {repr(state_value)}")
    print(f"🏛️ State length: {len(str(state_value))}")
    
    # Test the form_data loading logic
    form_data = df.iloc[0].to_dict()
    test_state = str(form_data.get('stateOrProvince', 'New York'))
    print(f"\n🔍 Test state from form_data.get(): '{test_state}'")
    
else:
    print("❌ Excel file not found")
    
    # Check CSV as fallback
    if os.path.exists('form_data.csv'):
        print("📄 CSV file found, reading...")
        df = pd.read_csv('form_data.csv')
        print(df.to_string())
    else:
        print("❌ No CSV file either")
