import { FunctionComponent, useEffect, useState } from 'react';
import './App.css';

import FilesSection from './Components/FileSystem/FilesSection';

import { TaskProcessState } from './Components/TaskSystem/TaskProcessState';
import { Tasks, Task } from './Components/TaskSystem/Tasks'; // should be retrieved from the backend, this should be associated with each task in python
import TasksSection from './Components/TaskSystem/TasksSection';
import ColumnHeader from "./Components/TaskSystem/ColumnHeader.tsx";
import RowTaskSelect from './Components/TaskSystem/RowTaskSelect.tsx';
import Button from './Components/buttons/Button.tsx';

const App: FunctionComponent = () => {
  const [task, setTask] = useState<Task>(Tasks[0]);
  const [taskState, setTaskState] = useState<TaskProcessState>(TaskProcessState.selecting);
  useEffect(() => {
    if (task.id === 0) {
      setTaskState(TaskProcessState.selecting);
    } else {
      setTaskState(TaskProcessState.ready)
    }
  }, [task]);

  return (
    <>
      <div className="top-bar pack-horizontally">
        <h1>Strategy AI</h1>
      </div>
      <div className="content pack-horizontally">
        <div className="left-inner">
          <FilesSection />
        </div>
        <div className="right-inner">
          <TasksSection>
            <ColumnHeader titleText="Execute Tasks" />
            <div style={{ padding: "0.5rem 0.5rem 0rem", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
              <RowTaskSelect
                setTask={setTask}
                taskList={Tasks}
                selectedTask={task}
                locked={taskState === TaskProcessState.executing || taskState === TaskProcessState.complete}
              />
              <div className="row3">
                <Button disabled={taskState !== TaskProcessState.ready}>START</Button>
              </div>
            </div>
          </TasksSection>
        </div>
      </div>
    </>
  )
}

export default App;
