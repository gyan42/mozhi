<template>
  <div class ="block">
    <section class="hero is-dark">
      <div class="hero-body">
        <div class="container">
          <h1 class="title">DataBase Annotator</h1>
          <h2 class="subtitle">Database Connection Information</h2>
        </div>
      </div>
    </section>
    <br>
    <form>
      <div class="columns is-3">
        <div class="column">
          <label for="host" style="text-align:right" class="label is-large">Host</label>
        </div>
        <div class="column control">
          <input id="host" class="input is-medium"  type="text" placeholder="localhost" v-model.lazy="formData.host">
        </div>
        <!--        Dummy column for center alignment-->
        <div class="column control">
        </div>
      </div>

      <div class="columns is-mobile">
        <div class="column">
          <label for="port" style="text-align:right" class="label is-large is-right">Port</label>
        </div>
        <div class="column control">
          <input id="port" class="input is-medium"  type="text" placeholder="5432" v-model.lazy="formData.port">
        </div>
        <div class="column control">
        </div>
      </div>

      <div class="columns is-mobile">
        <div class="column">
          <label for="user" style="text-align:right" class="label is-large is-right">User</label>
        </div>
        <div class="column control">
          <input id="user" class="input is-medium"  type="text" placeholder="mozhi" v-model.lazy="formData.user">
        </div>
        <div class="column control">
        </div>
      </div>

      <div class="columns is-mobile">
        <div class="column">
          <label for="pass" style="text-align:right" class="label is-large is-right">Password</label>
        </div>
        <div class="column control">
          <input id="pass" class="input is-medium"  type="text" placeholder="mozhi" v-model.lazy="formData.password">
        </div>
        <div class="column control">
        </div>
      </div>

      <div class="columns is-mobile">
        <div class="column">
          <label for="dbname" style="text-align:right" class="label is-large is-right">Database Name</label>
        </div>
        <div class="column control">
          <input id="dbname" class="input is-medium"  type="text" placeholder="mozhidb" v-model.lazy="formData.db_name">
        </div>
        <div class="column control">
        </div>
      </div>

      <div class="columns is-mobile">
        <div class="column">
          <label for="txttblname" style="text-align:right" class="label is-large is-right">Text Table Name</label>
        </div>
        <div class="column control">
          <input id="txttblname" class="input is-medium"  type="text" placeholder="conll2003_train" v-model.lazy="formData.text_table_name">
        </div>
        <div class="column control">
        </div>
      </div>

      <div class="columns is-mobile">
        <div class="column">
          <label for="tagtblname" style="text-align:right" class="label is-large is-right">Tag Table Name</label>
        </div>
        <div class="column control">
          <input id="tagtblname" class="input is-medium"  type="text" placeholder="conll2003_train_tags" v-model.lazy="formData.tag_table_name">
        </div>
        <div class="column control">
        </div>
      </div>

      <div class="columns is-mobile">
        <div class="column">
          <label for="startid" style="text-align:right" class="label is-large is-right">Start ID</label>
        </div>
        <div class="column control">
          <input id="startid" class="input is-medium"  type="text" placeholder="0" v-model.lazy="formData.start_id">
        </div>
        <div class="column control">
        </div>
      </div>


      <div class="columns is-mobile">
        <div class="column">
          <label for="incolname" style="text-align:right" class="label is-large is-right">Input Column Name</label>
        </div>
        <div class="column control">
          <input id="incolname" class="input is-medium"  type="text" placeholder="text" v-model.lazy="formData.text_col_name">
        </div>
        <div class="column control">
        </div>
      </div>
    </form>

    <br>
    <div class="control">
      <button class="button is-primary" @click="onSubmit" >Submit</button>
    </div>
    <br>
  </div>
</template>

<script>
import {mapMutations, mapGetters} from "vuex";
import axios from "../../../axios";

export default {
  name: "DBDetailsPage",
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
        db_name: process.env.VUE_APP_DB_NAME,
        text_table_name: process.env.VUE_APP_DB_TEXT_TABLE_NAME,
        tag_table_name: process.env.VUE_APP_DB_TAG_TABLE_NAME,
        text_col_name: process.env.VUE_APP_DB_TABLE_INPUT_COL_NAME,
        features_col_name: 'features',
        labels_col_name: 'lables',
        start_id: process.env.VUE_APP_DB_TABLE_START_ID
      }
    }
  },
  created() {
    // this.formData.host =
  },
  methods: {
    ...mapMutations('databaseInfo', ['setFormData', 'setCurrentText', 'setCurrentRowId', 'setTotalCounts']),
    ...mapGetters('databaseInfo', ['getFormData']),
    ...mapMutations('tokenizerInfo', ['addClass']),

    async onSubmit() {
      this.$store.commit("tokenizerInfo/resetClass", []);
      console.info(this.formData)
      let headers =   {
        timeout: 50000
      }

      // Get the total rows count from backend to update progress bar
      let totalRows = 0
      axios
          .post("/vf/db/text/get/counts", this.formData, headers)
          .then((res) => {
            console.log(res)
            totalRows = parseInt(res.data["count"])
          })
          .catch((err) => alert(err))
          .finally(() => {
            this.setTotalCounts(totalRows);
          })

      // Get all tags to setup the NER labels
      let tags = []
      axios
          .post("vf/db/text/get/tags", this.formData, headers)
          .then((res) => {
            console.log(res)
            tags = res.data["tags"]
          })
          .catch((err) => alert(err))
          .finally(() => {
            tags.forEach((t) => {
              // console.log(t)
              // self.addClass(t)
              if (t !== 'O') {
                this.$store.commit("tokenizerInfo/addClass", t);
              }

            })
          })

      let data = ""
      axios
          .post("/vf/db/text/table/" + this.formData.start_id, this.formData, headers)
          .then((res) => {
            console.log("get features", res)
            data = res.data["features"]
          })
          .catch((err) => alert(err))
          .finally(()=> {this.setCurrentText(data);});

      this.setFormData(this.formData)
      this.setCurrentRowId(parseInt(this.formData.start_id))

      // route: '/annotator/db'
      setTimeout(() => {
        this.$router.push({name: 'DBAnnotatorPage', params: {isInitialized: true}});
      } , 500);
    }
  }
}
</script>

<style scoped>

</style>