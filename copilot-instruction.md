# AWS Data Subject Rights (DSR) Scripts - Usage Instructions

This repository contains multiple scripts for handling Data Subject Rights (DSR) requests using AWS services like DynamoDB and SNS. Below are instructions for using these scripts.

## Environment Setup

1. Ensure you have the AWS CLI configured with the appropriate profile:
   - Profile name: `cb-data-subject-rights-nonprod-dev-cli`

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Script Categories

### DynamoDB Insert Scripts

These scripts insert DSR requests into DynamoDB:

- **DSR_Dynamo_insert_Delete_Request.py**: Inserts DELETE_REQUEST type DSR requests
- **DSR_Dynamo_insert_Delete_Nodatafound_Request.py**: Inserts NO_DATA_FOUND type requests
- **DSR_Dynamo_insert_Info_Request.py**: Inserts INFO_REQUEST type requests

### SNS Publication Scripts

These scripts publish DSR request confirmations to SNS topics:

- **Single App ID scripts**:
  - SNS_Publish_Confirmation_DSR_Delete_Request.py
  - SNS_Publish_Confirmation_DSR_Delete_Nodatafound.py
  - SNS_Publish_Confirmation_DSR_Info_Request_QUERY.py
  - SNS_Publish_Confirmation_DSR_Info_Request_NO_DATA_FOUND.py

- **Multiple App ID scripts**:
  - SNS_Publish_Confirmation_DSR_multipleappid_Delete_Request.py
  - SNS_Publish_Confirmation_DSR_multipleappid_Delete_NoDataFound.py
  - SNS_Publish_Confirmation_DSR_multipleappid_info_request_QUERY.py
  - SNS_Publish_Confirmation_DSR_multipleappid_info_request_NO_DATA_FOUND.py

## Common Parameters

### DynamoDB Scripts
- `RequestId`: Unique identifier for the DSR request
- `DsrRequestType`: Type of request (DELETE_REQUEST, INFO_REQUEST, NO_DATA_FOUND)
- `PersonId`: Subject's person identifier
- User Data: Personal information like name, email, address, etc.

### SNS Scripts
- `app_ids`: List of application IDs to send notifications to
- `sns_topic_arn`: ARN of the SNS topic to publish to
- Message payload with request details and user data

## UAT Environment

The repository also contains UAT environment specific scripts:
- DSR_Dynamo_insert_Delete_Request_for_env_UAT.py
- SNS_Publish_Confirmation_DSR_multipleappid_Delete_Request_for_env_UAT.py

## Best Practices

1. Always verify the AWS profile before running scripts
2. Check the SNS topic ARN is correct for your environment
3. Ensure proper data format in the request payload
4. Validate DynamoDB table name before insertions
5. For multiple app ID scripts, verify the app_ids list is accurate

## Troubleshooting

If you encounter errors:
1. Verify AWS credentials are valid
2. Check network connectivity to AWS
3. Ensure the DynamoDB table exists and is accessible
4. Validate JSON structure in requests
5. Check SNS topic permissions
