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
                <label for="" class="label">Email</label>
                <div class="control has-icons-left">
                  <input type="email" placeholder="e.g. admin@mozhi.com" class="input" required>
                  <span class="icon is-small is-left">
                  <i class="fa fa-envelope"></i>
                </span>
                </div>
              </div>

              <div class="field">
                <label for="" class="label">Password</label>
                <div class="control has-icons-left">
                  <input type="password" placeholder="*******" class="input" required>
                  <span class="icon is-small is-left">
                  <i class="fa fa-lock"></i>
                </span>
                </div>
              </div>
              <div class="field">
                <label for="" class="checkbox">
                  <input type="checkbox">
                  Remember me
                </label>
              </div>
              <div class="field">
                <button class="button is-success">
                  Login
                </button>
              </div>
            </form>

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
import PageHeader from "@/components/PageHeader"

export default {
  name: "LogIn",
  components: {PageHeader},
  methods: {
    onSignUp() {
      console.log("moveToSignUpPage")
      this.$router.push({name: 'SignUp'});
    }
  }
}
</script>

<style scoped>

</style>