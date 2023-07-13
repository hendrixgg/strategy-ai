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
def run_task(id):
    # run the task and have it put the output files in the ai_files directory
    # return the results in a json
    results_text = ""
    with open(".\\strategy_ai\\available_data\\hidden_files\\ai_output\\Company-objectives-using-csv-3.md", "r") as f:
        results_text = f.read()
    return {
        "text": results_text,
        "file_name": "Company-objectives-using-csv-3.md",
    }


@api.route("/saveoutput/<filename>")
def save_output(filename):
    # make a copy of ".\\strategy_ai\\available_data\\hidden_files\\ai_output\\filename" in the directory: ".\\strategy_ai\\available_data\\ai_files"
    import shutil
    shutil.copyfile(
        f".\\strategy_ai\\available_data\\hidden_files\\ai_output\\{filename}",
        f".\\strategy_ai\\available_data\\visible_files\\ai_files\\{filename}"
    )
    return {"success": True}
