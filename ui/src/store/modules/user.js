export default {
    namespaced: true,
    state: {
        token: "",
        username: "",
        email: "mozhi@mozhi.com",
        password: "mozhi",
        is_active: true,
        is_superuser: true,
        is_verified: false
    },
    getters: {
        getUserToken(state) {
            console.info("getUserToken", state)
            return state.token
        },
    },
    mutations: {
    }
}