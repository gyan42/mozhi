import axios from "axios";

const predictionAPI = axios.create({
  baseURL: process.env.VUE_APP_TORCH_SERVE_PRED_BASE_URL, //"http://vf-api-torchserve-svc:6543",
  timeout: 3000,
});

const managementAPI = axios.create({
  baseURL: process.env.VUE_APP_TORCH_SERVE_MGMT_BASE_URL, //"http://vf-api-torchserve-svc:6544",
  timeout: 3000,
});

export default {
  predictionAPI,
  managementAPI
};


