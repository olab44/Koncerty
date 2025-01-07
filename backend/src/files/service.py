from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from users.models import User, Member, File, FileOwnership
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


def verify_user_kapelmistrz_role():
    # TODO sprawdzić uprawnienia usera w grupie
    # existing_member = db.query(Member).filter(Member.user_id == user.id, Member.group_id == request.parent_group).first()

    # if not existing_member:
    #     raise HTTPException(status_code=404, detail="User is not a member of the group")

    # if existing_member.role != "Kapelmistrz":
    #     raise HTTPException(status_code=403, detail="User must have Kapelmistrz role")
    pass


def upload_to_drive(db: Session, email: str, file_path: str, file_name: str):
    
    existing_user = db.query(User).filter(User.email == email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    verify_user_kapelmistrz_role()

    if db.query(File).filter(File.name == file_name).first():
        raise HTTPException(status_code=404, detail=f"File {file_name} already exists")

    service = establish_drive_connection()
    file_metadata = {
        'name': file_name,
        'parents': [FOLDER_ID]
    }

    file = service.files().create(
        body=file_metadata,
        media_body=file_path,
        fields='id'
    ).execute()

    new_file = File(
        name = file_name,
        google_drive_id = file['id']
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    # print(f"Uploaded file: {file_name} File ID: {file['id']}")
    return new_file


def download_from_drive(db: Session, email: str, file_name: str):

    existing_user = db.query(User).filter(User.email == email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    file = db.query(File).filter(File.name == file_name).first()
    if not file:
        raise HTTPException(status_code=404, detail=f"File {file_name} not found")

    service = establish_drive_connection()
    request = service.files().get_media(fileId=file.google_drive_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)
    done = False

    while not done:
        status, done = downloader.next_chunk()
    
    fh.seek(0)
    file_path = os.path.join('/files_storage', file_name)

    with open(file_path, 'wb') as f:
        f.write(fh.read())
        f.close()

    return file_path


def delete_from_drive(db: Session, email: str, file_name: str):

    existing_user = db.query(User).filter(User.email == email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    file = db.query(File).filter(File.name == file_name).first()
    if not file:
        raise HTTPException(status_code=404, detail=f"File {file_name} not found")

    service = establish_drive_connection()
    service.files().delete(fileId=file.google_drive_id).execute()

    db.delete(file)
    db.commit()


