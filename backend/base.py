from flask import Flask
from flask_cors import CORS

api = Flask(__name__)
CORS(api, origins="*")


@api.route('/profile')
def my_profile():
    response_body = {
        "name": "Hendrix",
        "about": "I'm making an application that takes company documents and identifies their strategy with AI."
    }

    return response_body


@api.route("/files")
def files_json():
    return
