# Pinecone Assistants Sample App

Use this sample app to interact with assistants you have created in the Pinecone console. This app allows you to create a deployable Next.js application to interact with your assistants and their uploaded files.

### Built With

- Pinecone Assistant
- Next.js + Python + Tailwind + Flask Backend
- Node version 20 or higher

---
## Running the Sample App

### Want to move fast?

Use `npx create-pinecone-app` to adopt this project quickly.
This will clone the project, and prompt you for necessary secrets. Make sure you've created your assistant and uploaded your files in the Pinecone console at this point.

### Create a Pinecone API key
**Grab an API key [here](https://app.pinecone.io)**

Before you start, this application requires you to build Pinecone Assistant in the Console first. You'll also need to upload files to this assistant. Any set of PDF files will do!

### Environment Variables

This app uses two optional environment variables to control certain features:

1. `SHOW_ASSISTANT_FILES`: Set to 'true' to display the files uploaded to your Pinecone Assistant. Default is 'false'.
2. `SHOW_CITATIONS`: Set to 'true' to display citations and references in the assistant's responses. Default is 'true'.

You can set these variables in your `.env.local` file:

```
SHOW_ASSISTANT_FILES=true
SHOW_CITATIONS=true
```

### Start the project

In order to isolate Python dependencies, create a conda environment and install the dependencies there.

```bash
conda create -n pinecone-assistant-env python=3.12
conda activate pinecone-assistant-env
```

#### Dependency Installation

```bash
cd pinecone-assistant && npm install --force
```

Then, launch the app:

```bash
npm run dev
```
This will start the backend Python server as well as install dependencies in your conda environment. Navigate to localhost:3000 to see the app.

## Project structure

TODO

## Known Issues

### Vercel Python Runtime Streaming Limitation

Currently, there is an open issue regarding the lack of support for streaming responses in the Vercel Python runtime. This limitation affects applications that require real-time data streaming, such as chat applications or AI-powered assistants.

For more information and updates on this issue, please refer to the following GitHub discussion:
[Support streaming with Vercel python runtime](https://github.com/orgs/vercel/discussions/2756)

If your application requires streaming functionality, you may need to consider alternative deployment options or wait for official support from Vercel.

---
## Troubleshooting
Experiencing any issues with the sample app?
Submit an issue, create a PR, or post in our community forum!
---