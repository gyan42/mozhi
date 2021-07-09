<template>
    <section class="hero is-dark">
      <div class="hero-body">
        <div class="container">
          <h1 class="title">Dataframe Annotator Page</h1>
<!--          <h2 class="subtitle">Annotate DataFrame Model training</h2>-->
        </div>
      </div>
    </section>
  <div class="columns is-desktop">
    <!--Sidebar-->
    <div class="column is-one-fifth">
      <DFAnnotationSidebar :current="currentSentence"/>
    </div>
    <!--Sidebar-->

    <!--Right Side-->
    <div class="column">

      <!--Right Pannel-->
      <div class="panel m-4">
        <!--NER TAGS-->
        <div class="panel-heading">
          <classes-block />
        </div>
        <!--NER TAGS-->

        <!--Text-->
        <div class="panel-block">
          <div id="editor">
            <component
                :is="t.type === 'token' ? 'Token' : 'TokenBlock'"
                :id="'t' + t.start"
                v-for="t in tm.tokens"
                :token="t"
                :key="t.start"
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
              <button class="button" @click="skipCurrentSentence">Skip</button>
            </p>
            <p class="control">
              <button class="button is-link" @click="onPrev">Previous</button>
            </p>
            <p class="control">
              <button class="button is-success" @click="onNext">Next</button>
            </p>
          </div>
        </div>
        <!--Buttons-->
      </div>
      <!--Right Pannel-->
    </div>
    <!--Right Side-->

  </div>
</template>

<script>
import DFAnnotationSidebar from "@/views/annotator/df/DFAnnotationSidebar";
import Token from "../../../components/Token";
import TokenBlock from "../../../components/TokenBlock";
import ClassesBlock from "../../../components/ClassesBlock.vue";
import TokenManager from "../../../components/token-manager";
import {mapState} from "vuex";
import axios from "@/axios";


// https://blog.tensorflow.org/2020/08/introducing-danfo-js-pandas-like-library-in-javascript.html
// https://gmousse.gitbooks.io/dataframe-js/content/doc/BASIC_USAGE.html#sql-module
export default {
  name: "DFAnnotator",
  data: function() {
    return {
      tm: new TokenManager([]),
      currentSentence: {},
      currentIndex: 0,
      redone: "",
    };
  },
  components : {
    DFAnnotationSidebar,
    Token,
    TokenBlock,
    ClassesBlock,
  },
  computed: {
    ...mapState(["inputSentences", "classes", "annotations", "currentClass"]),
  },
  created() {
    if (this.inputSentences.length) {
      this.tokenizeCurrentSentence();
    }
    document.addEventListener("mouseup", this.selectTokens);
  },
  beforeUnmount() {
    document.removeEventListener("mouseup", this.selectTokens);
  },
  methods : {
    tokenizeCurrentSentence() {
      if (this.currentIndex >= this.inputSentences.length) {
        // TODO show completed message
        alert("You have completed all the sentences")
        return;
      }
      if (this.currentIndex < 0) {
        alert("No more sentences to navigate back")
        return;
      }
      this.currentSentence = this.inputSentences[this.currentIndex];
      console.info(this.currentSentence)
      axios
          .post("/vf/nlp/tokenize", this.currentSentence)
          .then((res) => {
            this.tm = new TokenManager(res.data.tokens);
          })
          .catch((err) => alert(err));
    },
    selectTokens() {
      let selection = document.getSelection();

      if (selection.anchorOffset === selection.focusOffset &&
          selection.anchorNode === selection.focusNode)
        return;
      let startIdx, endIdx;
      try {
        startIdx = parseInt(
            selection.anchorNode.parentElement.id.replace("t", "")
        );
        endIdx = parseInt(
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
      this.tm.addNewLabelTag(startIdx, endIdx, this.currentClass);
      selection.empty();
    },
    onRemoveBlock(blockStart) {
      this.tm.removeBlock(blockStart);
    },
    resetBlocks() {
      this.tm.resetBlocks();
    },
    skipCurrentSentence() {
      this.currentIndex++;
      this.tokenizeCurrentSentence();
    },
    onPrev() {
      this.currentIndex--;
      this.tokenizeCurrentSentence();
    },
    onNext() {
      this.saveTags()
      this.currentIndex++;
      this.tokenizeCurrentSentence();
    },
    saveTags() {
      axios
          .post("/vf/ner/detokenize", { tokens: this.tm.words })
          .then((res) => {
            this.$store.commit("addAnnotation", [
              res.data.text,
              { entities: this.tm.exportAsAnnotation() },
            ]);
            // this.currentIndex++;
            // this.tokenizeCurrentSentence();
          })
          .catch((e) => {
            console.log(e);
          });
    },
  }
}
</script>

<style lang="scss">
#editor {
  padding: 1rem;
}
</style>