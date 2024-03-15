from flask import Flask, request, jsonify
import json
import RealS3ServiceOperator

class S3ServiceOperatorServer:
    def __init__(self, name=__name__, port=8000):
        self.app = Flask(name)
        self.port = port
        self.client = RealS3ServiceOperator("", "", "") # toy values, get from environment

        @self.app.route('/tree/<course_code>/<course_year>/<coordinator_id>', methods=['GET', 'PUT', 'DELETE'])
        async def tree_operation(course_code, course_year, coordinator_id):
            s3_url = f"/tree/{course_code}/{course_year}/{coordinator_id}"

            if request.method == "GET":
                try:
                    json_data = self.get_json_data_from_s3("S3_BUCKET_NAME", s3_url)
                    if json_data:
                        return jsonify(json_data)
                    else:
                        return 'Error getting JSON data from S3', 500
                except Exception as e:
                    return str(e), 404
                
            elif request.method == "DELETE":
                try:
                    result = await self.client.delete_file("S3_BUCKET_NAME", s3_url)
                    return result
                except Exception as e:
                    return str(e), 404
                
            elif request.method == "PUT":
                try:
                    # WE NEED DATA FROM THE REQUEST, AND NEED TO CONVERT INTO BYTESIO
                    result = await self.client.upload_file("S3_BUCKET_NAME", s3_url)
                    return result
                except Exception as e:
                    return str(e), 404
        
    def get_json_data_from_s3(self, bucket_name, object_key):
        try:
            # Get JSON data from S3
            response = self.client.get_object(bucket_name=bucket_name, key=object_key)
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
