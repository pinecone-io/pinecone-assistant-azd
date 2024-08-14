# Define variables
$FUNCTION_APP_NAME = "scheduler-function-app"
$RESOURCE_GROUP_NAME = $env:AZURE_RESOURCE_GROUP
$ZIP_FILE = "file_manager.zip"

# Zip the function app code
Set-Location -Path "src/file_manager/"
Compress-Archive -Path * -DestinationPath "../../$ZIP_FILE"
Set-Location -Path "../.."

# Deploy the function app code
az functionapp deployment source config-zip `
  --resource-group $RESOURCE_GROUP_NAME `
  --name $FUNCTION_APP_NAME `
  --src $ZIP_FILE

# Clean up
Remove-Item -Path $ZIP_FILE