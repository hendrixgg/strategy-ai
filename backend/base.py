from flask import Flask
from flask_cors import CORS

from strategy_ai.tasks.path_to_json import path_to_dict

api = Flask(__name__)
CORS(api, origins="*")


@api.route('/profile')
def my_profile():
    response_body = {
        "name": "Hendrix",
        "about": "I'm making an application that takes company documents and identifies their strategy with AI."
    }

    return response_body


@api.route("/files/<dir>")
def files(dir):
    return path_to_dict(f".\\strategy_ai\\available_data\\{dir}")
