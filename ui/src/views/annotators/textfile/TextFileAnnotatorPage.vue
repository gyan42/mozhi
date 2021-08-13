<template>
  <div class="columns is-desktop">
    <div class="column is-one-fifth">
      <TextFileAnnotationSidebar :current="currentSentence" />
    </div>
    <div class="column">
      <div class="panel m-4">
        <div class="panel-heading">
          <classes-block />
        </div>
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
              <button class="button is-link" @click="saveTags">Save</button>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { mapState } from "vuex";
import mozhiapi from "@/backend/mozhiapi";
import Token from "@/components/Token";
import TokenBlock from "@/components/TokenBlock";
import ClassesBlock from "@/components/ClassesBlock.vue";
import TokenManager from "@/services/token-manager";

import TextFileAnnotationSidebar from "./TextFileAnnotationSidebar.vue";

export default {
  name: "TextAnnotationPage",
  data: function() {
    return {
      tm: new TokenManager([]),
      currentSentence: {},
      currentIndex: 0,
      redone: "",
    };
  },
  components: {
    Token,
    TokenBlock,
    TextFileAnnotationSidebar,
    ClassesBlock,
  },
  computed: {
    ...mapState(["inputSentences", "classes", "annotations", "currentClass"]),
  },
  watch: {
    inputSentences() {
      this.currentIndex = 0;
      this.tokenizeCurrentSentence();
    }

  },
  created() {
    if (this.inputSentences.length) {
      this.tokenizeCurrentSentence();
    }
    else {
      // if empty go back to load screen
      this.$router.push('/annotator/textfile');
    }
    document.addEventListener("mouseup", this.selectTokens);
  },
  beforeUnmount() {
    document.removeEventListener("mouseup", this.selectTokens);
  },
  methods: {
    tokenizeCurrentSentence() {
      if (this.currentIndex >= this.inputSentences.length) {
        // TODO show completed message
        alert("You have completed all the sentences")
        return;
      }
      this.currentSentence = this.inputSentences[this.currentIndex];
      mozhiapi
        .post(process.env.VUE_APP_API_TOKENIZE, this.currentSentence)
        .then((res) => {
          this.tm = new TokenManager(res.data.tokens);
        })
        .catch((err) => alert(err));
    },
    selectTokens() {
      let selection = document.getSelection();

      if (
        selection.anchorOffset === selection.focusOffset &&
        selection.anchorNode === selection.focusNode
      )
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
    saveTags() {
      mozhiapi
        .post(process.env.VUE_APP_API_DETOKENIZE, { tokens: this.tm.words })
        .then((res) => {
          this.$store.commit("addAnnotation", [
            res.data.text,
            { entities: this.tm.exportAsAnnotation() },
          ]);
          this.currentIndex++;
          this.tokenizeCurrentSentence();
        })
        .catch((e) => {
          console.log(e);
        });
    },
  },
};
</script>

<style lang="scss">
#editor {
  padding: 1rem;
}
</style>
