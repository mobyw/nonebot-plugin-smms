from typing import List, Optional, Union

from pydantic import BaseModel


class EmptyData(BaseModel):
    pass


class FileInfo(BaseModel):
    """
    sm.ms File Info
    """

    width: int
    height: int
    filename: str
    storename: str
    size: int
    path: str
    hash: str
    url: str
    delete: str
    page: str
    file_id: Optional[int] = None
    created_at: Optional[str] = None


class ApiResponse(BaseModel):
    """
    sm.ms API Response
    """

    success: bool
    code: str
    message: Optional[str] = None
    data: Union[List[FileInfo], FileInfo, EmptyData, None] = None
