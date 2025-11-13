import boto3
import json
from decimal import Decimal

# AWS CLI profile name
aws_profile = 'cb-data-subject-rights-nonprod-dev-cli'

# Initialize the session with the specified profile
session = boto3.Session(profile_name=aws_profile)

# Create a DynamoDB resource
dynamodb = session.resource('dynamodb')

# Replace 'YourTableName' with your actual DynamoDB table name
table_name = 'uat-dsr-request-handler-DsrReadStore'
table = dynamodb.Table(table_name)

# JSON payload to insert into DynamoDB
item = {
   "RequestId": "sssf6a3f9-b6ad-45e9-b7af-g47622926650",
    "DsrRecordType": "DSR",
    "AlternateEmail": [
        "random.email1@outlook.com",
        "random.email2@yahoo.com"
    ],
    "BirthDate": "01/01/2005",
    "FirstName": "RandomFirstName",
    "LastName": "RandomLastName",
    "CatapultId": "12345",
    "CreatedTimestamp": "",
    "CsrComment": "This is a random comment for testing purposes.",
    "DsrRequestType": "DELETE_REQUEST",
    "DsrStatus": "PENDING",
    "EmailAddress": "random.email@google.com",
    "OneTrustEventId": "random-event-id",
    "OneTrustEventTimestamp": "2025-05-23T10:00:00Z",
    "PersonId": "123456789",
    "AlternatePersonId": [
        "987654321",
        "123123123"
    ],
    "ProfessionalId": "54321",
    "AlternateProfessionalId": [
        "54321",
        "67890"
    ],
    "ProfessionalAccountId": "67890", 
    "PhoneNumber": "123-456-7890",
    "StudentSchool": "Random High School",
    "EducatorSchoolAffiliation": "West County Elementary",
    "Channel": "C",
    "Persona": "EDUCATOR",
    "Address": {
        "AddressLine1": "123 Random Street",
        "AddressLine2": "Apt 456",
        "City": "Random City",
        "State": "RS",
        "Country": "US",
        "Zipcode": "12345"
    },
    "UpdatedTimestamp": "2025-05-23T10:00:00Z",
    "Username": "random.username"
}

# Insert the item into the DynamoDB table
response = table.put_item(Item=item)

# Print the response from the DynamoDB put_item action
print("DynamoDB Insert Response:", response)
