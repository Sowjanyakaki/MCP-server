# Railway Deployment Guide

This guide details how to deploy the Google MCP Server to [Railway](https://railway.app/).

## Prerequisites

1. A Railway account
2. A GitHub account with the project repository
3. Your local `credentials.json` and `token.json` files for Google API access

## 1. Important Code Considerations for Production

Before deploying to Railway, be aware of the following modifications that are necessary for production:

### Interactive Terminal Blocker
The current application uses `input("Approve? (y/n): ")` to enforce human-in-the-loop security. 
- **The Issue:** Railway environments do not have interactive terminals. Code waiting for `input()` will hang indefinitely and cause requests to timeout.
- **The Fix:** We will bypass this check in production by checking for a `RAILWAY_ENVIRONMENT` environment variable. If present, the server will automatically approve actions without prompting.

### Secure Credentials Handling
You should **never** commit `credentials.json` and `token.json` to GitHub. 
- **The Fix:** You need to update your `auth.py` file to load these credentials from environment variables. A common approach is converting the JSON contents into Base64 encoded strings and storing them as variables in the Railway dashboard.

## 2. Configuration Files

Add a `railway.toml` to the root of your project to specify how Railway should build and run your application.

```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "uvicorn server:app --host 0.0.0.0 --port $PORT"
```

*Note: Railway automatically assigns a dynamic port using the `$PORT` environment variable. Ensure your start command utilizes it.*

## 3. Deployment Steps

1. **Push to GitHub**: Make sure all your code (excluding the `.json` credential files and `venv`) is pushed to your GitHub repository.
2. **Create Railway Project**:
   - Go to the Railway dashboard.
   - Click **New Project** > **Deploy from GitHub repo**.
   - Select your MCP Server repository.
3. **Configure Environment Variables**:
   - Once the service is created, go to the **Variables** tab.
   - Add your Google credentials (e.g., `GOOGLE_CREDENTIALS_JSON`, `GOOGLE_TOKEN_JSON`) depending on how you implement the auth fix.
4. **Deploy**:
   - Railway will automatically trigger a deployment. 
   - Wait for the build to complete.
5. **Generate a Domain**:
   - Go to the **Settings** tab of your service.
   - Under "Networking", click **Generate Domain** to get a public URL for your server.

## 4. Verifying the Deployment

You can test the deployment by sending a POST request to your new Railway domain:

```bash
curl -X POST https://your-railway-app-url.up.railway.app/append_to_doc \
  -H "Content-Type: application/json" \
  -d '{"doc_id": "YOUR_DOC_ID", "content": "Hello from Railway!"}'
```

*(Ensure you have resolved the interactive approval blocker before testing, otherwise the request will time out).*
