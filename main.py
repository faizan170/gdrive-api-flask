from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']



def createDir(path):
    file_metadata = {
    'mimeType': 'application/vnd.google-apps.folder',
    'name' : 'sa',
    'parents':["1AwOY8g6WyM2MVOyurIyb_cnOJfewvrDF"]
    }
    
    
    file = service.files().create(body=file_metadata,
                                        fields='id').execute()
    print('Folder ID: %s' % file.get('id'))


def uploadFile2(service):
    file_name = "test"
    print("Uploading file " + file_name + "...")
    p = [{"id": "1AwOY8g6WyM2MVOyurIyb_cnOJfewvrDF", "kind": "drive#childList"}]
    #We have to make a request hash to tell the google API what we're giving it
    body = {'name': file_name, "parents" : p, 'mimeType': 'application/vnd.google-apps.document'}

    #Now create the media file upload object and tell it what file to upload,
    #in this case 'test.html'
    media = MediaFileUpload('test.html', mimetype = 'text/html')

    #Now we're doing the actual post, creating a new file of the uploaded type
    fiahl = service.files().create(body=body, media_body=media).execute()

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    
    

    #uploadFile2(service)
    # Call the Drive v3 API
    results = service.files().list(fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

if __name__ == '__main__':
    main()