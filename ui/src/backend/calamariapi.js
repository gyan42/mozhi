import axios from "axios";


var url = (process.env.VUE_APP_CALAMRI_API_BASE_URL.includes("localhost")) ? process.env.VUE_APP_CALAMRI_API_BASE_URL: "http://" + location.host + "/" + process.env.VUE_APP_CALAMRI_API_BASE_URL 
console.log(url)

// ("http://localhost:8088").includes("localhost")

const calamariAPI = axios.create({
  baseURL: url,
  timeout: 3000,
});

export default calamariAPI;
