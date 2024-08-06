#!/bin/bash

remove_quotes() {
    local value=$1
    local quote_char=${2:-'"'}

    if [[ ${value:0:1} == "$quote_char" && ${value: -1} == "$quote_char" ]]; then
        value=${value:1:-1}
    fi

    echo "$value"
}

read_env_vars() {
    local path=$1
    local env_vars=()

    if [[ ! -f $path ]]; then
        # File does not exist so there is nothing to do
        echo "$(declare -p env_vars)"
        return
    fi

    while IFS='=' read -r key value; do
        if [[ -z $value ]]; then
            env_vars+=("$key=")
        else
            value=$(remove_quotes "$value" '"')
            value=$(remove_quotes "$value" "'")
            env_vars+=("$key=$value")
        fi
    done < "$path"

    echo "$(declare -p env_vars)"
}

read_azd_env_vars() {
    local env_vars=()

    azd_env=$(azd env get-values)

    while IFS= read -r entry; do
        if [[ -z $entry || $entry != *"="* ]]; then
            continue
        fi

        key=$(echo "$entry" | cut -d'=' -f1)
        value=$(echo "$entry" | cut -d'=' -f2-)

        if [[ -z $key || $key == *" "* ]]; then
            continue
        fi

        if [[ -z $value ]]; then
            env_vars+=("$key=")
        else
            value=$(remove_quotes "$value" '"')
            value=$(remove_quotes "$value" "'")
            env_vars+=("$key=$value")
        fi
    done <<< "$azd_env"

    echo "$(declare -p env_vars)"
}

merge_objects() {
    local base=("${!1}")
    local with=("${!2}")
    local merged=("${base[@]}")

    for entry in "${with[@]}"; do
        key=$(echo "$entry" | cut -d'=' -f1)
        value=$(echo "$entry" | cut -d'=' -f2-)
        found=false

        for i in "${!merged[@]}"; do
            if [[ "${merged[$i]}" == "$key="* ]]; then
                found=true
                if [[ -n $value ]]; then
                    merged[$i]="$key=$value"
                fi
                break
            fi
        done

        if [[ $found == false ]]; then
            merged+=("$key=$value")
        fi
    done

    echo "$(declare -p merged)"
}

script_dir="$(dirname "$(readlink -f "$0")")"

env_azd_path="$script_dir/../../.azure/${AZURE_ENV_NAME}/.env"

if [[ -z $AZURE_ENV_NAME ]]; then
    eval "$(read_azd_env_vars)"
else
    eval "$(read_env_vars "$env_azd_path")"
fi
env_azd=("${env_vars[@]}")

# Output info required for domain verification
for entry in "${env_azd[@]}"; do
    key=$(echo "$entry" | cut -d'=' -f1)
    value=$(echo "$entry" | cut -d'=' -f2-)
    case "$key" in
        "AZURE_CONTAINER_STATIC_IP") static_ip="$value" ;;
        "AZURE_WEB_APP_FQDN") fqdn="$value" ;;
        "AZURE_CONTAINER_DOMAIN_VERIFICATION_CODE") verification_code="$value" ;;
    esac
done

echo "=== Container apps domain verification ==="
echo "Static IP: $static_ip"
echo "FQDN: $fqdn"
echo "Verification code: $verification_code"
