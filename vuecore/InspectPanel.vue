<template>
  <div id="inspect_panel">
    <div class="inspect-panel-root">
      <div class="inspect-panel-display">
        <div class="inspect-panel-image silver-bordered">
          <img v-bind:src="img_path" />
        </div>
        <div class="inspect-panel-info silver-bordered-no-left">
          <table class="table ins-info-table is-paddingless" width="100%">
            <template v-for="(item, key) in info_data">
              <!-- <span v-bind:key="key"/> -->
              <tr v-if="key == 'general_info'" v-bind:key="'general_info_' + key">
                <td colspan="2" class="is-cyan">GENERAL INFO</td>
              </tr>
              <tr v-if="key == 'animation_info'" v-bind:key="'animation_info_' + key">
                <td colspan="2" class="is-cyan">ANIMATION INFO</td>
              </tr>
              <tr v-for="(iprop, key, index) in item" v-bind:key="'iprop_' + key">
                <td style="width: 123px">
                  <strong
                    ><span class="is-white-d">{{ iprop.label }}</span></strong
                  >
                </td>
                <template v-if="key == 'loop_count' && iprop.value == 0">
                  <td style="max-width: 369px; word-wrap: break-all">Infinite</td>
                </template>
                <template v-else>
                  <td style="max-width: 369px; word-wrap: break-all">
                    {{ iprop.value }}
                  </td>
                </template>
              </tr>
            </template>
          </table>
        </div>
      </div>
      <div class="inspect-panel-controls">
        <a
          v-on:click="loadImage"
          class="button is-neon-emerald"
          v-bind:class="{
            'is-loading': INS_IS_INSPECTING,
            'is-static': isButtonFrozen,
          }"
        >
          <span class="icon is-small">
            <i class="fas fa-plus"></i>
          </span>
          <span>Load Any Image</span>
        </a>
        <a
          v-on:click="clearImage"
          class="button is-neon-crimson"
          v-bind:class="{ 'is-static': isButtonFrozen }"
        >
          <span class="icon is-small">
            <i class="fas fa-times"></i>
          </span>
          <span>Clear</span>
        </a>
        <a
          v-on:click="toggleCheckerBG"
          class="button is-neon-white"
          v-bind:class="{ 'is-active': checkerbg_active }"
        >
          <span class="icon is-medium">
            <i class="fas fa-chess-board"></i>
          </span>
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import { webFrame } from "electron";
const remote = require("electron").remote;
const dialog = remote.dialog;
const mainWindow = remote.getCurrentWindow();
const session = remote.getCurrentWebContents().session;
// const { client } = require("./Client.vue");
const { randString } = require("./Utility.vue");
const { tridentEngine } = require("./Client.vue");

let extension_filters = [
  {
    name: "Images",
    extensions: ["png", "gif", "jpg"],
  },
];
let file_dialog_props = ["openfile"];
let dir_dialog_props = ["openDirectory", "createDirectory"];

var data = {
  img_path: "",
  checkerbg_active: false,
  isButtonFrozen: false,
  INS_IS_INSPECTING: false,
  info_data: "",
};

function loadImage() {
  var options = {
    properties: file_dialog_props,
  };
  dialog
    .showOpenDialog(mainWindow, options)
    .then((result) => {
      let chosen_paths = result.filePaths;
      console.log(`chosen path: ${chosen_paths}`);
      if (chosen_paths === undefined || chosen_paths.length == 0) {
        return;
      }
      data.INS_IS_INSPECTING = true;
      console.log(chosen_paths);
      tridentEngine(["inspect-one", chosen_paths[0]], (error, res) => {
        if (error) {
          console.log("stderr error: ", error);
          console.error(error);
        }
        else {
          console.log({
            RES: res,
          });
          res = JSON.parse(res);
          console.table(res);
          data.info_data = res;
          if (res.general_info || res.animation_info) {
            data.img_path = `${
              res.general_info.absolute_url.value
            }?timestamp=${randString()}`;
          }
          console.log(res);
        }
        data.INS_IS_INSPECTING = false;
      });
    })
    .catch((err) => {
      console.log(err);
    });
}

function clearImage() {
  data.img_path = "";
  data.info_data = "";
  webFrame.clearCache();
}

function toggleCheckerBG() {
  data.checkerbg_active = !data.checkerbg_active;
  console.log("now checkerbg is", data.checkerbg_active);
}
export default {
  data: function () {
    return data;
  },
  methods: {
    loadImage: loadImage,
    clearImage: clearImage,
    toggleCheckerBG: toggleCheckerBG,
  },
};
</script>
