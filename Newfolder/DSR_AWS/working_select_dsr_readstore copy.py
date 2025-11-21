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
print(f"Filters: createdTimestamp < '2025-10-15T20:39:27.973Z' AND dsrRecordType IN ('499', '501')\n")

# Scan with filter expression
response = table.scan(
    FilterExpression=Attr('createdTimestamp').lt('2025-10-15T20:39:27.973Z') & 
                     (Attr('dsrRecordType').eq('499') | Attr('dsrRecordType').eq('501'))
)
items = response['Items']

# Handle pagination if there are more items
while 'LastEvaluatedKey' in response:
    response = table.scan(
        FilterExpression=Attr('createdTimestamp').lt('2025-10-15T20:39:27.973Z') & 
                         (Attr('dsrRecordType').eq('499') | Attr('dsrRecordType').eq('501')),
        ExclusiveStartKey=response['LastEvaluatedKey']
    )
    items.extend(response['Items'])

# Display the results
print(f"Total child records found: {len(items)}\n")

if len(items) > 0:
    # Get unique requestIds from the child records
    unique_request_ids = set(item['requestId'] for item in items)
    
    # Fetch ALL parent records (dsrRecordType = 'DSR') at once
    print(f"Fetching all parent records (dsrRecordType='DSR')...")
    
    parent_response = table.scan(
        FilterExpression=Attr('dsrRecordType').eq('DSR')
    )
    all_parents = parent_response['Items']
    
    # Handle pagination for parent records
    while 'LastEvaluatedKey' in parent_response:
        parent_response = table.scan(
            FilterExpression=Attr('dsrRecordType').eq('DSR'),
            ExclusiveStartKey=parent_response['LastEvaluatedKey']
        )
        all_parents.extend(parent_response['Items'])
    
    # Create a dictionary of parent records by requestId
    parent_records = {parent['requestId']: parent for parent in all_parents if 'requestId' in parent}
    
    # Filter to only parents for our request IDs
    relevant_parents = {req_id: parent_records[req_id] for req_id in unique_request_ids if req_id in parent_records}
    
    print(f"Found {len(all_parents)} total parent records in table")
    print(f"Found {len(relevant_parents)} parent records for our {len(unique_request_ids)} unique request IDs")
    print(f"Displaying all {len(items)} child records with parent status\n")
    
    # Define the columns we want to display
    display_columns = ['requestId', 'dsrRecordType', 'dsrStatus', 'parentStatus', 'action', 'createdTimestamp', 'updatedTimestamp']
    
    # Column widths
    col_widths = {
        'requestId': 25,
        'dsrRecordType': 15,
        'dsrStatus': 12,
        'parentStatus': 15,
        'action': 15,
        'createdTimestamp': 26,
        'updatedTimestamp': 26
    }
    
    # Print header
    header_parts = [f"{col:{col_widths[col]}}" for col in display_columns]
    header = " | ".join(header_parts)
    separator = "-" * len(header)
    
    print(header)
    print(separator)
    
    # Print each row with parent status
    for item in items:
        row_values = []
        request_id = item.get('requestId', '')
        parent_status = relevant_parents.get(request_id, {}).get('dsrStatus', 'N/A')
        
        for col in display_columns:
            if col == 'parentStatus':
                value_str = parent_status
            else:
                value = item.get(col, '')
                value_str = str(value) if value else ''
            
            # Truncate if needed
            max_width = col_widths[col]
            if len(value_str) > max_width:
                value_str = value_str[:max_width-3] + "..."
            row_values.append(f"{value_str:{max_width}}")
        print(" | ".join(row_values))
    
    print(f"\n{separator}")
    print(f"Total: {len(items)} child records with parent status")
else:
    print("No records found in the table.")
