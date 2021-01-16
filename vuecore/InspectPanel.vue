<template>
  <div id="inspect_panel">
    <div class="inspect-panel-root">
      <div class="inspect-panel-display" >
        <div class="inspect-panel-image silver-bordered" @contextmenu="$emit('inspect-ctxmenu', $event, inspect_image_payload)">
          <div class="inspect-panel-msgbox" v-show="inspect_msgbox != false">
            <p class="is-left-paddingless is-border-colorless is-white-d">{{ inspect_msgbox }}</p>
          </div>
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
              <tr v-for="(iprop, ikey, index) in item" v-bind:key="'iprop_' + key + '_' + index">
                <td style="width: 123px">
                  <strong
                    ><span class="is-white-d">{{ iprop.label }}</span></strong
                  >
                </td>
                <template v-if="ikey == 'loop_count' && iprop.value == 0">
                  <td style="max-width: 369px; word-wrap: break-all">Infinite</td>
                </template>
                <template v-else>
                  <td style="max-width: 369px; word-wrap: break-all" @contextmenu="$emit('inspect-ctxmenu', $event, inspect_info_payload)">
                    {{ iprop.value }}
                  </td>
                </template>
              </tr>
            </template>
          </table>
        </div>
      </div>
      <div class="inspect-panel-controls">
        <a v-on:click="loadImage" class="button is-neon-emerald"
          v-bind:class="{
            'is-loading': INS_IS_INSPECTING,
            'is-static': isButtonFrozen,
          }">
          <span class="icon is-small">
            <i class="fas fa-plus"></i>
          </span>
          <span>Load Any Image</span>
        </a>
        <a v-on:click="clearImage" class="button is-neon-crimson"
          v-bind:class="{ 'is-static': isButtonFrozen }">
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
import { webFrame, clipboard } from "electron";
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
  inspect_msgbox: "",
  inspect_image_payload: [
    {'id': 'copy_image', 'name': "Copy Image", 'callback': copyImage},
    {'id': 'share_image', 'name': "Share Image", 'callback': shareImage},
    {'id': 'send_to', 'name': 'Send To', 'callback': sendTo},
  ],
  inspect_info_payload: [
    {'name': "Copy Info", 'callback': copyInfo}
  ]
};

function addInspectImagePayload(payloads) {
  let combined_payload = data.inspect_image_payload.concat(payloads);
  data.inspect_image_payload = combined_payload;
}

function removeInspectImagePayload(ids) {
  let filtered_payloads = data.inspect_image_payload.filter(payload => !ids.includes(payload.id));
  data.inspect_image_payload = filtered_payloads;
}

function formatShouter(event) {
  console.log("formatShouter");
  let format = data.info_data.general_info.format.value
  console.log(format);
}

function copyImage(event) {
  console.log("copyImage");
  console.log(event);
}

function shareImage(event) {
  console.log("shareImage")
}

function sendTo(even) {
  console.log("sendTo");
}

function copyInfo(event) {
  console.log("copyInfo");
  console.log(event);
  let text = event.srcElement.innerText;
  console.log(`text ${text}`);
  if (text)
    clipboard.writeText(text);
}

function clearMsgBox() {
  data.inspect_msgbox = "";
  removeInspectImagePayload(['format']);
}

function loadImage() {
  var options = {
    filters: extension_filters,
    properties: file_dialog_props,
  };
  dialog.showOpenDialog(mainWindow, options).then((result) => {
    let chosen_paths = result.filePaths;
    console.log(`chosen path: ${chosen_paths}`);
    if (chosen_paths === undefined || chosen_paths.length == 0) {
      return;
    }
    data.INS_IS_INSPECTING = true;
    console.log(chosen_paths);
    tridentEngine(["inspect-one", chosen_paths[0]], (error, res) => {
      if (error) {
        let error_data = JSON.parse(error);
        data.inspect_msgbox = error_data.error;
      }
      else {
        console.log(res);
        res = JSON.parse(res);
        console.log(res);
        if (res.data) {
          let res_data = res.data;
          data.info_data = res_data;
          // if (res_data.general_info || res_data.animation_info) {
            data.img_path = `${
              res_data.general_info.absolute_url.value
            }?timestamp=${randString()}`;
          // }
          addInspectImagePayload([{'id': 'format', 'name': 'Format', 'callback': formatShouter}])
        }
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
  clearMsgBox();
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
