export default {
    namespaced: true,
    state: {
        connectionInfo: {
            host: process.env.VUE_APP_MINIO_HOST,
            port: process.env.VUE_APP_MINIO_PORT,
            accessKey: process.env.VUE_APP_MINIO_ACCESS_KEY,
            secretKey: process.env.VUE_APP_MINIO_SECRET_KEY,
        },
    },
    getters: {
        getConnectionMinIOInfo(state) {
            console.info("getConnectionInfo", state.connectionInfo)
            return state.connectionInfo
        }
    },
    mutations: {
        setConnectionMinIOInfo(state, payload) {
            console.info("setConnectionInfo", payload)
            state.connectionInfo = payload
        }
    }
}