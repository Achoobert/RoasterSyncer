from oauth2client.service_account import ServiceAccountCredentials
#from oauth2client import file, client, tools
from apiclient.discovery import build
from apiclient.http import MediaFileUpload

#Set up a credentials object I think
creds = ServiceAccountCredentials.from_json_keyfile_name('internet-of-beans-c596a4591f1c.json', ['https://www.googleapis.com/auth/drive'])

#Now build our api object, thing
drive_api = build('drive', 'v3', credentials=creds)

file_name = "test"
print ("Uploading file " + file_name + "...")

#We have to make a request hash to tell the google API what we're giving it
body = {'name': file_name, 'mimeType': 'application/vnd.google-apps.document'}

#Now create the media file upload object and tell it what file to upload,
#in this case 'test.html'
media = MediaFileUpload('test.html', mimetype = 'text/html')

#Now we're doing the actual post, creating a new file of the uploaded type
fiahl = drive_api.files().create(body=body, media_body=media).execute()

#Because verbosity is nice
print ("Created file '%s' id '%s'." % (fiahl.get('name'), fiahl.get('id')))
