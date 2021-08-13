<template>
  <page-header>
    <h1 class="title">Welcome to Mozhi! </h1>
  </page-header>

  <section class="hero">
    <div class="hero-body">
      <div class="container">
        <div class="columns is-centered">
          <div class="column is-5-tablet is-4-desktop is-3-widescreen">

            <form action="" class="box">
              <div class="field">
                <label for="emailinput" class="label">Email</label>
                <div class="control has-icons-left">
                  <input id= "emailinput" type="email" placeholder="e.g. admin@mozhi.com" class="input" required v-model="formData.email">
                  <span class="icon is-small is-left">
                  <i class="fa fa-envelope"></i>
                </span>
                </div>
              </div>

              <div class="field">
                <label for="passwordinput" class="label">Password</label>
                <div class="control has-icons-left">
                  <input id = "passwordinput" type="password" placeholder="*******" class="input" required v-model="formData.password">
                  <span class="icon is-small is-left">
                  <i class="fa fa-lock"></i>
                </span>
                </div>
              </div>

              <!--              <div class="field">-->
              <!--                <label for="checkbocsuper" class="checkbox">-->
              <!--                  <input id= "checkbocsuper" type="checkbox" v-model="formData.is_superuser">-->
              <!--                  Is Super User?-->
              <!--                </label>-->
              <!--              </div>-->

              <div class="control">
                <div class="field">
                  <button class="button is-success" @click="onSignUp">
                    Sign Up!
                  </button>
                </div>
              </div>

            </form>
          </div>
        </div>
      </div>
    </div>
  </section>

  <div class="field">
    <button class="button is-warning" @click="onBack">
      Back
    </button>
  </div>

</template>

<script>
import PageHeader from "@/components/PageHeader"
import mozhiapi from "@/backend/mozhiapi"

export default {
  name: "LogIn",
  data() {
    return {
      formData: {
        "email": "mozhi@mozhi.com",
        "password": "mozhi",
        "is_active": true,
        "is_superuser": true,
        "is_verified": false
      }
    }
  },
  components: {PageHeader},
  methods: {
    onSignUp() {
      console.log(this.formData)
      let headers =   {
        timeout: 50000
      }
      mozhiapi
          .post(process.env.VUE_APP_AUTH_API_REGISTER, this.formData, headers)
          .then((res) => {
            console.log(res)
          })
          .catch((err) => alert(err))
          .finally(() => {
            console.log(this.formData)
          })
      this.$router.push({name: "LogIn"})
    },
    onBack() {
      this.$router.push({name: "LogIn"})

    }
  }
}
</script>

<style scoped>

</style>