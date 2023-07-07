import React, { useState, useEffect } from "react";
import axios from "axios";
import FileSearchBar from "./FileSearchBar";
import Directory from "./Directory";
import FileDirectory from "./FileDirectory";
import "./FilesSection.css"

function FilesSection(): React.JSX.Element {
    const [clientFiles, setClientFiles] = useState<FileDirectory | null>(null)
    const [aiFiles, setAiFiles] = useState<FileDirectory | null>(null)

    useEffect(() => {
        axios({
            method: "GET",
            url: "/api/files/client_documents",
        }).then((response) => {
            setClientFiles(response.data)
        }).catch((error) => {
            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
            }
        })
        axios({
            method: "GET",
            url: "/api/files/ai_documents",
        }).then((response) => {
            setAiFiles(response.data)
        }).catch((error) => {
            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
            }
        })
    }, [])

    return (
        <div>
            <FileSearchBar />
            <div className="elipses">
                <Directory files={clientFiles} indent={0} />
                <Directory files={aiFiles} indent={0} />
            </div>
        </div>
    )
}

export default FilesSection;