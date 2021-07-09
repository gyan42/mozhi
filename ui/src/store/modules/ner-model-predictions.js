export default {
    namespaced: true,
    state: {
        modelName: 'spacy',
        dataSetName: 'plaintext',
        predictions: [], // [{text, start, end, label, type}...
        classes: []
    },
    getters: {
        getModelName(state) {
            console.info("getModelName", state)
            return state.modelName
        },
        getDataSetName(state) {
            console.info("getDataSetName", state)
            return state.dataSetName
        },
        getClasses(state) {
            console.info("getClasses")
            return state.classes
        },
        getPredictions(state) {
            console.info("getPredictions", state.predictions)
            return state.predictions
        }
    },
    mutations: {
        setModelName(state, payload) {
            console.info("setModelName", payload)
            state.modelName = payload
        },
        setDatasetName(state, payload) {
            console.info("setDatasetName", payload)
            state.dataSetName = payload
        },
        setPredictions(state, payload) {
            console.info("setPredictions", payload)
            state.predictions = payload
        },
        setClasses(state, payload) {
            console.info("setClasses", payload)
            state.classes = payload
        }
    }
}