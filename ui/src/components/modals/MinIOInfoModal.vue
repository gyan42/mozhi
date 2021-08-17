<template>

  <div class="modal"  @keydown.esc="isActive" tabindex="0" v-bind:class="{'is-active':isActive}">
    <div class="modal-background"></div>

    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Admin Connection Info</p>
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
              <input id="host" class="input is-medium"  type="text" placeholder="localhost" v-model.lazy="connectionInfo.host">
            </div>
          </div>

          <div class="columns">
            <div class="column is-one-third">
              <label for="port" style="text-align:right" class="label is-large is-right">Port</label>
            </div>
            <div class="column">
              <input id="port" class="input is-medium"  type="text" placeholder="5432" v-model.lazy="connectionInfo.port">
            </div>
          </div>

          <div class="columns">
            <div class="column is-one-third">
              <label for="user" style="text-align:right" class="label is-large is-right">AccessKey</label>
            </div>
            <div class="column">
              <input id="user" class="input is-medium"  type="text" placeholder="mozhi" v-model.lazy="connectionInfo.accessKey">
            </div>
          </div>

          <div class="columns">
            <div class="column is-one-third">
              <label for="pass" style="text-align:right" class="label is-large is-right">SecretKey</label>
            </div>
            <div class="column">
              <input id="pass" class="input is-medium"  type="text" placeholder="mozhi" v-model.lazy="connectionInfo.secretKey">
            </div>
          </div>

        </form>
      </section>
      <footer class="modal-card-foot">
        <button class="button is-success" @click="onSave">Save changes</button>
        <button @click="close" class="button">Close</button>
      </footer>
    </div>
  </div>

</template>

<script>
import {mapMutations, mapGetters} from "vuex";

export default {
  name: "DBInfoDialogBox",
  props: ['isActive', 'close'],
  data() {
    return {
      connectionInfo: {
        host: process.env.VUE_APP_MINIO_HOST,
        port: process.env.VUE_APP_MINIO_PORT,
        accessKey: process.env.VUE_APP_MINIO_ACCESS_KEY,
        secretKey: process.env.VUE_APP_MINIO_SECRET_KEY,
      }
    }
  },
  computed: {
    ...mapGetters('minio', ['getConnectionMinIOInfo'])

  },
  methods: {
    ...mapMutations('minio', ['setConnectionMinIOInfo']),
    onSave() {
      this.setConnectionMinIOInfo(this.connectionInfo)
    }
  }
}
</script>

<style scoped>

</style>