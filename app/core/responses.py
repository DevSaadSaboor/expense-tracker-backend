from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

T = TypeVar("T")

class Meta(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class APIError(BaseModel):
    code: str
    message: str
    details: Optional[dict] = None

class APIResponse(Generic[T], BaseModel):
    success: bool
    data: Optional[T] = None
    error: Optional[APIError] = None
    meta: Meta = Field(default_factory=Meta)
