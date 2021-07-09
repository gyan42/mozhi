// import Vue from 'vue'
import { createApp } from "vue";
import router from './router'
import App from "./App.vue";
import "es6-promise/auto";
import { createStore } from "vuex";
import store from "./store/store.js";

import VueSidebarMenu from 'vue-sidebar-menu'
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'
import '@fortawesome/fontawesome-free/css/all.css'

//    "@fortawesome/fontawesome-svg-core": "^1.2.32",
// import { library } from "@fortawesome/fontawesome-svg-core";
// import {
//   faCoffee,
//   faFileAlt,
//   faPlusSquare,
//   faUser,
//     faFile
// } from "@fortawesome/free-solid-svg-icons";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import axios from "axios";

// library.add(faFileAlt, faUser, faPlusSquare, faCoffee, faFile);

// https://stackoverflow.com/questions/55883984/vue-axios-cors-policy-no-access-control-allow-origin
axios.defaults.headers.get['header-name'] = 'value'

const app = createApp(App);
app.use(router);
app.use(createStore(store));
app.use(VueSidebarMenu)
app.component("font-awesome-icon", FontAwesomeIcon);
app.mount("#app");