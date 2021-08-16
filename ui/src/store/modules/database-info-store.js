export default {
    namespaced: true,
    state: {
        connectionInfo: {
            host: process.env.VUE_APP_DB_HOST,
            port: process.env.VUE_APP_DB_PORT,
            user: process.env.VUE_APP_DB_USER,
            password: process.env.VUE_APP_DB_PASSWORD,
            dbname: process.env.VUE_APP_DB_NAME
        },
        tableInfo: {
            db_name: "mozhidb",
            text_table_name: 'conll2003_train',
            tag_table_name: 'conll2003_train_tags',
            text_col_name: 'text',
            features_col_name: 'features',
            labels_col_name: 'labels',
            start_id: 1
        },

        currentText: "demo text for annotation from store",
        currentId: 0, //current row id
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
            state.tableInfo = payload
        },
        setTextTableInfo(state, payload) {
            console.info("setTextTableInfo", payload)
            state.tableInfo.text_table_name = payload
        },
        setTagTableInfo(state, payload) {
            console.info("setTagTableInfo", payload)
            state.tableInfo.tag_table_name = payload
        },
        setUserDBInfo(state, payload) {
            console.info("setStartIdInfo", payload)
            state.tableInfo.db_name = payload
        },
        setStartIdInfo(state, payload) {
            console.info("setStartIdInfo", payload)
            state.tableInfo.start_id = payload
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