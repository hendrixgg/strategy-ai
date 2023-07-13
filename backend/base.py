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


@api.route("/files")
def files():
    return path_to_dict(f".\\strategy_ai\\available_data\\visible_files")


@api.route("/runtask/<id>")
def task(id):
    # run the task and have it put the output files in the ai_files directory
    # return the results in a json
    return {"text": open(".\\strategy_ai\\available_data\\visible_files\\ai_files\\Company-objectives-using-csv-3.md", "r").read()}
