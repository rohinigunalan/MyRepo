#!/usr/bin/env python3
"""
DSR Schema Validation Report - Latest Version
Validates JSON files against DSR confirmation schema

=== WORKING VALIDATION COMMAND ===
For quick validation of any JSON file, use this proven working command:

python -c "import json; from jsonschema import Draft7Validator; print('DSR Schema Validation for [FILENAME]'); print('='*50); schema_file = r'C:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\Newfolder\DSR_AWS\DSR_Schma_Validation\dsr-confirmation.schema.json'; json_file = r'C:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\Newfolder\DSR_AWS\DSR_Schma_Validation\[FILENAME].json'; schema=json.load(open(schema_file)); data=json.load(open(json_file)); print('Files loaded successfully'); print('Request ID:', data.get('requestId')); print('App ID:', data.get('appId')); print('Action:', data.get('action')); validator=Draft7Validator(schema); errors=list(validator.iter_errors(data)); print('VALIDATION SUCCESSFUL!' if not errors else f'VALIDATION FAILED - {len(errors)} errors found'); [print(f'  Error {i}: {e.message}') for i, e in enumerate(errors[:5], 1)] if errors else None; print('='*50)"

Examples:
- For MFCREP8A95_1.json: Replace [FILENAME] with "MFCREP8A95_1"  
- For new505.json: Replace [FILENAME] with "new505"

=== USAGE EXAMPLES ===
1. python -c "[command above with MFCREP8A95_1]"
2. python -c "[command above with new505]"

This inline method shows output reliably in PowerShell.
"""

import json
import sys
import os
from jsonschema import Draft7Validator

def validate_json_file(json_filename="MFCREP8A95_1.json"):
    print("=" * 70)
    print("DSR JSON Schema Validation Report - Latest Version")
    print("=" * 70)
    base_path = r"C:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\Newfolder\DSR_AWS\DSR_Schma_Validation"
    schema_file = os.path.join(base_path, "dsr-confirmation.schema.json")
    json_file = os.path.join(base_path, json_filename)
    print(f"📂 Base Path: {base_path}")
    print(f"📄 Schema File: dsr-confirmation.schema.json")
    print(f"📄 Target File: {json_filename}")
    print()
    try:
        if not os.path.exists(schema_file):
            print(f"❌ Schema file not found: {schema_file}")
            return False
        if not os.path.exists(json_file):
            print(f"❌ JSON file not found: {json_file}")
            return False
        print("✅ Both files found successfully")
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        print(f"✅ Schema loaded: {len(str(schema))} characters")
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ JSON data loaded: {len(str(data))} characters")
        print()
        print("📋 JSON Data Summary:")
        print(f"   Request ID: {data.get('requestId', 'N/A')}")
        print(f"   App ID: {data.get('appId', 'N/A')}")
        print(f"   Action: {data.get('action', 'N/A')}")
        request_type = "Unknown"
        subject_count = 0
        first_subject_name = "N/A"
        if 'detail' in data and 'responseDetails' in data['detail']:
            response_details = data['detail']['responseDetails']
            if 'delete' in response_details and 'subjects' in response_details['delete']:
                subjects = response_details['delete']['subjects']
                request_type = "Delete Request"
                subject_count = len(subjects)
                if subjects:
                    first = subjects[0]
                    first_subject_name = f"{first.get('firstName', '')} {first.get('lastName', '')}".strip()
            elif 'information' in response_details and 'subjects' in response_details['information']:
                subjects = response_details['information']['subjects']
                request_type = "Information Request"
                subject_count = len(subjects)
                if subjects:
                    first = subjects[0]
                    first_subject_name = f"{first.get('firstName', '')} {first.get('lastName', '')}".strip()
        print(f"   Request Type: {request_type}")
        print(f"   Subject Count: {subject_count}")
        if subject_count > 0:
            print(f"   First Subject: {first_subject_name}")
        print()
        print("🔍 Running Schema Validation...")
        validator = Draft7Validator(schema)
        errors = list(validator.iter_errors(data))
        if errors:
            print(f"❌ VALIDATION FAILED")
            print(f"   Errors Found: {len(errors)}")
            print()
            print("📝 Error Details:")
            for i, error in enumerate(errors[:10], 1):
                path_str = ' -> '.join(str(p) for p in error.path) if error.path else 'root'
                print(f"   Error {i}:")
                print(f"     Path: {path_str}")
                print(f"     Message: {error.message}")
                instance_str = str(error.instance)[:80]
                if len(str(error.instance)) > 80:
                    instance_str += "..."
                print(f"     Value: {instance_str}")
                print()
            return False
        else:
            print("✅ VALIDATION SUCCESSFUL!")
            print("   The JSON file fully conforms to the DSR confirmation schema.")
            print()
            print("🎯 Validation Summary:")
            print("   • Schema Compliance: ✅ PASSED")
            print("   • File Structure: ✅ VALID")
            print("   • Data Integrity: ✅ CONFIRMED")
            print("   • JSON Format: ✅ WELL-FORMED")
            return True
    except FileNotFoundError as e:
        print(f"❌ File Access Error: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parsing Error: {e}")
        print(f"   Line: {e.lineno}, Column: {e.colno}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        print()
        print("=" * 70)
        print("📝 Quick Validation Reminder:")
        print("   Use the inline command from the script header for fastest results")
        print("=" * 70)

def main():
    json_filename = sys.argv[1] if len(sys.argv) > 1 else "MFCREP8A95_1.json"
    success = validate_json_file(json_filename)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
