import { createStore } from "vuex";
import nerModelPredictions from "./modules/ner-model-predictions"
import databaseInfo from "@/store/modules/database-info-store"
import tokenizerInfo from "./modules/tokenizer-runtime-info"
import imageStore from "./modules/image-store"
import auth from "@/store/modules/auth"
import minio from "@/store/modules/minio-store"

export default createStore({
  state() {
    return {
    };
  },
  getters: {

  },
  mutations: {

  },
  actions: {},
  modules: {
    nerModelPredictions,
    databaseInfo,
    tokenizerInfo,
    imageStore,
    auth,
    minio
  }
});



