#!/bin/bash

# Check if a .venv directory exists, if not create one
script_dir="$(dirname "$(readlink -f "$0")")"
root_dir="$script_dir/../.."
venv_dir="$script_dir/../../.venv"

if [[ ! -d $venv_dir ]]; then
    python -m venv $venv_dir
    echo "Created virtual environment in $venv_dir"
else
    echo "Virtual environment already exists in $venv_dir"
fi

echo "Installing depencencies from requirements.txt into virtual environment."
$venv_dir/bin/python -m pip install -r $root_dir/requirements.txt -q

# Run script to generate the environment variables in .env
bash "$script_dir/../scripts/create-env.sh"

# Run script to generate an `env-vars.json` file used by the infra scripts
bash "$script_dir/../scripts/create-infra-env-vars.sh"