param name string
param location string = resourceGroup().location
param tags object = {}

resource keyVault 'Microsoft.KeyVault/vaults@2021-06-01-preview' = {
  name: name
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    accessPolicies: []
  }
  tags: tags
}

output keyVaultName string = keyVault.name
output keyVaultUri string = keyVault.properties.vaultUri
