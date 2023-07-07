import { FunctionComponent } from 'react'
import './App.css'
import FilesSection from './FileSystem/FilesSection'
import TopBar from './TopBar/TopBar';

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
          other stuff
        </div>
      </div>
    </>
  )
}

export default App;
