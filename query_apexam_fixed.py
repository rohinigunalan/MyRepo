"""
Query APExamResponse-OAT table - Fixed version
Usage: python query_apexam_fixed.py <MFA_CODE> <pKey> <cbExamCode> <adminYear>
"""
import boto3
from boto3.dynamodb.conditions import Key, Attr
import sys
import json
from decimal import Decimal


def get_temporary_credentials(mfa_code):
    """Get temporary credentials using MFA token."""
    session = boto3.Session(profile_name='cb-cia-admin-nonprod')
    sts_client = session.client('sts')

    response = sts_client.assume_role(
        RoleArn='arn:aws:iam::697643551692:role/HeroesReaderRole',
        RoleSessionName='claude-dynamodb-session',
        SerialNumber='arn:aws:iam::185718115448:mfa/rgunalan',
        TokenCode=mfa_code
    )

    return response['Credentials']


def query_data(credentials, pkey, cb_exam_code, admin_year):
    """Query DynamoDB table."""
    TABLE_NAME = "APExamResponse-OAT"

    session = boto3.Session(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
        region_name='us-east-1'
    )

    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)

    print(f"\n{'='*60}")
    print(f"Querying: {TABLE_NAME}")
    print(f"{'='*60}")
    print(f"  pKey: {pkey}")
    print(f"  cbExamCode: {cb_exam_code}")
    print(f"  adminYear: {admin_year}")
    print(f"{'='*60}\n")

    # Try multiple filter combinations to handle different data types
    filter_combinations = [
        # Try as integers
        (Attr('cbExamCode').eq(int(cb_exam_code)) & Attr('adminYear').eq(int(admin_year))),
        # Try as strings
        (Attr('cbExamCode').eq(str(cb_exam_code)) & Attr('adminYear').eq(str(admin_year))),
        # Try cbExamCode as int, adminYear as string
        (Attr('cbExamCode').eq(int(cb_exam_code)) & Attr('adminYear').eq(str(admin_year))),
        # Try cbExamCode as string, adminYear as int
        (Attr('cbExamCode').eq(str(cb_exam_code)) & Attr('adminYear').eq(int(admin_year))),
    ]

    items = []
    for i, filter_expr in enumerate(filter_combinations, 1):
        try:
            print(f"Attempt {i}...")
            response = table.query(
                KeyConditionExpression=Key('pKey').eq(pkey),
                FilterExpression=filter_expr
            )
            temp_items = response.get('Items', [])
            if temp_items:
                print(f"✓ Found {len(temp_items)} items with attempt {i}\n")
                items = temp_items
                break
            else:
                print(f"  No items found")
        except Exception as e:
            print(f"  Failed: {e}")

    if not items:
        print("\nNo items found with any filter combination")
        print("Trying query without filters to see what's in the table...")

        response = table.query(KeyConditionExpression=Key('pKey').eq(pkey))
        all_items = response.get('Items', [])
        print(f"\nTotal items for pKey={pkey}: {len(all_items)}")

        if all_items:
            print("\nSample of available data:")
            for item in all_items[:3]:
                print(f"  cbExamCode: {item.get('cbExamCode')} (type: {type(item.get('cbExamCode')).__name__})")
                print(f"  adminYear: {item.get('adminYear', 'N/A')} (type: {type(item.get('adminYear', 'N/A')).__name__})")
                print(f"  sKey: {item.get('sKey')}")
                print()
        return []

    # Display results
    print(f"{'='*60}")
    print(f"RESULTS: Found {len(items)} item(s)")
    print(f"{'='*60}\n")

    for i, item in enumerate(items, 1):
        print(f"Item {i}:")
        # Convert Decimal to int/float for JSON serialization
        item_clean = json.loads(json.dumps(item, default=str))
        print(json.dumps(item_clean, indent=2))
        print()

    return items


def main():
    if len(sys.argv) != 5:
        print("Usage: python query_apexam_fixed.py <MFA_CODE> <pKey> <cbExamCode> <adminYear>")
        print("\nExample:")
        print("  python query_apexam_fixed.py 123456 4443Y7XU 94 26")
        sys.exit(1)

    mfa_code = sys.argv[1]
    pkey = sys.argv[2]
    cb_exam_code = sys.argv[3]
    admin_year = sys.argv[4]

    try:
        print("Getting temporary credentials with MFA...")
        credentials = get_temporary_credentials(mfa_code)
        print("✓ Got temporary credentials\n")

        items = query_data(credentials, pkey, cb_exam_code, admin_year)

        print(f"{'='*60}")
        print(f"✓ Query completed")
        print(f"✓ Total items found: {len(items)}")
        print(f"{'='*60}\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
