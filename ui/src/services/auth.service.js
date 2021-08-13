import mozhiapi from "@/backend/mozhiapi"

class AuthService {
    login(user) {
        console.log("AuthService login", user)
        let headers =   {
            timeout: 3000,
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        // https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/490c554e23343eec0736b06e59b2108fdd057fdc/%7B%7Bcookiecutter.project_slug%7D%7D/frontend/src/api.ts
        const params = new URLSearchParams();
        params.append('username', user.username);
        params.append('password', user.password);
        params.append("grant_type", user.grant_type)
        params.append("scope", user.scope)
        params.append("client_id", user.client_id)
        params.append("client_secret", user.client_secret)

        return mozhiapi
            .post(process.env.VUE_APP_AUTH_API_LOGIN, params, headers)
            .then(response => {
                if (response.data.accessToken) {
                    // { "access_token": "...", "token_type": "bearer" }
                    localStorage.setItem('user', JSON.stringify(response.data));
                }
                // console.log(response.data)
                return response.data;
            });
    }

    logout() {
        localStorage.removeItem('user');
    }

    register(user) {
        console.log(user)
        let headers =  {
            timeout: 5000
        }
        return mozhiapi
            .post(process.env.VUE_APP_AUTH_API_REGISTER, user, headers)
            .then((res) => {
                console.log(res)
            })
            .catch((err) => alert(err))
            .finally(() => {
                console.log(user)
            })
    }
}

export default new AuthService();