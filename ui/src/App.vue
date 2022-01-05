<template >
  <link rel="favicon.ico" type="image/png" href="src/assets/mozhi-logo.png"/>
  <div id="app">
    <div
        id="sidebardiv"
        :class="[{'collapsed' : collapsed}, {'onmobile' : isOnMobile}]">

      <img alt="mozhi" src="./assets/mozhi-logo.png">

      <sidebar-menu
          collapsed=true
          :menu="menu"/>
      <router-view/>

      <div
          v-if="isOnMobile && !collapsed"
          class="sidebar-overlay"
          @click="collapsed = true"
      />
    </div>
  </div>
</template>

<script>
import "@/assets/styles.scss";
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'
// import mapGetters from "vuex";

export default {
  name: 'App',
  watch: {
    '$route' (to, from, next) { // eslint-disable-line no-unused-vars
      document.title = to.meta.title || 'mozhi'
    }
  },
  beforeCreate() {
    // this.isHide = !this.$store.state.isUserLoggedIn
    this.collapsed = true
  },
  data() {
    return {
      isHide: true,
      collapsed: false,
      isOnMobile: false,
      // https://github.com/yaminncco/vue-sidebar-menu
      menu: [
        {
          header: 'Menu',
          hiddenOnCollapse: true,
        },
        {
          href: '/',
          title: 'LogIn',
          icon: 'fas fa-sign-in-alt',
        },
        {
          href: '/home',
          title: 'Home',
          icon: 'fas fa-home',
        },
        {
          href: '/annotator/',
          title: 'Annotator',
          icon: 'fas fa-draw-polygon',
          child : [
            {
              href: '/annotator/db',
              title: 'Database',
              icon: 'fas fa-database'
            },
            {
              href: '/annotator/imagefile',
              title: 'TextImage',
              icon: 'fas fa-image'
            },
            {
              href: '/annotator/textfile',
              title: 'TextFile',
              icon: 'fas fa-file-alt',
            },
            {
              href: '/annotator/dffile',
              title: 'DataFrame',
              icon: 'fas fa-table'

            },
          ]
        },
        {
          href: '/ocr/',
          title: 'OCR',
          icon: 'fas fa-file-alt',
          child : [
            {
              href: '/ocr/tesseract',
              title: 'Tesseract',
              icon: 'fas fa-cube'
            },
            {
              href: '/ocr/calamari',
              title: 'Calamari',
              icon: 'fas fa-cubes'
            },
          ]
        },
        {
          href: '/ner',
          title: 'NER',
          icon: 'fas fa-glasses',
          child : [
            {
              href: '/ner/playground',
              title: 'NER Playground',
              icon: 'fas fa-cube'
            },
            {
              href: '/ner/receipts',
              title: 'Receipts',
              icon: 'fas fa-cubes'
            },
          ]
        },
        {
          href: '/controlpane',
          title: 'Control Pane',
          icon: 'fas fa-user-cog',
        },
      ],
      mounted () {
        this.onResize()
        window.addEventListener('resize', this.onResize)
      },
      methods: {
        onToggleCollapse () {
          console.log('onToggleCollapse')
        },
        onItemClick () {
          console.log('onItemClick')
          // console.log(event)
          // console.log(item)
        },
        onResize () {
          if (window.innerWidth <= 767) {
            this.isOnMobile = true
            this.collapsed = true
          } else {
            this.isOnMobile = false
            this.collapsed = false
          }
        }
      },
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

#sidebardiv {
  padding-left: 70px;
  transition: 0.3s ease;
}
#sidebardiv.collapsed {
  padding-left: 65px;
}
#sidebardiv.onmobile {
  padding-left: 65px;
}
</style>
