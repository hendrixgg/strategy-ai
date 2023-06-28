# strategy-ai

## What is This For?
This is an app designed to take your company's strategy documents and identify the core strategy of your business across the multiple perspectives, including:

- Financial
- Customer
- Internal
- Enabling

## What Types of Documents Can Be Uploaded?
The more documents uploaded the better the system will be able to provide insights into your strategy.

### Google
- Docs
- Sheets

### Microsoft
- Word
- Excel
- PowerPoint

### Meeting Recordings/Transcripts
- Audio and video files
    - file types to be determined
- Transcripts
    - text files
    - additional file types to be determined

## How is This App Built?

### Business Logic: Python + Flask
- https://dev.to/nagatodev/how-to-connect-flask-to-reactjs-1k8i
- https://dev.to/nagatodev/getting-started-with-flask-1kn1

### Front-End: ReactJs
- create the app: https://www.youtube.com/watch?v=vr-I2HIVmTw
- https://developer.okta.com/blog/2022/03/14/react-vite-number-converter
- need to figure out how to use typescript with all of this **maybe not cause will be slower to learn, but pretty sure it is industry standard

### step-by-step

1. install react with vite
    1. followed steps in [this article](https://blog.bitsrc.io/maximize-your-react-skills-build-a-to-do-list-app-from-start-to-finish-with-typescript-vite-b1b5e0faecbe)
    1. played around a bit by editing App.tsx
1. set up backend with python
    1. followed the steps in the article up to [here](https://dev.to/nagatodev/how-to-connect-flask-to-reactjs-1k8i#:~:text=backend/__pycache__-,Connecting,-the%20API%20endpoint)
    1. next step: continue from the above link
    1. had to modify some stuff in the vite.config.ts file