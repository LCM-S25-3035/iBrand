from pydantic import BaseModel, Field, HttpUrl, ConfigDict, field_validator
from typing import List, Optional
from datetime import datetime

class PostBase(BaseModel):
    platform: str
    content: str
    hashtags: List[str]
    image: HttpUrl
    created_at: Optional[datetime] = None

class PostCreate(PostBase):
    """
    Used when creating a post (e.g. after generation)
    """
    pass

class PostOut(BaseModel):
    model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True)

    id: str = Field(alias="_id")
    platform: str
    content: str
    hashtags: List[str]
    image: HttpUrl
    created_at: Optional[datetime] = None

    @classmethod
    def validate(cls, value):
        # Ensure _id is str
        if isinstance(value, dict) and isinstance(value.get("_id"), object):
            value["_id"] = str(value["_id"])
        return value
    
    @field_validator("created_at", mode="before")
    @classmethod
    def validate_datetime(cls, v):
        if v in (None, "", "Unknown"):
            return None
        return v
