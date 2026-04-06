"""
Query DynamoDB using AWS CLI's cached credentials
This works by letting AWS CLI handle the credentials, then using subprocess
Usage: python query_with_cli_creds.py <pKey> <cbExamCode> <adminYear>
"""
import subprocess
import json
import sys


def query_dynamodb(pkey, cb_exam_code, admin_year):
    """Query DynamoDB using AWS CLI (which uses cached credentials)."""
    PROFILE = "cb-apexamresponse-nonprod-reader"
    TABLE_NAME = "APExamResponse-OAT"
    REGION = "us-east-1"

    print(f"\n{'='*60}")
    print(f"Using AWS CLI with Profile: {PROFILE}")
    print(f"Table: {TABLE_NAME}")
    print(f"{'='*60}")
    print(f"  pKey: {pkey}")
    print(f"  cbExamCode: {cb_exam_code}")
    print(f"  adminYear: {admin_year}")
    print(f"{'='*60}\n")

    # Build filter expression
    # cbExamCode is Number, adminYear is String
    filter_expression = f"cbExamCode = :examcode AND adminYear = :year"
    expression_values = {
        ":examcode": {"N": str(cb_exam_code)},
        ":year": {"S": str(admin_year)}
    }

    # Build AWS CLI command
    cmd = [
        "aws", "dynamodb", "query",
        "--table-name", TABLE_NAME,
        "--region", REGION,
        "--profile", PROFILE,
        "--key-condition-expression", f"pKey = :pk",
        "--filter-expression", filter_expression,
        "--expression-attribute-values", json.dumps({
            ":pk": {"S": pkey},
            ":examcode": {"N": str(cb_exam_code)},
            ":year": {"S": str(admin_year)}
        }),
        "--output", "json"
    ]

    print("Querying (using cached credentials from AWS CLI)...\n")

    try:
        # Run AWS CLI command
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            print(f"❌ Error: {result.stderr}")
            return []

        # Parse result
        response = json.loads(result.stdout)
        items = response.get('Items', [])

        # Convert DynamoDB JSON format to regular JSON
        items_clean = []
        for item in items:
            clean_item = {}
            for key, value in item.items():
                # Extract value from DynamoDB format {"S": "value"} or {"N": "123"}
                if 'S' in value:
                    clean_item[key] = value['S']
                elif 'N' in value:
                    clean_item[key] = value['N']
                elif 'BOOL' in value:
                    clean_item[key] = value['BOOL']
                elif 'L' in value:
                    clean_item[key] = value['L']
                elif 'M' in value:
                    clean_item[key] = value['M']
            items_clean.append(clean_item)

        # Display results
        print(f"{'='*60}")
        print(f"RESULTS: Found {len(items_clean)} item(s)")
        print(f"{'='*60}\n")

        if items_clean:
            for i, item in enumerate(items_clean, 1):
                print(f"Item {i}:")
                print(json.dumps(item, indent=2))
                print()
        else:
            print("No items found with the specified criteria\n")

        return items_clean

    except subprocess.TimeoutExpired:
        print("❌ Query timed out")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse response: {e}")
        return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


def main():
    if len(sys.argv) != 4:
        print("Usage: python query_with_cli_creds.py <pKey> <cbExamCode> <adminYear>")
        print("\nExample:")
        print("  python query_with_cli_creds.py 4443Y7XU 94 26")
        print("\nNote:")
        print("  This uses AWS CLI, which automatically uses cached credentials!")
        print("  If cache expired, AWS CLI will prompt for MFA.")
        sys.exit(1)

    pkey = sys.argv[1]
    cb_exam_code = sys.argv[2]
    admin_year = sys.argv[3]

    items = query_dynamodb(pkey, cb_exam_code, admin_year)

    print(f"{'='*60}")
    print(f"✓ Query completed")
    print(f"✓ Total items found: {len(items)}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
