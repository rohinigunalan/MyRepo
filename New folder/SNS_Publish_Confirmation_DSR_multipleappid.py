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
            "env": "uat"
        }
    },
    "body": {
        "requestId": "33389012-bc3b-46d6-9608-597e2180bd0f",
        "appId": "130",
        "detail": {
            "type": "DELETE_REQUEST",
            "action": "DELETED",
            "responseDetails": {
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
                "phoneNumber": "919-386-7669",
                "sat": {
                    "data": {
                        "assessments": [
                            {
                                "PSAT/NMSQT Fall 2022 - Wed Standard Score": "1300"
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

# List of app IDs to publish messages for
app_ids = [111, 115, 130, 229, 274, 281, 302, 344, 366, 378, 383, 409, 421, 432, 439, 440, 445, 475, 495, 498, 501, 502, 503]

# Loop through each app ID and publish a message
for app_id in app_ids:
    # Update the appId in the message body
    message["body"]["appId"] = str(app_id)

    # Publish the message to the SNS topic
    response = sns.publish(
        TopicArn=sns_topic_arn,
        Message=json.dumps(message),
        Subject=f'DSR Request Update for App ID {app_id}'
    )

    # Print the response from the SNS publish action
    print(f"SNS Publish Response for App ID {app_id}:", response)
