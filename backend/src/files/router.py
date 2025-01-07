from fastapi import APIRouter
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session

from database import get_session
from .service import upload_to_drive, download_from_drive, delete_from_drive, assign_file_to_user
from .service import assign_file_to_subgroup, assign_file_to_composition
from .schemas import * 
from users.models import User
from users.service import decode_app_token

router = APIRouter()

@router.post("/uploadFile", status_code=201)
def upload_file_to_drive(request: UploadFileRequest, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = decode_app_token(token)
    
    file_path = "/files_storage/test_photo.jpg"

    uploaded_file = upload_to_drive(db, user_data.get("email"), file_path, request)
    if not uploaded_file:
        raise HTTPException(status_code=404, detail="Error uploading file")
    return { "created_file": uploaded_file }


@router.get("/downloadFile", response_model=DownloadFileResponse)
def get_file_from_drive(request: DownloadFileRequest, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = decode_app_token(token)

    file, file_path = download_from_drive(db, user_data.get("email"), request)
    if not file_path:
        raise HTTPException(status_code=404, detail=f"Error downloading file {request.file_id}")
    
    file_model = FileModel.from_orm(file)

    return {
        "downloaded_file": file_model,
        "file_path": file_path
    }


@router.delete("/deleteFile", status_code=204)
def delete_file_from_drive(request: DeleteFileRequest, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = decode_app_token(token)
    
    file = delete_from_drive(db, user_data.get("email"), request)

    return { "deleted_file": file }


@router.post("/assignFileToUser", status_code=201)
def assign_to_user(request: FileToUserRequest, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = decode_app_token(token)

    file_ownership = assign_file_to_user(db, user_data.get("email"), request)

    return {
        "assigned": file_ownership
    }


@router.post("/assignFileToSubgroup", status_code=201)
def assign_to_subgroup(request: FileToSubgroupRequest, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = decode_app_token(token)

    file_ownerships = assign_file_to_subgroup(db, user_data.get("email"), request)

    response_data = [FileOwnershipModel.from_orm(ownership) for ownership in file_ownerships]

    return {
        "assigned": response_data
    }


@router.post("/assignFileToComposition", status_code=201)
def assign_to_user(request: FileToUserRequest, db: Session = Depends(get_session), token: str = Header(..., alias="Authorization")):
    user_data = decode_app_token(token)

    file = assign_file_to_composition(db, user_data.get("email"), request)

    return {
        "assigned": file
    }




# get user files

# get subgroup files

# get composition files

# deprive user of file

# deprive subgroup of file

# deprive composition of file