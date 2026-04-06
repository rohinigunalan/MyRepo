"""
Query APExamResponse-OAT table by specific keys
Usage: python query_apexam_by_key.py <MFA_CODE> <pKey> [cbExamCode]
"""
import boto3
from boto3.dynamodb.conditions import Key, Attr
import sys
import json


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

    credentials = response['Credentials']
    return credentials


def query_by_pkey(credentials, pkey, cb_exam_code=None, admin_year=None):
    """
    Query DynamoDB table by pKey and optionally filter by cbExamCode and adminYear.

    Args:
        credentials: AWS temporary credentials
        pkey: Partition key value (e.g., "4443Y7XU")
        cb_exam_code: Optional cbExamCode to filter (e.g., 12)
        admin_year: Optional adminYear to filter (e.g., "26")
    """
    TABLE_NAME = "APExamResponse-OAT"

    # Create session with temporary credentials
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
    print(f"Account: aws-apexamresponse-nonprod")
    print(f"{'='*60}\n")

    # Query by pKey
    print(f"Query parameters:")
    print(f"  pKey = {pkey}")
    if cb_exam_code:
        print(f"  cbExamCode = {cb_exam_code}")
    if admin_year:
        print(f"  adminYear = {admin_year}")
    print()

    # Build query
    query_kwargs = {
        'KeyConditionExpression': Key('pKey').eq(pkey)
    }

    # Add filters if provided
    # Note: cbExamCode is stored as Number, adminYear is stored as String
    filters = []
    if cb_exam_code is not None:
        filters.append(Attr('cbExamCode').eq(int(cb_exam_code)))  # Number type
    if admin_year is not None:
        filters.append(Attr('adminYear').eq(str(admin_year)))     # String type

    # Combine filters with AND
    if filters:
        filter_expression = filters[0]
        for f in filters[1:]:
            filter_expression = filter_expression & f
        query_kwargs['FilterExpression'] = filter_expression

    # Execute query
    print(f"Executing query...\n")
    response = table.query(**query_kwargs)
    items = response.get('Items', [])

    # Show results
    print(f"{'='*60}")
    print(f"RESULTS: Found {len(items)} item(s)")
    print(f"{'='*60}\n")

    if items:
        for i, item in enumerate(items, 1):
            print(f"Item {i}:")
            print(json.dumps(item, indent=2, default=str))
            print()
    else:
        print("No items found with the specified criteria")

    return items


def get_item_by_key(credentials, pkey):
    """
    Get a specific item by its primary key.

    Args:
        credentials: AWS temporary credentials
        pkey: Partition key value
    """
    TABLE_NAME = "APExamResponse-OAT"

    session = boto3.Session(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
        region_name='us-east-1'
    )

    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)

    print(f"\nGetting item with pKey = {pkey}\n")

    response = table.get_item(Key={'pKey': pkey})
    item = response.get('Item')

    if item:
        print(f"Found item:")
        print(json.dumps(item, indent=2, default=str))
    else:
        print(f"No item found with pKey = {pkey}")

    return item


def main():
    if len(sys.argv) < 3:
        print("Usage: python query_apexam_by_key.py <MFA_CODE> <pKey> [cbExamCode] [adminYear]")
        print("\nExamples:")
        print("  # Query by pKey only")
        print("  python query_apexam_by_key.py 123456 4443Y7XU")
        print()
        print("  # Query by pKey and filter by cbExamCode")
        print("  python query_apexam_by_key.py 123456 4443Y7XU 12")
        print()
        print("  # Query by pKey, cbExamCode, and adminYear")
        print("  python query_apexam_by_key.py 123456 4443Y7XU 12 26")
        sys.exit(1)

    mfa_code = sys.argv[1]
    pkey = sys.argv[2]
    cb_exam_code = sys.argv[3] if len(sys.argv) > 3 else None
    admin_year = sys.argv[4] if len(sys.argv) > 4 else None

    try:
        print("Getting temporary credentials with MFA...")
        credentials = get_temporary_credentials(mfa_code)
        print("✓ Got temporary credentials")

        # Query the table
        items = query_by_pkey(credentials, pkey, cb_exam_code, admin_year)

        print(f"\n{'='*60}")
        print(f"✓ Query completed successfully")
        print(f"✓ Found {len(items)} matching item(s)")
        print(f"{'='*60}\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
