import { createApp } from "vue";
import router from './router'
import App from "./App.vue";
import "es6-promise/auto";
import  store from "./store/store.js";
import VueSidebarMenu from 'vue-sidebar-menu'
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'
import '@fortawesome/fontawesome-free/css/all.css'
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import VeeValidate from 'vee-validate';
import moshaToast from 'mosha-vue-toastify'
import 'mosha-vue-toastify/dist/style.css'


// import LogIn from "@/views/LogIn";

// import axios from "axios";
// https://stackoverflow.com/questions/55883984/vue-axios-cors-policy-no-access-control-allow-origin
// axios.defaults.headers.get['header-name'] = 'value'

const app = createApp(App);
app.use(router);
app.use(VeeValidate)
app.use(store);
app.use(VueSidebarMenu)
app.use(moshaToast)
app.component("font-awesome-icon", FontAwesomeIcon);
app.mount("#app");