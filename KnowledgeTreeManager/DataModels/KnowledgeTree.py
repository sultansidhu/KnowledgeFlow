from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class KnowledgeTree(Base):
    __tablename__ = 'knowledge_trees'
    id = Column(Integer, primary_key=True, autoincrement=True)
    coordinator_id = Column(Integer, ForeignKey('coordinators.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    s3_link = Column(String(100))

    # Define relationships with Coordinator and Course classes
    coordinator = relationship("Coordinator")
    course = relationship("Course")

    # Add a unique constraint to ensure (coordinator_id, course_id) pairs are unique
    __table_args__ = (
        UniqueConstraint('coordinator_id', 'course_id'),
    )