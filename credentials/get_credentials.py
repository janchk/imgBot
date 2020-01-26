import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_discord_creds():
    if os.path.exists('credentials/discord_credentials.txt'):
                with open('credentials/discord_credentials.txt', 'r') as token:
                    TOKEN = token.read()
    else:
        try:
             TOKEN = os.environ['DISCORD_CREDENTIALS']
        except KeyError: 
                 print("Can't get discord token")
                 return 0
    
    return TOKEN

def get_gdrive_creds():
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None
    if os.path.exists('credentials/token.pickle'):
            with open('credentials/token.pickle', 'rb') as token:
                creds = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
    if not creds: # or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        elif (os.path.exists('credentials/credentials.json')):
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/credentials.json', SCOPES)
            creds = flow.run_local_server()
        elif os.environ['GDRIVE_CREDENTIALS']:
            cred_var = os.environ['GDRIVE_CREDENTIALS']
            with open('credentials/service_credentials.json', 'w+') as cred_file:
                cred_file.write(cred_var)
            creds = service_account.Credentials.from_service_account_file("credentials/service_credentials.json", scopes=SCOPES) 
        else:
            print("Can't get google drive credentials")

        # Save the credentials for the next run
        with open('credentials/token.pickle', 'wb') as token:
            pickle.dump(creds, token)
        return creds