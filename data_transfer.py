import pickle
import os
import mimetypes

import requests
import shutil

from datetime import datetime
from common.checker import file_ext_checker

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload


SCOPES = ['https://www.googleapis.com/auth/drive']

class DataHandler:
    def __init__(self):
        self.folder_id = None
        self.drive = None
        self.root_folder_id = None

        self.__upload_init()
        self.__get_root_folder_id()
        self.__folder_init()
    
    def __del__(self):
        pass


    def upload(self, data):
        """
        """
        # content = data.attachments[0]
        for d_file in data:

            attc_content = d_file.attachments[0]
            r = requests.get(attc_content.url, stream=True)
            
            orig_ext = attc_content.filename.split('.')[-1]
            filename = str(d_file.id) + "." + orig_ext
            mimetype = mimetypes.guess_type(filename)[0]

            file_pres = file_ext_checker(self.drive, filename, mimetype)

            if (not file_pres):
                with open(filename ,'wb') as out_file:
                    shutil.copyfileobj(r.raw, out_file)
                # file_drive = drive.CreateFile({'title':d_file.filename})

                file_metadata = {'name':filename, 'parents':[self.folder_id]}
                media = MediaFileUpload(filename, mimetype=mimetype)
                file = self.drive.files().create(body=file_metadata, media_body=media, fields='id').execute()
                os.remove(filename)
            else:
                pass


    
    def __upload_init(self):
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
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

            # Save the credentials for the next run
            with open('credentials/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.drive = build('drive', 'v3', credentials=creds)



    def __folder_init(self):
        folder_name = str(datetime.date(datetime.now()))
        mimeType = 'application/vnd.google-apps.folder'
        file_metadata = {
        'name': folder_name,
        'mimeType': mimeType,
        'parents':[self.root_folder_id]}

        folder_pres = file_ext_checker(self.drive, folder_name, mimeType )

        if (not folder_pres):
            file = self.drive.files().create(body=file_metadata,fields='id').execute()
            self.folder_id = file.get('id')
        else:
            self.folder_id = folder_pres

    def __get_root_folder_id(self):
        folder_name = "EVR_PHOTOS"
        mimeType = 'application/vnd.google-apps.folder'
        file_metadata = {
        'name': folder_name,
        'mimeType': mimeType}

        folder_pres = file_ext_checker(self.drive, folder_name, mimeType )

        if (not folder_pres):
            file = self.drive.files().create(body=file_metadata,fields='id').execute()
            self.root_folder_id = file.get('id')
        else:
            self.root_folder_id = folder_pres
        
        