from __future__ import print_function

import os.path
import io
from traceback import print_exc

import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
import googleapiclient.errors as errors 

class GoogleDrive:
    drive_service = None
    def __init__(self, SCOPES, CLIENT_ID):
        try:
            if str(CLIENT_ID).endswith(".json"):
                self.SCOPES = SCOPES
                self.CLIENT_ID = CLIENT_ID
                drive_service = self.__oauth2(self.CLIENT_ID, self.SCOPES)
            else:
                raise ValueError(
                    str(CLIENT_ID)
                        + " is not a valid json file for credentials")
        except:
            print_exc()
    
    @classmethod
    def from_token(cls, token):
        try:
            if os.path.exists(token):
                with open(token, 'rb') as tk:
                    creds = pickle.load(tk)
                    cls.drive_service = build('drive', 'v3', credentials=creds)
                    return cls
            else:
                raise FileNotFoundError(str(token) + " does not exist as path")
        except:
            print_exc()
            return None
    
    def __oauth2(self, credentials, scopes):
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials, scopes)
        creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

        service = build('drive', 'v3', credentials=creds)
        return service
    
    @classmethod
    def upload(cls, fpath, title, description=None, mimetype=None, folder=None):
        try:
            if os.path.exists(fpath):
                body = {
                'path': fpath,
                'name': fpath.split("\\")[len(fpath.split("\\")) - 1],
                'title': title,
                'description': None,
                'mimetype': None,
                'parents': None
                }
                if description:
                    body['description'] = description
                if mimetype:
                    body['mimetype'] = mimetype
                if folder:
                    body['parents'] = folder
                
                media = MediaFileUpload(
                    body.get('path'),
                    resumable=True)
                
                if cls.drive_service.files().get(
                    fileId=cls.search(folder)[0].get('id')).execute() == None:
                    if body.get('parents') != None:
                        body['parents'] = [
                            cls.create_folder(folder).get('id')
                        ]
                else:
                    body['parents'] = [
                        cls.search(folder)[0].get('id')
                    ]
                
                upload = cls.drive_service.files().create(
                    body=body,
                    media_body=media,
                    fields='id').execute()

                # Uncomment the following line to print the File ID
                print('File ID: %s' % upload.get('id'))
                
                return upload
            else:
                raise FileNotFoundError(str(fpath) + "does not exist in the given folder")
        except errors.HttpError as error:
            print("An error occurred during uploading: " + str(error))
            print_exc()
        except:
            print_exc()
    
    @classmethod
    def create_folder(cls, name):
        metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = cls.drive_service.files().create(
            body=metadata,
            fields='id').execute()
        # Uncomment the following line to print the File ID
        #print('Folder ID: %s' % folder.get('id'))
        return folder
    
    @classmethod
    def search(cls, name):
        page_token = None
        found = []
        try:
            while True:
                #Set the query string
                q = "name='{}'".format(name)
                #Search with provided query string
                response = cls.drive_service.files().list(
                    q=q,
                    spaces='drive',
                    fields='nextPageToken, files(id, name, mimeType)',
                    pageToken=page_token).execute()
                #Insert the results of the research 
                for element in response.get('files', []):
                    found.append(element)

                #Interrupt the research when page_token is None
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break
        except:
            print_exc()
        finally:
            return found
    
    @classmethod
    def download(cls, id):
        """
        It's the basic code of the Google Drive APIs standard doc
        """
        request = cls.drive_service.files().get_media(fileId=id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
