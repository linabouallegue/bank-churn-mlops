# Configuration
$ResourceGroup = "rg-mlops-bank-churn"

# Get Subscription ID
Write-Host "Fetching Subscription ID..."
$SubscriptionId = (az account show --query id -o tsv).Trim()

if (-not $SubscriptionId) {
    Write-Error "Could not retrieve Subscription ID. Are you logged in to Azure CLI (az login)?"
    return
}

Write-Host "Using Subscription ID: $SubscriptionId"
Write-Host "Creating Service Principal for Resource Group: $ResourceGroup"

# 1. Create the Service Principal and capture output
$Timestamp = [DateTimeOffset]::Now.ToUnixTimeSeconds()
$SpName = "github-actions-$Timestamp"

$SpJson = az ad sp create-for-rbac `
  --name $SpName `
  --role contributor `
  --scopes "/subscriptions/$SubscriptionId/resourceGroups/$ResourceGroup" `
  --output json | ConvertFrom-Json

# 2. Format for GitHub Actions
$Credentials = @{
    clientId       = $SpJson.appId
    clientSecret   = $SpJson.password
    subscriptionId = $SubscriptionId
    tenantId       = $SpJson.tenant
}

Write-Host "------------------------------------------------------"
Write-Host "Copy the JSON below into your GitHub Secret (AZURE_CREDENTIALS):"
Write-Host "------------------------------------------------------"
$Credentials | ConvertTo-Json -Compress
Write-Host "------------------------------------------------------"
