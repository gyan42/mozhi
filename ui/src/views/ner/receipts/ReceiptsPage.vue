<template>
  <page-header>
    <h1 class="title">Receipts Auto Form Filling</h1>
  </page-header> 

   Note: Results are displayed as it is, no post processing applied!
   <br><br>


  <div class="columns">
    <div class="column">
        <!--Image-->
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
                  v-on:change="onImageUpload"
              />
              <span class="file-cta mr-5" style="text-align:center">
                <span class="file-icon" style="text-align:center">
                  <font-awesome-icon icon="file-alt" />
                </span>
                <span class="file-label" style="text-align:center">
                  Load Image
                </span>
              </span>
            </label>

            <button class="button is-link ml-5" v-on:click="onImageSample" > Sample a Test Image </button>

          </div>
        </div>
      </section>

      <div class="box" style="background-color:transparent;">
        <p v-if="imageFile.length > 0"> <img v-bind:src="imageFile" /></p>
      </div>
      <!--Image-->
    </div>

    <div class="column">
      <ul style="list-style-type:none;">
        <div class="field is-horizontal">
          <label class="label mr-5">Available Dataset Models</label>
          <div class="select is-primary">
            <select  name="torchmodel"
                        id="torchmodel"
                        v-model="selectedTorchModel">
              <option v-for="torchModel in torchAvailableModels" :key="torchModel.modelUrl">
                {{torchModel.modelName}}
              </option>
            </select>
          </div>
        </div>

        <br>
        <h2 class="block has-text-danger">{{status}}</h2>
        <br>

        <li v-for="prediction in predictions" :key="prediction.id">
          <div class="field is-horizontal">
            <div class="field-label is-normal">
              <label class="label">{{prediction.tag}}</label>
            </div>
            <div class="field-body mr-5">
              <div class="field">
                <div class="control">
                  <input class="input" type="text" v-model=prediction.token>
                </div>
              </div>
            </div>
          </div>
          <br>
        </li>
      </ul>

        <br><br><br>
        <h2 class="block has-text-info">Total Processing time: {{timeElapsed / 1000}} seconds</h2>
        <h2 class="block has-text-info">OCR Processing time: {{ocrTimeElapsed / 1000}} seconds</h2>
        <h2 class="block has-text-info">Model Processing time: {{modelTimeElapsed / 1000}} seconds</h2>
        <br>

    </div>
  </div>

</template>>

<script>
import PageHeader from "@/components/PageHeader"
import mozhiapi from "@/backend/mozhiapi";
import torchserveapi from "@/backend/torchserveapi"

export default {
  name: "ReceiptsAutoFormFilling",
  data() {
      return {
        imageFileName: '',
        imageFile: '',
        predictions: [
          {id: 1, tag: "TAG1", token: "TOKEN1"}, 
          {id:2, tag: "TAG2", token: "TOKEN2"}
        ],
        torchAvailableModels: {},
        selectedTorchModel: 'sroie2019v1',
        status: "No Image Loaded",
        startTime: 0,
        timeElapsed: 0,
        ocrStartTime: 0,
        ocrTimeElapsed: 0,
        modelStartTime: 0,
        modelTimeElapsed: 0
      }
  },
  components: {
      PageHeader
  },
  computed: {

  },
  created() {
    torchserveapi.managementAPI.get("/models").then(value => {
      console.info(value["data"]["models"])
      this.torchAvailableModels = value["data"]["models"]
    })
  },
  methods: {
    async onRunOCR() {
      this.status = "Running Tesseract"
      this.ocrStartTime = performance.now()
      console.info("Running Tesseract")
      console.info(process.env.VUE_APP_API_BASE_URL,  process.env.VUE_APP_API_OCR_TESSERACT)
      let formData = new FormData();
      formData.append('file', this.imageFileName);
      console.info(this.imageFileName)
      console.info(formData)
      let headers =   {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        timeout: 30000
      }

      mozhiapi
          .post(process.env.VUE_APP_API_OCR_TESSERACT, formData, headers)
          .then(res => {
            console.info(res);
            this.inTextData = res["data"]['text']
            this.ocrTimeElapsed = performance.now() - this.ocrStartTime
            this.predict()
          })
          .catch((err) => alert(err));
      // if (event) {
      //   console(event.target.tagName)
      // }
    },
    extractTags(predictions) {
      // preditions = [(TOKEN1: TAG1), (TOKEN2: TAG2), ...]

      // create a default dict object
      let handler = {
        get: function(target, name) {
          return name in target ? target[name] : "";
          }
      };
      let emptyObj = {};
      let p = new Proxy(emptyObj, handler);

      // Iterate through prediction tuple list and concatenate tokens for same tag
      for (var i=0; i<predictions.length; i++) {
        var token = predictions[i][0]
        var tag = predictions[i][1]
        p[tag] = p[tag] + " " + token
      }

      // Create list of object to populate lists 
      var data = []
      var j = 0
      for (let key in p) {
        if (key != 'O') {
          data.push({id: j, tag: key, token: p[key].replaceAll('[SEP]', '').replaceAll(' ##', '').replace(' #', '').replace('#', '')})
        }
        j = j + 1
      }
      this.predictions = data
      console.log(data)
      this.status = ""
      this.modelTimeElapsed = performance.now() - this.modelStartTime
      this.timeElapsed = performance.now() - this.startTime
    },
    predict(){
      this.status = "Running Transformer Model"
      this.modelStartTime = performance.now()
      torchserveapi.predictionAPI.post("predictions/" + this.selectedTorchModel, {"text": this.inTextData}, {timeout: 20000})
          .then(value => {
            console.info(value["data"])
            this.extractTags(value["data"])
          })
    },
    onImageUpload() {
      console.info("onImageUpload")
      this.startTime = performance.now()
      this.timeElapsed = 0
      this.modelTimeElapsed = 0
      this.ocrTimeElapsed = 0
      
      this.predictions = []
      this.imageFileName = this.$refs.imgLoader.files[0]
      console.info(this.imageFileName )
      this.createImage(this.imageFileName);
      var reader = new FileReader();
      reader.readAsDataURL(this.imageFileName);
      this.onRunOCR()
    },
    onImageSample() {

      console.info("onImageSample")
      this.startTime = performance.now()
      this.timeElapsed = 0
      this.modelTimeElapsed = 0
      this.ocrTimeElapsed = 0

      this.predictions = []

      // Number of test iamges are 138!
      const rndInt = Math.floor(Math.random() * 138) + 1
      console.log(rndInt)

      const blobUrlToFile = (blobUrl)  => new Promise((resolve) => {
          fetch(blobUrl).then((res) => {
            res.blob().then((blob) => {
            const fileName = blobUrl.split("/")[2]
            console.info(fileName)
            const file = new File([blob], fileName, {type: blob.type})
            resolve(file)
            })
          })
       })

      blobUrlToFile(require("@/assets/images/test/"+rndInt+".jpg")).then( f => {
          this.imageFileName = f
          console.info(this.imageFileName )
          this.createImage(this.imageFileName);
          this.onRunOCR()
        }
      )
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

</style>
