import { useCallback, useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';

import { TaskProcessState } from '../TaskProcessState';

import { Task } from '../Tasks';
import { api_url } from '../../../api/variables';
import Button from '../../buttons/Button';

import axios from "axios";
const saveResults = async (resultsData: any) => {
    // const response = await axios.request({
    //     method: "GET",
    //     "url": `/save_output/${resultsData.file_name}`
    // });
    // if (response.data.success) {
    //     console.log("results saved!");
    // }
};

const ResultsSection = ({ taskState, setTaskState, task }: {
    taskState: TaskProcessState,
    setTaskState: Function,
    task: Task,
}) => {
    const [results, setResults] = useState<string>("");
    // this id uniquely identifies the task that is being run at this time
    const [uniqueTaskID, setUniqueTaskID] = useState<string>("");
    const [saved, setSaved] = useState<boolean>(false);

    const runTask = useCallback(async () => {
        const startResponse = await axios.get(`${api_url}/init_task/${task.id}`);
        console.log(startResponse.data);
        setUniqueTaskID(startResponse.data.task_uuid);

        setTaskState(TaskProcessState.executing);
        const intervalID = setInterval(async () => {
            const resultsResponse = await axios.get(`${api_url}/task_results/${startResponse.data.task_uuid}`);
            setResults(resultsResponse.data.results);
        }, 500);
        // this starts running the task on the backend
        axios.get(`${api_url}/task_stream/${startResponse.data.task_uuid}`).then((response) => {
            console.log(response);
            setTaskState(TaskProcessState.complete);
            clearInterval(intervalID);
        });
    }, [task.id]);



    useEffect(() => {
        switch (taskState) {
            case TaskProcessState.selecting:
                setSaved(false);
                setResults("");
                break;
            case TaskProcessState.ready:
                setSaved(false);
                setResults("");
                break;
            case TaskProcessState.start:
                setSaved(false);
                runTask();
                break;
            case TaskProcessState.executing:
                // setResults("executing...");
                break;
            case TaskProcessState.complete:
                // setResults("complete");
                break;
        }
    }, [taskState]);

    return (
        <>
            {taskState > TaskProcessState.start &&
                <div style={{ padding: "0.5rem 0.5rem 0rem", overflowY: "auto", height: "24rem" }}>
                    <ReactMarkdown>
                        {results}
                    </ReactMarkdown>
                </div>}
            {taskState == TaskProcessState.complete &&
                <div style={{ padding: "0.5rem 0.5rem 0rem", height: "fit-oontent" }}>
                    <Button onClick={() => { saveResults("resultsData"), setSaved(true) }} disabled={saved}>Save</Button>
                </div>
            }
        </>
    )

}


export default ResultsSection;