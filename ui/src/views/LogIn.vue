<template>
  <page-header>
    <h1 class="title">Welcome to Mozhi! {{formData.username}}</h1>
  </page-header>

  <section class="hero">
    <div class="hero-body">
      <div class="container">
        <div class="columns is-centered">
          <div class="column is-5-tablet is-4-desktop is-3-widescreen">

            <div class="box">

              <div class="field">
                <label for="emailinput" class="label">Email</label>
                <div class="control has-icons-left">
                  <input id= "emailinput"  type="email" placeholder="e.g. admin@mozhi.com" class="input" required v-model="formData.username">
                  <span class="icon is-small is-left">
                  <i class="fa fa-envelope"></i>
                </span>
                </div>
              </div>

              <div class="field">
                <label for="passinput" class="label">Password</label>
                <div class="control has-icons-left">
                  <input id= "passinput"  type="password" placeholder="*******" class="input" required v-model="formData.password">
                  <span class="icon is-small is-left">
                  <i class="fa fa-lock"></i>
                </span>
                </div>
              </div>
              <div class="field">
                <label for="remembermecheckbox" class="checkbox">
                  <input id="remembermecheckbox" type="checkbox">
                  Remember me
                </label>
              </div>

              <div class="control">
                <div class="field">
                  <button class="button is-success" @click="onLogIn">
                    Login
                  </button>
                </div>
              </div>

            </div>

          </div>
        </div>
      </div>
    </div>
  </section>

  <div class="field">
    <button class="button is-warning" @click="onSignUp">
      Sign Up
    </button>
  </div>

</template>

<script>
import "@/assets/styles.scss";
import PageHeader from "@/components/PageHeader"
// import loginService from "@/services/auth.service"
import UserLogInfo from "@/models/user-login-info";
import {mapMutations, mapGetters, mapActions} from "vuex";

export default {
  name: "LogIn",
  components: {PageHeader},
  data() {
    return{
      formData: new UserLogInfo("mageswaran1989@gmail.com", "newpassword", "", "", "", "")
    }
  },
  computed: {
    ...mapGetters('auth', ['isLoggedIn']),
  },
  created() {
    if (this.isLoggedIn) {
      console.log(this.formData)
    //  this.$router.push({name: 'Home'});
    }
  },
  methods: {
    ...mapMutations('auth', ['loginSuccess', 'loginFailure', 'logout', 'registerSuccess', 'registerFailure']),
    ...mapActions("auth", ['login']),
    onLogIn() {
      console.log("formData", this.formData)
      // loginService.login(this.formData)
      this.login(this.formData).then(
          () => {
            this.$router.push({name: 'Home'})
          },
          error => {console.log("login error", error)}
      )
      if (this.isLoggedIn) {
        this.$router.push({name: 'Home'});
      } else {
        console.log("login error")
      }


    },
    onSignUp() {
      console.log("moveToSignUpPage")
      this.$router.push({name: 'SignUp'});
    }
  }
}
</script>

<style scoped>

</style>