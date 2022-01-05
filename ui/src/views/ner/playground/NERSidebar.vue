<template>
  <nav class="px-3">
    <dataset-type-selector class="mt-4 mb-5" />
    <model-type-selector class="mt-4 mb-5" v-bind:models="models"/>
  </nav>
</template>

<script>
import DatasetTypeSelector from "@/views/ner/playground/DatasetTypeSelector";
import ModelTypeSelector from "@/views/ner/playground/ModelTypeSelector";

export default {
  name: "NERSidebar",
  props: {
    models: {
      type: Array[Object],
      requried: true
    }
  },
  components: {
    DatasetTypeSelector,
    ModelTypeSelector
  },
  computed: {
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
