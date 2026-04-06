"""
Script to query DynamoDB from aws-apexamresponse-nonprod account
Using profile: cb-apexamresponse-nonprod-reader
"""
import boto3
from boto3.dynamodb.conditions import Key, Attr
from typing import List, Dict, Any


def get_dynamodb_resource(profile_name: str = "cb-apexamresponse-nonprod-reader"):
    """
    Create DynamoDB resource with specific AWS profile.

    Args:
        profile_name: AWS profile name to use

    Returns:
        boto3 DynamoDB resource
    """
    session = boto3.Session(profile_name=profile_name)
    dynamodb = session.resource('dynamodb')
    return dynamodb


def get_dynamodb_client(profile_name: str = "cb-apexamresponse-nonprod-reader"):
    """
    Create DynamoDB client with specific AWS profile.

    Args:
        profile_name: AWS profile name to use

    Returns:
        boto3 DynamoDB client
    """
    session = boto3.Session(profile_name=profile_name)
    client = session.client('dynamodb')
    return client


def list_tables(profile_name: str = "cb-apexamresponse-nonprod-reader") -> List[str]:
    """
    List all DynamoDB tables in the account.

    Args:
        profile_name: AWS profile name to use

    Returns:
        List of table names
    """
    client = get_dynamodb_client(profile_name)
    response = client.list_tables()
    return response.get('TableNames', [])


def scan_table(
    table_name: str,
    limit: int = 100,
    filter_expression: str = None,
    profile_name: str = "cb-apexamresponse-nonprod-reader"
) -> List[Dict[str, Any]]:
    """
    Scan DynamoDB table and return items.

    Args:
        table_name: Name of the table to scan
        limit: Maximum number of items to return
        filter_expression: Optional filter expression
        profile_name: AWS profile name to use

    Returns:
        List of items from the table
    """
    dynamodb = get_dynamodb_resource(profile_name)
    table = dynamodb.Table(table_name)

    scan_kwargs = {'Limit': limit}

    if filter_expression:
        # Example: filter_expression = Attr('status').eq('active')
        scan_kwargs['FilterExpression'] = filter_expression

    response = table.scan(**scan_kwargs)
    items = response.get('Items', [])

    # Handle pagination if needed
    while 'LastEvaluatedKey' in response and len(items) < limit:
        scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
        response = table.scan(**scan_kwargs)
        items.extend(response.get('Items', []))

    return items[:limit]


def query_table(
    table_name: str,
    key_condition_expression,
    limit: int = 100,
    profile_name: str = "cb-apexamresponse-nonprod-reader"
) -> List[Dict[str, Any]]:
    """
    Query DynamoDB table with key condition.

    Args:
        table_name: Name of the table to query
        key_condition_expression: Key condition (e.g., Key('userId').eq('123'))
        limit: Maximum number of items to return
        profile_name: AWS profile name to use

    Returns:
        List of items matching the query
    """
    dynamodb = get_dynamodb_resource(profile_name)
    table = dynamodb.Table(table_name)

    response = table.query(
        KeyConditionExpression=key_condition_expression,
        Limit=limit
    )

    return response.get('Items', [])


def get_item(
    table_name: str,
    key: Dict[str, Any],
    profile_name: str = "cb-apexamresponse-nonprod-reader"
) -> Dict[str, Any]:
    """
    Get a single item from DynamoDB table.

    Args:
        table_name: Name of the table
        key: Primary key of the item (e.g., {'id': '123'})
        profile_name: AWS profile name to use

    Returns:
        Item from the table
    """
    dynamodb = get_dynamodb_resource(profile_name)
    table = dynamodb.Table(table_name)

    response = table.get_item(Key=key)
    return response.get('Item', {})


# Example usage
if __name__ == "__main__":
    # Profile to use
    PROFILE = "cb-apexamresponse-nonprod-reader"
    TABLE_NAME = "APExamResponse-OAT"

    print(f"Using AWS profile: {PROFILE}")
    print(f"Account: aws-apexamresponse-nonprod (6976-4355-1692)")
    print(f"Table: {TABLE_NAME}")
    print("-" * 60)

    try:
        # 1. List all tables
        print("\n1. Listing all DynamoDB tables:")
        tables = list_tables(PROFILE)
        for i, table in enumerate(tables, 1):
            print(f"   {i}. {table}")

        if not tables:
            print("   No tables found")

        # 2. Scan APExamResponse-OAT table
        print(f"\n2. Scanning table: {TABLE_NAME} (first 10 items)")
        items = scan_table(TABLE_NAME, limit=10, profile_name=PROFILE)
        print(f"   Found {len(items)} items")

        if items:
            # Show structure of first item
            print(f"\n   Sample item structure:")
            first_item = items[0]
            for key, value in first_item.items():
                print(f"      {key}: {type(value).__name__}")

            # Show all items
            print(f"\n   Items:")
            for i, item in enumerate(items, 1):
                print(f"   {i}. {item}")
        else:
            print("   No items found in table")

        # 3. Example: Query with key condition (uncomment if you know the partition key)
        # print(f"\n3. Querying specific item:")
        # items = query_table(
        #     TABLE_NAME,
        #     key_condition_expression=Key('examId').eq('12345'),  # Replace with actual key name
        #     limit=10,
        #     profile_name=PROFILE
        # )
        # print(f"   Found {len(items)} items")

        # 4. Example: Get specific item (uncomment if you know a specific key)
        # print(f"\n4. Getting specific item:")
        # item = get_item(
        #     TABLE_NAME,
        #     key={'examId': '12345'},  # Replace with actual partition key
        #     profile_name=PROFILE
        # )
        # print(f"   Item: {item}")

        # 5. Example: Scan with filter (uncomment to filter results)
        # print(f"\n5. Scanning with filter:")
        # items = scan_table(
        #     TABLE_NAME,
        #     limit=50,
        #     filter_expression=Attr('status').eq('completed'),  # Replace with actual attribute
        #     profile_name=PROFILE
        # )
        # print(f"   Found {len(items)} items with filter")

    except Exception as e:
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you've authenticated: aws sso login --profile cb-apexamresponse-nonprod-reader")
        print("2. Or if using MFA, it will prompt when running")
        print("3. Check that you have read permissions for the table")
