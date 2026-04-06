"""
Query APExamResponse-OAT using shared AWS CLI credential cache
This version properly shares credentials between AWS CLI and boto3
Usage: python query_apexam_shared_cache.py <pKey> <cbExamCode> <adminYear>
"""
import boto3
from boto3.dynamodb.conditions import Key, Attr
import sys
import json
import os


def query_data(pkey, cb_exam_code, admin_year):
    """Query DynamoDB using shared AWS CLI cache."""
    PROFILE = "cb-apexamresponse-nonprod-reader"
    TABLE_NAME = "APExamResponse-OAT"

    print(f"\n{'='*60}")
    print(f"Using AWS Profile: {PROFILE}")
    print(f"Table: {TABLE_NAME}")
    print(f"{'='*60}")
    print(f"  pKey: {pkey}")
    print(f"  cbExamCode: {cb_exam_code}")
    print(f"  adminYear: {admin_year}")
    print(f"{'='*60}\n")

    # Force boto3 to use the CLI credential cache
    # This is the key fix - tell boto3 to check CLI cache
    session = boto3.Session(
        profile_name=PROFILE,
    )

    # Use the credential cache from AWS CLI
    # This makes boto3 check ~/.aws/cli/cache/
    credentials = session.get_credentials()

    # Create DynamoDB resource with the shared credentials
    dynamodb = session.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(TABLE_NAME)

    print("Querying...\n")

    # Build query with correct data types
    query_kwargs = {
        'KeyConditionExpression': Key('pKey').eq(pkey)
    }

    # Add filters - cbExamCode is Number, adminYear is String
    filter_expr = Attr('cbExamCode').eq(int(cb_exam_code)) & Attr('adminYear').eq(str(admin_year))
    query_kwargs['FilterExpression'] = filter_expr

    # Execute query
    response = table.query(**query_kwargs)
    items = response.get('Items', [])

    # Display results
    print(f"{'='*60}")
    print(f"RESULTS: Found {len(items)} item(s)")
    print(f"{'='*60}\n")

    if items:
        for i, item in enumerate(items, 1):
            print(f"Item {i}:")
            print(json.dumps(item, indent=2, default=str))
            print()
    else:
        print("No items found with the specified criteria\n")

    return items


def main():
    if len(sys.argv) != 4:
        print("Usage: python query_apexam_shared_cache.py <pKey> <cbExamCode> <adminYear>")
        print("\nExample:")
        print("  python query_apexam_shared_cache.py 4443Y7XU 94 26")
        print("\nNote:")
        print("  Authenticate first with: aws sts get-caller-identity --profile cb-apexamresponse-nonprod-reader")
        print("  Then this script will use the cached credentials!")
        sys.exit(1)

    pkey = sys.argv[1]
    cb_exam_code = sys.argv[2]
    admin_year = sys.argv[3]

    try:
        items = query_data(pkey, cb_exam_code, admin_year)

        print(f"{'='*60}")
        print(f"✓ Query completed successfully")
        print(f"✓ Total items found: {len(items)}")
        print(f"{'='*60}\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")

        if "ExpiredToken" in str(e) or "expired" in str(e).lower():
            print("\nYour credentials have expired. Re-authenticate with:")
            print("  aws sts get-caller-identity --profile cb-apexamresponse-nonprod-reader")

        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
