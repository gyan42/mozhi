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
  name: "UploadTextFilesModal",
  props: ['isActive', 'close'],
  data() {
    return {
      dbname: ""
    }
  },
  mounted() {
    const fileInput = document.querySelector('#files-upload-div input[type=file]');
    fileInput.onchange = () => {
      if (fileInput.files.length > 2) {
        const fileName = document.querySelector('#files-upload-div .file-name');
        // Only three files are showed on the UI
        fileName.textContent = fileInput.files[0].name + " " + fileInput.files[1].name + " " + fileInput.files[2].name;
      }
    }
  },
  computed: {
    ...mapGetters('databaseInfo', ['getConnectionInfo', 'getTableInfo', 'getCurrentRowId'])
  },
  methods: {
    ...mapMutations('databaseInfo', ['setConnectionInfo', 'setTableInfo']),
    onUpload() {
      //https://stackoverflow.com/questions/54519998/upload-multiple-file-with-vue-js-and-axios/54520177
      let formData = new FormData();

      for( var i = 0; i < this.$refs.fileloader.files.length; i++ ){
        let file = this.$refs.fileloader.files[i];
        formData.append('files', file);
      }
      formData.append('connection_info', JSON.stringify(this.getConnectionInfo))

      DBServiceAPI.upload_text_files(formData).then(
          (filePaths) => {
             console.log("filePaths", filePaths)
          },
          error => {console.log("filePaths error", error)}
      )

    }

  }
}
</script>

<style scoped>

</style>