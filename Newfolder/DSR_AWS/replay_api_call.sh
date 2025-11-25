#!/bin/bash

# Configuration
CLIENT_ID="7k21jrh4jr6d8e2a30tljmheqc"
CLIENT_SECRET="1hvmefps6o0euo2ssl5eht9b0q0itb4ofa461auqkag2aa3g6b9d"
COGNITO_URL="https://uat-onetrust.auth.us-east-1.amazoncognito.com/oauth2/token"
REPLAY_API_URL="https://15suwkrmfj.execute-api.us-east-1.amazonaws.com/dsr/replay"

# Step 1: Get auth token
echo "Step 1: Getting auth token from Cognito..."
TOKEN_RESPONSE=$(curl --silent --location --request POST "${COGNITO_URL}?grant_type=client_credentials&client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}&scope=cbot%2Fwrite" \
--header 'Content-Type: application/x-www-form-urlencoded' \
--header 'Cookie: XSRF-TOKEN=ac5cd416-1baa-4a78-9112-f71572437e67')

# Extract access token using grep and sed (works without jq)
ACCESS_TOKEN=$(echo "$TOKEN_RESPONSE" | grep -o '"access_token":"[^"]*' | sed 's/"access_token":"//')

if [ -z "$ACCESS_TOKEN" ]; then
    echo "Error: Failed to get access token"
    echo "Response: $TOKEN_RESPONSE"
    exit 1
fi

echo "✓ Auth token obtained successfully"
echo ""

# Step 2: Call replay API with the token
echo "Step 2: Calling replay API..."
REQUEST_ID="${1:-68HDZWN84M_1}"
APP_ID="${2:-525}"

REPLAY_RESPONSE=$(curl --location "${REPLAY_API_URL}" \
--header "Authorization: Bearer ${ACCESS_TOKEN}" \
--header 'Content-Type: application/json' \
--data "{
    \"requestId\": \"${REQUEST_ID}\",
    \"appId\": \"${APP_ID}\"
}")

echo "Response:"
echo "$REPLAY_RESPONSE"
