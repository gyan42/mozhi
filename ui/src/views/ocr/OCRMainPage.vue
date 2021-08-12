<template>
  <page-header>
    <h1 class="title">OCR - Optical Character Recognition</h1>
  </page-header>

  <nav class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-item has-dropdown is-hoverable">
      <a class="navbar-link">
        <h2 class="subtitle"> Choose one... </h2>
      </a>

      <div class="navbar-dropdown">
        <a class="navbar-item">
          <h2 class="subtitle">
            <router-link to="/ocr/tesseract">
              Tesseract
            </router-link>
          </h2>
        </a>
        <a class="navbar-item">
          <h2 class="subtitle">
            <router-link to="/ocr/calamari">
              Calamari
            </router-link>
          </h2>
        </a>
      </div>
    </div>
  </nav>

</template>

<script>
import PageHeader from "@/components/PageHeader"

export default {
  name: "OCRMainPage",
  components: {PageHeader}

}
</script>

<style scoped>

</style>