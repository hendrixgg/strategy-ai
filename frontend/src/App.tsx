import React, { FunctionComponent, useEffect, useState, useRef, useCallback } from 'react';
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
  const dividerRef = useRef<HTMLInputElement>(null);
  const [isResizing, setIsResizing] = useState<boolean>(false);
  const [dividerPos, setdividerPos] = useState<number>(0.2 * window.innerWidth);
  const [resizeMousePosOffset, setResizeMousePosOffset] = useState<number>(0);

  const startResizing = useCallback((mouseDownEvent: any) => {
    setIsResizing(true);
    if (dividerRef.current) {
      setResizeMousePosOffset(mouseDownEvent.clientX);
    } else {
      setResizeMousePosOffset(0);
    }
  }, []);

  const stopResizing = useCallback(() => {
    setIsResizing(false);
  }, []);

  const resize = React.useCallback(
    (mouseMoveEvent: any) => {
      if (isResizing && dividerRef.current) {
        setdividerPos(
          dividerPos
          + mouseMoveEvent.clientX
          - resizeMousePosOffset
        );
      }
    },
    [isResizing]
  );

  useEffect(() => {
    window.addEventListener("mousemove", resize);
    window.addEventListener("mouseup", stopResizing);
    return () => {
      window.removeEventListener("mousemove", resize);
      window.removeEventListener("mouseup", stopResizing);
    };
  }, [resize, stopResizing]);

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
  }, [taskState]);

  return (
    <div className="app-container">
      <div className="top-bar pack-horizontally">
        <h1>Strategy AI</h1>
      </div>
      <div className="content">
        <div className="left-inner" style={{ width: dividerPos + 2 }} >
          <FilesSection />
        </div>
        <div ref={dividerRef} className="divider" style={{ top: 0, left: dividerPos }} onMouseDown={startResizing} />
        <div className="right-inner" style={{ left: dividerPos + 4 }} >
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
                  onClick={() => setTaskState(TaskProcessState.start)}>
                  START
                </Button>
              </div>
            </div>
            <ColumnHeader titleText="Results" />
            <div style={{ padding: "0.5rem 0.5rem 0rem", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
              <ResultsSection taskState={taskState} setTaskState={setTaskState} selectedTask={task} />
            </div>
          </TasksSection>
        </div>
      </div>
    </div >
  )
}

export default App;
