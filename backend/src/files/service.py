from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from users.models import User, Member, File, FileOwnership, Composition
from .schemas import UploadFileRequest, DownloadFileRequest, DeleteFileRequest
from .schemas import FileToUserRequest, FileToSubgroupRequest, FileToCompositionRequest
from .schemas import DeleteFileToCompositionRequest
import io
import os

SERVICE_ACCOUNT_FILE = "service_account.json"
FOLDER_ID = "1ya1s2rfji2GPKjp-k3HWMkMSyNVokOIL"

def establish_drive_connection():
    """Establish a connection to Google Drive."""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/drive.file"]
    )
    service = build('drive', 'v3', credentials=credentials)
    return service

def verify_user(db: Session, email: str, parent_group: int) -> User:
    """Verify that a user exists, belongs to the group, and has the 'Kapelmistrz' role."""
    existing_user = db.query(User).filter(User.email == email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    existing_member = db.query(Member).filter(Member.user_id == existing_user.id, Member.group_id == parent_group).first()
    if not existing_member:
        raise HTTPException(status_code=404, detail="User is not a member of the group")
    if existing_member.role != "Kapelmistrz":
        raise HTTPException(status_code=403, detail="User must have Kapelmistrz role")
    return existing_user

def upload_to_drive(db: Session, email: str, file_stream, file_name, parent_group):
    """Upload a file to Google Drive and associate it with a user."""
    user = verify_user(db, email, parent_group)
    if db.query(File).filter(File.name == file_name).first():
        raise HTTPException(status_code=404, detail=f"File {file_name} already exists")
    service = establish_drive_connection()
    file_metadata = {
        'name': file_name,
        'parents': [FOLDER_ID]
    }
    media = MediaIoBaseUpload(file_stream, mimetype="application/octet-stream")
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    new_file = File(
        name=file_name,
        google_drive_id=file['id']
    )
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    assign_file_to_user(db, email, FileToUserRequest(file_id=new_file.id, user_id=user.id, parent_group=parent_group))
    return new_file

def download_from_drive(db: Session, email: str, request: DownloadFileRequest):
    """Download a file from Google Drive."""
    verify_user(db, email, request.parent_group)
    file = db.query(File).filter(File.id == request.file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail=f"File {request.file_id} not found")
    service = establish_drive_connection()
    request = service.files().get_media(fileId=file.google_drive_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    file_path = os.path.join('/files_storage', file.name)
    with open(file_path, 'wb') as f:
        f.write(fh.read())
        f.close()
    return file, file_path

def delete_from_drive(db: Session, email: str, request: DeleteFileRequest):
    """Delete a file from Google Drive and the database."""
    verify_user(db, email, request.parent_group)
    file = db.query(File).filter(File.id == request.file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail=f"File {request.file_id} not found")
    service = establish_drive_connection()
    service.files().delete(fileId=file.google_drive_id).execute()

    compositions = db.query(FileOwnership).filter(FileOwnership.file_id == request.file_id).all()
    for comp in compositions:
        db.delete(comp)
    db.commit()

    db.delete(file)
    db.commit()

def create_file_ownership(db: Session, user_id: int, file_id: int, parent_group: int) -> FileOwnership:
    """Create a file ownership record for a user."""
    if not db.query(File).filter(File.id == file_id).first():
        raise HTTPException(status_code=404, detail=f"File {file_id} not found")
    existing_member = db.query(Member).filter(Member.user_id == user_id, Member.group_id == parent_group).first()
    if not existing_member:
        raise HTTPException(status_code=404, detail="User is not a member of the group")
    new_file_ownership = FileOwnership(
        user_id=user_id,
        file_id=file_id
    )
    return new_file_ownership

def assign_file_to_user(db: Session, email: str, request: FileToUserRequest):
    """Assign a file to a user."""
    verify_user(db, email, request.parent_group)
    new_file_ownership = create_file_ownership(db, request.user_id, request.file_id, request.parent_group)
    if not db.query(FileOwnership).filter(FileOwnership.file_id == request.file_id, FileOwnership.user_id == request.user_id).first():
        db.add(new_file_ownership)
        db.commit()
        db.refresh(new_file_ownership)
    return new_file_ownership

def assign_file_to_subgroup(db: Session, email: str, request: FileToSubgroupRequest):
    """Assign a file to all members of a subgroup."""
    verify_user(db, email, request.group_id)
    existing_members = db.query(Member).filter(Member.group_id == request.group_id)
    file_ownerships = []
    for member in existing_members:
        if not db.query(FileOwnership).filter(FileOwnership.file_id == request.file_id, FileOwnership.user_id == member.user_id).first():
            new_file_ownership = create_file_ownership(db, member.user_id, request.file_id, request.group_id)
            file_ownerships.append(new_file_ownership)
            db.add(new_file_ownership)
    db.commit()
    for ownership in file_ownerships:
        db.refresh(ownership)
    return file_ownerships

def assign_file_to_composition(db: Session, email: str, request: FileToCompositionRequest):
    """Assign a file to a composition."""
    verify_user(db, email, request.parent_group)
    file = db.query(File).filter(File.id == request.file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail=f"File {request.file_id} not found")
    file.composition_id = request.composition_id
    db.commit()
    return file

def deprive_user_of_file(db: Session, email: str, request: FileToUserRequest):
    """Remove a file's ownership from a user."""
    verify_user(db, email, request.parent_group)
    file_ownership = db.query(FileOwnership).filter(FileOwnership.file_id == request.file_id, FileOwnership.user_id == request.user_id).first()
    if not file_ownership:
        raise HTTPException(status_code=404, detail=f"File ownership file_id: {request.file_id}, user_id: {request.user_id} not found")
    db.delete(file_ownership)
    db.commit()

def deprive_subgroup_of_file(db: Session, email: str, request: FileToSubgroupRequest):
    """Remove a file's ownership from a subgroup."""
    verify_user(db, email, request.group_id)
    existing_members = db.query(Member).filter(Member.group_id == request.group_id)
    for member in existing_members:
        file_ownership = db.query(FileOwnership).filter(FileOwnership.file_id == request.file_id, FileOwnership.user_id == member.id).first()
        if file_ownership:
            db.delete(file_ownership)
    db.commit()

def deprive_composition_of_file(db: Session, email: str, request: DeleteFileToCompositionRequest):
    """Remove a file's association with a composition."""
    verify_user(db, email, request.parent_group)
    file = db.query(File).filter(File.id == request.file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail=f"File {request.file_id} not found")
    file.composition_id = None
    db.commit()
    return file
