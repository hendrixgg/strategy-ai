import { FunctionComponent, useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';

import { TaskProcessState } from '../TaskProcessState';

import { Task } from '../Tasks';
import useAxiosFetch from '../../../hooks/useAxiosFetch';

const ResultsSection: FunctionComponent<{
    taskState: TaskProcessState,
    setTaskState: Function,
    task: Task,
}> = ({ taskState, setTaskState, task }) => {
    const [results, setResults] = useState<string>("");
    const [resultsData, error, loading, fetchResultsData] = useAxiosFetch({
        method: "GET",
        url: `/runtask/${task.id}`,
    });

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
                setResults("");
                break;
            case TaskProcessState.ready:
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
    }, [taskState])

    return (
        <>
            <div style={{ padding: "0.5rem 0.5rem 0rem", overflowY: "auto", height: "30rem" }}>
                <ReactMarkdown>
                    {results}
                </ReactMarkdown>
            </div>
        </>
    )

}


export default ResultsSection;