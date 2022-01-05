import axios from "axios";

var url = (process.env.VUE_APP_API_BASE_URL.includes("localhost")) ? process.env.VUE_APP_API_BASE_URL: "http://" + location.host + "/" + process.env.VUE_APP_API_BASE_URL 
console.log(url)

const instance = axios.create({
  baseURL: url,
  timeout: 3000,
});

export default instance;
