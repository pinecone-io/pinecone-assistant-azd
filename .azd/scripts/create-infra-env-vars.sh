#!/bin/bash

# Function to remove quotes from a value
remove_quotes() {
    local value=$1
    local quote_char=${2:-'"'}
    echo "$value" | sed "s/^$quote_char//;s/$quote_char$//"
}

# Function to read env vars from a file and store them in a global array
read_env_vars() {
    local path=$1
    local -a temp_vars=()

    if [[ ! -f $path ]]; then
        return
    fi

    while IFS= read -r line || [ -n "$line" ]; do
        # Remove comments and trim whitespace
        line=$(echo "$line" | cut -d'#' -f1 | xargs)

        # Skip empty lines
        if [[ -z $line ]]; then
            continue
        fi

        # Split the line into key and value
        IFS='=' read -r key value <<< "$line"

        # Remove newlines and carriage returns
        value=$(echo "$value" | tr -d '\n\r')

        # Remove quotes
        value=$(remove_quotes "$value" '"')
        value=$(remove_quotes "$value" "'")

        # Store the key-value pair in the temp array
        temp_vars+=("$key=$value")
    done < "$path"

    # Merge temp_vars into env_vars, overwriting existing keys
    for entry in "${temp_vars[@]}"; do
        key=$(echo "$entry" | cut -d'=' -f1)
        value=$(echo "$entry" | cut -d'=' -f2-)
        found=false

        for i in "${!env_vars[@]}"; do
            if [[ "${env_vars[$i]}" == "$key="* ]]; then
                env_vars[$i]="$key=$value"
                found=true
                break
            fi
        done

        if [[ $found == false ]]; then
            env_vars+=("$key=$value")
        fi
    done
}

# Initialize the env_vars array
env_vars=()

# Read `.env`, `.env.production`, and `.env.local` files into the env_vars array
script_dir="$(dirname "$(readlink -f "$0")")"

env_path="$script_dir/../../.env"
read_env_vars "$env_path"

env_production_path="$script_dir/../../.env.production"
read_env_vars "$env_production_path"

env_local_path="$script_dir/../../.env.local"
read_env_vars "$env_local_path"

# Produce a `env-vars.json` file that can be used by the infra scripts
output_path="$script_dir/../../infra/env-vars.json"

# Convert the env_vars array to JSON format and write to output_path using jq
echo '{' > "$output_path"
for entry in "${env_vars[@]}"; do
    key=$(echo "$entry" | cut -d'=' -f1)
    value=$(echo "$entry" | cut -d'=' -f2-)
    echo "  \"$key\": \"$value\"," >> "$output_path"
done
# Remove the trailing comma and close the JSON object
sed -i '' -e '$ s/,$//' "$output_path"
echo '}' >> "$output_path"

# Verify the content of the output file
#cat "$output_path"
