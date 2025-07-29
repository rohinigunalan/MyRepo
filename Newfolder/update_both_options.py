import pandas as pd

# Read current CSV
df = pd.read_csv('form_data.csv')

# Update the delete options based on user requirement:
# Both student and parent have data (should be selected)
# Educator has no data (should not be selected)
df.loc[0, 'delete_student'] = 'Student data (if any)'  # Has data - select it
df.loc[0, 'delete_parent'] = 'Parent data (if any)'    # Has data - select it  
df.loc[0, 'delete_educator'] = ''                       # No data - don't select

# Save the updated CSV
df.to_csv('form_data.csv', index=False)

print("Updated delete options to match Excel:")
print(f"delete_student: '{df.loc[0, 'delete_student']}'")
print(f"delete_parent: '{df.loc[0, 'delete_parent']}'")
print(f"delete_educator: '{df.loc[0, 'delete_educator']}'")
print("CSV file updated successfully!")
