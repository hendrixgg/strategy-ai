import { FunctionComponent, useState, useEffect } from "react";
import axios from "axios";
import FileSearchBar from "./FileSearchBar";
import Directory from "./Directory";
import FileDirectory from "./FileDirectory";
import "./FilesSection.css"

const FilesSection: FunctionComponent = () => {
    const [clientFiles, setClientFiles] = useState<FileDirectory | null>(null)
    const [aiFiles, setAiFiles] = useState<FileDirectory | null>(null)

    // might add a button in this component to refresh the files
    function fetchFiles() {
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
    }

    useEffect(fetchFiles, [])

    return (
        <div className="files-section">
            <FileSearchBar />
            <div className="files elipses">
                <Directory files={clientFiles} />
                <Directory files={aiFiles} />
            </div>
        </div>
    )
}

export default FilesSection;

// import { FunctionComponent } from 'react';
// import './FilesSection.css';
// const FilesSection: FunctionComponent = () => {
//     return (
//         <div className="column-20">
//             <div className="row-top">
//                 <div className="row-search">
//                     <div className="placeholder-text">Search file name</div>
//                     <img className="magnifying-glass-icon" alt="" src="magnifying-glass.svg" />
//                 </div>
//                 <div className="toggle-sidebar">
//                     <div className="rectangle-parent">
//                         <div className="group-child">
//                         </div>
//                         <div className="group-item">
//                         </div>
//                         <div className="group-inner">
//                         </div>
//                     </div>
//                 </div>
//             </div>
//             <div className="row-files">
//                 <div className="column">
//                     <div className="nested-list">
//                         <div className="toggle-sidebar">
//                             <img className="bullet-toggletrue-icon" alt="" src="bullet-toggle/true.svg" />
//                             <div className="list-itemtrue">
//                                 <img className="magnifying-glass-icon" alt="" src="folder-icon.svg" />
//                                 <div className="folder-name">item name</div>
//                             </div>
//                         </div>
//                     </div>
//                     <div className="nested-list">
//                         <div className="toggle-sidebar">
//                             <img className="bullet-toggletrue-icon" alt="" src="bullet-toggle/true.svg" />
//                             <div className="list-itemtrue">
//                                 <img className="magnifying-glass-icon" alt="" src="../assets/folder-icon.svg" />
//                                 <div className="folder-name">item name</div>
//                             </div>
//                         </div>
//                     </div>
//                 </div>
//             </div>
//         </div>);
// };

// export default FilesSection;
