#!/bin/bash

script_dir="$(dirname "$(readlink -f "$0")")"

# Run script to generate the environment variables in .env
"$script_dir/../scripts/create-env.sh"

# Run script to generate an `env-vars.json` file used by the infra scripts
"$script_dir/../scripts/create-infra-env-vars.sh"

# Function to get secret from Key Vault
get_secret() {
    local secret_name=$1
    local fallback_value=$2
    #local secret_value=$(az keyvault secret show --vault-name "$KEY_VAULT_NAME" --name "$secret_name" --query value -o tsv 2>/dev/null)
    if [ -z "$secret_value" ]; then
        echo "$fallback_value"
    else
        echo "$secret_value"
    fi
}

# Export environment variables, using Key Vault secrets if they exist
export ENVIRONMENT_NAME=$(get_secret "ENVIRONMENT_NAME" "$ENVIRONMENT_NAME")
export LOCATION=$(get_secret "LOCATION" "$LOCATION")
export PINECONE_API_KEY=$(get_secret "PINECONE_API_KEY" "$PINECONE_API_KEY")
export AZURE_CONTAINER_NAME=$(get_secret "AZURE_CONTAINER_NAME" "$AZURE_CONTAINER_NAME")
export AZURE_STORAGE_SUBSCRIPTION=$(get_secret "AZURE_STORAGE_SUBSCRIPTION" "$AZURE_STORAGE_SUBSCRIPTION")
export PINECONE_ASSISTANT_NAME=$(get_secret "PINECONE_ASSISTANT_NAME" "$PINECONE_ASSISTANT_NAME")

