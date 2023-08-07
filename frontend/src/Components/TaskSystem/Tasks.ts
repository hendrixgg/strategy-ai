
export interface Task {
    id: number,
    name: string,
    description: string,
}

export const Tasks: Array<Task> = [
    {
        id: 0,
        name: "Select Task",
        description: "",
    },
    {
        id: 1,
        name: "Strategy Surfacing",
        description: "Surface the key elements of the business strategy based on the provided documents. Simplify the strategy down to a list of objectives. This currently only assesses strategy for performance, not for risk management purposes.",
    },
    {
        id: 2,
        name: "Strategy Assessment",
        description: "Assess the organization's ability to execute on their strategy.",
    },
    {
        id: 3,
        name: "Prioritize Objectives",
        description: "Assign priorities to objectives based on their strategic impact on the business.",
    },
    {
        id: 4,
        name: "Identify Departments",
        description: "",
    },
    {
        id: 5,
        name: "Ontology",
        description: "",
    },
    {
        id: 6,
        name: "Make OKRs",
        description: "",
    },
]