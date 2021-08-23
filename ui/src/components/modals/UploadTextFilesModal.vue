<template>

  <div class="modal"  @keydown.esc="isActive" tabindex="0" v-bind:class="{'is-active':isActive}">
    <div class="modal-background"></div>

    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Upload Data</p>
        <button @click="close" class="delete" aria-label="close"></button>
        <!--        <button @click="close" class="modal-close"></button>-->

      </header>

      <section class="modal-card-body">

        <div className="control">
          <label className="label">
            Database
          </label>
          <div className="select">
            <select name="dblist"
                    id="dblist"
                    v-model="dbSelected"
                    @change="onDBChange">
              <option v-for="db in dbList" :key="db">{{db}}</option>
            </select>
          </div>
        </div>

        <!--        <form method="post" action="#" id="" enctype="multipart/form-data">-->
        <div id="files-upload-div" class="file is-info has-name">
          <label class="file-label">
            <input class="file-input" ref="fileloader" type="file" name="resume" multiple>
            <span class="file-cta">
              <span class="file-icon">
                <i class="fas fa-upload"></i>
              </span>
              <span class="file-label">
                train/test/val text files...
              </span>
            </span>
            <span class="file-name" style="overflow: auto;">
              No files selected...
            </span>
          </label>
        </div>
        <!--        </form>-->

      </section>
      <footer class="modal-card-foot">
        <button class="button is-success" @click="onUpload">
          Upload files
        </button>
        <button @click="close" class="button">
          Close
        </button>
      </footer>
    </div>
  </div>
</template>

<script>
import {mapMutations, mapGetters} from "vuex";
import DBServiceAPI from "@/backend/dbservice-api"
import { createToast } from 'mosha-vue-toastify';

export default {
  name: "UploadTextFilesModal",
  props: ['isActive', 'close'],
  data() {
    return {
      dbname: "",
      isTextFile: true,
      dbList: [],
      dbSelected: "",
    }
  },
  mounted() {
    const fileInput = document.querySelector('#files-upload-div input[type=file]');
    fileInput.onchange = () => {
      if (fileInput.files.length === 3) {
        const fileName = document.querySelector('#files-upload-div .file-name');

        // Only three files are showed on the
        console.log(this.isTextFile)

        if (this.getFileextension(fileInput.files[0].name) !== "txt" ||  this.getFileextension(fileInput.files[1].name) !== "txt" ||  this.getFileextension(fileInput.files[2].name) !== "txt") {
          this.isTextFile = false
        }
        console.log(this.isTextFile)

        fileName.textContent = fileInput.files[0].name + " " + fileInput.files[1].name + " " + fileInput.files[2].name;
      }
    }

    DBServiceAPI.get_db_list(this.getConnectionInfo).then((res) => {
          console.log(res)
          this.dbList = res
        }
    )
  },
  computed: {
    ...mapGetters('databaseInfo', ['getConnectionInfo', 'getTableInfo', 'getCurrentRowId'])
  },
  methods: {
    ...mapMutations('databaseInfo', ['setConnectionInfo', 'setTableInfo']),

    getFileextension(fileName) {
      return fileName.slice((Math.max(0, fileName.lastIndexOf(".")) || Infinity) + 1);
    },
    onUpload() {
      console.log(this.isTextFile)

      //https://stackoverflow.com/questions/54519998/upload-multiple-file-with-vue-js-and-axios/54520177
      let formData = new FormData();

      if (!this.isTextFile || this.$refs.fileloader.files.length !== 3) {
        // https://szboynono.github.io/mosha-vue-toastify/
        createToast('Upload Error',
            {
              description: "Please select text files",
              position: 'bottom-right',
              type: 'danger',
              transition: 'slide',
              timeout: 1500
            })
      } else {
        createToast('Upload In Progress...',
            {
              description: "Wait for Success toast",
              position: 'bottom-right',
              type: 'info',
              transition: 'slide',
              timeout: 2000
            })

        for( var i = 0; i < this.$refs.fileloader.files.length; i++ ){
          let file = this.$refs.fileloader.files[i];
          formData.append('files', file);
        }
        var connectionInfo = this.getConnectionInfo
        connectionInfo.dbname = this.dbSelected
        formData.append('connection_info', JSON.stringify(connectionInfo))

        DBServiceAPI.upload_text_files(formData).then(
            (filePaths) => {
              console.log("filePaths", filePaths)
              createToast('Upload Success',
                  {
                    description: "Please select text files",
                    position: 'bottom-right',
                    type: 'info',
                    transition: 'slide',
                    timeout: 1500
                  })

            },
            error => {
              console.log("filePaths error...", error)
              createToast('Upload Error',
                  {
                    description: "Upload Error on server side",
                    position: 'bottom-right',
                    type: 'danger',
                    transition: 'slide',
                    timeout: 1500
                  })
            }
        )
      }
    }
  }
}
</script>

<style scoped>

</style>