targetScope = 'subscription'

@minLength(1)
@maxLength(6)
@description('Name of the the environment e.g. `dev`, `uat`, `prod`')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

@description('API Key for Pinecone')
param pineconeApiKey string

@description('Region for Pinecone')
param pineconeRegion string

@description('Name of the Azure Blob Container')
param azureContainerName string

@description('Azure Storage Subscription ID')
param azureStorageSubscription string

@description('Assistant Name for Pinecone')
param pineconeAssistantName string

// Load abbreviations from the JSON file
var abbrs = loadJsonContent('./abbreviations.json')

// Generate a unique token to be used in naming resources
var resourceToken = take(toLower(uniqueString(subscription().id, environmentName, location)), 4)

// Functions for building resource names based on a naming convention
func buildResourceGroupName(abbr string, envName string) string => toLower('${abbr}${envName}')
func buildProjectResourceName(abbr string, envName string, token string) string => toLower('${abbr}${envName}-${token}')

// Tags that should be applied to all resources
var tags = {
  'azd-env-name': environmentName
}

// Resource Group
resource resourceGroup 'Microsoft.Resources/resourceGroups@2022-09-01' = {
  name: buildResourceGroupName(abbrs.resourcesResourceGroups, environmentName)
  location: location
  tags: tags
}

// Module to deploy resources within the resource group
module resources 'modules/resources.bicep' = {
  name: 'deployResources'
  scope: resourceGroup
  params: {
    environmentName: environmentName
    location: location
    resourceToken: resourceToken
    abbrs: abbrs
    pineconeApiKey: pineconeApiKey
    pineconeRegion: pineconeRegion
    azureContainerName: azureContainerName
    azureStorageSubscription: azureStorageSubscription
    pineconeAssistantName: pineconeAssistantName
    tags: tags
  }
}

// Outputs
output storageAccountName string = resources.outputs.storageAccountName
output containerName string = resources.outputs.containerName
output webAppUrl string = resources.outputs.webAppUrl
