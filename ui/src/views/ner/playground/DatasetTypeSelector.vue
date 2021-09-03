<template>
  <section>
    <div class="control">
      <label class="label">
        Input Type
      </label>
      <div class="select">
        <!--          :disabled="annotations.length"-->
        <select name="split_type"
                id="split_type"
                v-model="dataSetNameModel">
          <option value="plainText">Plain English Text</option>
          <option value="image">Image</option>
        </select>
      </div>
    </div>
  </section>
</template>

<script>
import { mapState, mapMutations, mapGetters } from "vuex";

export default {
  name: "DatasetTypeSelector",
  data() {
    return {
    };
  },
  computed: {
    dataSetNameModel: {
      get() {
        return this.getDataSetName()
      },
      set(value) {
        this.setDatasetName(value)
      },
    },
  },
  methods: {
    ...mapMutations('nerModelPredictions', ['setDatasetName']),
    ...mapState('nerModelPredictions', ['dataSetName']),
    ...mapGetters('nerModelPredictions', ['getDataSetName'])
  },
};
</script>
