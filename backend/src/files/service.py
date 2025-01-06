from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import os


SERVICE_ACCOUNT_FILE = "service_account.json"
FOLDER_ID = "1ya1s2rfji2GPKjp-k3HWMkMSyNVokOIL"

def establish_drive_connection():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/drive.file"]
    )

    service = build('drive', 'v3', credentials=credentials)

    return service

def upload_to_drive(file_path: str, file_target_name: str) -> str:

    service = establish_drive_connection()

    file_metadata = {
        'name': file_target_name,
        'parents': [FOLDER_ID]
    }

    file = service.files().create(
        body=file_metadata,
        media_body=file_path,
        fields='id'
    ).execute()

    print(f"Uploaded file: {file_target_name} File ID: {file['id']}")

    return str(file['id'])

def download_from_drive(file_id: str, file_target_name: str):

    service = establish_drive_connection()

    request = service.files().get_media(fileId=file_id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)
    done = False

    while not done:
        status, done = downloader.next_chunk()
        print('Download progress {0}'.format(status.progress() * 100))
    
    fh.seek(0)

    file_path = os.path.join('/files_storage', file_target_name)

    with open(file_path, 'wb') as f:
        f.write(fh.read())
        f.close()

    return file_path
    