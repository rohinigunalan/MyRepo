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
sns_topic_arn = 'arn:aws:sns:us-east-1:228209566668:nonprod-domainbus-topic'

# Update the message to publish with the provided JSON structure
message = {
  "header": {
    "version": "1.0.0",
    "event": {
      "category": "compliance",
      "name": "data-subject-rights-confirmation",
      "type": "data",
      "version": "1.0.0",
      "origin": "cb",
      "timestamp": "2024-03-13T18:13:13.260Z"
    },
    "cb": {
      "env": "qa"
    }
  },
  "body": {
    "requestId": "FZJ9FJZE9Z_1",
    "appId": 250,
    "action": "APPROVED_EXCEPTION",
    "exception": "NO DATA"
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
