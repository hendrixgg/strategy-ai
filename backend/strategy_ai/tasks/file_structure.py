import os
from pydantic import BaseModel, Field, validator
from typing import Optional, List

# q: how can I search for all uses of a class in vscode?
# a: ctrl+shift+f, then type in the class name


class FileStruct(BaseModel):
    name: str = Field(..., description="The name of the file or directory")
    is_dir: bool = Field(..., description="Is this a directory or file?")
    path: str
    root_path: Optional[str] = None
    children: Optional[List['FileStruct']] = None

    class Config:
        title = "File Structure Model"

    @validator("children", pre=True)
    def check_is_dir(cls, v, values):
        if values["is_dir"] and v is None:
            raise ValueError("Directories must have a list of children")
        if not values["is_dir"] and v is not None:
            raise ValueError("Files cannot have a list of children")
        return v


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
