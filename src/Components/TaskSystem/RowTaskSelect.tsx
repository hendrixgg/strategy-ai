import { FunctionComponent } from 'react';
import styles from './RowTaskSelect.module.css';
import DropDownList from './DropDownList';
import DescriptionBox from './DescriptionBox'
import { Task } from './Tasks.ts'


const RowTaskSelect: FunctionComponent<{
    setTask: Function,
    taskList: Array<Task>,
    selectedTask: Task,
    locked: boolean,
}> = ({ setTask, taskList, selectedTask, locked }) => {


    return (
        <>
            <div className={styles.rowTitle}>
                <h4>Task Selection</h4>
            </div>
            <div className={styles.rowTaskSelect}>
                <DropDownList
                    setTask={setTask}
                    selectedOption={selectedTask}
                    options={taskList}
                    disabled={locked}
                />
                <DescriptionBox>
                    {selectedTask.description}
                </DescriptionBox>
            </div>
        </>
    );
};

export default RowTaskSelect;

