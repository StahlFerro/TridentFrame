<template>
  <div class="status-bar">
    <input
      :value="statusText"
      type="text"
      class="status-textbox"
      readonly="readonly"
    />
  </div>
</template>

<script>
import Vue from 'vue';
export default {
  data: function() {
    return {
      statusText: "",
    }
  },
  props: {
    bus: Vue,
  },
  methods: {
    logClear() {
      console.log("Clearing log...");
      this.statusText = "";
    },
    logProcessing(message) {
      console.log(message);
      this.statusText = message;
    },
    logMessage(message) {
      console.log(message);
      this.statusText = message;
    },
    logSuccess(message) {
      console.log(message);
      this.statusText = message;
    },
    logWarning(message) {
      console.log(message);
      this.statusText = message;
    },
    logError(message) {
      console.log(message);
      this.statusText = message;
    },
  },
  mounted() {
    this.bus.$on("logClear", this.logClear);
    this.bus.$on("logProcessing", this.logProcessing);
    this.bus.$on("logMessage", this.logMessage);
    this.bus.$on("logSuccess", this.logSuccess);
    this.bus.$on("logWarning", this.logWarning);
    this.bus.$on("logError", this.logSuccess);
  }
};
</script>
