from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models import User, Note
from schemas import NoteDto
from utils import decode_token
from fastapi import Query
from dateutil.parser import isoparse

notes_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(authorization: str = Header(..., alias="Authorization"), db: Session = Depends(get_db)) -> User:
    try:
        token = authorization.replace("Bearer ", "")
        payload = decode_token(token)
        username = payload.get("sub")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Пользователь не найден")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Недействительный токен")

@notes_router.get("/sync", response_model=List[NoteDto])
def get_notes(
    after: str = Query(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        try:
            after_dt = isoparse(after)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Неверный формат даты: {after}")

        notes = db.query(Note).filter(
            Note.user_id == user.id,
            Note.updated_at > after_dt.isoformat()
        ).all()

        return [
            NoteDto(id=n.id, title=n.title, content=n.content, updated_at=n.updated_at)
            for n in notes
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении заметок: {str(e)}")

@notes_router.post("/sync")
def sync_notes(notes: List[NoteDto], user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    for n in notes:
        if n.id:
            existing = db.query(Note).filter(Note.id == n.id, Note.user_id == user.id).first()
        else:
            existing = None

        if existing:
            existing.title = n.title
            existing.content = n.content
            existing.updated_at = n.updated_at
        else:
            new_note = Note(
                id=n.id if n.id else None,
                title=n.title,
                content=n.content,
                updated_at=n.updated_at,
                owner=user
            )
            db.add(new_note)

    db.commit()
    return {"status": "success"}
