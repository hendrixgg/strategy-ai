import os
import json
from pydantic import BaseModel, Field
from typing import Optional, List

# q: how can I search for all uses of a class in vscode?
# a: ctrl+shift+f, then type in the class name


class FileStruct(BaseModel):
    name: str
    is_dir: bool = False
    path: str
    root_path: Optional[str] = None
    children: Optional[List['FileStruct']] = None

    class Config:
        title = "File Structure Model"


def path_to_file_struct(rootPath: str, path: str = os.curdir, include_root_path: bool = False) -> FileStruct:
    fullPath = os.path.join(rootPath, path) if path != os.curdir else rootPath
    return FileStruct(
        name=os.path.basename(fullPath),
        is_dir=os.path.isdir(fullPath),
        path=path,
        root_path=rootPath if include_root_path else None,
        children=[path_to_file_struct(rootPath, os.path.join(
            path, x)) for x in os.listdir(fullPath)] if os.path.isdir(fullPath) else None,
    )


def path_to_dict(rootPath: str, path: str = os.curdir) -> dict:
    """returns a dict representation of the file structure at the given path"""
    return path_to_file_struct(rootPath=rootPath, path=path).dict()


def path_to_json(rootPath: str, path: str = os.curdir, indent: int = 4) -> str:
    return path_to_file_struct(rootPath=rootPath, path=path).json(indent=indent)
