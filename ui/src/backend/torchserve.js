import axios from "axios";


class TorchServe {
    constructor() {
        this.api = axios.create({
            baseURL: process.env.VUE_APP_TORCH_SERVE_MGMT_BASE_URL,
            timeout: 1000 * 60, // seconds
        });
    }

    register_model(bucket, prefix) {
        // curl -X POST  "http://localhost:6544/models?initial_workers=1&synchronous=true&url=http://minio:80/mozhi/model-store/sroie2019v1.mar"
        // curl -X POST  "http://localhost:6544/models?initial_workers=1&synchronous=true&url=http://localhost:9000/mozhi/model-store/conll2003v1.mar"
        return this.api.post("models?initial_workers=1&synchronous=true&url=" +
            `http://minio:80/${bucket}${prefix}`)
            .then((res) => {
                console.log(res)
                return Promise.resolve(res)
            })
            .catch(function (error) {
                if (error.response) {
                    // The request was made and the server responded with a status code
                    // that falls out of the range of 2xx
                    console.log(error.response.data);
                    console.log(error.response.data.message);
                    console.log(error.response.status);
                    console.log(error.response.headers);
                    return Promise.reject(error.response.data.message)

                } else if (error.request) {
                    // The request was made but no response was received
                    // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                    // http.ClientRequest in node.js
                    console.log(error.request);
                } else {
                    // Something happened in setting up the request that triggered an Error
                    console.log('Error', error.message);
                }
                console.log(error.config);
            });
    }
}

export default new TorchServe()
