import AuthService from '@/services/auth.service';

const user = JSON.parse(localStorage.getItem('user'));

// { status: {status: true/false}, user: { "access_token": "...", "token_type": "bearer" } }
const initialState = user ? { status: { loggedIn: true }, user } : { status: { loggedIn: false }, user: null };


export default {
  namespaced: true,
  state: initialState,
  getters: {
    isLoggedIn(state) {
      console.info("isLoggedIn", state)
      return state.status.loggedIn
    },
  },
  mutations: {
    loginSuccess(state, user) {
      state.status.loggedIn = true;
      state.user = user;
    },
    loginFailure(state) {
      state.status.loggedIn = false;
      state.user = null;
    },
    logout(state) {
      state.status.loggedIn = false;
      state.user = null;
    },
    registerSuccess(state) {
      state.status.loggedIn = false;
    },
    registerFailure(state) {
      state.status.loggedIn = false;
    }
  },
  actions: {
    login({ commit }, user) {
      console.log("login", user)
      return AuthService.login(user).then(
          user => {
            console.log("loginSuccess")
            commit('loginSuccess', user);
            return Promise.resolve(user);
          },
          error => {
            console.log("loginFailure")
            commit('loginFailure');
            return Promise.reject(error);
          }
      );
    },
    logout({ commit }) {
      AuthService.logout();
      commit('logout');
    },
    register({ commit }, user) {
      return AuthService.register(user).then(
          response => {
            commit('registerSuccess');
            return Promise.resolve(response.data);
          },
          error => {
            commit('registerFailure');
            return Promise.reject(error);
          }
      );
    }
  }
}