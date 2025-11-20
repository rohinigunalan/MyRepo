import boto3
import json
from decimal import Decimal

# Helper function to convert Decimal to standard Python types
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

# AWS CLI profile name
aws_profile = 'cb-data-subject-rights-nonprod-dev-cli'

# Initialize the session with the specified profile
session = boto3.Session(profile_name=aws_profile)

# Create a DynamoDB client
dynamodb = session.resource('dynamodb')
dynamodb_client = session.client('dynamodb')

# List all available tables
print("\n=== Available DynamoDB Tables ===")
tables = dynamodb_client.list_tables()
table_names = tables['TableNames']

for idx, table_name in enumerate(table_names, 1):
    print(f"{idx}. {table_name}")

# Prompt user to select a table
print("\nEnter the number of the table you want to query: ", end='')
table_choice = int(input())

if table_choice < 1 or table_choice > len(table_names):
    print("Invalid choice!")
    exit(1)

selected_table_name = table_names[table_choice - 1]
print(f"\nSelected table: {selected_table_name}")

# Get the table
table = dynamodb.Table(selected_table_name)

# Scan the table to retrieve all items
print(f"\n=== Scanning table: {selected_table_name} ===\n")
response = table.scan()
items = response['Items']

# Handle pagination if there are more items
while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    items.extend(response['Items'])

# Display the results
print(f"Total records found: {len(items)}\n")

if len(items) > 0:
    # Print each item in a readable format
    for idx, item in enumerate(items, 1):
        print(f"\n--- Record {idx} ---")
        print(json.dumps(item, indent=2, default=decimal_default))
else:
    print("No records found in the table.")
