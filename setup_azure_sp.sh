#!/bin/bash

# Configuration
RESOURCE_GROUP="rg-mlops-bank-churn"

# Get Subscription ID
echo "Fetching Subscription ID..."
SUBSCRIPTION_ID=$(az account show --query id -o tsv | tr -d '\r')

if [ -z "$SUBSCRIPTION_ID" ]; then
    echo "Error: Could not retrieve Subscription ID. Are you logged in to Azure CLI (az login)?"
    exit 1
fi

echo "Using Subscription ID: $SUBSCRIPTION_ID"
echo "Creating Service Principal for Resource Group: $RESOURCE_GROUP"

# 1. Create the Service Principal and capture output
SP_JSON=$(az ad sp create-for-rbac \
  --name "github-actions-$(date +%s)" \
  --role contributor \
  --scopes "/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}" \
  --output json)

# 2. Extract and format for GitHub Actions
echo "------------------------------------------------------"
echo "Copy the JSON below into your GitHub Secret (AZURE_CREDENTIALS):"
echo "------------------------------------------------------"
python3 -c "import sys, json; sp=json.load(sys.stdin); print(json.dumps({'clientId': sp['appId'], 'clientSecret': sp['password'], 'subscriptionId': '$SUBSCRIPTION_ID', 'tenantId': sp['tenant']}, separators=(',', ':')))" <<EOF
$SP_JSON
EOF
echo ""
echo "------------------------------------------------------"
