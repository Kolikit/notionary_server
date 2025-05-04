from fastapi import FastAPI
from database import Base, engine
from auth import auth_router
from notes import notes_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(notes_router, prefix="/notes", tags=["notes"])
