// import { useState } from 'react'
// import axios from "axios"
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'
import Directory from './FileSystem/Directory'
import files from "./FileSystem/files.json"

// interface ProfileData {
//   profile_name: string,
//   about_me: string,
// }

function App(): React.JSX.Element {

  return (
    <>
      <div className="top-bar">top bar</div>
      <div className="container align-horizontally">
        <div className="files left-inner"><Directory files={files} /></div>
        <div className="interaction right-inner">other stuff</div>
      </div>
    </>
  )
}

export default App
