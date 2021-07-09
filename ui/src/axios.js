import axios from "axios";

const instance = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL, // "http://vf-api-cpu-svc:8088",
  timeout: 3000,
});

export default instance;
