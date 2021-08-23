<template>

  <div class="modal"  @keydown.esc="isActive" tabindex="0" v-bind:class="{'is-active':isActive}">
    <div class="modal-background"></div>

    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Register Pytorch MAR Model</p>
        <button @click="close" class="delete" aria-label="close"></button>
        <!--        <button @click="close" class="modal-close"></button>-->

      </header>
      <section class="modal-card-body">
        <form>
          <div class="columns">
            <div class="column is-one-third">
              <label for="host" style="text-align:right" class="label is-large">MinIO Bucket</label>
            </div>
            <div class="column">
              <input id="host" class="input is-medium"  type="text" placeholder="localhost" v-model.lazy="serverInfo.bucket">
            </div>
          </div>

          <div class="columns">
            <div class="column is-one-third">
              <label for="port" style="text-align:right" class="label is-large is-right">Prefix</label>
            </div>
            <div class="column">
              <input id="port" class="input is-medium"  type="text" placeholder="5432" v-model.lazy="serverInfo.prefix">
            </div>
          </div>

          <div class="columns">
            <div class="column is-one-third">
              <label for="user" style="text-align:right" class="label is-large is-right">Initial Worker Counts</label>
            </div>
            <div class="column">
              <input id="user" class="input is-medium"  type="text" placeholder="mozhi" v-model.lazy="serverInfo.initialWorkersCount">
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
import MinIOService from "@/backend/minio-service-api"
import TorchServe from "@/backend/torchserve"
import { createToast } from 'mosha-vue-toastify';

export default {
  name: "DBInfoDialogBox",
  props: ['isActive', 'close'],
  data() {
    return {
      serverInfo: {
        bucket:"mozhi",
        prefix: "/data/model/conll2003v1.mar",
        initialWorkersCount: 1,
      }
    }
  },
  computed: {
    ...mapGetters('minio', ['getConnectionMinIOInfo'])

  },
  methods: {
    ...mapMutations('minio', ['setConnectionMinIOInfo']),
    onSave() {
      console.log(this.getConnectionMinIOInfo)

      MinIOService.set_policy(this.serverInfo.bucket, this.serverInfo.prefix, this.getConnectionMinIOInfo)

      TorchServe.register_model(this.serverInfo.bucket, this.serverInfo.prefix)
          .then(res => {
            // https://szboynono.github.io/mosha-vue-toastify/
            createToast({
                  title: 'Sucess',
                  description: res
                },
                {
                  type: 'info',
                  timeout: 3000,
                  position: 'bottom-right'
                })
          })
          .catch(err => {
                console.log(err)
                // https://szboynono.github.io/mosha-vue-toastify/
                createToast({
                      title: 'Error',
                      description: err
                    },
                    {
                      type: 'danger',
                      timeout: 8000,
                      position: 'bottom-right'
                    })
              }
          )
    }
  }
}
</script>

<style scoped>

</style>