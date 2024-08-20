#!/bin/bash

merge_env_files() {
    local base=$1
    local with=$2
    local output=$3

    local -a temp_vars=()
    local -a merged_vars=()

    while IFS= read -r line || [ -n "$line" ]; do
        # Remove comments and trim whitespace
        line=$(echo "$line" | cut -d'#' -f1 )
        # Trim whitespace
        line=$(echo "$line" | sed 's/^[ \t]*//;s/[ \t]*$//')

        # Skip empty lines
        if [[ -z $line ]]; then
            continue
        fi

        # Split the line into key and value
        IFS='=' read -r key value <<< "$line"

        # Remove newlines and carriage returns
        value=$(echo "$value" | tr -d '\n\r')

        # Store the key-value pair in the temp array
        temp_vars+=("$key=$value")
    done < <(cat "$base" "$with")

    for entry in "${temp_vars[@]}"; do
        key=$(echo "$entry" | cut -d'=' -f1)
        value=$(echo "$entry" | cut -d'=' -f2-)
        found=false

        for i in "${!merged_vars[@]}"; do
            if [[ "${merged_vars[$i]}" == "$key="* ]]; then
                merged_vars[$i]="$key=$value"
                found=true
                break
            fi
        done

        if [[ $found == false ]]; then
            merged_vars+=("$key=$value")
        fi
    done

    {
        for entry in "${merged_vars[@]}"; do
            key=$(echo "$entry" | cut -d'=' -f1)
            value=$(echo "$entry" | cut -d'=' -f2-)
            echo "$key=$value"
        done | sort
    } > "$output"
}

script_dir="$(dirname "$(readlink -f "$0")")"

env_local="$script_dir/../../.env.local"
env_azd="$script_dir/../../.azure/${AZURE_ENV_NAME}/.env"

env_azure="$script_dir/../../.env.azure"

if [[ ! -f $env_local ]]; then
    cp "$env_azd" "$env_azure"
    exit 0
fi

merge_env_files "$env_local" "$env_azd" "$env_azure"
