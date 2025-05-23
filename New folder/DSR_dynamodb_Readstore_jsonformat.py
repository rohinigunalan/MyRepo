import boto3
import json
from boto3.dynamodb.conditions import Key
from decimal import Decimal

# AWS CLI profile name
aws_profile = 'cb-data-subject-rights-nonprod-dev-cli'

# Initialize the session with the specified profile
session = boto3.Session(profile_name=aws_profile)

# Create a DynamoDB resource
dynamodb = session.resource('dynamodb')

# Replace 'YourTableName' with your actual DynamoDB table name
table_name = 'uat-dsr-request-handler-DsrReadStore'
table = dynamodb.Table(table_name)

# Query for the item with specific login and password
response = table.query(
    KeyConditionExpression=Key('RequestId').eq('76070532-bc3b-46d6-9608-597e2180bd0f') & Key('DsrRecordType').eq('130')
)

# Get the items from the response
items = response['Items']

# Function to convert Decimal objects to float
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

# Convert the items to JSON format
json_data = json.dumps(items, indent=4, default=decimal_default)

# Print the JSON data
print(json_data)