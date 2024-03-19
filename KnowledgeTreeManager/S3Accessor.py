"""
This file contains the S3Accessor class, which is used to access the S3 bucket through
the S3ServiceOperatorServer. The S3Accessor class is used to upload and retrieve files from the S3 bucket.
This file makes http requests to the S3ServiceOperatorServer to upload and retrieve files from the S3 bucket.
"""
import os
import requests

class S3Accessor:
    def __init__(self):
        self.service_url = os.environ.get("S3_SERVICE_URL", "http://localhost:8000")

    def get_knowledge_tree_with_s3_link(self, s3_url):
        pass

    def get_s3_link_for_knowledge_tree(self, course_id, coordinator_id, offering_year):
        pass


