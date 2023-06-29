import React, { useState } from "react";
import FileDirectory from "./FileDirectory";

function Directory({ files, indent }: {
    files: FileDirectory | null,
    indent: number,
}): React.JSX.Element {
    const [isExpanded, toggleExpanded] = useState<boolean>(false);
    if (!files) {
        return (
            <>
                <h4>no files to load...</h4>
            </>
        )
    }
    if (files.type === "file") {
        return (
            <>
                <h3 className="file-name">{files.name}</h3>
            </>
        )
    }
    return (
        <div className="folder">
            <h2 className="folder-title" onClick={() => toggleExpanded(!isExpanded)}>{files.name}</h2>
            {
                isExpanded && files.children && files.children.map((item) => <Directory key={item.path} files={item} indent={indent + 1} />)
            }
        </div>
    )
}

export default Directory;