import pandas as pd
import numpy as np

# Read CSV with specific handling for N/A values
# We want to keep "N/A" as text, not convert to NaN
df = pd.read_csv('form_data.csv', keep_default_na=False, na_values=[''])

# Check current educator field value
current_value = df.loc[0, 'educatorSchoolAffiliation']
print(f"Current educatorSchoolAffiliation: '{current_value}' (type: {type(current_value)})")

# Update the educator field to be "N/A" if it's currently nan or empty
if pd.isna(current_value) or current_value == 'nan' or current_value == '':
    df.loc[0, 'educatorSchoolAffiliation'] = 'N/A'
    print("✅ Updated educatorSchoolAffiliation to 'N/A'")
else:
    print(f"✅ educatorSchoolAffiliation already has value: '{current_value}'")

# Save the updated CSV
df.to_csv('form_data.csv', index=False)

print("\nUpdated values:")
print(f"educatorSchoolAffiliation: '{df.loc[0, 'educatorSchoolAffiliation']}'")
print("CSV file updated successfully!")
