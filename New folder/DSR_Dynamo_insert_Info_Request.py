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
    "RequestId": "22r6a3f9-b6ad-45e9-b7af-g47622926650",
    "DsrRecordType": "DSR",
    "AlternateEmail": [
        "joe.smith@outlook.com",
        "joe.smith@yahoo.com"
    ],
    "BirthDate": "09/09/1970",
    "firstName": "ray",
    "lastName": "duo",
    "CatapultId": "",
    "CreatedTimestamp": "",
    "CsrComment": "This is for the delete request",
    "DsrRequestType": "DELETE_REQUEST",
    "DsrStatus": "PENDING",
    "EmailAddress": "ray.due@google.com",
    "OneTrustEventId": "",
    "OneTrustEventTimestamp": "",
    "PersonId": "140131335",
    "AlternatePersonId": [
        "140131337",
        "150231335"
    ],
    "ProfessionalId": "12432",
    "AlternateProfessionalId": [
        "12432",
        "14232"
    ],
    "ProfessionalAccountId": "234523",
    "PhoneNumber": "919-386-7669",
    "StudentSchool": "Rose Hamilton Elementary",
    "EducatorSchoolAffiliation": [
        "Rose Hamilton Elementary",
        "Centerville High School"
    ],
    "Address": {
        "AddressLine1": "1310 NW Naito Parkway",
        "AddressLine2": "Unit 1006",
        "City": "Portland",
        "State": "OR",
        "Country": "US",
        "Zipcode": "97209"
    },
    "UpdatedTimestamp": "",
    "Username": ""
}

# Insert the item into the DynamoDB table
response = table.put_item(Item=item)

# Print the response from the DynamoDB put_item action
print("DynamoDB Insert Response:", response)
