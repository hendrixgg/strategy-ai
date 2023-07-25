import os
import json


def path_to_dict(rootPath: str, path: str):
    fullPath = os.path.join(rootPath, path)
    d = {'name': os.path.basename(fullPath), 'path': path, 'root': rootPath}
    if os.path.isdir(fullPath):
        d['type'] = "directory"
        d['children'] = [path_to_dict(rootPath, os.path.join(path, x))
                         for x in os.listdir(fullPath)]
    else:
        d['type'] = "file"
    return d


def path_to_json(rootPath: str, path: str):
    return json.dumps(path_to_dict(rootPath, path))
