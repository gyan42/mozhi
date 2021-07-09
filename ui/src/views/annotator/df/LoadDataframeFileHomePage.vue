<template>
  <div class="field">
    <div class="file is-centered is-primary has-name is-boxed my-4">
      <label class="file-label">
        <input
            ref="dfFileLoader"
            id="dfFileLoader"
            class="file-input"
            type="file"
            name="dfFileLoader"
            v-on:change="onFileSelected"
        />
        <span class="file-cta">
          <span class="file-icon">
            <font-awesome-icon icon="file-alt" />
          </span>
          <span class="file-label">
            Load DataFrame File
          </span>
        </span>
      </label>
    </div>
  </div>
</template>

<script>
import { mapMutations } from "vuex";
import DataFrame from "dataframe-js";

export default {
  name: "LoadTextFile",
  emits: ["file-loaded"],
  methods: {
    ...mapMutations(["setInputSentences"]),
    ...mapMutations("tokenizerInfo", ["resetClass"]),

    onFileSelected() {
      this.resetClass()

      const setInput = this.setInputSentences
      const emit = this.$emit
      var reader = new FileReader();
      reader.onload = function (event){
        console.info("readDataframe")
        // dfd.read_csv(event.target.result).then(df=> df.show())
        DataFrame.fromCSV(event.target.result)
            .then(df=>
            {
              console.info(">>>> onFileSelected")
              let data = df.select('text').toArray().map( x => x[0])
              console.info(data)
              setInput(data)
              emit("file-loaded");
              console.info("<<<< onFileSelected")

            })



      }
      reader.readAsDataURL(this.$refs.dfFileLoader.files[0]);
    },
  },
};
</script>
