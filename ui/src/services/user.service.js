import mozhiapi from "@/backend/mozhiapi"
import authHeader from './auth-header';

const API_URL = process.env.VUE_APP_AUTH_API_PROFILE_ME

class UserService {

    getUserMe() {
        return mozhiapi.get(API_URL, { headers: authHeader() });
    }

    patchUserMe() {
        return mozhiapi.get(API_URL + 'mod', { headers: authHeader() });
    }

    getUser(id) {
        return mozhiapi.get(API_URL + '/' + id, { headers: authHeader() });
    }

    deleteUser(id) {
        return mozhiapi.get(API_URL + '/' + id, { headers: authHeader() });
    }
}

export default new UserService();