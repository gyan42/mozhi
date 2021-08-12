<template>
  <nav class="px-3">
    <d-b-progress-bar class="mb-5" :completed="current.id+1" :total="inputSentences.length" />
    <p class="control">
      <button class="button is-link" @click="generateJSONExport">Download</button>
    </p>
  </nav>
</template>

<script>
import {mapState} from "vuex";
import DBProgressBar from './DFProgressBar';

export default {
  name: "DFAnnotationSidebar",
  props: {
    current: {
      type: Object,
      required: true,
    },
  },
  components: {
    DBProgressBar,
  },
  computed: {
    ...mapState(["inputSentences", "annotations", "classes"]),
    visibleSentences() {
      let start = this.current.id;
      if (start + 10 > this.inputSentences.length) {
        start = this.inputSentences.length - 10;
      }
      let end = start + 10;
      return this.inputSentences.slice(start, end);
    },
  },
  methods: {
    generateJSONExport() {
      const filename = "training_data.json";
      const output = {
        "classes": this.classes.map(c => c.name),
        "annotations": this.annotations
      }
      const jsonStr = JSON.stringify(output);

      let element = document.createElement("a");
      element.setAttribute(
          "href",
          "data:text/plain;charset=utf-8," + encodeURIComponent(jsonStr)
      );
      element.setAttribute("download", filename);

      element.style.display = "none";
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    },
  },
};
</script>

<style lang="scss">
.is-single-line {
  width: 90%;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
}
</style>
