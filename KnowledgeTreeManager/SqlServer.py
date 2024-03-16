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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataModels import KnowledgeTree, Coordinator, Course
from SqlServerEngine import SqlServerEngine


class SqlServer:
    def __init__(self):
        self.sql_server_engine = SqlServerEngine()