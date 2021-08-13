export default {
    namespaced: true,
    state: {
        dbConnectionInfo: {
            host: 'localhost',
            port: '5432',
            user: 'mozhi',
            password: 'mozhi',
        },
        formData: {
            host: 'localhost',
            port: '5432',
            user: 'mozhi',
            password: 'mozhi',
            db_name: 'mozhidb',
            text_table_name: 'conll2003_train',
            tag_table_name: 'conll2003_train_tags',
            text_col_name: 'text',
            features_col_name: 'features',
            labels_col_name: 'labels',
            start_id: 1},
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