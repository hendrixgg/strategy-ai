import React from "react";
import FileSearchBar from "./FileSearchBar"
import Directory from "./Directory";
import files from "./files.json"

function FilesBox(): React.JSX.Element {

    return (
        <>
            <div className="files">
                <FileSearchBar />
                <Directory files={files} indent={0} />
            </div>
        </>
    )
}

export default FilesBox;