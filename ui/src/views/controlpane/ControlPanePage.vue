<template>
  <page-header>
    <h1 class="title"> Control Pane </h1>
  </page-header>

  <d-b-info-dialog-box :isActive="isDBDialogActive"
                       :message="message"
                       :close="close"/>

  <min-i-o-info-dialog-box :isActive="isMinIODialogActive"
                           :message="message"
                           :close="close"/>

  <!--  Tabs -->
  <div class="tabs is-centered is-medium">
    <ul>
      <li v-bind:class="{ 'is-active': activeTab === 'db' }">
        <span class="icon is-small"><i class="fas fa-database" aria-hidden="true"></i></span>
        <a v-on:click="activeTab = 'db'">Database</a>
      </li>
      <li v-bind:class="{ 'is-active': activeTab === 'objstorage' }">
        <span class="icon is-small"><i class="fas fa-hdd" aria-hidden="true"></i></span>
        <a v-on:click="activeTab = 'objstorage'">Object Storage</a>
      </li>
    </ul>
  </div>

  <!--  Tabs Contents-->
  <div class="tab-contents">

    <div class="content" v-bind:class="{ 'is-active': activeTab === 'db' }">

      <nav class="panel is-info">
        <p class="panel-heading">
          Postgresql
        </p>

        <a class="panel-block is-active">
          <button v-on:click="launch" class="button is-white is-medium">Connection Info</button>
        </a>
        <a class="panel-block is-active">
          <button v-on:click="launch" class="button is-white is-medium">Create New Database</button>
        </a>
        <a class="panel-block is-active">
          <button v-on:click="launch" class="button is-white is-medium">Upload Tagged Data</button>
        </a>
        <a class="panel-block is-active">
          <button v-on:click="launch" class="button is-white is-medium">Upload Raw Data</button>
        </a>
      </nav>

    </div>
  </div>


  <div class="tab-contents">
    <div class="content" v-bind:class="{ 'is-active': activeTab === 'objstorage' }">
      <nav class="panel is-info">
        <p class="panel-heading">
          MinIO
        </p>
        <a class="panel-block is-active">
          <button v-on:click="launch" class="button is-white is-medium">Connection Info</button>
        </a>
        <a class="panel-block is-active">
          <button v-on:click="launch" class="button is-white is-medium">Create Bucket</button>
        </a>
        <a class="panel-block is-active">
          <button v-on:click="launch" class="button is-white is-medium">Upload file(s)..</button>
        </a>
      </nav>
    </div>
  </div>


</template>

<script>
import PageHeader from "@/components/PageHeader"
import DBInfoDialogBox from "@/components/modals/DBInfoModal";
import MinIOInfoDialogBox from "@/components/modals/MinIOInfoModal";

export default {
  name: "ControlPanePage",
  components: {
    PageHeader,
    DBInfoDialogBox,
    MinIOInfoDialogBox
  },
  data() {
    return {
      isDBDialogActive: false,
      isMinIODialogActive: false,
      activeTab: "db",
      isActive: "pictures"
    }
  },
  methods: {
    launch() {
      this.isDBDialogActive = true;
      this.isMinIODialogActive = true;
    },
    close() {
      this.isDBDialogActive = false;
      this.isMinIODialogActive = false;
    },
  },
  computed: {
    message() {
      return "Hello Bulma Modal";
    }
  },
  mounted() {
    // Close modal with 'esc' key
    document.addEventListener("keydown", (e) => {
      if (e.keyCode === 27) {
        this.isDBDialogActive = false;
        this.isMinIODialogActive = false;
      }
    });
  },
}
</script>

<style scoped>
.tab-contents .content {
  display: none;
}
.tab-contents .content.is-active {
  display: block;
}
</style>