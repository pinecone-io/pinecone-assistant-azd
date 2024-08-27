# Pinecone Assistants Sample App

Use this sample app to interact with assistants you have created in the Pinecone console. This app allows you to create a deployable Next.js application to interact with your assistants and their uploaded files.

### Built With

- Pinecone Assistant
- Azure `azd` templates
- Next.js + Tailwind + Python
- Node version 20 or higher

---

## Running the Sample App

### Want to move fast?

The quickest way to try this `azd` template out is using [GitHub Codespaces](https://docs.github.com/en/codespaces) or in a [VS Code Dev Container](https://code.visualstudio.com/docs/devcontainers/containers):

[![Open in GitHub Codespaces](https://img.shields.io/static/v1?style=for-the-badge&label=GitHub+Codespaces&message=Open&color=brightgreen&logo=github)](https://github.com/codespaces/new/pinecone-io/pinecone-assistant-azd)
[![Open in Dev Container](https://img.shields.io/static/v1?style=for-the-badge&label=Dev+Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/pinecone-io/pinecone-assistant-azd)

You can also get started quickly using a terminal. Simply run `azd init -t pinecone-io/pinecone-assistant-azd` to clone the project.

**Note**
> This template is only guaranteed to work on MacOS or Linux. It lacks Windows support, so if you would like to add that, please feel free to do so and submit a PR.

### Create a Pinecone API key

**Grab an API key [here](https://app.pinecone.io/-/projects/-/keys)**

### Environment Variables

There are two required environment variables:

1. `PINECONE_API_KEY`: You can get this from the [Pinecone console](https://app.pinecone.io/-/projects/-/keys). If you're running the app locally then add this to your environment. If you're running in Github CI, be sure to add it as a [secret in your repository](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions). To configure required secrets for connecting to Azure, simply run `azd pipeline config`.
2. `PINECONE_ASSISTANT_NAME`: This defaults to `example-assistant` but you can name it whatever you like. If the assistant doesn't exist one will be created during post-deploy operations.

All of the other environment variables in `.env.template` are completely optional.

This app uses two additional optional environment variables to control certain features:

1. `SHOW_ASSISTANT_FILES`: Set to 'true' to display the files uploaded to your Pinecone Assistant. Default is 'false'.
2. `SHOW_CITATIONS`: Set to 'true' to display citations and references in the assistant's responses. Default is 'true'.

You can set these variables in your `.env.local` file:

```bash
SHOW_ASSISTANT_FILES=true
SHOW_CITATIONS=true
```

### Start the project

Before doing anything else be sure to clone the repo.

In order to isolate Python dependencies, create a virtual environment and install the dependencies there.

MacOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

#### Dependency Installation

```bash
pip install -r requirements.txt
```

Then, deploy the app:

```bash
# follow the prompts to sign in to your Azure account
azd auth login

# install dependencies
npm i

# create a `.env.local` file from the provided template
npm run env:init

# follow the prompts to provision the infrastructure resources in Azure
azd provision

# deploy the app to the provisioned infrastructure
azd deploy
```

**Note:**
> If deployment fails initially, try running

```bash
sh ./.azd/hooks/postprovision.sh
```

> to make sure your environment is setup properly.

This will provision the necessary Azure resources, run the Python import script to seed your new assistant with the sample PDFs in /assets, and deploy the application to Azure.

### Adding new files to the Assistant

To add new files, you can upload them directly in the [Pinecone console](https://app.pinecone.io/-/projects/-/assistant). Or, download them to your local filesystem in the project's `assets/` directory. You can then run

```bash
python src/file_manager/upload.py
```

The script will find any new PDF or text files (ending in `pdf` or `txt`) in that directory and add them to the Assistant.

**Note:**
> The script ignores any files it's seen before, as tracked in the `processed_files` file. Remove or edit that file, or give the new versions different names, if you want to replace or supplement files you've previously uploaded.

## Project structure

TODO

## Known Issues

---

## Troubleshooting

Experiencing any issues with the sample app? Submit an issue, create a PR, or post in our [community forum](https://community.pinecone.io)!

---
