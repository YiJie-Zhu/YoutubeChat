# System imports
import os

# Library imports
from flask import Flask
from flask_restful import Api, Resource
from dotenv import load_dotenv

# Custom imports
from api.routes.video_comments import VideoComments

# Load environment variables
load_dotenv()

# Initialize flask and api
app = Flask(__name__)
api = Api(app)

# Base route
api.add_resource(VideoComments, "/video/<string:video_id>")

if __name__ == "__main__":
    env = os.getenv("env")
    if env == "dev":
        app.run(debug=True)
    elif env=="prod":
        app.run(host='0.0.0.0', port=8080)

