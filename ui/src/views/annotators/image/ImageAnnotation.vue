<template>
  <img alt="mozhi" src="@/assets/mozhi-logo.png" id="my-image">
  <div class="columns is-desktop">
    <!--Sidebar-->
    <div class="column is-one-fifth">
      <div class="file is-centered is-primary has-name is-boxed my-4" style="display: none;">
        <label class="file-label block">
          <input
              ref="imgLoader"
              id="imgLoader"
              class="file-input"
              type="file"
              name="imgLoader"
              v-on:change="handleImage"
          />
          <span class="file-cta">
          <span class="file-icon">
            <font-awesome-icon icon="file-alt" />
          </span>
          <span class="file-label">
            Load Image
          </span>
        </span>
        </label>
      </div>

      <br><br><br><br><br><br><br><br>
      <div class="columns is-multiline is-mobile">
        <div class='column'>
          <button class="button is-info block" v-on:click="onPrevious">Previous Image</button> <br>
        </div>
        <div class='column'>
          <button class="button is-primary block" v-on:click="onNext">Next Image</button> <br>
        </div>
        <div class='column'>
          <button class="button is-success block" v-on:click="onSave">Save</button> <br>
        </div>
      </div>
      <!--      <button class="button is-info block" v-on:click="onLoad">Load Json</button> <br>-->
      <!--      <a class="button is-link" href="https://codebeautify.org/jsonviewer" target="_blank">Online Jsonviewer</a>-->
    </div>
    <!--Sidebar-->

    <!--Right Side-->
    <div class="column">

      <!--Right Pannel-->
      <div class="panel m-4">
        <!--NER TAGS-->
        <div class="panel-heading">
          <div class="field is-grouped is-grouped-multiline">
            <div class="control" v-for="cl in classes" :key="cl.id">
              <div class="tags is-medium has-addons">
                <a
                    class="tag is-medium"
                    :class="{ 'is-link': cl.id === currentClass.id }"
                    @click="setCurrentClass(cl.id)"
                >
                  {{ cl.name }}
                </a>
                <a class="tag is-medium is-delete" @click="removeClass(cl.id)"></a>
              </div>
            </div>

            <p class="control" v-if="showNewClassInput || classes.length === 0">
              <input
                  type="text"
                  class="input is-inline"
                  v-model="newClassName"
                  @keyup="onInputKeyup"
                  placeholder="NER TAG"
              />
              <button class="button is-info is-inline" @click="saveNewClass">
                Add
              </button>
            </p>

            <p class="control">
              <button
                  class="button is-primary"
                  @click="showNewClassInput = true">
                  <span class="icon">
                    <font-awesome-icon class="fa-lg" icon="plus-square" />
                  </span>
              </button>
            </p>

            <p class="control">
              <button id="drawbutton" class="button is-warning" @click="drawb">
                <span>
                  Draw
                </span>
              </button>
            </p>

            <p class="control">
              <button class="button is-success" @click="selectb">
                  <span>
                    Select
                  </span>
              </button>
            </p>

            <p class="control">
              <button id ="delete" v-if="IsDelButton" class="button is-primary is-outlined" @click="deleteb" >
                <span>
                  Delete
                </span>
              </button>
            </p>

            <p>
              <text style="font-size:12px" >
              <span>
               Current mode: {{ mode }}; Image: {{ width }} x {{ height }}
              </span>
              </text>

            </p>

          </div>
        </div>
        <!--NER TAGS-->

        <br>
        <div class="panel-block">
          <div class="columns">
            <!--Image-->
            <div class="box column is-narrow">
              <!--          style="border: 1px solid #2f2c2c;"-->
              <canvas  id="canvas" ref="canvas"   width="640" height="480" style="border:1px solid #000000;">
              </canvas>
            </div>
            <!--Image-->

            <!--OCR Text-->
            <div class="column" style="background-color:transparent;">
              <div class="box">
                <h2 class="block"><b>Preview</b></h2>
                <p style="white-space: pre-line" v-if="ocrText.length > 0"> <span> {{ ocrText }} </span></p>
              </div>
            </div>
            <!--OCR Text-->
          </div>
        </div>
      </div>

    </div>
    <!--Right Pannel-->
  </div>
  <!--Right Side-->

  <!--  </div>-->
</template>

<script>

//https://stackoverflow.com/questions/9417603/fabric-js-free-draw-a-rectangle
//https://stackoverflow.com/questions/39102493/how-to-select-covered-objects-via-mouse-in-fabricjs
//https://stackoverflow.com/questions/10906734/how-to-upload-image-into-html5-canvas
//https://github.com/lf-achyutpkl/image-annotation/blob/master/lib/components/ImageAnnotationEdit.js

