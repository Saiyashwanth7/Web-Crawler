from database import Base
from sqlalchemy.orm import Session
from sqlalchemy import Integer,String,TIMESTAMP,Column,Text
from pydantic import Field
from datetime import timedelta,timezone,datetime

class ContentStorage(Base):
    __tablename__='contentstorage'
    id = Column(Integer,primary_key=True)
    url = Column(String,unique=True)
    html_content=Column(Text)
    status_code=Column(Integer)
    method_name=Column(String,default='aiohttp')
    crawled_at=Column(TIMESTAMP,default=datetime.now)
    