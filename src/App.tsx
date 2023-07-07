import { FunctionComponent } from 'react'
import './App.css'
import TopBar from './TopBar/TopBar';
import FilesSection from './FileSystem/FilesSection'
import TasksSection from './TaskSystem/TasksSection'

const App: FunctionComponent = () => {

  return (
    <>
      <div className="top-bar">
        <TopBar />
      </div>
      <div className="content pack-horizontally">
        <div className="left-inner">
          <FilesSection />
        </div>
        <div className="right-inner">
          <TasksSection />
        </div>
      </div>
    </>
  )
}

export default App;
