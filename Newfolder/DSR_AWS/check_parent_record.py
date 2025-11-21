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
table = dynamodb.Table(selected_table_name)

# Get all parent records
request_id = 'IntTest-RequestId-abc123'
print(f"Searching for parent record with requestId: {request_id}")

# Fetch ALL parent records
print("Fetching all parent records...")
response = table.scan(
    FilterExpression=Attr('dsrRecordType').eq('DSR')
)
all_parents = response['Items']

while 'LastEvaluatedKey' in response:
    response = table.scan(
        FilterExpression=Attr('dsrRecordType').eq('DSR'),
        ExclusiveStartKey=response['LastEvaluatedKey']
    )
    all_parents.extend(response['Items'])

print(f"Total parent records found: {len(all_parents)}")

# Find the specific parent
parent = None
for p in all_parents:
    if p.get('requestId') == request_id:
        parent = p
        break

if parent:
    print(f"\nParent Record Found:")
    print(json.dumps(parent, indent=2, default=decimal_default))
else:
    print(f"\nNo parent record found for requestId: {request_id}")
