
from typing import Optional
from pydantic import BaseModel 
from datetime import date

# Article

class ArticleBase(BaseModel):
    title: str
    content: str
    published: str

class ArticleCreate(ArticleBase):
    published: date
    uc: str

class ArticleUpdate(ArticleBase):
    title: Optional[str]
    content: Optional[str]
    published: Optional[date]
    uc: str

class Article(ArticleBase):
    key: str # key for NoSQL Deta Base.

    class Config:
        orm_mode = True # enables reading attributes like item.id