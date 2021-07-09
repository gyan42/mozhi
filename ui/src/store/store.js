import nerModelPredictions from "./modules/ner-model-predictions"
import databaseInfo from "./modules/database-info"
import tokenizerInfo from "./modules/tokenizer-runtime-info"
import imageStore from "./modules/image-store"

export const mutations = {
};

export const getters = {};
export default {
  state() {
    return {
    };
  },
  getters,
  mutations,
  actions: {},
  modules: {
    nerModelPredictions,
    databaseInfo,
    tokenizerInfo,
    imageStore
  }
};