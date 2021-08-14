export default {
    namespaced: true,
    state: {
        connectionInfo: {
            host: 'localhost',
            port: '5432',
            user: 'mozhi',
            password: 'mozhi',
            dbname: 'mozhidb'
        },
        tableInfo: {
            text_table_name: 'conll2003_train',
            tag_table_name: 'conll2003_train_tags',
            text_col_name: 'text',
            features_col_name: 'features',
            labels_col_name: 'labels',
            start_id: 1
        },

        currentText: "demo text for annotation from store",
        currentId: 1, //current row id
        currentAnnotations: "",
        totalRows: 0

    },
    getters: {
        getConnectionInfo(state) {
            console.info("getConnectionInfo")
            return state.connectionInfo
        },
        getTableInfo(state) {
            console.log("getCurrentRowId", state)
            return state.tableInfo
        },
        getCurrentRowId(state) {
            console.log("getCurrentRowId", state)
            return state.getCurrentRowId
        }
    },
    mutations: {
        setConnectionInfo(state, payload) {
            console.info("setConnectionInfo", payload)
            state.connectionInfo = payload
        },
        setTableInfo(state, payload) {
            console.info("setTableInfo", payload)
            state.connectionInfo = payload
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