# strategy-ai

## What is This For?
This is an app designed to take company's strategy documents and identify the core strategy of the business across the multiple perspectives, including:

- Financial
- Customer
- Internal
- Enabling

This is currently just software that can used internally and also be shown as a demo to clients, this software is not planned to be distributed.

## How to run?

### Running Development Environment
1. Ensure that all dependencies are installed
    1. node_modules (npm install)
    1. python packages (see backend/requirements.txt)
1. Create a file in the backend directory titled ".env" containing OPENAI_API_KEY="your api key here"
1. Open up split cmd terminals  
1. In one terminal start the python server by running: "npm run dev-backend"
1. In the other terminal open the vite react app by running: "npm run dev"

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

#### UI
1. install react with vite
    1. followed steps in [this article](https://blog.bitsrc.io/maximize-your-react-skills-build-a-to-do-list-app-from-start-to-finish-with-typescript-vite-b1b5e0faecbe)
    1. played around a bit by editing App.tsx
1. install react-markdown to show the results from the Tasks being run
    1. run "npm install react-markdown"
1. I did not log all the work I did here up to 2023-07-27, after this day, I began loggin the work done on the UI here\

#### Backend
Set up backend using **python**, but realize that all of the same functionality could be implemented with **node.js** since langchain is supported there also, this would allow the whole system to be javascript based but I'm not sure if this makes that much of a difference and I have worked a lot more with python in the past compared to node.js.
1. followed the steps in the article up to [here](https://dev.to/nagatodev/how-to-connect-flask-to-reactjs-1k8i#:~:text=backend/__pycache__-,Connecting,-the%20API%20endpoint)
2. python modules explicitly installed with pip install (versions and implicit dependencies found in backend/requirements.txt):
    - Flask
    - Flask-Cors
    - langchain
    - "unstructured[local-inference]"
    - faiss-cpu
    - python-dotenv
    - tiktoken
    - openai
    - pydantic
    1. run "pip3 freeze" to see all the dependencies currently installed
    2. run "pip install -r requirements.txt" to install python modules
3. had to modify some stuff in the vite.config.ts file
4. base.py: this is where the flask app is run from
    1. load_dotenv environment variables so that ChatOpenAI can work properly
    2. origins for CORS (can be limited in future, for development all origins are allowed)
    3. tasks: dict for all the tasks of the current session
    4. File system, documents loaded, vector store, llm
        1. implement document loaders
            1. loading different document types
            2. loading websites
            3. A general purpose loader that uses the specific loader depending on the file type
        1. Document source: to organize loaded documents in the running python environment
        2. Document store: to take various document sources and split them into smaller chunks that can be inputted to a vector store
            1. **NEED TO DO** in the future, will implement ability to add new or update documents (may currently be supported by the vector store)
        3. vector store: uses OpenAI embeddings and the FAISS Vector Store to allow for retrieval of context based on natural language similarity search
            1. **NEED TO DO**: experiment with what text to use for the similarity search here. Should it be just the topic? the whole question?
    5. api route to send the file structure to the UI
        1. implement path_to_dict to retrieve file structure of available documents
    6. api route to initalize a task
        1. requires: BaseTask, Task1Surfacing
    7. api route to stream the task results
        1. requires: BaseTask, Task1Surfacing
    8. api route to save the results (tasks are saved automatically after they finished running, this is just to save a copy of readable text results from hidden_files/api_output to the visible_files/ai_files so that the output can be used for future task input)
        1. requires: BaseTask, Task1Surfacing
        1. **NEED TO DO**: consider updating the vector store and document store after running this so that the next tasks can use these results as input
5. task.py: BaseTask: abstract class that captures the essesntial functions and data that a task executed from this backend would have
    1. specify the basic data that will be stored about the task
    2. specify how results can be streamed as output (generate_results, generate_results_json_bytes)
    3. **NEED TO DO**: specify the format for BaseTask.generate_results() stream output with a dataclass or some reusable class
    4. specify how the task information is be saved (save function)
6. Task1Surfacing: class that allows for executing Strategy Surfacing
    1. specify the inputs: vector store (for context), available data (for metadata), llm (for the natural language AI, using ChatOpenAI)
    2. performance management framework
        1. defined objective categories and sub-objectives to look for
        2. defined the prompt templates that will allow for the surfacing of the objectives - **To be iterated and improved upon**
        3. defined the OpenAI GPT function call schema for formatted objectives - **To be iterated and improved upon**
            1. there is a new langchain update that gives a better way to specify this format with a python class
            2. I also read that higher temperatures may lead to better formatting, however this may not be a good thing since the reason for higher temperature giving better formatting is likely due to hallucination to fill in non-existing data to fit the format. Need to find a way around this
        4. defined the prompt template sequence for each objective with asynchronous calls to the llm
        5. defined the structure to store the surfaced objectives from each category
        6. implemented *abstractmethod* generate_results
    3. risk management framework - **NOT STARTED**
7. implement Assessment Task (Task 2)
    1. next step is to tweak what has been hard coded


### New features to do (extra) 
1. session saving:
    1. be able to create sessions with their associated files and history for all tasks that have been run
    1. be able to load a previous session on startup
    1. be able to open results from previously run tasks in the UI

1. create an agent that does everything with: https://python.langchain.com/docs/modules/agents/how_to/custom_multi_action_agent
