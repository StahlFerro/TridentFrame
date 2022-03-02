<template>
  <div class="status-bar">
    <div class="status-icon"> 
      <span class="icon" v-show="logLevel == EnumStatusLogLevel.INFO">
        <font-awesome-icon icon="info-circle" class="is-cyan"/>
        <!-- <i class="fas fa-info-circle is-cyan"></i> -->
      </span>
      <span class="icon" v-show="logLevel == EnumStatusLogLevel.PROCESSING">
        <font-awesome-icon icon="spinner" class="is-white-d" pulse/>
        <!-- <i class="fas fa-spinner fa-pulse is-white-d"></i> -->
      </span>
      <span class="icon" v-show="logLevel == EnumStatusLogLevel.SUCCESS">
        <font-awesome-icon icon="check" class="is-emerald"/>
        <!-- <i class="fas fa-check is-emerald"></i> -->
      </span>
      <span class="icon" v-show="logLevel == EnumStatusLogLevel.ERROR">
        <font-awesome-icon icon="times" class="is-crimson"/>
        <!-- <i class="fas fa-times is-crimson"></i> -->
      </span>
    </div>
    <div class="status-textbox">
      <input
        :value="statusText"
        type="text"
        readonly="readonly"
      />
    </div>
  </div>
</template>

<script>
import { EnumStatusLogLevel } from "../../modules/constants/loglevels.js";
export default {
  data() {
    return {
      statusText: "",
      logLevel: "",
      EnumStatusLogLevel,
    }
  },
  props: {
    // bus: Vue,
  },
  methods: {
    logClear() {
      console.log("Clearing log...");
      this.statusText = "";
      this.logLevel = "";
    },
    logInfo(message) {
      console.log(message);
      this.statusText = message;
      if (this.logLevel != EnumStatusLogLevel.INFO)
        this.logLevel = EnumStatusLogLevel.INFO;
    },
    logProcessing(message) {
      console.log(message);
      this.statusText = message;
      if (this.logLevel != EnumStatusLogLevel.PROCESSING)
        this.logLevel = EnumStatusLogLevel.PROCESSING;
    },
    logSuccess(message) {
      console.log(message);
      this.statusText = message;
      this.logLevel = EnumStatusLogLevel.SUCCESS;
    },
    logWarning(message) {
      console.log(message);
      this.statusText = message;
      this.logLevel = EnumStatusLogLevel.WARNING;
    },
    logError(message) {
      console.log("logError called");
      console.log(message);
      this.statusText = message;
      this.logLevel = EnumStatusLogLevel.ERROR;
      console.log(this.logLevel);
    },
  },
  mounted() {
    // this.bus.$on("logClear", this.logClear);
    // this.bus.$on("logProcessing", this.logProcessing);
    // this.bus.$on("logMessage", this.logInfo);
    // this.bus.$on("logSuccess", this.logSuccess);
    // this.bus.$on("logWarning", this.logWarning);
    // this.bus.$on("logError", this.logError);
  }
};
</script>
