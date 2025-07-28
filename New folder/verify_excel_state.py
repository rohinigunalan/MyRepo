import pandas as pd

print("=== EXCEL STATE VERIFICATION ===")

# Load Excel file
df = pd.read_excel('form_data.xlsx')
state = df.iloc[0]['stateOrProvince']

print(f"State in Excel: '{state}'")
print(f"State type: {type(state)}")
print(f"State length: {len(str(state))}")

# Test the exact logic used in the script
test_state = str(df.iloc[0].to_dict().get('stateOrProvince', 'New York'))
print(f"Processed state: '{test_state}'")

if state != "New York":
    print("⚠️  WARNING: Excel file does not contain 'New York'!")
    print("This explains why Alabama might be selected instead.")
    print("The state in Excel should be changed to 'New York' if that's what you want.")
else:
    print("✅ Excel file correctly contains 'New York'")
