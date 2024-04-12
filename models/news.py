from datetime import date
from beanie import Document, PydanticObjectId
from typing import Optional


class news_model(Document):
    title: str
    content: str
    created_at: Optional[date]
    photo_path: Optional[PydanticObjectId]
    view_count: Optional[int]
