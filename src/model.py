from typing import Optional

from pydantic import BaseModel


class Data(BaseModel):
    activity: str
    title: str
    content: Optional[str] = None
    status_content: Optional[str] = None
    link: Optional[str] = None
