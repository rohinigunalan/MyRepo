import boto3
import json
from boto3.dynamodb.conditions import Key
from decimal import Decimal

# AWS CLI profile name
aws_profile = 'cb-data-subject-rights-nonprod-dev-cli'

# Initialize the session with the specified profile
session = boto3.Session(profile_name=aws_profile)

# Create an SNS client using the same session
sns = session.client('sns')

# Update the SNS topic ARN with the provided details
sns_topic_arn = 'arn:aws:sns:us-east-1:228209566668:cbconfig-topic-228209566668'

# Update the message to publish with the provided JSON structure
message = {
    "header": {
        "version": "1.0.0",
        "event": {
            "category": "compliance",
            "name": "data-subject-rights-confirmation",
            "type": "data",
            "version": "1.1.0",
            "origin": "cb",
            "timestamp": "2024-03-13T18:13:13.260Z"
        },
        "cb": {
            "env": "UAT"
        }
    },
    "body": {
        "requestId": "101e6a3f9-b6ad-45e9-b7af-g47622926650",
        "appId": "111",
        "detail": {
            "type": "DELETE_REQUEST",
            "action": "DELETED",
            "responseDetails": {
                "firstName": "Bob",
                "lastName": "Smith",
                "personId": "200780162",
                "alternatePersonId": [
                    "140131337",
                    "150231335"
                ],
                "professionalId": "891034",
                "alternateProfessionalId": [
                    "12432",
                    "14232"
                ],
                "proffessionalAccountId": "234523",
                "emailAddress": "joe.smith@google.com",
                "alternateEmail": [
                    "joe.smith@outlook.com",
                    "joe.smith@yahoo.com"
                ],
                "address": {
                    "addressLine1": "1310 NW Naito Parkway",
                    "addressLine2": "Unit 1006",
                    "city": "Portland",
                    "state": "OR",
                    "country": "US",
                    "zipcode": "97209"
                },
                "birthdate": "09/09/1970",
                "phoneNumbers": ["919-386-7669", "765-977-7177"],
                "accommodations management": {
                    "data": {
                        "disability": [
                            {
                                "SAT Fall 2022 - Wed Standard Score": "1300"
                            },
                            {
                                "SAT August 2023 Score:": "1520"
                            },
                            {
                                "SAT December 2023 Score:": "1530"
                            }
                        ]
                    }
                }
            }
        }
    }
}

# Publish the message to the SNS topic
response = sns.publish(
    TopicArn=sns_topic_arn,
    Message=json.dumps(message),
    Subject='DSR Request Update'
)

# Print the response from the SNS publish action
print("SNS Publish Response:", response)
