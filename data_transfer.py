import os
import mimetypes

import requests
import shutil

from datetime import datetime
from common.checker import file_ext_checker
from credentials.get_credentials import get_gdrive_creds

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

                # file_metadata = {'name':filename, 'parents':[self.folder_id]}
                file_metadata = {'name':filename, 'parents':[self.root_folder_id]}
                media = MediaFileUpload(filename, mimetype=mimetype)
                file = self.drive.files().create(body=file_metadata, media_body=media, fields='id').execute()
                os.remove(filename)
            else:
                pass


    
    def __upload_init(self):
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = get_gdrive_creds()

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
    
    def __share_folder(self, email, role='writer'):
        """
        roles = 'writer', 'commenter', 'reader'
        """
        file_id = self.root_folder_id
        user_permission = {
            'type': 'user', 
            'role': role,
            'emailAddress': email
        }
        command = self.drive.permissions().create(fileId=file_id, body=user_permission, fields='id')
        command.execute