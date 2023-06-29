export default interface FileDirectory {
    path: string,
    name: string,
    type: string,
    children: FileDirectory[] | null
}