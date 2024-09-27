from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.db_model import User, Translation, FileTranslation, Base
from datetime import datetime
from typing import List
from src.models import Bn2EnTranslator


app = FastAPI()

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///db/translation_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
bn2en = Bn2EnTranslator()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"status": "ok"}


# Pydantic model for request body
class UserAuth(BaseModel):
    username: str
    password: str


@app.post("/validate-user")
def validate_user(user_auth: UserAuth, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user_auth.username).first()
    if db_user and db_user.password == user_auth.password:
        return {"status": "success"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")


class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime   


@app.get("/users", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@app.get("/users/{username}/translations/")
def get_translations(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    translations = db.query(Translation).filter(Translation.user_id == user.id).all()
    return translations


@app.get("/users/{username}/translations-batch/")
def get_translations_batch(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    translations = db.query(FileTranslation).filter(FileTranslation.user_id == user.id).all()
    return translations


# Pydantic models for request and response bodies
class TranslationCreate(BaseModel):
    english_text: str
    bengali_text: str
    session_id: str


@app.post("/users/{username}/translations/")
def create_translation(username: str, translation: TranslationCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_translation = Translation(
        user_id=user.id,
        english_text=translation.english_text,
        bengali_text=translation.bengali_text,
        session_id=translation.session_id,
        translated_at=datetime.now()
    )
    db.add(new_translation)
    db.commit()
    db.refresh(new_translation)
    return new_translation


@app.post("/users/{username}/translations-batch/")
def create_translation_batch(username: str, translation: TranslationCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_translation = FileTranslation(
        user_id=user.id,
        input_file=translation.bengali_text,
        output_file=translation.english_text,
        translated_at=datetime.now()
    )
    db.add(new_translation)
    db.commit()
    db.refresh(new_translation)
    print(new_translation)
    return new_translation


class TranslationResponse(BaseModel):
    text_bn: str
    text_en: str


@app.get('/translate/')
async def translate(text: str):
    """
    Translates a sentence from Bangla to English
    :param text: Bengali text
    :return: English text
    """
    text_en = bn2en.translate(text)
    # text_en = bn2en(text)
    translation = TranslationResponse(text_bn=text, text_en=text_en)
    return translation


@app.get('/translate-batch/')
async def translate_batch(text: str):
    """
    Translates a sentence from Bangla to English in batch mode
    :param text: Bengali text
    :return: English text
    """
    text_en = bn2en.split_n_translate(text)
    translation = TranslationResponse(text_bn=text, text_en=text_en)
    return translation


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


