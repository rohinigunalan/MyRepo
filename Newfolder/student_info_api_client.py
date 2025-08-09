#!/usr/bin/env python3
"""
Student Info Manager API Client
Replicates Postman API calls for creating person info
"""

import requests
import json
import sys
import os
import argparse

# Add current directory to path to import payload files
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class StudentInfoAPIClient:
    def __init__(self, authorization_token=None, env="palm", x_api_key="zfcpjwq1jk"):
        """
        Initialize API client with Postman environment parameters
        """
        self.base_url = "https://vpce-0ba2f2a0a5f765c66-wh6eytko.execute-api.us-east-1.vpce.amazonaws.com"
        self.env = env
        self.x_api_key = x_api_key
        self.authorization_token = authorization_token
        
        # Build full API URL
        self.api_url = f"{self.base_url}/{self.env}/student-info-manager"
        
        # Setup headers based on Postman environment
        self.headers = {
            "Content-Type": "application/json",
            "x-spigw-api-id": self.x_api_key
        }
        
        # Add authorization if provided
        if self.authorization_token:
            self.headers["Authorization"] = self.authorization_token  # Try without Bearer prefix
    
    def make_api_call(self, payload_data, student_name="Unknown"):
        """
        Make API call with payload data
        """
        try:
            print("=" * 60)
            print("Testing Student Info Manager API")
            print("=" * 60)
            print(f"Making API call to: {self.api_url}")
            print(f"Headers: {json.dumps({k: v[:20] + '...' if k == 'Authorization' and len(v) > 20 else v for k, v in self.headers.items()}, indent=2)}")
            print(f"Payload preview: {student_name}")
            
            if not self.authorization_token:
                print("⚠️  WARNING: No authorization token provided!")
                print("   This may result in a 403 Forbidden error.")
                print()
            
            response = requests.post(
                url=self.api_url,
                json=payload_data,
                headers=self.headers,
                timeout=30
            )
            
            print(f"\nResponse Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            
            if response.text:
                try:
                    response_json = response.json()
                    print("Response JSON:")
                    print(json.dumps(response_json, indent=2))
                except json.JSONDecodeError:
                    print(f"Response Text: {response.text}")
            
            if response.status_code == 200:
                print("✅ API call successful!")
                return response, True
            elif response.status_code == 201:
                print("✅ API call successful! (Created)")
                return response, True
            elif response.status_code == 403:
                print("❌ API call failed with status 403")
                print("   This usually means missing or invalid authorization.")
                return response, False
            else:
                print(f"❌ API call failed with status {response.status_code}")
                return response, False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error making API request: {e}")
            return None, False

def load_payload_file(filename):
    """
    Load payload from a specific CO-Payload file
    """
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("payload_module", filename)
        payload_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(payload_module)
        return payload_module.payload
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

def get_student_name_from_payload(payload_data):
    """
    Extract student name from payload for display
    """
    try:
        person_info = payload_data.get("studentInfoManagerRequest", {}).get("personInfo", {})
        first_name = person_info.get("firstNm", "")
        last_name = person_info.get("lastNm", "")
        return f"{first_name} {last_name}".strip()
    except:
        return "Unknown"

def get_default_payload():
    """
    Default payload (Ethan Rodriguez)
    """
    return {
        "studentInfoManagerRequest": {
            "requestName": "createPersonInfo",
            "channel": {
                "type": "C",
                "orgId": "0"
            },
            "personInfo": {
                "matchInd": "Y",
                "genderCd": "M",
                "firstNm": "Ethan",
                "lastNm": "Rodriguez",
                "genderTxt": "",
                "middleInitial": "D",
                "studentSearchOptInInd": "N",
                "birthDt": "2004-08-30",
                "hsGradDt": "2022-05-28",
                "incomingAdminDt": None,
                "aiCd": "012345",
                "educationLevelCd": None,
                "preferredFirstNm": "",
                "sundayTestTakerInd": "N",
                "deceasedInd": "N",
                "activeInd": "Y"
            },
            "homeAddress": {
                "streetAddr1": "8765 Valley Vista Way",
                "streetAddr2": "",
                "streetAddr3": "",
                "urbanization": "",
                "city": "Westminster",
                "zip5": "80031",
                "zip4": "1357",
                "stateCd": "CO",
                "carrierRt": "",
                "regionFipsCd": "",
                "province": "",
                "intlPostalCode": "",
                "countyFipsCd": "",
                "countryIsoCd": "US"
            },
            "personalEmail": {
                "emailAddress": "ethan.rodriguez@mailinator.com"
            },
            "homePhone": {
                "ndc": "303",
                "cc": "1",
                "local": "5554680",
                "prefInd": "Y",
                "intlPhone": None,
                "txtMsgAllowInd": "Y",
                "deviceTypeCd": 1
            },
            "altPhone": {
                "ndc": None,
                "cc": "39",
                "local": None,
                "prefInd": "U",
                "intlPhone": "312345678",
                "txtMsgAllowInd": "Y",
                "deviceTypeCd": 2
            },
            "personParent": {
                "firstNm": "Patricia",
                "lastNm": "Rodriguez",
                "emailAddr": "patricia.rodriguez@mailinator.com",
                "newsletterSubscriptionInd": "Y",
                "ccSelectedInd": "Y"
            },
            "callerAppId": 303,
            "aiDomainCd": "SAT"
        }
    }

def test_default_payload(client):
    """
    Test with default Ethan Rodriguez payload
    """
    payload = get_default_payload()
    student_name = get_student_name_from_payload(payload)
    response, success = client.make_api_call(payload, student_name)

def test_specific_payload(client, payload_file):
    """
    Test with a specific payload file
    """
    payload = load_payload_file(payload_file)
    if payload:
        student_name = get_student_name_from_payload(payload)
        print(f"Testing with payload from {payload_file}")
        response, success = client.make_api_call(payload, student_name)
    else:
        print(f"❌ Failed to load payload from {payload_file}")

def test_all_payloads(client):
    """
    Test all CO payload files
    """
    payload_files = [
        "CO-Payload-2.py", "CO-Payload-3.py", "CO-Payload-4.py", 
        "CO-Payload-5.py", "CO-Payload-6.py", "CO-Payload-7.py",
        "CO-Payload-8.py", "CO-Payload-9.py", "CO-Payload-10.py"
    ]
    
    results = []
    for payload_file in payload_files:
        if os.path.exists(payload_file):
            print(f"\n{'='*80}")
            print(f"Testing {payload_file}")
            print('='*80)
            
            payload = load_payload_file(payload_file)
            if payload:
                student_name = get_student_name_from_payload(payload)
                response, success = client.make_api_call(payload, student_name)
                results.append((payload_file, student_name, success))
            else:
                print(f"❌ Failed to load {payload_file}")
                results.append((payload_file, "Failed to load", False))
        else:
            print(f"⚠️  {payload_file} not found")
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print('='*80)
    for filename, student_name, success in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status} - {filename} ({student_name})")

def main():
    """
    Main function with command line argument support
    """
    parser = argparse.ArgumentParser(description='Student Info Manager API Client')
    parser.add_argument('--auth', help='Authorization token')
    parser.add_argument('--env', default='palm', help='Environment (default: palm)')
    parser.add_argument('--api-key', default='zfcpjwq1jk', help='X-API-Key (default: zfcpjwq1jk)')
    parser.add_argument('--payload', help='Specific payload file to use (e.g., CO-Payload-2.py)')
    parser.add_argument('--test-all', action='store_true', help='Test all CO payload files')
    
    args = parser.parse_args()
    
    # Initialize API client
    client = StudentInfoAPIClient(
        authorization_token=args.auth,
        env=args.env,
        x_api_key=args.api_key
    )
    
    if args.test_all:
        # Test all CO payload files
        test_all_payloads(client)
    elif args.payload:
        # Test specific payload file
        test_specific_payload(client, args.payload)
    else:
        # Test default payload
        test_default_payload(client)

if __name__ == "__main__":
    main()
