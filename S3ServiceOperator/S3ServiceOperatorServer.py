from flask import Flask

class S3ServiceOperatorServer:
    def __init__(self, name=__name__, port=8000):
        self.app = Flask(name)
        self.port = port

        # Define routes
        @self.app.route('/')
        def hello_world():
            return 'Hello, World! This is my Flask server.'

    def run(self):
        # Run the Flask application on the specified port
        self.app.run(debug=True, port=self.port)

if __name__ == '__main__':
    # Create an instance of MyFlaskApp and run it
    my_app = S3ServiceOperatorServer(port=8000)
    my_app.run()
