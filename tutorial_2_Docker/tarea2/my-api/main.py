from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
    
@app.post("/get_news/", response_model=schemas.News)
def create_news(news: schemas.NewsCreate, db: Session = Depends(get_db)):
    db_news = crud.get_news_by_title(db, title=news.title)
    if db_news:
        raise HTTPException(status_code=400, detail="Title is already in used")
    return crud.create_news(db=db, news=news)


@app.get("/news/", response_model=List[schemas.News])
def read_news(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    news = crud.get_news(db, skip=skip, limit=limit)
    return news


@app.get("/news/{news_id}", response_model=schemas.News)
def read_news(news_id: int, db: Session = Depends(get_db)):
    db_news = crud.get_news(db, news_id=news_id)
    if db_news is None:
        raise HTTPException(status_code=404, detail="News not found")
    return db_news

@app.post("/news/{news_id}/category/", response_model=schemas.Category)
def assign_category_to_news(
    news_id: int, category: schemas.CategoryAssign, db: Session = Depends(get_db)):
        return crud.create_user_item(db=db, news_id=news_id, category=category)


@app.get("/category/", response_model=List[schemas.Category])
def read_category(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    category = crud.get_category(db, skip=skip, limit=limit)
    return category

#Listo