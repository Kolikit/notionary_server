from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class NoteDto(BaseModel):
    id: Optional[str]
    title: str
    content: str
    updated_at: datetime

    class Config:
        orm_mode = True
