import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from KnowledgeTreeManager.DataModels.KnowledgeTree import KnowledgeTree
from KnowledgeTreeManager.DataModels.Coordinator import Coordinator
from KnowledgeTreeManager.DataModels.Course import Course

class SqlServerEngine:
    def __init__(self):
        load_dotenv()
        db_url = f'mysql://root:{os.getenv("MYSQL_ROOT_PASSWORD")}@mysql:3306/{os.getenv("MYSQL_DATABASE")}'
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def add_coordinator(self, coordinator):
        session = self.Session()
        session.add(coordinator)
        session.commit()
        session.close()

    def add_course(self, course):
        session = self.Session()
        session.add(course)
        session.commit()
        session.close()

    def add_knowledge_tree(self, knowledge_tree):
        session = self.Session()
        session.add(knowledge_tree)
        session.commit()
        session.close()

    def update_knowledge_tree(self, knowledge_tree):
        session = self.Session()
        session.query(KnowledgeTree).filter(KnowledgeTree.id == knowledge_tree.id).update({
            'course_id': knowledge_tree.course_id,
            'coordinator_id': knowledge_tree.coordinator_id,
            'storage_link': knowledge_tree.storage_link
        })
        session.commit()
        session.close()


