import { FunctionComponent, useEffect, useState } from 'react';
import './App.css';

import FilesSection from './Components/FileSystem/FilesSection';

import { TaskProcessState } from './Components/TaskSystem/TaskProcessState';
import { Tasks, Task } from './Components/TaskSystem/Tasks'; // should be retrieved from the backend, this should be associated with each task in python
import TasksSection from './Components/TaskSystem/TasksSection';
import ColumnHeader from "./Components/TaskSystem/ColumnHeader.tsx";
import RowTaskSelect from './Components/TaskSystem/RowTaskSelect.tsx';
import Button from './Components/buttons/Button.tsx';

import ResultsSection from './Components/TaskSystem/Results/ResultsSection.tsx'

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

  useEffect(() => {
    console.log(taskState)
  }, [taskState])

  return (
    <>
      <div className="top-bar pack-horizontally">
        <h1>Strategy AI</h1>
      </div>
      <div className="content">
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
                locked={taskState === TaskProcessState.executing}
              />
              <div className="row3">
                <Button
                  disabled={taskState !== TaskProcessState.ready}
                  onClick={() => setTaskState(TaskProcessState.executing)}>
                  START
                </Button>
              </div>
            </div>
            <ColumnHeader titleText="Results" />
            {taskState !== TaskProcessState.selecting && taskState !== TaskProcessState.ready &&
              <>
                <div style={{ padding: "0.5rem 0.5rem 0rem", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
                  <ResultsSection taskState={taskState} setTaskState={setTaskState} task={task} />
                </div>
              </>
            }
          </TasksSection>
        </div>
      </div>
    </>
  )
}

export default App;
