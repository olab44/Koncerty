from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List

from src.database import get_session
from users.service import decode_app_token
from .schemas import AnnouncementCreate, AnnouncementInfo
from .service import create_announcement, get_announcements


router = APIRouter()


from fastapi import HTTPException

@router.post("/createAnnouncement", status_code=201, response_model=AnnouncementInfo)
def post_announcement(
    request: AnnouncementCreate,
    db: Session = Depends(get_session),
    token: str = Header(..., alias="Authorization"),
):
    try:
        # Attempt to decode the token and check for its validity
        user_data = decode_app_token(token)
        
        # If the token is decoded successfully, check if the user has the required role
        if user_data.get("role") not in ["admin", "moderator"]:
            raise HTTPException(status_code=403, detail="Access denied: You need admin or moderator role")
        
        # Proceed to create the announcement
        return create_announcement(db, user_data["id"], request)

    except ValueError as ve:
        # In case of token decoding failure (invalid token structure)
        raise HTTPException(status_code=401, detail="Invalid token: The token format or data is incorrect")
    
    except KeyError as ke:
        # If there is an issue with decoding the token (missing fields)
        raise HTTPException(status_code=401, detail="Invalid token: Missing required fields in the token")
    
    except Exception as ex:
        # Catch any other unknown errors and specify them
        raise HTTPException(status_code=401, detail=f"Token validation failed: {str(ex)}")



@router.get("/announcements", response_model=List[AnnouncementInfo])
def fetch_announcements(
    group_id: int = None,
    subgroup_id: int = None,
    db: Session = Depends(get_session),
    token: str = Header(..., alias="Authorization"),
):
    try:
        user_data = decode_app_token(token)
        return get_announcements(db, group_id, subgroup_id)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
