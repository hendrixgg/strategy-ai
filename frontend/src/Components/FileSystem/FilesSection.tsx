import { FunctionComponent, useState, useEffect } from "react";
import FileSearchBar from "./FileSearchBar";
import Directory from "./Directory";
import FileDirectory from "./FileDirectory";
import useAxiosFetch from "../../hooks/useAxiosFetch";
import "./FilesSection.css"

const FilesSection: FunctionComponent<{}> = ({ }) => {
    const [files, setFiles] = useState<Array<FileDirectory>>([]);
    const [fileData, error, loading, fetchFileData] = useAxiosFetch({
        method: "GET",
        url: "/files",
    });

    useEffect(() => {
        if (fileData) {
            setFiles(fileData.children);
            console.log(fileData);
        } else {
            setFiles([]);
        }
    }, [fileData]);

    useEffect(() => {
        if (error) {
            console.log(error);
            setFiles([]);
        }
    }, [error]);

    useEffect(() => {
        if (loading) {
            console.log("retrieving files...");
            setFiles([]);
        }
    }, [loading]);

    function alternativeMessage() {
        if (loading) {
            return "loading...";
        } else if (files.length === 0) {
            return "no files here...";
        }
    }

    return (
        <div className="files-section">
            <div className="files-top-bar">
                <FileSearchBar />
                <button className="refresh-button" onClick={() => fetchFileData()}>
                    <img className="refresh-icon" src="refresh-svgrepo-com.svg" />
                </button>
            </div>
            <div className="files elipses">
                {files.map((child) => {
                    return <Directory key={child.path} files={child} />
                })}
                {alternativeMessage()}
            </div>
        </div>
    )
}

export default FilesSection;