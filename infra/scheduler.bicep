param location string = resourceGroup().location
param storageAccountName string
param functionAppName string
param appServicePlanName string
param keyVaultName string

resource storageAccount 'Microsoft.Storage/storageAccounts@2021-09-01' existing = {
  name: storageAccountName
}

resource keyVault 'Microsoft.KeyVault/vaults@2022-07-01' existing = {
  name: keyVaultName
}

resource functionApp 'Microsoft.Web/sites@2021-02-01' = {
  name: functionAppName
  location: location
  kind: 'functionapp'
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: storageAccount.properties.primaryEndpoints.blob
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
        {
          name: 'WEBSITE_RUN_FROM_PACKAGE'
          value: '1'
        }
        {
          name: 'AZURE_KEY_VAULT_NAME'
          value: keyVault.name
        }
      ]
    }
  }
}

resource appServicePlan 'Microsoft.Web/serverfarms@2021-02-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: 'Y1'
    tier: 'Dynamic'
  }
}

resource timerTrigger 'Microsoft.Web/sites/functions@2021-02-01' = {
  name: 'TimerTrigger'
  parent: functionApp
  properties: {
    config: {
      bindings: [
        {
          name: 'myTimer'
          type: 'timerTrigger'
          direction: 'in'
          schedule: '0 */5 * * * *'  // Every 5 minutes
        }
      ]
    }
  }
}
