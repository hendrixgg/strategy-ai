import { useState, useEffect } from "react";
import axios, { AxiosRequestConfig } from "axios";

axios.defaults.baseURL = "http://127.0.0.1:5000";

const useAxiosFetch = (initParams: AxiosRequestConfig<any>) => {
    const [params, setParams] = useState<AxiosRequestConfig<any>>(initParams);
    const [data, setData] = useState<any>(null);
    const [error, setError] = useState<any>(null);
    const [loading, setLoading] = useState<boolean>(true);

    const fetchData = async (): Promise<void> => {
        try {
            const response = await axios.request(params);
            setData(response.data);
        } catch (error) {
            if (axios.isAxiosError(error)) {
                setError("Axios Error with Message: " + error.message);
            } else {
                setError(error);
            }

            setLoading(false);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    return [data, error, loading, fetchData, setParams] as const;
};

export default useAxiosFetch;