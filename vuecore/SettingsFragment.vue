<template>
  <div id="settings_panel" class="container" style="display: none; padding:10px;">
    <div class="content">
      <table class="table is-borderless" style="padding: 5px;" width="100%">
        <tr>
          <td>
            <a v-on:click="refreshWindow" class="button is-large is-neon-cyan">
              <span class="icon is-large">
                <i class="fas fa-redo-alt"></i>
              </span>
              <span>Reload Window</span>
            </a>
          </td>
          <td>
            <a v-on:click="purgeCache" class="button is-large is-neon-cyan">
              <span class="icon is-large">
                <i class="fas fa-ban"></i>
              </span>
              <span>Purge Cache</span>
            </a>
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
const remote = require("electron").remote;
const dialog = remote.dialog;
const session = remote.getCurrentWebContents().session;
const { client } = require("./Client.vue");

function refreshWindow() {
  remote.getCurrentWindow().reload();
  session.clearCache(testcallback);
}

function purgeCache() {
  client.invoke("purge_cache", (error, res) => {
    if (error) {
      console.error(error);
    } else if (res) {
      console.log(res);
    }
  });
}

export default {
  methods: {
    refreshWindow: refreshWindow,
    purgeCache: purgeCache,
  }
};
</script>
