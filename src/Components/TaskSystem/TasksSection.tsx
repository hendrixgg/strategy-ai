import { FunctionComponent } from "react";

const TasksSection: FunctionComponent<{
    onTaskSelect: Function,
    onProgressUpdate: Function,
    task: string | null,
}> = () => {
    return (
        <div>
            Tasks
        </div>
    )
}

export default TasksSection;