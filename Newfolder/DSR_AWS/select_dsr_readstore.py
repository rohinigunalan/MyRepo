import boto3
import json
from decimal import Decimal
from boto3.dynamodb.conditions import Attr

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

# Directly use the specified table
selected_table_name = 'uat-dsr-request-handler-DsrReadStore'
print(f"\nQuerying table: {selected_table_name}")

# Get the table
table = dynamodb.Table(selected_table_name)

# Query the table with filters
print(f"\n=== Querying table: {selected_table_name} ===")
print(f"Filters: createdTimestamp = '2025-10-15T20:39:27.973Z' AND dsrRecordType IN ('499', '501')\n")

# Scan with filter expression
response = table.scan(
    FilterExpression=Attr('createdTimestamp').eq('2025-10-15T20:39:27.973Z') & 
                     (Attr('dsrRecordType').eq('499') | Attr('dsrRecordType').eq('501'))
)
items = response['Items']

# Handle pagination if there are more items
while 'LastEvaluatedKey' in response:
    response = table.scan(
        FilterExpression=Attr('createdTimestamp').eq('2025-10-15T20:39:27.973Z') & 
                         (Attr('dsrRecordType').eq('499') | Attr('dsrRecordType').eq('501')),
        ExclusiveStartKey=response['LastEvaluatedKey']
    )
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
