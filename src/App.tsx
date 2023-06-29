import React from 'react'
import './App.css'
import FilesSection from './FileSystem/FilesSection'

function App(): React.JSX.Element {

  return (
    <>
      <div className="app-view pack-vertically">
        <div className="top-bar">
          <h2>Strategy AI</h2>
        </div>
        <div className="content pack-horizontally">
          <div className="files left-inner">
            <FilesSection />
          </div>
          <div className="interaction right-inner">other stuff</div>
        </div>
      </div>
    </>
  )
}

export default App
