import { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';

import { TaskProcessState } from '../TaskProcessState';

import { Task } from '../Tasks';
import useAxiosFetch from '../../../hooks/useAxiosFetch';
import Button from '../../buttons/Button';

import axios from "axios";
const saveResults = async (resultsData: any) => {
    const response = await axios.request({
        method: "GET",
        "url": `/save-output/${resultsData.file_name}`
    });
    if (response.data.success) {
        console.log("results saved!");
    }
};

const subscribeToTask = (taskUuid: string) => {
    // call axios fetch with:
    const parameters = {
        method: "GET",
        url: "/"
    };
    const response = {
        status: "",
        message: "",
        date: "",
        task_data: {
            task_type_id: 0,
            uuid: "",
            progress_info: "",
            results: "",
            files_used: ["", ""],
            metadata: {},
        },
    };
};

const ResultsSection = ({ taskState, setTaskState, task }: {
    taskState: TaskProcessState,
    setTaskState: Function,
    task: Task,
}) => {
    const [results, setResults] = useState<string>("");
    // this id uniquely identifies the task that is being run
    const [uniqueTaskId, setUniqueTaskId] = useState<string>("");
    const [saved, setSaved] = useState<boolean>(false);

    // call to start the task
    const startTask = () => {
        // call axios fetch with:
        const parameters = {
            method: "GET",
            url: `/start-task/${task.id}`,
        };
    };

    // call to fetch the results
    const [resultsData, error, loading, fetchResultsData, setParams] = useAxiosFetch({
        method: "GET",
        url: `/task-results/${uniqueTaskId}`,
    });



    useEffect(() => {
        setParams((params) => {
            return {
                ...params,
                url: `/task-progress/${uniqueTaskId}`,
            };
        })
    }, [uniqueTaskId]);

    useEffect(() => {
        if (error) {
            console.log(error);
            setResults("");
        }
    }, [error]);

    useEffect(() => {
        if (loading) {
            console.log("retrieving results...");
            setResults("");
        }
    }, [loading]);

    useEffect(() => {
        if (resultsData && taskState === TaskProcessState.executing) {
            console.log(resultsData);
            setTaskState(TaskProcessState.complete);
        } else if (taskState === TaskProcessState.executing) {
            setTaskState(TaskProcessState.executing);
        }
    }, [resultsData]);


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
                setResults("");
                startTask();
            case TaskProcessState.executing:
                setResults("executing...");
                fetchResultsData();
                break;
            case TaskProcessState.complete:
                setResults(resultsData.text);
                break;
        }
    }, [taskState]);

    return (
        <>
            <div style={{ padding: "0.5rem 0.5rem 0rem", overflowY: "auto", height: "24rem" }}>
                <ReactMarkdown>
                    {results}
                </ReactMarkdown>
            </div>
            <div style={{ padding: "0.5rem 0.5rem 0rem", height: "fit-oontent" }}>
                <Button onClick={() => { saveResults(resultsData), setSaved(true) }} disabled={saved}>Save</Button>
            </div>
        </>
    )

}


export default ResultsSection;