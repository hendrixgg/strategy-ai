import React from 'react'
// import axios from "axios"
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'
import FilesBox from './FileSystem/FilesBox'

// interface ProfileData {
//   profile_name: string,
//   about_me: string,
// }

function App(): React.JSX.Element {

  return (
    <>
      <div className="app-view">
        <div className="top-bar">top bar</div>
        <div className="container align-horizontally">
          <div className="files left-inner"><FilesBox /></div>
          <div className="interaction right-inner">other stuff</div>
        </div>
      </div>
    </>
  )
}

export default App
