<template>
  <div>
    <section class="hero is-dark">
      <div class="hero-body">
        <div class="container">
          <h1 class="title">Image NER Annotator</h1>
          <h2 class="subtitle">Object Store and Database Connection Information</h2>
        </div>
      </div>
    </section>

    <br>

    <form>

      <div class="columns is-3">
        <div class="column">
          <label for="expname" style="text-align:right" class="label is-large">Experiment Name</label>
        </div>
        <div class="column control">
          <input id="expname" class="input is-medium"  type="text" placeholder="receipts" v-model.lazy="experimentName">
        </div>
        <!--        Dummy column for center alignment-->
        <div class="column control">
        </div>
      </div>


      <div class="columns is-3">
        <div class="column">
          <label for="host" style="text-align:right" class="label is-large">Host</label>
        </div>
        <div class="column control">
          <input id="host" class="input is-medium"  type="text" placeholder="localhost" v-model.lazy="storageServer.host">
        </div>
        <!--        Dummy column for center alignment-->
        <div class="column control">
        </div>
      </div>

      <div class="columns is-3">
        <div class="column">
          <label for="port" style="text-align:right" class="label is-large">Port</label>
        </div>
        <div class="column control">
          <input id="port" class="input is-medium"  type="text" placeholder="9000" v-model.lazy="storageServer.port">
        </div>
        <!--        Dummy column for center alignment-->
        <div class="column control">
        </div>
      </div>

      <div class="columns is-3">
        <div class="column">
          <label for="sc" style="text-align:right" class="label is-large">Storage Class</label>
        </div>
        <div class="column control">
          <!--          <input id="host" class="input is-medium"  type="text" placeholder="localhost" v-model.lazy="storageServer.storageClass">-->
          <select  id="sc" class="input is-medium" v-model.lazy="storageServer.storageClass">
            <option value="minio">MinIO</option>
          </select>
        </div>
        <!--        Dummy column for center alignment-->
        <div class="column control">
        </div>
      </div>

      <div class="columns is-mobile">
        <div class="column">
          <label for="acceskey" style="text-align:right" class="label is-large is-right">Access Key</label>
        </div>
        <div class="column control">
          <input id="acceskey" class="input is-medium"  type="text" placeholder="5432" v-model.lazy="storageServer.accessKey">
        </div>
        <div class="column control">
        </div>
      </div>

      <div class="columns is-mobile">
        <div class="column">
          <label for="secretkey" style="text-align:right" class="label is-large is-right">Secret Key</label>
        </div>
        <div class="column control">
          <input id="secretkey" class="input is-medium"  type="text" placeholder="5432" v-model.lazy="storageServer.secretKey">
        </div>
        <div class="column control">
        </div>
      </div>

      <div class="columns is-mobile">
        <div class="column">
          <label for="bucket" style="text-align:right" class="label is-large is-right">Bucket</label>
        </div>
        <div class="column control">
          <input id="bucket" class="input is-medium"  type="text" placeholder="5432" v-model.lazy="storageServer.bucket">
        </div>
        <div class="column control">
        </div>
      </div>

      <div class="columns is-mobile">
        <div class="column">
          <label for="prefix" style="text-align:right" class="label is-large is-right">Prefix</label>
        </div>
        <div class="column control">
          <input id="prefix" class="input is-medium"  type="text" placeholder="5432" v-model.lazy="storageServer.prefix">
        </div>
        <div class="column control">
        </div>
      </div>

      <div class="columns is-3">
        <div class="column">
          <label for="ocrengine" style="text-align:right" class="label is-large">OCR Engine</label>
        </div>
        <div class="column control">
          <select  id="ocrengine" class="input is-medium" v-model.lazy="storageServer.ocrEngine">
            <option value="tesseact">Tesseract</option>
          </select>
        </div>
        <!--        Dummy column for center alignment-->
        <div class="column control">
        </div>
      </div>
    </form>

    <br>
    <br>
    <!--    ------------------------------------------------------------------  -->
    <div class="columns is-3">
      <div class="column">
        <label for="dbhost" style="text-align:right" class="label is-large">DB Host</label>
      </div>
      <div class="column control">
        <input id="dbhost" class="input is-medium"  type="text" placeholder="localhost" v-model.lazy="dbServerInfo.host">
      </div>
      <!--        Dummy column for center alignment-->
      <div class="column control">
      </div>
    </div>

    <div class="columns is-mobile">
      <div class="column">
        <label for="dbport" style="text-align:right" class="label is-large is-right">DB Port</label>
      </div>
      <div class="column control">
        <input id="dbport" class="input is-medium"  type="text" placeholder="5432" v-model.lazy="dbServerInfo.port">
      </div>
      <div class="column control">
      </div>
    </div>

    <div class="columns is-mobile">
      <div class="column">
        <label for="user" style="text-align:right" class="label is-large is-right">User</label>
      </div>
      <div class="column control">
        <input id="user" class="input is-medium"  type="text" placeholder="mozhi" v-model.lazy="dbServerInfo.user">
      </div>
      <div class="column control">
      </div>
    </div>

    <div class="columns is-mobile">
      <div class="column">
        <label for="pass" style="text-align:right" class="label is-large is-right">Password</label>
      </div>
      <div class="column control">
        <input id="pass" class="input is-medium"  type="text" placeholder="mozhi" v-model.lazy="dbServerInfo.password">
      </div>
      <div class="column control">
      </div>
    </div>

    <div class="columns is-mobile">
      <div class="column">
        <label for="dbname" style="text-align:right" class="label is-large is-right">Database Name</label>
      </div>
      <div class="column control">
        <input id="dbname" class="input is-medium"  type="text" placeholder="mozhidb" v-model.lazy="dbServerInfo.db_name">
      </div>
      <div class="column control">
      </div>
    </div>
    <br>
    <div class="control">
      <button class="button is-primary" @click="onSubmit" >Submit</button>
    </div>
    <br>

  </div>
