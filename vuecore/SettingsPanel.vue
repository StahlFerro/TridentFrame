<template>
  <div id="settings_panel" class="container" style="display: none; padding:10px;">
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
          <a v-on:click="purgeCacheTemp" class="button is-large is-neon-cyan">
            <span class="icon is-large">
              <i class="fas fa-ban"></i>
            </span>
            <span>Purge Cache</span>
          </a>
        </td>
      </tr>
      <tr>
        <td>
          <a v-on:click="openInspector" class="button is-large is-neon-cyan">
            <span class="icon is-large">
              <i class="fas fa-bug"></i>
            </span>
            <span>Open Inspector</span>
          </a>
        </td>
        <td>
          <!-- <a v-on:click="openCWD" class="button is-large is-neon-cyan">
            <span class="icon is-large">
              <i class="fas fa-folder"></i>
            </span>
            <span>Print CWD</span>
          </a> -->
        </td>
      </tr>
    </table>
  </div>
</template>

<script>
const { remote, BrowserWindow } = require("electron");
const dialog = remote.dialog;
const session = remote.getCurrentWebContents().session;
const { client } = require("./Client.vue");

function refreshWindow() {
  remote.getCurrentWindow().reload();
  session.clearCache(() => {});
}

function purgeCacheTemp() {
  client.invoke("purge_cache_temp", (error, res) => {
    if (error) {
      console.error(error);
    } else if (res) {
      console.log(res);
    }
  });
}

function openInspector() {
  remote.getCurrentWebContents().openDevTools();
  var devtools = remote.getCurrentWindow().devToolsWebContents;
  if (devtools) { devtools.focus(); }
}

function openCWD() {
  console.log('openCWD');
  client.invoke("print_cwd", (error, res) => {
    if (error) {
      console.error(error);
    } else if (res) {
      console.log("JS DIRNAME", __dirname)
      console.log(res);
    }
  })
}

export default {
  methods: {
    refreshWindow: refreshWindow,
    purgeCacheTemp: purgeCacheTemp,
    openInspector: openInspector,
    openCWD: openCWD,
  }
};
</script>
