import { FunctionComponent } from "react";

import "./ListItem.css"

const ListItem: FunctionComponent<{
    iconPath: string, // square icon
    itemText: string,
}> = ({ iconPath, itemText }) => {

    return (
        <div>
            <span>
                <img className="icon" alt="" src={iconPath} />{itemText}
            </span>
        </div>
    )
}

export default ListItem;