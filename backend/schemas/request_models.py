from pydantic import BaseModel, Field
from typing import Optional


class URLRequest(BaseModel):
    url: str


class EmailRequest(BaseModel):
    subject: Optional[str] = Field(default="", max_length=1000)
    body: str = Field(..., min_length=1, max_length=100000)