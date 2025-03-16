from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

import os
os.environ['LOCAL_FILE_PATH'] = os.path.dirname(os.path.abspath(__file__))


gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

file1 = drive.CreateFile({'title': 'Hello.txt'})
file1.SetContentString('Hello')
file1.Upload() # Files.insert()
