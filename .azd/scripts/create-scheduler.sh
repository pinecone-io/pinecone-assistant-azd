#!/bin/bash

# Define variables
FUNCTION_APP_NAME="scheduler-function-app"
RESOURCE_GROUP_NAME=${AZURE_RESOURCE_GROUP}
ZIP_FILE="file_manager.zip"

# Zip the function app code
cd src/file_manager/
zip -r ../../$ZIP_FILE ./*
cd ../..

# Deploy the function app code
az functionapp deployment source config-zip \
  --resource-group $RESOURCE_GROUP_NAME \
  --name $FUNCTION_APP_NAME \
  --src $ZIP_FILE

# Clean up
rm $ZIP_FILE