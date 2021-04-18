<template>
  <div id="inspect_panel">
    <div class="inspect-panel-root">
      <div class="inspect-panel-display" >
        <div class="inspect-panel-image silver-bordered" @contextmenu="$emit('inspect-ctxmenu', $event, inspect_image_menu_options)">
          <div class="inspect-panel-msgbox" v-show="inspect_msgbox !== ''">
            <p class="is-left-paddingless is-border-colorless is-white-d">{{ inspect_msgbox }}</p>
          </div>
          <img v-bind:src="img_path" v-show="inspect_msgbox === ''"/>
        </div>
        <div class="inspect-panel-info silver-bordered-no-left">
          <table v-if="info_data" class="table ins-info-table is-paddingless" width="100%">
            <template v-for="meta_categ in metadata_settings.categories">
            <!-- <template v-for="(meta_list, meta_categ) in info_data"> -->
              <!-- <span v-bind:key="key"/> -->
              <template v-if="info_data[meta_categ]">
                <tr :key="meta_categ">
                  <td colspan="2" class="is-cyan">{{ headerMetaCategory(meta_categ) }}</td>
                </tr>
                <!-- <tr v-if="meta_categ == 'general_info'" :key="'general_info_' + meta_categ">
                  <td colspan="2" class="is-cyan">GENERAL INFO</td>
                </tr>
                <tr v-if="meta_categ == 'animation_info'" :key="'animation_info_' + meta_categ">
                  <td colspan="2" class="is-cyan">ANIMATION INFO</td>
                </tr> -->
                <tr v-for="attribute in metadata_settings.attributes[meta_categ]" 
                    :set="metadata_field = info_data[meta_categ][attribute]"
                    :key="'iprop_' + meta_categ + '_' + attribute">
                  <td style="width: 123px">
                    <strong><span class="is-white-d">{{ metadata_field.label }}</span></strong>
                  </td>
                  <template v-if="attribute == 'loop_count' && metadata_field.value == 0">
                    <td style="max-width: 369px; word-wrap: break-all">Infinite</td>
                  </template>
                  <!-- <template v-else-if="attribute == 'is_animated'">
                    <td style="max-width: 369px; word-wrap: break-all">{{ metadata_field.value? "Yes" : "No" }}</td>
                  </template>
                  <template v-else-if="attribute == 'delays_are_even'">
                    <td style="max-width: 369px; word-wrap: break-all">{{ delays_are_even.value? "Yes" : "No" }}</td>
                  </template> -->
                  <template v-else-if="typeof metadata_field.value == 'boolean'">
                    <td style="max-width: 369px; word-wrap: break-all">{{ metadata_field.value? "Yes" : "No" }}</td>
                  </template>
                  <template v-else-if="typeof metadata_field.value == 'number'">
                    <td style="max-width: 369px; word-wrap: break-all">{{ roundPrecise(metadata_field.value, 3) }}</td>
                  </template>
                  <template v-else>
                    <td style="max-width: 369px; word-wrap: break-all" @contextmenu="$emit('inspect-ctxmenu', $event, inspect_info_menu_options)">
                      {{ metadata_field.value }}
                    </td>
                  </template>
                </tr>
              </template>
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
        <a v-on:click="clearButton" class="button is-neon-crimson"
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
const { roundPrecise } = require("./Utility.vue");
const { tridentEngine, settings } = require("./PythonCommander.vue");

let extension_filters = [
  {
    name: "Images",
    extensions: ["png", "gif", "jpg"],
  },
];
let file_dialog_props = ["openfile"];
let dir_dialog_props = ["openDirectory", "createDirectory"];

let metadata_order = settings.image_metadata

var data = {
  img_path: "",
  checkerbg_active: false,
  isButtonFrozen: false,
  INS_IS_INSPECTING: false,
  info_data: "",
  inspect_msgbox: "",
  metadata_settings: settings.image_metadata,
  inspect_image_menu_options: [
    {'id': 'copy_image', 'name': "Copy Image", 'callback': copyImage},
    {'id': 'share_image', 'name': "Share Image", 'callback': shareImage},
    {'id': 'send_to', 'name': 'Send To', 'callback': sendTo},
  ],
  inspect_info_menu_options: [
    {'name': "Copy Info", 'callback': copyInfo}
  ],
};

console.table(data.metadata_settings)

function addExtraCtxOptions(payloads) {
  let combined_payload = data.inspect_image_menu_options.concat(payloads);
  data.inspect_image_menu_options = combined_payload;
}

function removeExtraCtxOptions(ids) {
  let filtered_payloads = data.inspect_image_menu_options.filter(payload => !ids.includes(payload.id));
  data.inspect_image_menu_options = filtered_payloads;
}

function formatShouter(event) {
  console.log("formatShouter");
  let format = data.info_data.general_info.format.value;
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
}

function headerMetaCategory(meta_categ) {
  return meta_categ.replace("_", " ").toUpperCase();
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
    tridentEngine(["inspect_one", chosen_paths[0]], (error, res) => {
      if (error) {
        try {
          // console.error(error);
          let error_data = JSON.parse(error);
          data.inspect_msgbox = error_data.error;
          clearImage(); 
          clearInfo();
        }
        catch (e) {
          // data.split_msgbox = error;
        }
      }
      else {
        console.log(res);
        res = JSON.parse(res);
        console.log(res);
        if (res.data) {
          clearMsgBox();
          let res_data = res.data;
          data.info_data = res_data;
          // if (res_data.general_info || res_data.animation_info) {
          // data.img_path = `${
          //   res_data.general_info.absolute_url.value
          // }?timestamp=${randString()}`;
          let localPath = res_data.general_info.absolute_url.value;
          // To allow loading images with percent signs on their name.
          localPath = localPath.replace("%", "%25");
          data.img_path = localPath;
          // }
          addExtraCtxOptions([{'id': 'format', 'name': 'Format', 'callback': formatShouter}])
        }
      }
      data.INS_IS_INSPECTING = false;
    });
  })
  .catch((err) => {
    console.log(err);
  });
}

function clearButton() {
  clearImage(); 
  clearInfo();
  clearMsgBox();
}

function clearInfo() {
  data.info_data = "";
}

function clearImage() {
  data.img_path = "";
  removeExtraCtxOptions(['format']);
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
    // clearImage: clearImage,
    // clearInfo: clearInfo,
    clearButton: clearButton,
    toggleCheckerBG: toggleCheckerBG,
    headerMetaCategory: headerMetaCategory,
    roundPrecise: roundPrecise,
  },
};
</script>
