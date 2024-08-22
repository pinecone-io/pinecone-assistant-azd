$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Run script to generate an `env-vars.json` file used by the infra scripts
& $(Join-Path $scriptDir "../scripts/create-infra-env-vars.ps1")

if [ -z $AZURE_ENV_NAME ]; then
    # The Azure environment hasn't been set yet. Check if there's a directory under .azure and use that. Otherwise, prompt for one.
    num_envs=$(ls .azure/ | grep -v -e .gitignore -e config.json | wc -l)
    if [ $num_envs = 1 ];then
        export AZURE_ENV_NAME=`ls .azure/ | grep -v -e .gitignore -e config.json | sed -e 's/\///'`
    else
        echo -n "Unable to determine AZURE_ENV_NAME, please provide it: "
        read value
        export AZURE_ENV_NAME=$value
    fi
fi