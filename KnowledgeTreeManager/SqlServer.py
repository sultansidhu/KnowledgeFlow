"""
A server that would be accessible, and would allow us to interact with the clients directly.
The clients would send a request where the post requests will contain data about
1. posting a new/update an existing knowledge tree in the database
     - We will access the S3 service to upload the file to the bucket and get the link to the store.
     - We can retreive a given knowledge tree from the database and send it to the client, given other info
2. posting a new coordinator in the database
3. posting a new course in the database
"""
from flask import Flask, request, jsonify
from DataModels.KnowledgeTree import KnowledgeTree
from DataModels.Coordinator import Coordinator
from DataModels.Course import Course
from SqlServerEngine import SqlServerEngine


class SqlServer:
    def __init__(self, name=__name__, port=5000):
        self.sql_server_engine = SqlServerEngine()
        self.app = Flask(name)
        self.port = port

        # KNOWLEDGE TREE OPERATIONS
        @self.app.route('/knowledge_tree', methods=['POST'])
        def add_knowledge_tree():
            req_data = request.json
            knowledge_tree = KnowledgeTree(
                course_id=req_data["course_id"],
                coordinator_id=req_data["coordinator_id"],
                storage_link=req_data["storage_link"]
            )
            self.sql_server_engine.add_knowledge_tree(knowledge_tree)
            return "Knowledge Tree added successfully", 200

        @self.app.route('/knowledge_tree', methods=['PUT'])
        def update_knowledge_tree():
            req_data = request.json
            knowledge_tree = KnowledgeTree(
                id=req_data["id"],
                course_id=req_data["course_id"],
                coordinator_id=req_data["coordinator_id"],
                storage_link=req_data["storage_link"]
            )
            self.sql_server_engine.update_knowledge_tree(knowledge_tree)
            return "Knowledge Tree updated successfully", 200

        @self.app.route('/knowledge_tree', methods=['GET'])
        def get_knowledge_tree():
            coordinator_id = request.args.get('coordinator_id')
            course_id = request.args.get('course_id')
            knowledge_trees = self.sql_server_engine.get_knowledge_tree(coordinator_id, course_id)
            return jsonify(knowledge_trees), 200

        @self.app.route('/knowledge_tree/<knowledge_tree_id>', methods=['GET'])
        def get_knowledge_tree_by_id(knowledge_tree_id):
            knowledge_tree = self.sql_server_engine.get_knowledge_tree_by_id(knowledge_tree_id)
            return jsonify(knowledge_tree), 200

        @self.app.route('/knowledge_tree/<knowledge_tree_id>', methods=['DELETE'])
        def delete_knowledge_tree(knowledge_tree_id):
            self.sql_server_engine.delete_knowledge_tree(knowledge_tree_id)
            return "Knowledge Tree deleted successfully", 200

        # COORDINATOR OPERATIONS
        @self.app.route('/coordinator', methods=['POST'])
        def add_coordinator():
            req_data = request.json
            coordinator = Coordinator(
                name=req_data["name"],
                email=req_data["email"]
            )
            self.sql_server_engine.add_coordinator(coordinator)
            return "Coordinator added successfully", 200

        @self.app.route('/coordinator/<coordinator_id>', methods=['GET'])
        def get_coordinator(coordinator_id):
            coordinator = self.sql_server_engine.get_coordinator(coordinator_id)
            return jsonify(coordinator), 200

        @self.app.route('/coordinator/<coordinator_id>', methods=['DELETE'])
        def delete_coordinator(coordinator_id):
            self.sql_server_engine.delete_coordinator(coordinator_id)
            return "Coordinator deleted successfully", 200

        # COURSE OPERATIONS
        @self.app.route('/course', methods=['POST'])
        def add_course():
            req_data = request.json
            course = Course(
                name=req_data["name"],
                description=req_data["description"]
            )
            self.sql_server_engine.add_course(course)
            return "Course added successfully", 200

        @self.app.route('/course/<course_id>', methods=['GET'])
        def get_course(course_id):
            course = self.sql_server_engine.get_course(course_id)
            return jsonify(course), 200

        @self.app.route('/course/<course_id>', methods=['DELETE'])
        def delete_course(course_id):
            self.sql_server_engine.delete_course(course_id)
            return "Course deleted successfully", 200