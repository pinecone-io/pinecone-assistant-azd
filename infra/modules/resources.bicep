param environmentName string
param location string
param resourceToken string
param abbrs object
param pineconeApiKey string
param azureContainerName string
param azureStorageSubscription string
param pineconeAssistantName string
param tags object

// Functions for building resource names based on a naming convention
func buildProjectResourceName(abbr string, envName string, token string) string => toLower('${abbr}${envName}-${token}')
func buildProjectResourceNameNoDash(abbr string, envName string, token string) string => toLower('${abbr}${envName}${token}')

// Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2021-09-01' = {
  name: buildProjectResourceNameNoDash(abbrs.storageStorageAccounts, environmentName, resourceToken)
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  tags: tags
}

// Blob Service
resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2021-09-01' = {
  name: 'default'
  parent: storageAccount
}

// Blob Container
resource blobContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2021-09-01' = {
  name: azureContainerName
  parent: blobService
  properties: {}
}

// App Service Plan
resource appServicePlan 'Microsoft.Web/serverfarms@2021-02-01' = {
  name: buildProjectResourceName(abbrs.webServerFarms, environmentName, resourceToken)
  location: location
  sku: {
    tier: 'Basic'
    name: 'B1'
  }
  tags: tags
}

// Web App
resource webApp 'Microsoft.Web/sites@2021-02-01' = {
  name: buildProjectResourceName(abbrs.webSitesAppService, environmentName, resourceToken)
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      appSettings: [
        {
          name: 'PINECONE_API_KEY'
          value: pineconeApiKey
        }
        {
          name: 'AZURE_CONTAINER_NAME'
          value: azureContainerName
        }
        {
          name: 'AZURE_STORAGE_SUBSCRIPTION'
          value: azureStorageSubscription
        }
        {
          name: 'PINECONE_ASSISTANT_NAME'
          value: pineconeAssistantName
        }
      ]
    }
  }
  tags: tags
}

// Outputs
output storageAccountName string = storageAccount.name
output containerName string = blobContainer.name
output webAppUrl string = webApp.properties.defaultHostName
