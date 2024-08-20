#!/bin/bash

script_dir="$(dirname "$(readlink -f "$0")")"

# Run script to generate the environment variables in .env
"$script_dir/../scripts/create-env.sh"

# Run script to generate an `env-vars.json` file used by the infra scripts
"$script_dir/../scripts/create-infra-env-vars.sh"

