"""
Quick script to query APExamResponse-OAT table
Profile: cb-apexamresponse-nonprod-reader
Account: aws-apexamresponse-nonprod (6976-4355-1692)
"""
import boto3
from boto3.dynamodb.conditions import Key, Attr
import json


def main():
    PROFILE = "cb-apexamresponse-nonprod-reader"
    TABLE_NAME = "APExamResponse-OAT"

    print(f"Connecting to DynamoDB...")
    print(f"Profile: {PROFILE}")
    print(f"Table: {TABLE_NAME}")
    print("-" * 60)

    # Create session with the profile (will prompt for MFA if needed)
    session = boto3.Session(profile_name=PROFILE)
    dynamodb = session.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(TABLE_NAME)

    # Get table info
    print(f"\n✓ Connected to table: {table.table_name}")
    print(f"  Status: {table.table_status}")
    print(f"  Item count: {table.item_count}")
    print(f"  Primary key: {table.key_schema}")

    # Scan first 10 items
    print(f"\n📊 Scanning first 10 items...")
    response = table.scan(Limit=10)
    items = response.get('Items', [])

    print(f"\n✓ Found {len(items)} items\n")

    if items:
        # Show keys from first item
        first_item = items[0]
        print(f"Attributes in table:")
        for key in sorted(first_item.keys()):
            value = first_item[key]
            value_type = type(value).__name__
            print(f"  - {key}: {value_type}")

        # Show all items
        print(f"\n{'='*60}")
        print(f"ITEMS:")
        print(f"{'='*60}")
        for i, item in enumerate(items, 1):
            print(f"\n{i}. Item:")
            print(json.dumps(item, indent=2, default=str))

    else:
        print("No items found in table")

    # Show total count
    print(f"\n{'='*60}")
    print(f"Total items in table: {table.item_count}")
    print(f"{'='*60}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"\nError type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
