# API Runner for Colorado Payloads
import requests
import json
import sys
import os

# Add current directory to path to import payload modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def load_payload(payload_file):
    """
    Load payload from a Python file
    """
    try:
        # Read the payload file and extract the payload dictionary
        with open(payload_file, 'r') as f:
            content = f.read()
        
        # Execute the file content to get the payload
        namespace = {}
        exec(content, namespace)
        return namespace.get('payload')
    except Exception as e:
        print(f"Error loading payload from {payload_file}: {e}")
        return None

def send_api_request(payload_data, api_url, headers=None):
    """
    Send API request with payload data
    """
    if headers is None:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    try:
        print(f"Sending request to: {api_url}")
        print(f"Payload: {json.dumps(payload_data, indent=2)}")
        
        response = requests.post(
            url=api_url,
            json=payload_data,
            headers=headers,
            timeout=30
        )
        
        print(f"\nResponse Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.text:
            try:
                response_json = response.json()
                print(f"Response JSON: {json.dumps(response_json, indent=2)}")
            except json.JSONDecodeError:
                print(f"Response Text: {response.text}")
        
        return response
        
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")
        return None

def main():
    # Configure your API endpoint here
    API_URL = "YOUR_API_ENDPOINT_URL_HERE"  # Replace with your actual API URL
    
    # Optional: Add authentication headers if needed
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        # 'Authorization': 'Bearer YOUR_TOKEN_HERE',  # Uncomment if you need auth
        # 'X-API-Key': 'YOUR_API_KEY_HERE',  # Uncomment if you need API key
    }
    
    # Load payload from CO-Payload-2.py
    payload_file = "CO-Payload-2.py"
    co_payload = load_payload(payload_file)
    
    if co_payload is None:
        print(f"❌ Failed to load payload from {payload_file}")
        return
    
    print("=== Running API Test with CO-Payload-2 ===")
    response = send_api_request(co_payload, API_URL, headers)
    
    if response and response.status_code == 200:
        print("✅ API call successful!")
    else:
        print("❌ API call failed!")

def test_multiple_payloads():
    """
    Test multiple CO payloads
    """
    API_URL = "YOUR_API_ENDPOINT_URL_HERE"  # Replace with your actual API URL
    
    payload_files = [
        "CO-Payload-2.py",
        "CO-Payload-3.py", 
        "CO-Payload-4.py",
        "CO-Payload-5.py",
        "CO-Payload-6.py"
    ]
    
    for payload_file in payload_files:
        if os.path.exists(payload_file):
            print(f"\n{'='*50}")
            print(f"Testing {payload_file}")
            print('='*50)
            
            payload = load_payload(payload_file)
            if payload:
                response = send_api_request(payload, API_URL)
                if response:
                    print(f"✅ {payload_file} - Status: {response.status_code}")
                else:
                    print(f"❌ {payload_file} - Failed")
        else:
            print(f"⚠️  {payload_file} not found")

if __name__ == "__main__":
    # Run single payload test
    main()
    
    # Uncomment below to test multiple payloads
    # test_multiple_payloads()
