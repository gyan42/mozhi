<template>
  <div>
    <section class="hero is-dark">
      <div class="hero-body">
        <div class="container">
          <h1 class="title">Dataframe File Annotator</h1>
          <h2 class="subtitle">Annotate DataFrame Model training</h2>
        </div>
      </div>
    </section>

    <div>
      <LoadDataframeFileHomePage class="pt-6" v-on:file-loaded="onFileLoaded" />
    </div>
  </div>
</template>

<script>
import LoadDataframeFileHomePage from "@/views/annotator/df/LoadDataframeFileHomePage";
export default {
  name: "DFUploadPage",
  emits: ["file-loaded"],
  components: {
    LoadDataframeFileHomePage,
  },
  methods: {
    onFileLoaded() {
      console.info(">>>> onFileLoaded")
      console.info(this.$store.state.inputSentences)
      this.$router.push('/annotator/df');
      this.$emit("file-loaded");
      console.info("<<<<  onFileLoaded")

    },
  },
}
</script>

<style scoped>

</style>