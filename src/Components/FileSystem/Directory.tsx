import { FunctionComponent, useState } from "react";
import FileDirectory from "./FileDirectory";
import ListItem from "./ListItem";

const fileIconPath = "/file-icon.svg";
const directoryIconPath = "/folder-icon.svg"

const Directory: FunctionComponent<{
    files: FileDirectory | null,
}> = ({ files }) => {
    const [isExpanded, toggleExpanded] = useState<boolean>(false);
    if (!files) {
        return (
            // <ListItem iconPath="" iconPosition="left" itemText="no files to load..." />
            <div>no files here...</div>
        )
    }
    if (files.type === "file") {
        return (
            <ListItem iconPath={fileIconPath} itemText={files.name} />
        )
    }
    return (
        <div className="folder">
            <span onClick={() => toggleExpanded(!isExpanded)}><ListItem iconPath={directoryIconPath} itemText={files.name} /></span>
            <div className="children">
                {
                    isExpanded
                    && files.children
                    && files.children.map((child) => <Directory key={child.path} files={child} />)
                }
            </div>
        </div>
    )
}

export default Directory;