# strategy-ai

## How to run?

### Development environment
1. Ensure that all dependencies are installed
    1. node_modules (vite react ts app + react-markdown)
    1. python packages (see backend/requirements.txt)
1. Open up split cmd terminals  
1. In the right terminal start the python server by running: "npm run start-backend"
1. In the left terminal open the vite react app by running: "npm run dev"

## What is This For?
This is an app designed to take company's strategy documents and identify the core strategy of the business across the multiple perspectives, including:

- Financial
- Customer
- Internal
- Enabling

This is currently just software that can used internally and also be shown as a demo to clients, this software is not planned to be distributed.

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

### Business Logic: Python + Flask + langchain
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
    1. had to modify some stuff in the vite.config.ts file
    1. run "pip3 freeze" to see all the required dependencies to be installed
1. install react-markdown to show the results from the Tasks being run
    1. run "npm install react-markdown"
