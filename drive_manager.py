from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth
import os

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

def upload_to_folder(file_name, file_path):
    results_folder_id = os.environ.get('RESULTS_FOLDER_ID')
    metadata = {
        'title': file_name,
        'mimeType': 'application/zip',
        'parents': [{'id': results_folder_id}]
    }
    file = drive.CreateFile(metadata)
    file.SetContentFile(file_path)
    file.Upload()

if __name__ == '__main__':
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        print('title: %s, id: %s' % (file1['title'], file1['id']))