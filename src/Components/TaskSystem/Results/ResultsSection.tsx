import { FunctionComponent, useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';

import { TaskProcessState } from '../TaskProcessState';

import { Task } from '../Tasks';
import useAxiosFetch from '../../../hooks/useAxiosFetch';
import Button from '../../buttons/Button';

import axios from "axios";
const saveResults = async (resultsData: any) => {
    const response = await axios.request({
        method: "GET",
        "url": `/saveoutput/${resultsData.file_name}`
    });
    if (response.data.success) {
        console.log("results saved!");
    }
}

const ResultsSection: FunctionComponent<{
    taskState: TaskProcessState,
    setTaskState: Function,
    task: Task,
}> = ({ taskState, setTaskState, task }) => {
    const [results, setResults] = useState<string>("");
    const [saved, setSaved] = useState<boolean>(false);
    const [resultsData, error, loading, fetchResultsData] = useAxiosFetch({
        method: "GET",
        url: `/runtask/${task.id}`,
    });

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