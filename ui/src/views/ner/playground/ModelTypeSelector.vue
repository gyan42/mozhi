<template>
  <section>
    <div className="control">
      <label className="label">
        ModelName and Type
      </label>
      <div className="select">
        <!--          :disabled="annotations.length"-->
        <select name="split_type"
                id="split_type"
                v-model="modelNameModel">
          <option v-for="model in models" :key="model.value">{{model.name}} {{model.type}}</option>
        </select>
      </div>
    </div>
  </section>
</template>

<script>
import {mapState, mapMutations, mapGetters} from "vuex";

export default {
  name: "ModelTypeSelector",
  data() {
    return {};
  },
  props: {
    models: {
      type: Array[Object],
      requried: true
    }
  },
  computed: {
    modelNameModel: {
      get() {
        return this.getModelName()
      },
      set(value) {
        this.setModelName(value)
      },
    },
  },
  methods: {
    ...mapMutations('nerModelPredictions', ['setModelName']),
    ...mapState('nerModelPredictions', ['modelName']),
    ...mapGetters('nerModelPredictions', ['getModelName'])
  },
};
</script>
