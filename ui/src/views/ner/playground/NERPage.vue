<template>
  <page-header>
    <h1 class="title">NER Playground</h1>
  </page-header>
  <div class="columns is-desktop">
    <!--Sidebar-->
    <div class="column is-one-fifth">
      <NERSidebar v-bind:models="availableModels"/>
    </div>
    <!--Sidebar-->

    <!--Right Side-->
    <div class="column">

      <!--Right Pannel-->
      <div class="panel m-4">
        <p v-if="dataSetName ==='plainText'" class="block subtitle is-4">Paste your text below</p>
        <textarea class="block" v-if="dataSetName ==='plainText'"
                  id="textAreaInput"
                  name="textAreaInput"
                  rows="2"
                  cols="100"
                  v-model="inTextData">
        </textarea>

        <!--NER TAGS-->
        <div class="panel-heading">
          <NERTagsBlock v-bind:classes="classes" v-bind:classColorMap="classColorMap"/>
        </div>
        <!--NER TAGS-->

        <!--Text-->
        <div class="panel-block">
          <div id="editor">
            <component
                :is="p.type === 'ner' ? 'EntityBlock' : 'Token'"
                :id="'p' + p.start"
                v-for="p in predictions"
                v-bind:token="p"
                v-bind:classColorMap="classColorMap"
                v-bind:key="p.start"
            />
          </div>
        </div>
        <!--Text-->

        <!--Buttons-->
        <div class="panel-block">
          <div class="field is-grouped">
            <p class="control">
              <button class="button is-link" @click="onPredict">Predict</button>
            </p>
          </div>
        </div>
        <!--Buttons-->

        <!--Image-->
        <section v-if="dataSetName ==='image'" class="hero block">
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

        <div v-if="dataSetName ==='image'" class="box" style="background-color:transparent;">
          <h2 class="block"><b>Uploaded Image</b></h2>
          <p v-if="imageFile.length > 0"> <img v-bind:src="imageFile" /></p>
        </div>
        <!--Image-->
      </div>
      <!--Right Pannel-->
    </div>
    <!--Right Side-->

  </div>
</template>

<script>
import NERSidebar from "@/views/ner/playground/NERSidebar";
import Token from "./Token";
import EntityBlock from "./EntityBlock";
import NERTagsBlock from "@/views/ner/playground/NERTagsBlock";
import {mapGetters, mapMutations, mapState} from "vuex";
import mozhiapi from "@/backend/mozhiapi";
import torchserveapi from "@/backend/torchserveapi"
import PageHeader from "@/components/PageHeader"


export default {
  name: "NERPredictor",
  data: function() {
    return {
      inTextData: "",
      classColorMap: {},
      imageFileName: '',
      imageFile: '',
      availableModels: [{name: "spacy", type: "inbuild", value: "spacy"}] //{name: "bertv1", type:"HF-Torch", value: "bertv1"}
    };
  },
  components : {
    NERSidebar,
    Token,
    EntityBlock,
    NERTagsBlock,
    PageHeader
  },
  computed: {
    ...mapState('nerModelPredictions', ['dataSetName', 'modelName', 'predictions', 'classes'])
  },
  created() {
    torchserveapi.managementAPI.get("/models").then(value => {

      let models = value["data"]["models"]
      models.forEach(model => {
        console.info(model)
        this.availableModels.push({name: model.modelName, type: "HF-Torch", value: model.modelName})
      })
      console.info("Done getting available models from Torch Server")
    })

  },
  beforeUnmount() {

  },
  methods : {
    ...mapGetters('nerModelPredictions', ['getClasses', 'getPredictions']),
    ...mapMutations('nerModelPredictions', ['setClasses', 'setPredictions']),

    getRandomColor() {
      var letters = '0123456789ABCDEF'.split('');
      var color = '#';
      for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * letters.length)];
      }
      return color;
    },
    extractClasses() {
      let classes = new Set();
      // let cls_id = 0
      for(const item of this.predictions) {
        if (item.label.length > 0) {
          classes.add(item.label)
          // cls_id += 1
          this.classColorMap[item.label] = this.getRandomColor()
        }
      }
      console.info("extractClasses", classes)
      this.setClasses(classes)
    },
    spacy() {
      let api = process.env.VUE_APP_API_NER_SPACY //+ this.modelName
      console.info("full url", mozhiapi.defaults.baseURL)
      console.info("api", api)

      mozhiapi
          .post(api, {text: this.inTextData})
          .then((res) => {
            this.setPredictions(Object.values(res.data['predictions']))
            this.extractClasses()
            console.info("classes", this.classes)
          })
          .catch((err) => alert(err));
    },
    // eslint-disable-next-line no-unused-vars
    predictionMapper(value, index, array) {
      // console.info(value, index, array)
      let type = ''
      if (value[1] === 'O')
        type = 'O'
      else
        type = 'ner'
      return {"text" : value[0], "label": value[1], "type": type}
    },
    transfomers() {
      let data = "test"
      // let text = "Hugging Face Inc. is a company based in New York City. Its headquarters are in DUMBO, therefore very close to the Manhattan Bridge."

      // Selection drop menu has both the name and type separated by space, extract the name alone
      torchserveapi.predictionAPI.post("predictions/"+this.modelName.split(" ")[0], {"text": this.inTextData}, {timeout: 5000})
          .then(value => {
            console.info(value["data"])
            data = value["data"]
            data = data.map(this.predictionMapper)
            // console.info(data)
            this.setPredictions(data)
            this.extractClasses()
          })
    },
    onPredict() {
      if (this.modelName.includes('spacy')) {
        this.spacy()
      }
      if (this.modelName.includes('HF-Torch')) {
        this.transfomers()
      }
    },
    async onRunOCR() {
      console.info("Running Tesseract")
      let formData = new FormData();
      formData.append('file', this.imageFileName);
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
            this.inTextData = res["data"]['text']
            console.info(res);
          })
          .catch((err) => alert(err));
      // if (event) {
      //   console(event.target.tagName)
      // }
    },
    onImageUpload() {
      console.info("onImageUpload")
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

<style lang="scss">
#editor {
  padding: 0.5rem;
}
</style>