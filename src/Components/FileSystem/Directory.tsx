import { FunctionComponent, useState } from "react";
import FileDirectory from "./FileDirectory";
import ListItem from "../ListItem/ListItem";

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
            <ListItem>
                <img className="icon" alt="" src={fileIconPath} />{files.name}
            </ListItem>
        )
    }
    return (
        <div className="folder">
            <span onClick={() => toggleExpanded(!isExpanded)}>
                <ListItem>
                    <img className="icon" alt="" src={directoryIconPath} />{files.name}
                </ListItem>
            </span>
            <div className="children" style={{ paddingLeft: "0.5rem" }}>
                {
                    isExpanded
                    && ((files.children?.length && files.children.map((child) => <Directory key={child.path} files={child} />))
                        || <Directory key={"./" + files.path} files={null} />)
                }
            </div>
        </div >
    )
}

export default Directory;