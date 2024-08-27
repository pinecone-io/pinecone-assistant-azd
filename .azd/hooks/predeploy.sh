#!/bin/bash

# Check that .env.azure exists, if not run the postprovision hook again.
script_dir="$(dirname "$(readlink -f "$0")")"
env_azure="$script_dir/../../.env.azure"

if [[ ! -f $env_azure ]]; then
    echo ".env.azure not found. Running postprovision hook again."
    sh "$script_dir/postprovision.sh"
else
    echo ".env.azure exists."
fi
