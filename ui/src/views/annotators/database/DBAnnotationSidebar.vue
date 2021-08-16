<template>
  <div class="box">
    <nav class="px-3">
      <!--    <split-type-selector class="mt-4 mb-5" />-->
      <d-b-progress-bar class="mb-5" :completed="currentId" :total="totalRows" />
    </nav>

    <div className="control">
      <label className="label">
        Database
      </label>
      <div className="select">
        <select name="dblist"
                id="dblist"
                v-model="dbSelected"
                @change="onDBChange">
          <option v-for="db in dbList" :key="db">{{db}}</option>
        </select>
      </div>
    </div>
    <br>
    <div className="control">
      <label className="label">
        Text Table
      </label>
      <div className="select">
        <!--          :disabled="annotations.length"-->
        <select name="tableSelected"
                id="tableSelected"
                v-model="tableSelected"
                @change="onTableChange">
          <option v-for="tbl in tableList" :key="tbl">{{tbl}}</option>
        </select>
      </div>
    </div>
    <br>
    <div className="control">
      <label className="label">
        Tag Table
      </label>
      <div className="select">
        <!--          :disabled="annotations.length"-->
        <select name="tagTableSelected"
                id="tagTableSelected"
                v-model="tagTableSelected"
                @change="onTagChange">
          <option v-for="tbl in tableList" :key="tbl">{{tbl}}</option>
        </select>
      </div>
    </div>
    <br>
    <div className="control">
      <label className="label">
        Start Id
      </label>
      <input id="start_id" class="input is-medium"
             @change="onStartId"
             type="text" placeholder="1" v-model="startId">
    </div>

    <hr>

    <button class="button is-success" @click="onSave">
      Save changes
    </button>


  </div>


</template>

<script>
import { mapGetters, mapMutations } from "vuex";
// import SplitTypeSelector from './SplitTypeSelector';
import DBProgressBar from './DBProgressBar';
import DBServiceAPI from "@/backend/dbservice-api"

export default {
  name: "DBAnnotationSidebar",
  data() {
    return {
      tableList: [],
      dbList: [],
      dbSelected: "",
      tableSelected: "",
      tagTableSelected: "",
      totalRows: 0,
      startId: 0
    }
  },
  created() {
    DBServiceAPI.get_db_list(this.getConnectionInfo).then((res) => {
          console.log(res)
          this.dbList = res
        }
    )
  },
  mounted() {
    this.resetClass()
  },
  props: ["currentId"],
  components: {
    DBProgressBar,
    // SplitTypeSelector
  },
  computed: {
    // ...mapState("databaseInfo",["totalRows"]),
    ...mapGetters('databaseInfo', ['getConnectionInfo', 'getTableInfo', 'getCurrentRowId'])
  },
  methods: {
    ...mapMutations('databaseInfo', ['setFormData', 'setCurrentText', 'setCurrentRowId',
      'setTotalCounts', 'setTextTableInfo', 'setTagTableInfo', 'setUserDBInfo', 'setStartIdInfo']),
    ...mapMutations('tokenizerInfo', ["resetClass"]),
    onDBChange() {
      console.log("onDBChange")
      var connectionInfo = this.getConnectionInfo
      connectionInfo.dbname = this.dbSelected
      this.setUserDBInfo(this.dbSelected)
      DBServiceAPI.get_table_list(connectionInfo).then((res) => {
            this.tableList = res
            console.log(res)
          }
      )
    },
    onTableChange() {
      var connectionInfo = this.getConnectionInfo
      connectionInfo.dbname = this.dbSelected
      this.setTextTableInfo(this.tableSelected)
      DBServiceAPI.get_total_rows(connectionInfo, this.tableSelected).then((res) => {
            this.totalRows = res
            this.setTotalCounts(this.totalRows)
            console.log(res)
          }
      )
    },
    onTagChange() {
      var connectionInfo = this.getConnectionInfo
      connectionInfo.dbname = this.dbSelected
      this.setTagTableInfo(this.tableSelected)
      let tags = []
      DBServiceAPI.get_tags(connectionInfo, this.tagTableSelected).then((res) => {
            tags = res
            console.log(res)
            tags.forEach((t) => {
              // console.log(t)
              // self.addClass(t)
              if (t !== 'O') {
                this.$store.commit("tokenizerInfo/addClass", t);
              }
            })
          }
      )
    },
    onSave() {
      this.setCurrentRowId(parseInt(this.startId))
      this.setStartIdInfo(parseInt(this.startId))
      this.$emit("renderText")
    }
  }
};
</script>

<style lang="scss">
.is-single-line {
  width: 90%;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
}
</style>
