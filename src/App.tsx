import { useState } from 'react'
import axios from "axios"
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

interface ProfileData {
  profile_name: string,
  about_me: string,
}

function App() {
  const [count, setCount] = useState<number>(0)
  const [profileData, setProfileData] = useState<ProfileData | null>(null)

  function getData(): void {
    axios({
      method: "GET",
      url: "/api/profile",
    })
      .then((response: any) => {
        const res = response.data
        setProfileData(({
          profile_name: res.name,
          about_me: res.about,
        }))
      }).catch((error) => {
        if (error.response) {
          console.log(error.response)
          console.log(error.response.status)
          console.log(error.response.headers)
        }
      })
  }

  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
      {/* new line start*/}
      <p>To get your profile details: </p>
      <button onClick={getData}>Click me</button>
      {profileData && <div>
        <p>Profile name: {profileData.profile_name}</p>
        <p>About me: {profileData.about_me}</p>
      </div>
      }
      {/* end of new line */}
    </>
  )
}

export default App
