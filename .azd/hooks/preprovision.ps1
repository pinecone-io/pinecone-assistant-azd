$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Run script to generate an `env-vars.json` file used by the infra scripts
& $(Join-Path $scriptDir "../scripts/create-infra-env-vars.ps1")

if (-not $env:AZURE_ENV_NAME) {
    # The Azure environment hasn't been set yet. Check if there's a directory under .azure and use that. Otherwise, prompt for one.
    $azureDir = Join-Path $scriptDir "../../.azure"
    $envDirs = Get-ChildItem -Path $azureDir -Directory | Where-Object { $_.Name -notin @('.gitignore', 'config.json') }

    if ($envDirs.Count -eq 1) {
        $env:AZURE_ENV_NAME = $envDirs[0].Name
    } else {
        $env:AZURE_ENV_NAME = Read-Host "Unable to determine AZURE_ENV_NAME, please provide it"
    }
}