from fastapi import APIRouter
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session

from database import get_session
from .service import upload_to_drive, download_from_drive, delete_from_drive
from .schemas import UploadFileRequest, DownloadFileRequest, DeleteFileRequest
from users.models import User
from users.service import decode_app_token

router = APIRouter()

@router.post("/uploadFile", status_code=201)
def upload_file_to_drive(file_name: str, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = decode_app_token(token)
    
    file_path = "/files_storage/test_photo.jpg"

    uploaded_file = upload_to_drive(db, user_data.get("email"), file_path, file_name)
    if not uploaded_file:
        raise HTTPException(status_code=404, detail="Error uploading file")
    return { "created": uploaded_file }


@router.get("/downloadFile", response_model=DownloadFileRequest)
def get_file_from_drive(file_name: str, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = decode_app_token(token)

    file_path = download_from_drive(db, user_data.get("email"), file_name)
    if not file_path:
        raise HTTPException(status_code=404, detail=f"Error downloading file {file_name}")
    return {
        "file_path": file_path
    }


@router.delete("/deleteFile", response_model=DeleteFileRequest)
def delete_file_from_drive(file_name: str, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = decode_app_token(token)

    delete_from_drive(db, user_data.get("email"), file_name)

    return {
        "deleted": file_name
    }
