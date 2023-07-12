import React, { FunctionComponent } from "react";

import "./ListItem.css"

const ListItem: FunctionComponent<{
    children: React.ReactNode,
}> = ({ children }) => {

    return (
        <div>
            <span>
                {children}
            </span>
        </div>
    )
}

export default ListItem;