import { useCallback, useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';

import { TaskProcessState } from '../TaskProcessState';

import { Task } from '../Tasks';
import { api_url } from '../../../api/variables';
import Button from '../../buttons/Button';
import FileDirectory from '../../FileSystem/FileDirectory';

interface TaskStreamResponse {
    type: "message" | "progress_info" | "results_text",
    body: string,
}

interface TaskData {
    date: string,
    files_available: FileDirectory | null,
    metadata: any,
    progress_info: string,
    status: string,
    task_name: string,
    task_type_id: number,
    task_uuid: string,
}

const saveResults = async (unique_id: string) => {
    const response = await fetch(`${api_url}/save_results/${unique_id}`, { method: "POST" });
    console.log(await response.json());
};

const ResultsSection = ({ taskState, setTaskState, task }: {
    taskState: TaskProcessState,
    setTaskState: Function,
    task: Task,
}) => {
    const [results, setResults] = useState<string>("");
    // this id uniquely identifies the task that is being run at this time
    const [saved, setSaved] = useState<boolean>(false);
    const [streamAbortController, setStreamAbortController] = useState<AbortController>(new AbortController());
    const [taskData, setTaskData] = useState<TaskData>({
        date: "",
        files_available: null,
        metadata: {},
        progress_info: "",
        status: "",
        task_name: "",
        task_type_id: 0,
        task_uuid: "",
    });

    const runTask = useCallback(async () => {
        // initalize the new task on the backend
        const initResponse = await fetch(`${api_url}/init_task/${task.id}`, { method: "GET" });
        const newTask = await initResponse.json();
        setTaskData(newTask);


        // this starts running the task on the backend
        // cancels the continuous retrieval of results once the task has been complete
        const handleStream = async (url: string, controller: AbortController) => {
            controller.signal.addEventListener("abort", () => console.log("aborted"));

            try {
                const streamResponse = await fetch(url, {
                    method: "GET",
                    signal: controller.signal,
                });
                const reader = streamResponse.body?.getReader();

                while (true) {
                    const { done, value } = await reader!.read();

                    if (done) {
                        break;
                    }

                    // Convert the Uint8Array chunk to a string
                    const chunkString = new TextDecoder().decode(value);
                    // console.log(chunkString.trimEnd().split("\n"));
                    const resultsTexts: string[] = chunkString
                        .trimEnd()
                        .split("\n")
                        .map(str => JSON.parse(str))
                        .filter((value: TaskStreamResponse) => value.type === "results_text")
                        .map((value) => value.body);
                    // console.log(resultsTexts)
                    setResults((text) => [text, ...resultsTexts].join("\n"));
                }
            } catch (error) {
                console.error("Error while streaming:", error);
            }
        };

        setTaskState(TaskProcessState.executing);
        await handleStream(`${api_url}/task_stream/${newTask.task_uuid}`, streamAbortController);
        // await handleStream(`${api_url}/test_stream/100`, streamAbortController);
        setStreamAbortController(new AbortController());
        setTaskState(TaskProcessState.complete);
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

    if (taskState < TaskProcessState.executing) {
        return <></>;
    }

    return (
        <>
            <div style={{ padding: "0.5rem 0.5rem 0rem", overflowY: "auto", height: "24rem" }}>
                <ReactMarkdown>
                    {results}
                </ReactMarkdown>
            </div>
            <div style={{ padding: "0.5rem 0.5rem 0rem", height: "fit-content" }}>
                <Button onClick={() => { saveResults(taskData.task_uuid), setSaved(true) }} disabled={saved || taskState == TaskProcessState.executing}>Save</Button>
            </div>
        </>
    );

}


export default ResultsSection;