import { FunctionComponent, useEffect, useState } from 'react'
import './App.css'
import TopBar from './Components/TopBar/TopBar';
import FilesSection from './Components/FileSystem/FilesSection'
import useAxiosFetch from './hooks/useAxiosFetch';
import TasksSection from './Components/TaskSystem/TasksSection'
import FileDirectory from './Components/FileSystem/FileDirectory';

const App: FunctionComponent = () => {
  const [task, setTask] = useState<string | null>(null);
  const [files, setFiles] = useState<Array<FileDirectory>>([]);

  const [fileData, error, loading, fetchFileData] = useAxiosFetch({
    method: "GET",
    url: "/files",
  });

  useEffect(() => {
    if (fileData) {
      setFiles(fileData.children);
      console.log(fileData);
    } else {
      setFiles([]);
    }
  }, [fileData]);

  useEffect(() => {
    if (error) {
      console.log(error);
      setFiles([]);
    }
  }, [error]);

  useEffect(() => {
    if (loading) {
      console.log("retrieving files...");
      setFiles([]);
    }
  }, [loading]);

  return (
    <>
      <div className="top-bar">
        <TopBar />
      </div>
      <div className="content pack-horizontally">
        <div className="left-inner">
          <FilesSection
            files={files}
            loading={loading}
            onRefresh={fetchFileData}
          />
        </div>
        <div className="right-inner">
          <TasksSection
            onTaskSelect={setTask}
            onProgressUpdate={fetchFileData}
            task={task}
          />
        </div>
      </div>
    </>
  )
}

export default App;
