<template>
  <div class="home">
    <page-header>
      <h1 class="title">Tesseract OCR</h1>
    </page-header>

    <section class="hero block">
      <div style="text-align: center;">
        <div class="file is-centered is-primary has-name">
          <label class="file-label">
            <input
                ref="imgLoader"
                id="imgLoader"
                class="file-input"
                type="file"
                name="imgLoader"
                v-on:change="onFileChange"
            />
            <span class="file-cta" style="text-align:center">
          <span class="file-icon" style="text-align:center">
            <font-awesome-icon icon="file-alt" />
          </span>
          <span class="file-label" style="text-align:center">
            Load Image
          </span>
        </span>
          </label>
        </div>
      </div>
    </section>

    <div class="row">
      <div class="box column" style="background-color:transparent;">
        <h2 class="block"><b>Uploaded Image</b></h2>
        <p v-if="imageFile.length > 0"> <img v-bind:src="imageFile" /></p>
      </div>
      <div class="box column" style="background-color:transparent;">
        <h2 class="block"><b>Text</b></h2>
        <p style="white-space: pre-line" v-if="text.length > 0"> <span> {{ text }} </span></p>
      </div>
    </div>

  </div>
</template>

<script>
import MozhiApi from "@/backend/mozhiapi";
import PageHeader from "@/components/PageHeader"

export default {
  components: {PageHeader},
  data()  {
    return {
      imageFileName: '',
      imageFile: '',
      text: ''
    }
  },
  methods: {
    async onRunOCR() {
      console.info("Running Tesseract")
      let formData = new FormData();
      formData.append('file', this.imageFileName);
      console.info("tesseract formData", formData)
      let headers =   {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        timeout: 5000
      }
      MozhiApi
          .post(process.env.VUE_APP_API_OCR_TESSERACT, formData, headers)
          .then(res => {
            this.text = res["data"]['text']
            console.info(res);
          })
          .catch((err) => alert(err));
      // if (event) {
      //   console(event.target.tagName)
      // }
    },
    onFileChange() {
      this.text = ''
      console.info("onFileChange")
      this.imageFileName = this.$refs.imgLoader.files[0]
      this.createImage(this.imageFileName);
      this.onRunOCR()
    },
    createImage(file) {
      var reader = new FileReader();
      reader.onload = (e) => {
        this.imageFile = e.target.result;
      };
      reader.readAsDataURL(file);
    },
  }
}
</script>

<style>
/* Create two equal columns that floats next to each other */
.column {
  float: left;
  width: 50%;
  padding: 10px;
  /*height: 300px; !* Should be removed. Only for demonstration *!*/
}

/* Clear floats after the columns */
.row:after {
  content: "";
  display: table;
  clear: both;
}
</style>