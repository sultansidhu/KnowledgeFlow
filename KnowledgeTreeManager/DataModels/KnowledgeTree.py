from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class KnowledgeTree:
    __tablename__ = 'knowledge_trees'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    coordinator_id = Column(Integer, ForeignKey('coordinators.id'), nullable=False)
    storage_link = Column(String(250), nullable=False)