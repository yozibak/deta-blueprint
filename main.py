from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

from settings import Settings

import schemas
from database import db

from urllib.parse import unquote


app = FastAPI()

origins = [
    'http://localhost:8080',
    'https://www.uslss.site',
    'https://n1whrl.deta.dev'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

def get_uc():
    return Settings()

@app.get("/")
def hello():
    return "Hey it's on live"

@app.get("/articles/latest/{after}/{last}", response_model=List[schemas.Article])
def fetch_articles(after:str, last:str):
    '''
    return latest 7 articles. If users want more, then dig and return older ones.
    Request must be provided with `after` (date string) parameter so that it won' be exhaustible.
    '''
    before = str(int(after[0:4])+1) + after[4:]
    # articles = db.fetch(query={"published?r": [after, before]}).items
    # articles = db.fetch(
    #     [ {"published?gte": after}, {"published?lt": before} ]
    #     ).items
    articles = db.fetch(query={"published?gte": after}).items
    articles.sort(key=lambda a: a["published"], reverse=True)

    print(after)
    print(articles)
    
    if last == 'initial':
        return articles[0:2] # the initial call.
    else:
        for i, dic in enumerate(articles):
            if dic["key"] == last:
                res_list = articles[i+1:i+3] # return 
                break
        return res_list

@app.get("/articles/{key}", response_model=schemas.Article)
def get_article(key: str):
    return db.get(key)

@app.get("/articles/", response_model=List[schemas.Article])
def fetch_articles():
    ''' list all the articles (title, key, published ) '''
    return db.fetch().items

@app.post("/articles/", response_model=schemas.Article)
def create_article( article: schemas.ArticleCreate, settings: Settings = Depends(get_uc)):
    uc = article.uc
    if uc != settings.uc:
        raise HTTPException(status_code=400, detail="Not allowed")
    pl = article.dict()
    del pl["uc"]
    pl['published'] = str(pl['published']) # date to str
    return db.put(pl)

@app.put("/articles/{key}", response_model=schemas.Article)
def update_article(key: str, article: schemas.ArticleUpdate, settings: Settings = Depends(get_uc)):
    uc = article.uc
    if not get_article(key):
        raise HTTPException(status_code=404, detail="Article not found")
    if uc != settings.uc:
        raise HTTPException(status_code=400, detail="Not allowed")
    pl = article.dict()
    del pl["uc"]
    pl['published'] = str(pl['published']) # date to str
    return db.put(pl, key=key)

@app.post("/articles/batch")
def batch_post_article( articles: List[schemas.ArticleCreate]):
    ''' just for migration. Disable this after that. '''
    articles = jsonable_encoder(articles)
    return db.put_many(articles)

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