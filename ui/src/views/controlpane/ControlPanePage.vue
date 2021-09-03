<template>
  <page-header>
    <h1 class="title"> Control Pane </h1>
  </page-header>

  <d-b-connection-info-modal :isActive="isDBModalActive"
                             :close="close"/>

  <min-i-o-info-modal :isActive="isMinIOModalActive"
                      :close="close"/>

  <create-d-b-modal :isActive="isCreateDBModalActive"
                    :close="close"/>

  <upload-text-files-modal :isActive="isUploadTextFilesModalActive"
                           :close="close"/>

  <torch-serve-modal :isActive="isTorchServeActive"
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
      <li v-bind:class="{ 'is-active': activeTab === 'torchserve' }">
        <span class="icon is-small"><i class="fas fa-server" aria-hidden="true"></i></span>
        <a v-on:click="activeTab = 'torchserve'">Torch Serve</a>
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
          <button v-on:click="launchDBConnectionInfoModal" class="button is-white is-medium">
            Connection Info
          </button>
        </a>
        <a class="panel-block is-active">
          <button v-on:click="launchCreateDBModal" class="button is-white is-medium">
            Create New Database
          </button>
        </a>
        <a class="panel-block is-active">
          <button v-on:click="launchUploadTextFilesModal" class="button is-white is-medium">
            Upload Tagged Data
          </button>
        </a>
        <!--        <a class="panel-block is-active">-->
        <!--          <button v-on:click="launch" class="button is-white is-medium">-->
        <!--            Upload Raw Data-->
        <!--          </button>-->
        <!--        </a>-->
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
          <button v-on:click="launchMinIOConnectionModal" class="button is-white is-medium">Connection Info</button>
        </a>
<!--        <a class="panel-block is-active">-->
<!--          <button v-on:click="launchMinIOConnectionModal" class="button is-white is-medium">Create Bucket</button>-->
<!--        </a>-->
<!--        <a class="panel-block is-active">-->
<!--          <button v-on:click="launchMinIOConnectionModal" class="button is-white is-medium">Upload file(s)..</button>-->
<!--        </a>-->
      </nav>
    </div>
  </div>


    <div class="tab-contents">
    <div class="content" v-bind:class="{ 'is-active': activeTab === 'torchserve' }">
      <nav class="panel is-info">
        <p class="panel-heading">
          Torch Serve
        </p>
        <a class="panel-block is-active">
          <button v-on:click="launchTorchServeModal" class="button is-white is-medium">Register PyTorch MAR Model</button>
        </a>
      </nav>
    </div>
  </div>



</template>

<script>
import PageHeader from "@/components/PageHeader"
import DBConnectionInfoModal from "@/components/modals/DBConnectionInfoModal";
import MinIOInfoModal from "@/components/modals/MinIOInfoModal";
import CreateDBModal from "@/components/modals/CreateDBModal";
import UploadTextFilesModal from "@/components/modals/UploadTextFilesModal"
import TorchServeModal from "@/components/modals/TorchServeModal";

export default {
  name: "ControlPanePage",
  components: {
    PageHeader,
    DBConnectionInfoModal,
    CreateDBModal,
    MinIOInfoModal,
    UploadTextFilesModal,
    TorchServeModal
  },
  data() {
    return {
      isDBModalActive: false,
      isMinIOModalActive: false,
      isCreateDBModalActive: false,
      isUploadTextFilesModalActive: false,
      isTorchServeActive: false,
      activeTab: "db",
      isActive: "pictures"
    }
  },
  methods: {
    launchDBConnectionInfoModal() {
      this.isDBModalActive = true;
    },
    launchMinIOConnectionModal() {
      this.isMinIOModalActive = true;
    },
    launchCreateDBModal() {
      this.isCreateDBModalActive = true
    },
    launchUploadTextFilesModal() {
      this.isUploadTextFilesModalActive = true
    },
    launchTorchServeModal() {
      this.isTorchServeActive = true
    },
    close() {
      this.isDBModalActive = false;
      this.isMinIOModalActive = false;
      this.isCreateDBModalActive = false
      this.isUploadTextFilesModalActive = false
      this.isTorchServeActive = false
    },
  },
  computed: {
  },
  mounted() {
    // Close modal with 'esc' key
    document.addEventListener("keydown", (e) => {
      if (e.keyCode === 27) {
        this.close()
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