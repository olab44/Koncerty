from pydantic import BaseModel
from typing import List, Optional

class UploadFileRequest(BaseModel):
    file_id: str


class DownloadFileRequest(BaseModel):
    file_path: str