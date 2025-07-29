import pandas as pd

# Read current CSV
df = pd.read_csv('form_data.csv')

# Update the delete options based on user requirement
df.loc[0, 'delete_student'] = 'no'  # Don't select student data
df.loc[0, 'delete_parent'] = 'yes'  # Select parent data (will need text input)
df.loc[0, 'delete_educator'] = 'no'  # Don't select educator data

# Save the updated CSV
df.to_csv('form_data.csv', index=False)

print("Updated delete options:")
print(f"delete_student: {df.loc[0, 'delete_student']}")
print(f"delete_parent: {df.loc[0, 'delete_parent']}")
print(f"delete_educator: {df.loc[0, 'delete_educator']}")
print("CSV file updated successfully!")
