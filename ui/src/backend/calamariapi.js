import axios from "axios";

const calamariAPI = axios.create({
  baseURL: process.env.VUE_APP_CALAMRI_API_BASE_URL,
  timeout: 3000,
});

export default calamariAPI;
