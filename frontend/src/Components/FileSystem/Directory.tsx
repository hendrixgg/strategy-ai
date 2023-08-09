import { FunctionComponent, useState } from "react";
import FileDirectory from "./FileDirectory";
import ListItem from "../ListItem/ListItem";

const fileIconPath = "/file-icon.svg";
const directoryIconPath = "/folder-icon.svg"

const Directory: FunctionComponent<{
    fileStructure: FileDirectory,
}> = ({ fileStructure }) => {
    const [isExpanded, toggleExpanded] = useState<boolean>(false);
    if (!fileStructure) {
        return (
            // <ListItem iconPath="" iconPosition="left" itemText="no files to load..." />
            <div>no files here...</div>
        )
    }
    if (!fileStructure.is_dir) {
        return (
            <ListItem>
                <img className="icon" alt="" src={fileIconPath} />{fileStructure.name}
            </ListItem>
        )
    }
    return (
        <div className="folder">
            <span role="button" onClick={() => toggleExpanded(!isExpanded)}>
                <ListItem>
                    <img className="icon" alt="" src={directoryIconPath} />{fileStructure.name}
                </ListItem>
            </span>
            <div className="children" style={{ paddingLeft: "0.5rem" }}>
                {
                    isExpanded
                    && fileStructure.children.map((child) => <Directory key={child.path} fileStructure={child} />)
                }
            </div>
        </div >
    )
}

export default Directory;