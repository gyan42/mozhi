<template>
  <nav class="px-3">
<!--    <split-type-selector class="mt-4 mb-5" />-->
    <d-b-progress-bar class="mb-5" :completed="currentId" :total="totalRows" />
  </nav>
</template>

<script>
import { mapState } from "vuex";
// import SplitTypeSelector from './SplitTypeSelector';
import DBProgressBar from './DBProgressBar';

export default {
  name: "DBAnnotationSidebar",
  props: ["currentId"],
  components: {
    DBProgressBar,
    // SplitTypeSelector
  },
  computed: {
    ...mapState("databaseInfo",["totalRows"]),
    // visibleSentences() {
    //   let start = this.current.id;
    //   if (start + 10 > this.inputSentences.length) {
    //     start = this.inputSentences.length - 10;
    //   }
    //   let end = start + 10;
    //   return this.inputSentences.slice(start, end);
    // },
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
