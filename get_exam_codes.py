"""
Scan APExamResponse-OAT to find all unique cbExamCode values
and associated metadata that might indicate exam names
"""
import boto3
from collections import defaultdict
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

    return response['Credentials']


def scan_for_exam_codes(credentials, admin_year='26'):
    """Scan table to find unique exam codes and related metadata."""
    TABLE_NAME = "APExamResponse-OAT"

    session = boto3.Session(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
        region_name='us-east-1'
    )

    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)

    print(f"\nScanning {TABLE_NAME} for exam codes...")
    print(f"Filter: adminYear = {admin_year}")
    print(f"{'='*60}\n")

    # Store unique exam codes with sample metadata
    exam_data = defaultdict(lambda: {
        'count': 0,
        'fpsIds': set(),
        'systemFormCodes': set(),
        'aiCodes': set(),
        'sample_item': None
    })

    # Scan table with filter (limit to reasonable number for analysis)
    from boto3.dynamodb.conditions import Attr
    scan_kwargs = {
        'Limit': 1000,
        'FilterExpression': Attr('adminYear').eq(admin_year)
    }
    items_scanned = 0

    while True:
        response = table.scan(**scan_kwargs)
        items = response.get('Items', [])

        for item in items:
            items_scanned += 1

            # Only look at exam records (not individual prompts)
            if item.get('sKey', '').startswith('exam#'):
                cb_exam_code = item.get('cbExamCode', 'N/A')

                exam_data[cb_exam_code]['count'] += 1

                # Collect metadata that might indicate exam type
                if 'fpsId' in item:
                    exam_data[cb_exam_code]['fpsIds'].add(item['fpsId'])
                if 'systemFormCode' in item:
                    exam_data[cb_exam_code]['systemFormCodes'].add(item['systemFormCode'])
                if 'aiCode' in item:
                    exam_data[cb_exam_code]['aiCodes'].add(item['aiCode'])

                # Store sample for reference
                if not exam_data[cb_exam_code]['sample_item']:
                    exam_data[cb_exam_code]['sample_item'] = item

        # Check if more pages
        if 'LastEvaluatedKey' not in response:
            break

        scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']

        # Stop after reasonable scan
        if items_scanned >= 5000:
            print(f"Note: Stopped after scanning {items_scanned} items")
            break

    print(f"Scanned {items_scanned} items total\n")
    print(f"{'='*60}")
    print(f"UNIQUE EXAM CODES FOUND")
    print(f"{'='*60}\n")

    # Sort by exam code
    for exam_code in sorted(exam_data.keys()):
        data = exam_data[exam_code]
        print(f"cbExamCode: {exam_code}")
        print(f"  Count: {data['count']} exam records")

        if data['fpsIds']:
            print(f"  fpsId(s): {', '.join(sorted(data['fpsIds']))}")
        if data['systemFormCodes']:
            print(f"  Form code(s): {', '.join(sorted(data['systemFormCodes']))}")
        if data['aiCodes']:
            print(f"  aiCode(s): {', '.join(sorted(data['aiCodes']))}")

        # Show sample exam record
        if data['sample_item']:
            sample = data['sample_item']
            print(f"  Sample exam:")
            print(f"    pKey: {sample.get('pKey', 'N/A')}")
            print(f"    adminCode: {sample.get('adminCode', 'N/A')}")
            print(f"    examWindow: {sample.get('examWindow', 'N/A')}")
            print(f"    examDate: {sample.get('examDate', 'N/A')}")

        print()

    print(f"{'='*60}")
    print(f"Total unique exam codes: {len(exam_data)}")
    print(f"{'='*60}\n")

    return exam_data


def main():
    if len(sys.argv) < 2:
        print("Usage: python get_exam_codes.py <MFA_CODE> [adminYear]")
        print("\nExamples:")
        print("  python get_exam_codes.py 123456       # Defaults to adminYear = 26")
        print("  python get_exam_codes.py 123456 25    # Filter by adminYear = 25")
        sys.exit(1)

    mfa_code = sys.argv[1]
    admin_year = sys.argv[2] if len(sys.argv) > 2 else '26'

    try:
        print("Getting temporary credentials with MFA...")
        credentials = get_temporary_credentials(mfa_code)
        print("✓ Got temporary credentials\n")

        exam_data = scan_for_exam_codes(credentials, admin_year)

        print("✓ Scan completed successfully\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
