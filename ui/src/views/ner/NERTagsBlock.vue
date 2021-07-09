<template>
  <div class="field is-grouped is-grouped-multiline">
    <div class="control" v-for="cls in classes" :key="cls">
      <div class="tags is-medium has-addons">
        <a class="tag is-medium" :style="{backgroundColor: classColorMap[cls]}">
          {{ cls }}
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import {mapMutations, mapGetters} from "vuex";
export default {
  name: "NERTagsBlock",
  data() {
    return {
    };
  },
  props: {
    classes: {
      type: Array,
      required: true
    },
    classColorMap: {
      type: Object,
      required: true
    },
  },
  computed: {
    ...mapGetters('nerModelPredictions', ['getClasses', 'getPredictions']),
  },
  methods: {
    ...mapMutations(["removeClass", "setCurrentClass"]),

  },
};
</script>
