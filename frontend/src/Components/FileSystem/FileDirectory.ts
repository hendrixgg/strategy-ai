type FileDirectory = {
    path: string,
    name: string,
    is_dir: false,
    children: null
} | {
    path: string,
    name: string,
    is_dir: true,
    children: FileDirectory[]
}

export default FileDirectory