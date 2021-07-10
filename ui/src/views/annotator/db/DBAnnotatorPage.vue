`<template>
  <div class ="block">
    <section class="hero is-dark">
      <div class="hero-body">
        <div class="container">
          <h1 class="title">DataBase Annotator</h1>
          <h2 class="subtitle">Annotate Table Data for Model training</h2>
        </div>
      </div>
    </section>
    <div class="columns is-desktop">
      <!--Sidebar-->
      <div class="column is-one-fifth">
        <DBAnnotationSidebar :currentId="currentId"/>
      </div>
      <!--Sidebar-->

      <!--Right Side-->
      <div class="column">

        <!--Right Pannel-->
        <div class="panel m-4">
          <!--NER TAGS-->
          <div class="panel-heading">
            <classes-block v-bind:classColorMap="classColorMap" />
          </div>
          <!--NER TAGS-->

          <!--Text-->
          <div class="panel-block">
            <div id="editor">
              <component
                  :is="t.type === 'token' || t.label === 'O' ? 'Token' : 'TokenBlock'"
                  :id="'t' + t.start"
                  v-for="t in tm.tokens"
                  :token="t"
                  :key="t.start"
                  v-bind:classColorMap="classColorMap"
                  @remove-block="onRemoveBlock"
              />
            </div>
          </div>
          <!--Text-->

          <!--Buttons-->
          <div class="panel-block">
            <div class="field is-grouped">
              <p class="control">
                <button class="button is-danger is-outlined" @click="resetBlocks">
                  Reset
                </button>
              </p>
              <p class="control">
                <button class="button" @click="changeColor">Tag Color</button>
              </p>
              <p class="control">
                <button class="button" @click="skipCurrentSentence">Skip</button>
              </p>
              <p class="control">
                <button class="button is-link" @click="previous">Previous</button>
              </p>
              <p class="control">
                <button class="button is-primary" @click="saveTags">Save</button>
              </p>
              <p class="control">
                <button class="button" @click="nextRow">Next</button>
              </p>
            </div>
          </div>
          <!--Buttons-->
        </div>
        <!--Right Pannel-->
      </div>
      <!--Right Side-->
    </div>

    <p>Note: Always select from left. Tag "O" is ignored from highlighting</p>
    <br>
    <p>Your text column start ID is {{ formData.start_id }} and current ID is {{ currentId }}</p>
    <br><br><br><br>

  </div>
</template>

<script>
import DBAnnotationSidebar from "@/views/annotator/db/DBAnnotationSidebar";
import Token from "../../../components/Token";
import TokenBlock from "../../../components/TokenBlock";
import ClassesBlock from "../../../components/ClassesBlock.vue";
import TokenManager from "../../../components/token-manager";
import {mapMutations, mapState, mapGetters} from "vuex";
import axios from "../../../axios";

export default {
  name: "DBAnnotator",
  components : {
    DBAnnotationSidebar,
    Token,
    TokenBlock,
    ClassesBlock,
  },
  data: function() {
    return {
      tm: new TokenManager([]),
      annotatedTokens: null,
      classColorMap: {},
    };
  },
  computed: {
    ...mapState("databaseInfo", ["currentText", "currentAnnotations", "formData", "totalRows", 'currentId']),
    ...mapState("tokenizerInfo", ["inputSentences", "classes", "annotations", "currentClass"]),
  },
  beforeCreate() {
    if (!this.$route.params["isInitialized"]) {
      // If landed on this page directly, move to DB details page
      this.$router.push({name: 'DBDetailsHomePage'}) //TODO is this right way ? to prevent stale data?
    }

  },
  created() {
    this.getInputText()
    // console.log("created:")
    // console.log(this.currentText)
    document.addEventListener("mouseup", this.selectTokens);

    this.changeColor()
  },
  beforeUnmount() {
    document.removeEventListener("mouseup", this.selectTokens);
  },
  methods : {
    ...mapGetters('databaseInfo', ['getFormData']),
    ...mapMutations('databaseInfo', ['setFormData', 'setCurrentText', 'setTotalCounts', 'setCurrentRowId']),

    getRandomColor() {
      var letters = '0123456789ABCDEF'.split('');
      var color = '#';
      for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * letters.length)];
      }
      return color;
    },

    getInputText() {
      console.log("getInputText")
      axios
          .post(process.env.VUE_APP_API_DB_TEXT_TABLE + this.currentId, this.formData, {timeout: 50000})
          .then((res) => {
            console.log(res)
            this.setCurrentText(res.data["text"]);
            if ("annotated" in res.data){
              this.annotatedTokens = JSON.parse(res.data["annotated"])
            }
            console.log("getInputText", this.annotatedTokens)
          })
          .catch((err) => alert(err))
          .finally(() => {
            // console.log("tokenize start")
            this.tokenizeCurrentSentence();
          });
    },

    tokenizeCurrentSentence() {
      if (this.annotatedTokens) {
        this.tm = new TokenManager(this.annotatedTokens)
        this.annotatedTokens = null
      }
      else {
        axios
            .post(process.env.VUE_APP_API_TOKENIZE, {"text" : this.currentText}, {timeout: 50000}) //TODO why "text" is needed ?
            .then((res) => {
              this.tm = new TokenManager(res.data.tokens);
            })
            .catch((err) => alert(err));
      }
    },
    selectTokens() {
      // Selection object represents the range of text selected by the user or the current position of the caret.
      // https://developer.mozilla.org/en-US/docs/Web/API/Selection
      let selection = document.getSelection();

      if (selection.anchorOffset === selection.focusOffset &&
          selection.anchorNode === selection.focusNode)
        return;

      let startIndex, endIndex;
      try {
        startIndex = parseInt(
            selection.anchorNode.parentElement.id.replace("t", "")
        );
        endIndex = parseInt(
            selection.focusNode.parentElement.id.replace("t", "")
        );
      } catch (e) {
        console.log("selected text were not tokens");
        return;
      }
      if (!this.classes.length && selection.anchorNode) {
        alert(
            "There are no Tags available. Kindly add some Tags before tagging."
        );
        selection.empty();
        return;
      }
      console.log("this.currentClass", this.currentClass)
      this.tm.addNewLabelTag(startIndex, endIndex, this.currentClass);
      selection.empty();
    },
    onRemoveBlock(blockStart) {
      console.log("AM I getting called????")  // Nope u my friend
      this.tm.removeBlock(blockStart);
    },
    resetBlocks() {
      this.tm.resetBlocks();
    },
    skipCurrentSentence() {
      this.setCurrentRowId(this.currentId + 1)
      this.getInputText()
    },
    previous() {
      // console.log("previous")
      // console.log(this.currentId, this.formData.startId)
      if (this.currentId <= this.formData.startId) {
        alert("previous: You have reached the start of dataset!")
        return
      } else {
        this.setCurrentRowId(this.currentId - 1)
        this.getInputText()
      }

    },
    nextRow() {
      if (this.currentId > this.totalRows) {
        alert("nextRow: You have reached the end of dataset!")
        return
      } else {
        if (this.currentId === this.totalRows) {
          alert("nextRow: You have reached the end of dataset!")
          return
        }
        this.setCurrentRowId(this.currentId + 1)
        this.getInputText()
      }
    },
    saveTags() {
      // console.log("saveTags")
      // console.log(this.currentId, this.totalRows)
      if (this.currentId > this.totalRows) {
        alert("saveTags: You have reached the end of dataset!")
        return
      } else {
        // let tokens, labels;
        // [tokens, labels] = this.tm.exportASCoNLLAnnotations()
        // console.log(tokens, labels)
        // let tokens = JSON.stringify(this.tm.tokens)
        let tokensTags = this.tm.exportASCoNLLAnnotations()
        console.log(tokensTags.join(" "))
        // console.log("saveTags", JSON.stringify(tokens))
        axios
            .post(process.env.VUE_APP_API_DB_TEXT_ANNOTATIONS,
                {"id": this.currentId,
                  "tokens": tokensTags[0].join(" "),
                  "labels": tokensTags[1].join(" "),
                  "form_data": this.formData},
                {timeout: 50000}) //TODO why "text" is needed ?
            .then((res) => {
              console.log("insert successfull", res)
            })
            .catch((err) => alert(err));

        if (this.currentId === this.totalRows) {
          alert("saveTags: You have reached the end of dataset!")
          return
        }

        this.setCurrentRowId(this.currentId + 1)
        this.getInputText()

      }
    },
    changeColor() {
      for(const item of this.classes) {
        // if (item.label.length > 0) {
        //   classes.add(item.label)
        //   // cls_id += 1
        console.log("********", item.label)
        this.classColorMap[item.name] = this.getRandomColor()
        // }
      }
    }
  }
}
</script>

<style lang="scss">
#editor {
  padding: 1rem;
}
</style>`