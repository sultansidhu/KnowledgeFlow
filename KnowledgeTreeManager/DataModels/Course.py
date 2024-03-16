from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(10), unique=True)
    offering = Column(Integer)
