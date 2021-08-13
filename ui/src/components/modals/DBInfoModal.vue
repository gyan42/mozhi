<template>

  <div class="modal"  @keydown.esc="isActive" tabindex="0" v-bind:class="{'is-active':isActive}">
    <div class="modal-background"></div>

    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Database Admin Connection Info</p>
        <button @click="close" class="delete" aria-label="close"></button>
<!--        <button @click="close" class="modal-close"></button>-->

      </header>
      <section class="modal-card-body">
        <form>
          <div class="columns">
            <div class="column is-one-third">
              <label for="host" style="text-align:right" class="label is-large">Host</label>
            </div>
            <div class="column">
              <input id="host" class="input is-medium"  type="text" placeholder="localhost" v-model.lazy="formData.host">
            </div>
          </div>

          <div class="columns">
            <div class="column is-one-third">
              <label for="port" style="text-align:right" class="label is-large is-right">Port</label>
            </div>
            <div class="column">
              <input id="port" class="input is-medium"  type="text" placeholder="5432" v-model.lazy="formData.port">
            </div>
          </div>

          <div class="columns">
            <div class="column is-one-third">
              <label for="user" style="text-align:right" class="label is-large is-right">User</label>
            </div>
            <div class="column">
              <input id="user" class="input is-medium"  type="text" placeholder="mozhi" v-model.lazy="formData.user">
            </div>
          </div>

          <div class="columns">
            <div class="column is-one-third">
              <label for="pass" style="text-align:right" class="label is-large is-right">Password</label>
            </div>
            <div class="column">
              <input id="pass" class="input is-medium"  type="text" placeholder="mozhi" v-model.lazy="formData.password">
            </div>
          </div>

        </form>
      </section>
      <footer class="modal-card-foot">
        <button class="button is-success">Save changes</button>
        <button @click="close" class="button">Cancel</button>
      </footer>
    </div>
  </div>

</template>

<script>
// import {mapMutations, mapGetters} from "vuex";

// import {mapGetters} from "vuex";

export default {
  name: "DBInfoDialogBox",
  props: ['isActive', 'close', 'message'],
  data() {
    return {
      // TODO: move to common module
      // Back End DB module needs to be in sync
      // Vue store needs to be in sync
      formData: {
        host: process.env.VUE_APP_DB_HOST,
        port: process.env.VUE_APP_DB_PORT,
        user: process.env.VUE_APP_DB_USER,
        password: process.env.VUE_APP_DB_PASSWORD,
      }
    }},
  methods: {
     // ...mapGetters('databaseInfo', ['getFormData']),
  }
}
</script>

<style scoped>

</style>