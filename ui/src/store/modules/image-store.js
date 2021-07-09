export default {
    namespaced: true,
    state: {
        filePrefixes: [],
        currentIndex: 0,
        experimentName: "receipts",
        storageServer: {
            host: "192.168.0.142",
            port: "9000",
            storageClass: "minio",
            accessKey: "admin",
            secretKey: "password",
            bucket: "mozhi",
            prefix: "data/receipts/",
            ocrEngine: "tesseact",
        },
        dbServerInfo: {
            host: "localhost",
            port: "5432",
            db_name: "mozhidb",
            user: "mozhi",
            password: "mozhi"
        },
    },
    getters: {
        getFileCurrentPrefix(state) {
            // console.info("getFileCurrentPrefix", state)
            return state.filePrefixes[state.currentIndex]
        },
        getFilesCount(state) {
            // console.info("getFilesCount", state.filePrefixes.length)
            return state.filePrefixes.length
        }
    },
    mutations: {
        setCurrentIndex(state, payload) {
            // console.info("setCurrentIndex", payload)
            state.currentIndex = payload
        },
        setFilePrefixes(state, payload) {
            // console.info("setFilePrefixes", payload)
            state.filePrefixes = payload
        }
    }
}
