import { FunctionComponent } from "react";
import FileSearchBar from "./FileSearchBar";
import Directory from "./Directory";
import FileDirectory from "./FileDirectory";
import "./FilesSection.css"

const FilesSection: FunctionComponent<{
    files: FileDirectory[],
    loading: boolean,
    onRefresh: Function,
}> = ({ files, loading, onRefresh }) => {
    let alternativeMessage = "";
    if (loading) {
        alternativeMessage = "loading...";
    } else if (files.length === 0) {
        alternativeMessage = "no files here...";
    }

    return (
        <div className="files-section">
            <div className="files-top-bar">
                <FileSearchBar />
                <button className="refresh-button" onClick={() => onRefresh()}>
                    <img className="refresh-icon" src="refresh-svgrepo-com.svg" /></button>
            </div>
            <div className="files elipses">
                {files.map((child) => {
                    return <Directory key={child.path} files={child} />
                })}
                {alternativeMessage}
            </div>
        </div>
    )
}

export default FilesSection;