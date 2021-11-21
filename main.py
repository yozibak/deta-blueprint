from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

import schemas
from deta_setup import db

from urllib.parse import unquote

app = FastAPI()

origins = [
    'http://localhost:8080',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get("/")
def hello():
    return "Hey it's on live"


@app.get("/articles/{key}", response_model=schemas.Article)
def get_article(key: str):
    return db.get(key)


@app.get("/articles/", response_model=List[schemas.Article])
def fetch_articles():
    return db.fetch().items


@app.post("/articles/", response_model=schemas.Article)
def create_article( article: schemas.ArticleCreate):    
    payload = article.dict()
    payload['published'] = str(payload['published']) # date to str
    return db.put(payload)


@app.put("/articles/{key}", response_model=schemas.Article)
def update_article(key: str, article: schemas.ArticleUpdate):
    if not get_article(key):
        raise HTTPException(status_code=404, detail="Article not found")
    payload = article.dict()
    return db.put(payload, key=key)


@app.get("/articles/search/{query}", response_model=List[schemas.Article])
def search_articles(query:str):
    query = unquote(query)
    articles = db.fetch([
        {
            "title?contains": query
        },
        {
            "content?contains": query
        }
    ]).items
    articles.sort(key=lambda a: a["published"], reverse=True)
    return articles