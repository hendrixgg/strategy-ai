import React, { useState } from "react";

interface FileDirectory {
    path: string,
    name: string,
    type: string,
    children: FileDirectory[] | null
}

function Directory({ files }: {
    files: FileDirectory,
}): React.JSX.Element {
    const [isExpanded, toggleExpanded] = useState<boolean>(false);

    if (files.type === "file") {
        return (
            <>
                <h3 className="file-name">{files.name}</h3>
            </>
        )
    }
    return (
        <div className="folder">
            <h2 className="folder-title" onClick={() => toggleExpanded(!isExpanded)}>{files.name}</h2><br />
            {
                isExpanded && files.children && files.children.map((item) => <Directory files={item} />)
            }
        </div>
    )
}

export default Directory;