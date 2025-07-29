import pandas as pd

# Read the CSV file
df = pd.read_csv('form_data.csv')

# Get the first row
row = df.iloc[0]

print("Delete options for first row:")
print(f"delete_student: {row['delete_student']}")
print(f"delete_parent: {row['delete_parent']}")
print(f"delete_educator: {row['delete_educator']}")
print(f"Request_type: {row['Request_type']}")
