import { FunctionComponent, useEffect, useState } from 'react';
import './App.css';

import useAxiosFetch from './hooks/useAxiosFetch';

import FilesSection from './Components/FileSystem/FilesSection';
import FileDirectory from './Components/FileSystem/FileDirectory';

import { Tasks, Task } from './Components/TaskSystem/Tasks'; // should be retrieved from the backend, this should be associated with each task in python
import TasksSection from './Components/TaskSystem/TasksSection';
import ColumnHeader from "./Components/TaskSystem/ColumnHeader.tsx";
import RowTaskSelect from './Components/TaskSystem/RowTaskSelect.tsx';
import { TaskProcessState } from './Components/TaskSystem/TaskProcessState';

const App: FunctionComponent = () => {
  const [task, setTask] = useState<Task>(Tasks[0]);
  const [taskState, setTaskState] = useState<TaskProcessState>(TaskProcessState.selecting);
  useEffect(() => {
    if (task.id !== 0) {
      setTaskState(TaskProcessState.ready);
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
            <RowTaskSelect
              setTask={setTask}
              taskList={Tasks}
              selectedTask={task}
              locked={taskState === TaskProcessState.executing || taskState === TaskProcessState.complete}
            />
            <div></div>
          </TasksSection>
        </div>
      </div>
    </>
  )
}

export default App;
