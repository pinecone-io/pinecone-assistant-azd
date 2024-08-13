param name string
param location string = resourceGroup().location
param tags object = {}
param containerName string

resource storageAccount 'Microsoft.Storage/storageAccounts@2021-09-01' = {
  name: name
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  tags: tags
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2021-09-01' = {
  name: 'default'
  parent: storageAccount
}

resource blobContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2021-09-01' = {
  name: containerName
  parent: blobService
  properties: {}
}

output storageAccountName string = storageAccount.name
output containerName string = blobContainer.name
output storageAccountEndpoint string = storageAccount.properties.primaryEndpoints.blob
