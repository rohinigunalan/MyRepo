"""
Query APExamResponse-OAT with cached credentials
Uses AWS profile directly - only prompts for MFA once, then caches for session duration
Usage: python query_apexam_cached.py <pKey> <cbExamCode> <adminYear>
"""
import boto3
from boto3.dynamodb.conditions import Key, Attr
import sys
import json


def query_data(pkey, cb_exam_code, admin_year):
    """Query DynamoDB using cached profile credentials."""
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

    # Use profile directly - AWS will handle MFA and caching
    # First time: prompts for MFA
    # Subsequent calls: uses cached credentials
    session = boto3.Session(profile_name=PROFILE)
    dynamodb = session.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(TABLE_NAME)

    print("Querying (may prompt for MFA on first use)...\n")

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
        print("Usage: python query_apexam_cached.py <pKey> <cbExamCode> <adminYear>")
        print("\nExample:")
        print("  python query_apexam_cached.py 4443Y7XU 94 26")
        print("\nNote:")
        print("  - First run will prompt for MFA")
        print("  - Subsequent runs use cached credentials (valid ~1 hour)")
        print("  - No need to provide MFA code in command!")
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

        if "MultiFactorAuthentication" in str(e) or "ExpiredToken" in str(e):
            print("\nTip: Your cached credentials may have expired.")
            print("Run this command to refresh:")
            print("  aws sts get-caller-identity --profile cb-apexamresponse-nonprod-reader")

        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
