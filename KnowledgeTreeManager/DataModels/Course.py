from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Course:
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    course_code = Column(String(10), nullable=False)
    course_name = Column(String(100), nullable=False)
    offering_year = Column(Integer, nullable=False)
