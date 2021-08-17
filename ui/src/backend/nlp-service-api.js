import mozhiapi from "@/backend/mozhiapi"

class NlpServiceApi {
    tokenize(text) {
        return mozhiapi
            .post(process.env.VUE_APP_API_TOKENIZE, {"text" : text}, {timeout: 50000}) //TODO why "text" is needed ?
            .then((res) => {
                return Promise.resolve(res.data.tokens);
            })
            .catch((err) => {
                alert(err)
                return Promise.reject(err)
            });
    }
}

export default new NlpServiceApi();