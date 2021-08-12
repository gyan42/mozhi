<template>
  <page-header>
    <h1 class="title">Annotators</h1>
  </page-header>


  <nav class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-item has-dropdown is-hoverable">
      <a class="navbar-link">
        <h2 class="subtitle"> Choose one... </h2>
      </a>

      <div class="navbar-dropdown">
        <a class="navbar-item">
          <h2 class="subtitle">
            <router-link to='/annotator/dbdetails'>Database Annotation</router-link>
          </h2>
        </a>
        <a class="navbar-item">
          <h2 class="subtitle"><router-link to='/annotator/imagehome'>Image Annotation</router-link>
          </h2>
        </a>
        <a class="navbar-item">
          <h2 class="subtitle"><router-link to='/annotator/textfile'>User Text File</router-link>
          </h2>
        </a>

        <a class="navbar-item">
          <h2 class="subtitle"> <router-link to='/annotator/dffile'>DataFrame User File</router-link>
          </h2>
        </a>
      </div>
    </div>
  </nav>


</template>

<script>
import PageHeader from "@/components/PageHeader"

export default {
  name: "AnnotationMainPage",
  components: {PageHeader}

}
</script>

<style scoped>

</style>