from fastapi import APIRouter
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session

from database import get_session
from .service import upload_to_drive, download_from_drive
from .schemas import UploadFileRequest, DownloadFileRequest
from users.models import User
from users.service import decode_app_token

router = APIRouter()

@router.post("/uploadFile", response_model=UploadFileRequest)
def get_group_structure(db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    file_path = "/files_storage/test_photo.jpg"
    
    # Nazwa pliku w Google Drive
    file_target_name = "test.jpg"

    uploaded_file_id = upload_to_drive(file_path, file_target_name)
    if not uploaded_file_id:
        raise HTTPException(status_code=404, detail="Error uploading file")
    return {
        "file_id": uploaded_file_id
    }


@router.get("/downloadFile", response_model=DownloadFileRequest)
def get_group_structure(db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    file_id = "13bdCbN3fFyt7pX5k15r2nPl5tkkB03po"
    
    # Nazwa pliku w Google Drive
    file_target_name = "test.jpg"

    file_path = download_from_drive(file_id, file_target_name)
    if not file_path:
        raise HTTPException(status_code=404, detail=f"Error downloading file {file_id}")
    return {
        "file_path": file_path
    }