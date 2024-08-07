param location string = resourceGroup().location
param abbrs object
param resourceToken string
param tags object = {}

@description('Service principal that should be granted read access to the KeyVault. If unset, no service principal is granted access by default')
param principalId string = ''

@description('Name of the the environment e.g. `dev`, `uat`, `prod`')
param environmentName string

@description('API Key for Pinecone')
param pineconeApiKey string

@description('Name of the Azure Blob Container')
param azureContainerName string

@description('Azure Storage Subscription ID')
param azureStorageSubscription string

@description('Assistant Name for Pinecone')
param pineconeAssistantName string

var defaultAccessPolicies = !empty(principalId) ? [
  {
    objectId: principalId
    permissions: { secrets: [ 'get', 'list' ] }
    tenantId: subscription().tenantId
  }
] : []

// Functions for building resource names based on a naming convention
func buildProjectResourceName(abbr string, envName string, token string) string => toLower('${abbr}${envName}-${token}')

resource keyVault 'Microsoft.KeyVault/vaults@2022-07-01' = {
  name: buildProjectResourceName(abbrs.keyVaultVaults, environmentName, resourceToken)
  location: location
  tags: tags
  properties: {
    tenantId: subscription().tenantId
    sku: { family: 'A', name: 'standard' }
    enabledForTemplateDeployment: true
    accessPolicies: union(defaultAccessPolicies, [
      // define access policies here
    ])
  }
}

resource environmentNameSecret 'Microsoft.KeyVault/vaults/secrets@2022-07-01' = {
  parent: keyVault
  name: 'ENVIRONMENT_NAME'
  properties: {
    value: environmentName
  }
}

resource locationSecret 'Microsoft.KeyVault/vaults/secrets@2022-07-01' = {
  parent: keyVault
  name: 'LOCATION'
  properties: {
    value: location
  }
}

resource pineconeApiKeySecret 'Microsoft.KeyVault/vaults/secrets@2022-07-01' = {
  parent: keyVault
  name: 'PINECONE_API_KEY'
  properties: {
    value: pineconeApiKey
  }
}

resource azureContainerNameSecret 'Microsoft.KeyVault/vaults/secrets@2022-07-01' = {
  parent: keyVault
  name: 'AZURE_CONTAINER_NAME'
  properties: {
    value: azureContainerName
  }
}

resource azureStorageSubscriptionSecret 'Microsoft.KeyVault/vaults/secrets@2022-07-01' = {
  parent: keyVault
  name: 'AZURE_STORAGE_SUBSCRIPTION'
  properties: {
    value: azureStorageSubscription
  }
}

resource pineconeAssistantNameSecret 'Microsoft.KeyVault/vaults/secrets@2022-07-01' = {
  parent: keyVault
  name: 'PINECONE_ASSISTANT_NAME'
  properties: {
    value: pineconeAssistantName
  }
}

output endpoint string = keyVault.properties.vaultUri
output name string = keyVault.name