// https://michaelnthiessen.com/this-is-undefined
//
import {fabric} from 'fabric';
import {mapGetters, mapMutations, mapState} from "vuex";
import mozhiapi from "@/backend/mozhiapi";

export default {
  name: "ImageAnnotation",
  data: function()  {
    return {
      imageFileName: '',
      imageFile: '',
      text: '',
      canvas: '',
      fabricCanvas:  '',
      origX : 0,
      origY: 0,
      started: false,
      height: 640,
      width: 480,
      isSelectMode: false,
      isRegistered: false,
      IsDelButton: false,
      mode:'draw',
      showNewClassInput: false,
      newClassName: "",
      currentIndex: -1,
      ocrText: "",
      fabricJsonData: "",
      dbDetails : {
        host: "localhost",
        port: "5432",
        db_name: "mozhidb",
        user: "mozhi",
        password: "mozhi"
      },
      dummy1: "",
      dummy2: ""
    }
  },
  beforeCreate() {
    // Flag to get Storage authentication information
    if (!this.$route.params["isInitialized"]) {
      // If landed on this page directly, move to DB details page
      this.$router.push({name: 'ImageHome'}) //TODO is this right way ? to prevent auth info leak?
    }
  },
  watch: {
    newClassName(now, then) {
      if (now != then) {
        this.newClassName = now.toUpperCase();
      }
    },
  },
  mounted() {
    const canvas = this.$refs.canvas;
    this.canvas = canvas
    this.fabricCanvas = new fabric.Canvas(canvas);
    this.fabricCanvas.hoverCursor = 'pointer';
    this.fabricCanvas.stateProperties
    this.registerCallbacks()
    // this.tryCacheOrLoad()
  },
  computed: {
    ...mapState("tokenizerInfo", ["classes", "currentClass"]),
    ...mapState("imageStore", ["dbServerInfo", "experimentName", "storageServer"]),
  },
  methods: {
    ...mapMutations("tokenizerInfo", ["removeClass", "setCurrentClass"]),
    ...mapGetters('imageStore', ['getFileCurrentPrefix', 'getFilesCount']),
    ...mapMutations('imageStore', ['setCurrentIndex', 'setFilePrefixes']),

    registerCallbacks: function() {
      if (!this.isRegistered) {
        // console.info("registerCallbacks")
        this.fabricCanvas.on('mouse:down', e => this.mousedown(e));
        this.fabricCanvas.on('mouse:move',  e => this.mousemove(e));
        this.fabricCanvas.on('mouse:up',  e => this.mouseup(e));
        this.isRegistered = true
      }
    },
    deRegisterCallbacks: function() {
      if (this.isRegistered) {
        // console.info("deRegisterCallbacks")
        this.fabricCanvas.off('mouse:down', e => this.mousedown(e));
        this.fabricCanvas.off('mouse:move',  e => this.mousemove(e));
        this.fabricCanvas.off('mouse:up',  e => this.mouseup(e));
        this.isRegistered = false
      }
    },
    mousedown : function (e){
      if (this.isSelectMode) {
        var curr_rect = this.fabricCanvas.getActiveObject();
        if (curr_rect) {
          curr_rect.set('fill', 'rgb(197,214,248)')
        }
        return;
      }
      // console.info("mousedown")
      var mouse = this.fabricCanvas.getPointer(e);
      this.started = true
      this.origX = mouse.x
      this.origY = mouse.y
      // console.info("mousedown drawing rect")

      var rect = new fabric.Rect({
        // originX: 'left',
        // originY: 'top',
        left: this.origX,
        top: this.origY,
        width: mouse.x-this.origX,
        height: mouse.y-this.origY,
        angle: 0,
        fill: 'rgb(197,214,248)',
        transparentCorners: false,
        hasBorders: true,
        hasControls: false,
      });
      // Add tag name to rect bounding box object
      rect.toObject = (function(toObject) {
        return function() {
          return fabric.util.object.extend(toObject.call(this), {
            ner_tag: this.ner_tag
          });
        };
      })(rect.toObject);
      rect.ner_tag = this.currentClass.name

      // console.log(rect.stateProperties)
      rect.stateProperties = rect.stateProperties.concat("ner_tag")
      // console.log(rect.stateProperties)

      rect.on('selected', this.enableDelButton)
      this.fabricCanvas.renderAll();
      this.fabricCanvas.setActiveObject(rect);
    },
    mousemove: function(e) {
      if (this.isSelectMode) {
        return;
      }
      // console.info("mousemove")
      if(!this.started) {
        return false;
      }
      var mouse = this.fabricCanvas.getPointer(e);
      var rect = this.fabricCanvas.getActiveObject();

      if (this.origX > mouse.x) {
        rect.set({ left: Math.abs(mouse.x) });
      }

      if (this.origY > mouse.y) {
        rect.set({ top: Math.abs(mouse.y) });
      }

      var w = Math.abs(this.origX - mouse.x),
          h = Math.abs(this.origY - mouse.y);
      if (!w || !h) {
        return false;
      }
      rect.stroke = 'red'
      rect.strokeWidth = 1
      rect.fill = 'transparent'
      rect.set('width', w).set('height', h);
      rect.setCoords()
      this.fabricCanvas.renderAll();
    },
    mouseup: function() {
      if (this.isSelectMode) {
        var curr_rect = this.fabricCanvas.getActiveObject();
        if (curr_rect) {
          curr_rect.set('fill', 'transparent')
        }
        return;
      }
      if(this.started) {
        this.started = false;
      }
      var rect = this.fabricCanvas.getActiveObject();
      this.fabricCanvas.add(rect);
      this.fabricCanvas.renderAll();
    },
    saveNewClass() {
      this.$store.commit("tokenizerInfo/addClass", this.newClassName);
      this.showNewClassInput = false;
      this.newClassName = "";
    },
    onInputKeyup(e) {
      if (e.key === "Enter") {
        this.saveNewClass();
      }
    },
    selectb() {
      this.height = this.canvas.height
      this.width = this.canvas.width
      this.mode = 'select'
      // console.info("onselect")
      // http://jsfiddle.net/beewayne/z0qn35Lo/
      // this.fabricCanvas.isDrawingMode = false
      this.isSelectMode = true
      // this.fabricCanvas.selectable = true
      // this.deRegisterCallbacks()
    },
    drawb() {
      this.mode = 'draw'
      this.height = this.canvas.height
      this.width = this.canvas.width
      // console.info("onDraw")
      // this.registerCallbacks()
      this.isSelectMode = false
      // this.fabricCanvas.selection = false
    },
    enableDelButton() {
      this.IsDelButton = true
    },
    // # https://stackoverflow.com/questions/31727049/let-user-delete-a-selected-fabric-js-object
    deleteb() {
      this.mode = 'delete'
      // console.info("onDelete")

      var canvas = this.fabricCanvas
      var activeObject = canvas.getActiveObject()
      if (activeObject) {
        activeObject.set('fill', 'rgb(197,214,248)')
        canvas.renderAll()
        // if (confirm('Are you sure?')) {
        canvas.remove(activeObject);
        // }
        this.IsDelButton = false
      }
    },
    loadFabricJson() {
      // console.log("loadFabricJson")
      // Careful with loading the data, the backend query details
      // i.e storage server authentication needs to be established before loading
      this.fabricCanvas.loadFromJSON(this.fabricJsonData,
          this.fabricCanvas.renderAll.bind(this.fabricCanvas),
          function(o, object) {
            object.stateProperties = object.stateProperties.concat("ner_tag")
            object.toObject = (function(toObject) {
              return function() {
                return fabric.util.object.extend(toObject.call(this), {
                  ner_tag: this.ner_tag
                });
              };
            })(object.toObject);
            object.ner_tag = o['ner_tag']
          });
    },
    tryCacheOrLoad() {
      console.log("tryCacheOrLoad")
      console.log(this.experimentName, this.dbServerInfo, this.storageServer)
      mozhiapi
          .post(process.env.VUE_APP_API_DB_IMAGE_BBOX_GET, {'experiment_name': this.experimentName, 'prefix':this.getFileCurrentPrefix()})
          .then((res) => {
            console.log(res.data['ocr_text'])
            this.ocrText = res.data['ocr_text']
            console.log(this.ocrText)
            this.fabricJsonData = res.data['bbox_json'];
          })
          .catch((err) => alert(err))
          .finally(async () => {
            this.renderWebImage()
          })
    },
    renderWebImage() {
      console.log("renderWebImage")
      this.fabricCanvas.clear()
      // this.canvas.width = 640
      // this.canvas.height = 480
      this.canvas.getContext('2d').clearRect(0, 0, this.canvas.width, this.canvas.height);
      var fabricCanvas = this.fabricCanvas
      var canvas = this.canvas
      const params = new URLSearchParams();
      params.append('bucket', this.storageServer.bucket);
      params.append('file_prefix', this.getFileCurrentPrefix());

      // console.log(this.dummy1)
      // Fetch the annotation data from current prefix and check for annotated data
      if (this.fabricJsonData.length > 0 && this.ocrText.length > 0)
      {
        console.log("Found previous annotated data...")
        console.log(params.toString())

        this.loadFabricJson()
        // Reload the image to resize the canvas accordingly TODO better way?
        new fabric.Image.fromURL(mozhiapi.defaults.baseURL+ process.env.VUE_APP_API_MINIO_GET_IMAGE + '?'+ params.toString(),
            function (img) {
              fabricCanvas.setWidth(img.width)
              fabricCanvas.setHeight(img.height)
              fabricCanvas.setBackgroundImage(img)
              canvas.width = img.width
              canvas.height = img.height
              fabricCanvas.renderAll()
              // console.log("loading done!", img.width, img.height)
            },{});
      }
      else
      {
        console.log("Found no previous annotated data...")
        console.log(params.toString())
        // console.log(this.getFileCurrentPrefix())
        // imgData = "data:" + res.headers["content-type"] + ";base64," + this.utf8_to_b64(res.data).toString('base64')
        new fabric.Image.fromURL(mozhiapi.defaults.baseURL+ process.env.VUE_APP_API_MINIO_GET_IMAGE + '?'+ params.toString(),
            function (img) {
              fabricCanvas.setWidth(img.width)
              fabricCanvas.setHeight(img.height)
              fabricCanvas.setBackgroundImage(img)
              canvas.width = img.width
              canvas.height = img.height
              fabricCanvas.renderAll()
              // console.log("loading done!", img.width, img.height)
            },{}
        );
        mozhiapi.defaults.timeout = 30000;
        mozhiapi
            .get(process.env.VUE_APP_API_MINIO_GET_TEXT, {params: params})
            .then(res => {
              this.ocrText = res["data"]['text']
              // console.info(res);
            })
            .catch((err) => alert(err));

        mozhiapi
            .get(process.env.VUE_APP_API_MINIO_GET_TEXTINFO, {params: params})
            .then(res => {
              // this.ocrText = res["data"]['text']
              console.info(res);
            })
            .catch((err) => alert(err));
      }

    },
    onPrevious(){
      if (this.currentIndex <= 0) {
        alert("You reached the end of the file list")
        return
      }
      this.currentIndex = this.currentIndex-1
      this.setCurrentIndex(this.currentIndex)

      this.tryCacheOrLoad()
    },
    onNext() {
      this.ocrText = ""
      let c = this.getFilesCount()
      if (this.currentIndex >= parseInt(c) - 1) {
        alert("You reached the end of the file list")
        return
      }
      this.currentIndex = this.currentIndex+1
      this.setCurrentIndex(this.currentIndex)

      this.tryCacheOrLoad()
    },
    onSave() {
      // let data = this.fabricCanvas.toObject()["objects"].filter(function(e) {
      //   return e.type != 'image'
      // })

      // Careful with loading the data, the backend query details
      // i.e storage srever authentication needs to be estabilised before loading
      this.fabricJsonData = JSON.stringify(this.fabricCanvas)
      // console.info(JSON.stringify(this.fabricCanvas))
      let bboxdata = {"experiment_name": "receipts",
        "bbox_json" : this.fabricJsonData,
        "prefix": this.getFileCurrentPrefix(),
        "ocr_text": this.ocrText}
      mozhiapi
          .post(process.env.VUE_APP_API_DB_IMAGE_BBOX_GET,
              bboxdata, {timeout: 30000})
          .catch((err) => alert(err))
    },
    //http://jsfiddle.net/influenztial/qy7h5/
    //https://stackoverflow.com/questions/44010057/add-background-image-with-fabric-js
    handleImage() {
      this.fabricCanvas.clear()
      var reader = new FileReader();
      var fabricCanvas = this.fabricCanvas
      var canvas = this.canvas

      reader.onload = function (event){
        var imgObj = new Image();
        // console.log("data",  event.target.result)
        imgObj.src = event.target.result;
        imgObj.onload = function () {
          fabricCanvas.setWidth(imgObj.width)
          fabricCanvas.setHeight(imgObj.height)
          // fabricCanvas = new fabric.Canvas(canvas)
          canvas.width = imgObj.width
          canvas.height = imgObj.height
          fabricCanvas.renderAll();
          var image = new fabric.Image(imgObj);
          var fabImgObj = image.set({
            left: 0,
            top: 0,
            angle: 0,
            padding: 10,
            cornersize:10,
            height:canvas.height,
            width:canvas.width,
          });
          fabImgObj.selectable = false
          fabricCanvas.setBackgroundImage(image)
          fabricCanvas.renderAll();
        }
      }
      reader.readAsDataURL(this.$refs.imgLoader.files[0]);
    }
  }
};
</script>

<style scoped>
#my-image{display:none;}
.canvas-container {
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: scroll;
  /*width: 640px;*/
  /*height: 480px;*/
}
</style>