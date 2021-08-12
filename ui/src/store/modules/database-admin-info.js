export default {
    namespaced: true,
    state: {
        formData: {
            host: 'localhost',
            port: '5432',
            user: 'mozhi',
            password: 'mozhi'
        },
        currentText: "demo text for annotation from store",
        currentId: 1, //current row id
        currentAnnotations: "",
        totalRows: 0

    },
    getters: {
        getFormData(state) {
            console.info("getFormData", state)
            return state.formData
        },
        getCurrentRowId(state) {
            console.log("getCurrentRowId", state)
            return state.currentId
        }
    },
    mutations: {
        setFormData(state, payload) {
            console.info("setFormData", payload)
            state.formData = payload
        },
        setCurrentText(state, payload) {
            console.info("setCurrentText", payload)
            state.currentText = payload
        },
        setTotalCounts(state, payload) {
            console.info("setTotalCounts", payload)
            state.totalRows = payload
        },
        setCurrentRowId(state, payload) {
            console.log("setCurrentRowId", payload)
            state.currentId = payload
        }
    }
}