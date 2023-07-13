import React, { FunctionComponent } from "react";

const TasksSection: FunctionComponent<{
    children: React.ReactNode,
}> = ({ children }) => {
    return (
        <div style={{ padding: "0.5rem 2.5rem 0rem", maxHeight: "100%" }}>
            {children}
        </div >
    )
}

export default TasksSection;