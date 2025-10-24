import boto3
import json
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr

# AWS CLI profile name
aws_profile = 'cb-data-subject-rights-nonprod-dev-cli'

# Initialize the session with the specified profile
session = boto3.Session(profile_name=aws_profile)

# Create a DynamoDB resource
dynamodb = session.resource('dynamodb')

# Replace 'YourTableName' with your actual DynamoDB table name
table_name = 'uat-dsr-request-handler-DsrReadStore'
table = dynamodb.Table(table_name)

def query_by_request_id(request_id):
    """Query table by requestId (assuming it's the primary key)"""
    try:
        response = table.get_item(Key={'requestId': request_id})
        return response.get('Item')
    except Exception as e:
        print(f"Error querying by requestId: {e}")
        return None

def query_by_dsr_record_type(dsr_record_type):
    """Query table by dsrRecordType"""
    try:
        response = table.scan(
            FilterExpression=Attr('dsrRecordType').eq(dsr_record_type)
        )
        return response['Items']
    except Exception as e:
        print(f"Error querying by dsrRecordType: {e}")
        return []

def query_by_email(email_address):
    """Query table by emailAddress"""
    try:
        response = table.scan(
            FilterExpression=Attr('emailAddress').eq(email_address)
        )
        return response['Items']
    except Exception as e:
        print(f"Error querying by emailAddress: {e}")
        return []

def query_by_dsr_status(dsr_status):
    """Query table by dsrStatus"""
    try:
        response = table.scan(
            FilterExpression=Attr('dsrStatus').eq(dsr_status)
        )
        return response['Items']
    except Exception as e:
        print(f"Error querying by dsrStatus: {e}")
        return []

def query_by_name(first_name, last_name):
    """Query table by firstName and lastName"""
    try:
        response = table.scan(
            FilterExpression=Attr('firstName').eq(first_name) & Attr('lastName').eq(last_name)
        )
        return response['Items']
    except Exception as e:
        print(f"Error querying by name: {e}")
        return []

def query_by_date_range(start_date, end_date):
    """Query table by createdTimestamp date range"""
    try:
        response = table.scan(
            FilterExpression=Attr('createdTimestamp').between(start_date, end_date)
        )
        return response['Items']
    except Exception as e:
        print(f"Error querying by date range: {e}")
        return []

def scan_all_records():
    """Scan all records from the table"""
    try:
        response = table.scan()
        return response['Items']
    except Exception as e:
        print(f"Error scanning table: {e}")
        return []

def query_with_multiple_filters(filters):
    """
    Query with multiple filter conditions
    filters: dict with column names as keys and values to filter by
    Example: {'dsrStatus': 'PENDING', 'dsrRequestType': 'INFO_REQUEST'}
    """
    try:
        filter_expressions = []
        for column, value in filters.items():
            filter_expressions.append(Attr(column).eq(value))
        
        # Combine all filter expressions with AND
        combined_filter = filter_expressions[0]
        for expr in filter_expressions[1:]:
            combined_filter = combined_filter & expr
        
        response = table.scan(FilterExpression=combined_filter)
        return response['Items']
    except Exception as e:
        print(f"Error querying with multiple filters: {e}")
        return []

# Example usage
if __name__ == "__main__":
    print("DynamoDB Query for Request ID: S85GM83V9P_1")
    print("=" * 50)
    
    # Query by specific requestId
    request_id_to_search = "S85GM83V9P_1"
    print(f"\nSearching for Request ID: {request_id_to_search}")
    
    item = query_by_request_id(request_id_to_search)
    if item:
        print("\n✓ FOUND RECORD:")
        print("-" * 30)
        print(json.dumps(item, indent=2, default=str))
        
        # Display key information in a formatted way
        print("\n📋 KEY INFORMATION:")
        print("-" * 30)
        if 'requestId' in item:
            print(f"Request ID: {item['requestId']}")
        if 'dsrRecordType' in item:
            print(f"Record Type: {item['dsrRecordType']}")
        if 'dsrStatus' in item:
            print(f"Status: {item['dsrStatus']}")
        if 'dsrRequestType' in item:
            print(f"Request Type: {item['dsrRequestType']}")
        if 'emailAddress' in item:
            print(f"Email: {item['emailAddress']}")
        if 'firstName' in item and 'lastName' in item:
            print(f"Name: {item['firstName']} {item['lastName']}")
        if 'createdTimestamp' in item:
            print(f"Created: {item['createdTimestamp']}")
    else:
        print(f"\n❌ NO RECORD FOUND for Request ID: {request_id_to_search}")
        print("Double-check the Request ID or verify it exists in the table.")
    
    # Example 2: Query by dsrRecordType
    print("\n2. Query by dsrRecordType:")
    items = query_by_dsr_record_type("DSR")
    print(f"Found {len(items)} items with dsrRecordType 'DSR'")
    
    # Example 3: Query by email
    print("\n3. Query by emailAddress:")
    items = query_by_email("random.email@google.com")
    print(f"Found {len(items)} items with email 'random.email@google.com'")
    
    # Example 4: Query by status
    print("\n4. Query by dsrStatus:")
    items = query_by_dsr_status("PENDING")
    print(f"Found {len(items)} items with status 'PENDING'")
    
    # Example 5: Query by name
    print("\n5. Query by firstName and lastName:")
    items = query_by_name("RandomFirstName", "RandomLastName")
    print(f"Found {len(items)} items with name 'RandomFirstName RandomLastName'")
    
    # Example 6: Query with multiple filters
    print("\n6. Query with multiple filters:")
    filters = {
        'dsrStatus': 'PENDING',
        'dsrRequestType': 'INFO_REQUEST'
    }
    items = query_with_multiple_filters(filters)
    print(f"Found {len(items)} items matching multiple criteria")
    
    # Example 7: Scan all records (use with caution for large tables)
    print("\n7. Scan all records:")
    all_items = scan_all_records()
    print(f"Total items in table: {len(all_items)}")
    
    # Display columns available for querying
    print("\n8. Available columns for querying:")
    columns = [
        "requestId", "dsrRecordType", "action", "alternateEmail", "birthDate",
        "channels", "completionDueDate", "createdTimestamp", "dsrRequestType",
        "dsrStatus", "educatorSchoolAffiliation", "emailAddress", "firstName",
        "identifierSubtaskId", "initiationSubtaskId", "lastName", 
        "lastPublishedTimestamp", "oneTrustEventTimestamp", "phoneNumber",
        "residentialAddress", "studentGraduationYear", "students",
        "studentSchoolName", "subjects", "updatedTimestamp"
    ]
    
    for column in columns:
        print(f"  - {column}")
    
    print("\nNote: Modify the query functions above to search by any of these columns.")

