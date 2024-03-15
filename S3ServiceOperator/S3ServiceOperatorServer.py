from flask import Flask, request, jsonify
from io import BytesIO
import json
from RealS3ServiceOperator import RealS3ServiceOperator
from FakeS3ServiceOperator import FakeS3ServiceOperator
import yaml


class S3ServiceOperatorServer:
    def __init__(self, name=__name__, port=8000):
        self.app = Flask(name)
        self.port = port
        with open("config.yml", "r") as file:
            self.config = yaml.safe_load(file)
        
        aws_key = self.config["aws"]["access_key_id"]
        secret_access_key = self.config["aws"]["secret_access_key"]
        region_name = self.config["aws"]["region_name"]

        self.bucket_name = self.config["s3"]["bucket_name"]

        self.client: RealS3ServiceOperator = RealS3ServiceOperator(aws_key, secret_access_key, region_name)
        self.fake_client: FakeS3ServiceOperator = FakeS3ServiceOperator(aws_key, secret_access_key, region_name)

        @self.app.route('/faketree/<course_code>/<course_year>/<coordinator_id>', methods=['GET', 'PUT', 'DELETE'])
        async def fake_tree_operation(course_code, course_year, coordinator_id):
            s3_url = f"/tree/{course_code}/{course_year}/{coordinator_id}"

            if request.method == "GET":
                return await self.fake_client.get_file(self.bucket_name, s3_url)
                
            elif request.method == "DELETE":
                return await self.fake_client.delete_file(self.bucket_name, s3_url)
                
            elif request.method == "PUT":
                req_data = request.json
                json_data = jsonify(req_data)
                print(f"Json data from request: {json_data}")
                return await self.fake_client.upload_file(self.bucket_name, s3_url, BytesIO(json_data))
            
            else:
                return f"Invaild Request Type {request.method}", 400

        @self.app.route('/tree/<course_code>/<course_year>/<coordinator_id>', methods=['GET', 'PUT', 'DELETE'])
        async def tree_operation(course_code, course_year, coordinator_id):
            s3_url = f"/tree/{course_code}/{course_year}/{coordinator_id}"

            if request.method == "GET":
                try:
                    json_data = self.get_json_data_from_s3(self.bucket_name, s3_url)
                    if json_data:
                        return jsonify(json_data)
                    else:
                        return 'Error getting JSON data from S3', 500
                except Exception as e:
                    return str(e), 404
                
            elif request.method == "DELETE":
                try:
                    result = await self.client.delete_file(self.bucket_name, s3_url)
                    return result
                except Exception as e:
                    return str(e), 404
                
            elif request.method == "PUT":
                try:
                    req_data = request.json
                    json_data = jsonify(req_data)
                    result = await self.client.upload_file(self.bucket_name, s3_url, BytesIO(json_data))
                    return result
                except Exception as e:
                    return str(e), 404
                
            else:
                return f"Invaild Request Type {request.method}", 400

        @self.app.route('/tree/<course_code>/<course_year>/<coordinator_id>/copy', methods=['POST'])
        async def copy_tree(course_code, course_year, coordinator_id):
            new_course_year = request.json.get('new_course_year')
            new_coordinator_id = request.json.get('new_coordinator_id')

            if not new_course_year or not new_coordinator_id:
                return 'New course year and new coordinator id are required to copy', 400

            s3_url = f"/tree/{course_code}/{course_year}/{coordinator_id}"
            new_s3_url = f"/tree/{course_code}/{new_course_year}/{new_coordinator_id}"

            try:
                json_data = await self.client.get_file(self.bucket_name, s3_url)
                if json_data:
                    result = await self.client.upload_file(self.bucket_name, new_s3_url, json_data)
                    return result
                else:
                    return 'Error getting JSON data from S3', 500
            except Exception as e:
                return str(e), 404
        
    async def get_json_data_from_s3(self, bucket_name, object_key):
        try:
            # Get JSON data from S3
            response = await self.client.get_object(bucket_name=bucket_name, key=object_key)
            json_data = response['Body'].read().decode('utf-8')
            return json.loads(json_data)
        except Exception as e:
            print(f"Error getting JSON data from S3: {e}")
            return None

    def run(self):
        # Run the Flask application on the specified port
        self.app.run(debug=True, port=self.port)


if __name__ == '__main__':
    # Create an instance of MyFlaskApp and run it
    my_app = S3ServiceOperatorServer(port=8000)
    my_app.run()
