from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from .database import Base #Se importa el objeto Base desde el archivo database.py

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
class News(Base): 

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), unique=True, index=True)
    date = Column(Date)
    url = Column(Boolean, default=True, unique=True, index=True)
    media_outlet = Column(String(50))

    has_category = relationship("HasCategory", back_populates="owner")

class HasCategory(Base):

    __tablename__ = "has_category"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String(50))
    
    owner_id = Column(Integer, ForeignKey("news.id"))
    owner = relationship("News", back_populates="has_category")

#Listo 