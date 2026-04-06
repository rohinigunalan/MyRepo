"""
Query APExamResponse-OAT table with MFA token
Usage: python query_apexam_with_mfa.py <MFA_CODE>
"""
import boto3
import sys
import json


def get_temporary_credentials(mfa_code):
    """Get temporary credentials using MFA token."""
    # Base profile for authentication
    session = boto3.Session(profile_name='cb-cia-admin-nonprod')
    sts_client = session.client('sts')

    # Assume role with MFA
    response = sts_client.assume_role(
        RoleArn='arn:aws:iam::697643551692:role/HeroesReaderRole',
        RoleSessionName='claude-dynamodb-session',
        SerialNumber='arn:aws:iam::185718115448:mfa/rgunalan',
        TokenCode=mfa_code
    )

    credentials = response['Credentials']
    return credentials


def query_table(credentials):
    """Query the DynamoDB table using temporary credentials."""
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
    print(f"Connected to: {TABLE_NAME}")
    print(f"Account: aws-apexamresponse-nonprod")
    print(f"{'='*60}\n")

    # Get table info
    print(f"Table status: {table.table_status}")
    print(f"Item count: {table.item_count}")
    print(f"Primary key: {table.key_schema}\n")

    # Scan first 10 items
    print(f"Scanning first 10 items...\n")
    response = table.scan(Limit=10)
    items = response.get('Items', [])

    if items:
        # Show structure
        print(f"Attributes in table:")
        for key in sorted(items[0].keys()):
            print(f"  - {key}")

        # Show all items
        print(f"\n{'='*60}")
        print(f"ITEMS ({len(items)} found):")
        print(f"{'='*60}\n")

        for i, item in enumerate(items, 1):
            print(f"{i}. {json.dumps(item, indent=2, default=str)}\n")

        print(f"{'='*60}")
        print(f"Total items in table: {table.item_count}")
    else:
        print("No items found")

    return items


def main():
    if len(sys.argv) != 2:
        print("Usage: python query_apexam_with_mfa.py <MFA_CODE>")
        print("\nExample:")
        print("  python query_apexam_with_mfa.py 123456")
        sys.exit(1)

    mfa_code = sys.argv[1]

    try:
        print("Getting temporary credentials with MFA...")
        credentials = get_temporary_credentials(mfa_code)
        print("✓ Got temporary credentials\n")

        items = query_table(credentials)

        print(f"\n✓ Successfully retrieved {len(items)} items")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
