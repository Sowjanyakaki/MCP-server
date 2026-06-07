import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/gmail.compose'
]

def get_credentials():
    import json
    creds = None
    
    # Try reading token from environment variable first
    env_token = os.environ.get('GOOGLE_TOKEN_JSON')
    if env_token:
        try:
            token_data = json.loads(env_token)
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)
        except Exception as e:
            print(f"Error loading token from env: {e}")
    # Fallback to token.json
    elif os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Check for credentials in env
            env_creds = os.environ.get('GOOGLE_CREDENTIALS_JSON')
            if env_creds:
                client_config = json.loads(env_creds)
                flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            
            # For Railway, you should generate the token locally first and pass via GOOGLE_TOKEN_JSON.
            # Local flow:
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run (locally)
        try:
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        except Exception:
            pass

    return creds

if __name__ == '__main__':
    print("Fetching credentials, please log in if prompted...")
    get_credentials()
    print("Authentication successful, token.json saved.")
