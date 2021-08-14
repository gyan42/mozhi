<template>

  <div class="modal"  @keydown.esc="isActive" tabindex="0" v-bind:class="{'is-active':isActive}">
    <div class="modal-background"></div>

    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Create New Database</p>
        <button @click="close" class="delete" aria-label="close"></button>
        <!--        <button @click="close" class="modal-close"></button>-->

      </header>
      <section class="modal-card-body">
        <!--        <form>-->
        <div class="columns">
          <div class="column is-one-third">
            <label for="host" style="text-align:right" class="label is-large">
              Name
            </label>
          </div>
          <div class="column">
            <input id="host" class="input is-medium"  type="text" placeholder="test123" v-model.lazy="dbname">
          </div>
        </div>
        <!--        </form>-->

      </section>
      <footer class="modal-card-foot">
        <button class="button is-success" @click="onSave">
          Save changes
        </button>
        <button @click="close" class="button">
          Cancel
        </button>
      </footer>
    </div>
  </div>

</template>

<script>
import {mapMutations, mapGetters} from "vuex";
import DBServiceAPI from "@/backend/dbservice"

export default {
  name: "CreateDBModal",
  props: ['isActive', 'close', 'message'],
  data() {
    return {
      dbname: ""
    }},
  computed: {
    ...mapGetters('databaseInfo', ['getConnectionInfo', 'getTableInfo', 'getCurrentRowId'])
  },
  methods: {
    ...mapMutations('databaseInfo', ['setConnectionInfo', 'setTableInfo']),
    onSave() {
      this.setConnectionInfo(this.dbConnectionInfo)
      DBServiceAPI.create_db(this.getConnectionInfo, this.dbname)
    }
  }
}
</script>

<style scoped>

</style>