</template>

<script>
import axios from "../../../axios";
import {mapMutations, mapGetters, mapState} from "vuex";

export default {
  name: "ImageHome",
  data() {
    return {
      experimentName: "receipts",
      storageServer: {
        host: process.env.VUE_APP_MINIO_HOST,
        port: process.env.VUE_APP_MINIO_PORT,
        storageClass: "minio",
        accessKey: process.env.VUE_APP_MINIO_ACCESS_KEY,
        secretKey: process.env.VUE_APP_MINIO_SECRET_KEY,
        bucket: process.env.VUE_APP_MINIO_BUCKET,
        prefix: process.env.VUE_APP_MINIO_PREFIX,
        ocrEngine: "tesseact",
      },
      dbServerInfo : {
        host: process.env.VUE_APP_DB_HOST,
        port: process.env.VUE_APP_DB_PORT,
        db_name: process.env.VUE_APP_DB_NAME,
        user: process.env.VUE_APP_DB_USER,
        password: process.env.VUE_APP_DB_PASSWORD,
      }
    }
  },
  computed: {
    ...mapState("imageStore", ["dbServerInfo", "experimentName", "storageServer"]),
  },
  methods: {
    ...mapGetters('imageStore', ['getFileCurrentPrefix', 'getFilesCount']),
    ...mapMutations('imageStore', ['setCurrentIndex', 'setFilePrefixes']),
    ...mapMutations("tokenizerInfo", ["resetClass"]),

    onSubmit() {
      console.info(this.storageServer)
      this.resetClass()
      let headers =   {
        timeout: 50000
      }

      // Get the total rows count from backend to update progress bar
      let files = ''
      axios
          .post("/vf/storage/minio/list", this.storageServer, headers)
          .then((res) => {
            console.log(res)
            files = res.data
          })
          .catch((err) => alert(err))
          .finally(() => {
            console.log("res")
            // this.setTotalCounts(totalRows);
            this.setFilePrefixes(files)
          })

      // Create the imag table to hold image annotations
      axios
          .post("/vf/db/image/create", {"db_server": this.dbServerInfo, "experiment_name": this.experimentName}, headers)
          .then((res) => {
            console.log(res)
          })
          .catch((err) => alert(err))
          .finally(() => {
            console.log("finally: image annotation table created successfully!")
          })


      // route: '/annotator/imagefile'
      setTimeout(() => {
        this.$router.push({name: 'ImageAnnotation', params: {isInitialized: true}});
      } , 500);
    }
  },
}
</script>