<template>
  <div id="inspect_panel">
    <div class="inspect-panel-root">
      <div class="inspect-panel-display" >
        <!-- <div class="inspect-panel-image silver-bordered" @contextmenu="$emit('inspect-ctxmenu', $event, inspect_image_menu_options)" -->
        <div class="inspect-panel-image silver-bordered"
           v-bind:class="{'has-checkerboard-bg': checkerbg_active }"  v-cloak @drop.prevent="helidropFile" @dragover.prevent>
          <div v-if="load_has_error" class="inspect-panel-msgbox">
            <h2 class="is-2 is-crimson"><span class="icon is-large"><i class="fas fa-exclamation-circle fa-2x"></i></span></h2>
            <p class="is-left-paddingless is-border-colorless is-white-d">{{ inspect_msgbox }}</p>
          </div>
          <div v-else-if="inspect_msgbox === '' && img_path === ''" class="inspect-panel-hint">
            <h2 class="is-2 is-white-d"><span class="icon is-large"><i class="fas fa-file-upload fa-2x"></i></span></h2>
            <p class="is-border-colorless is-white-d">Drop your image here</p>
          </div>
          <img v-bind:src="escapeLocalPath(img_path)" v-show="inspect_msgbox === ''"/>
        </div>
        <div class="inspect-panel-info silver-bordered-no-left">
          <table v-if="info_data" class="table ins-info-table is-paddingless" width="100%">
            <template v-for="meta_categ in metadata_settings.categories">
            <!-- <template v-for="(meta_list, meta_categ) in info_data"> -->
              <!-- <span v-bind:key="key"/> -->
              <template v-if="info_data[meta_categ]">
                <tr :key="meta_categ">
                  <td colspan="2" class="is-cyan">{{ varToSpaceUpper(meta_categ) }}</td>
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
                    <td style="max-width: 369px; word-wrap: break-all">
                      {{ metadata_field.value? "Yes" : "No" }}
                    </td>
                  </template>
                  <template v-else-if="typeof metadata_field.value == 'number'">
                    <td style="max-width: 369px; word-wrap: break-all">
                      {{ roundPrecise(metadata_field.value, 3) }}
                      </td>
                  </template>
                  <template v-else>
                    <!-- <td style="max-width: 369px; word-wrap: break-all" @contextmenu="$emit('inspect-ctxmenu', $event, inspect_info_menu_options)"> -->
                    <td style="max-width: 369px; word-wrap: break-all">
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
          <span>Load Image</span>
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
const { webFrame, clipboard, ipcRenderer } = require("electron");
// const { client } = require("./Client.vue");
const { roundPrecise } = require("./modules/utility");
const { varToSpaceUpper, escapeLocalPath } = require("./modules/formatters");
const { tridentEngine } = require("./modules/tridentEngine");
const { SETTINGS } = require("./modules/config");
const { DIALOG_INSPECTING_EXT_FILTERS, INSPECTING_IMG_EXTS } = require("./modules/constants")
const mime = require("mime-types");


// var data = {
//   img_path: "",
//   checkerbg_active: false,
//   isButtonFrozen: false,
//   INS_IS_INSPECTING: false,
//   info_data: "",
//   inspect_msgbox: "",
//   load_has_error: false,
//   metadata_settings: SETTINGS.image_metadata,
//   inspect_image_menu_options: [
//     {'id': 'copy_image', 'name': "Copy Image", 'callback': copyImage},
//     {'id': 'share_image', 'name': "Share Image", 'callback': shareImage},
//     {'id': 'send_to', 'name': 'Send To', 'callback': sendTo},
//   ],
//   inspect_info_menu_options: [
//     {'name': "Copy Info", 'callback': copyInfo}
//   ],
// };


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



// function _inspectImage(image_path) {
//   this.INS_IS_INSPECTING = true;
//   console.log(image_path);
//   tridentEngine(["inspect_one", image_path], (error, res) => {
//     if (error) {
//       try {
//         this.load_has_error = true;
//         this.inspect_msgbox = error;
//         clearImage(); 
//         clearInfo();
//       }
//       catch (e) {
//         // data.split_msgbox = error;
//       }
//     }
//     else {
//       if (res.data) {
//         clearMsgBox();
//         let res_data = res.data;
//         this.info_data = res_data;
//         // if (res_data.general_info || res_data.animation_info) {
//         // data.img_path = `${
//         //   res_data.general_info.absolute_url.value
//         // }?timestamp=${randString()}`;
//         let localPath = res_data.general_info.absolute_url.value;
//         // To allow loading images with percent signs on their name.
//         this.img_path = localPath;
//         // }
//         addExtraCtxOptions([{'id': 'format', 'name': 'Format', 'callback': formatShouter}])
//       }
//     }
//     this.INS_IS_INSPECTING = false;
//   });
// }

// function loadImage() {
//   let dialog_options = {
//     filters: DIALOG_INSPECTING_EXT_FILTERS,
//     properties: ["openFile"],
//   };
  
//   ipcRenderer.invoke('open-dialog', dialog_options).then((result) => {
//   // dialog.showOpenDialog(mainWindow, options).then((result) => {
//     console.log(result);
//     let chosen_paths = result.filePaths;
//     console.log(`chosen path: ${chosen_paths}`);
//     if (chosen_paths === undefined || chosen_paths.length == 0) {
//       return;
//     }
//     _inspectImage(this, chosen_paths[0]);
    
//   })
//   .catch((err) => {
//     console.log(err);
//   });
// }



let vm = {
  data: function () {
    return {
      img_path: "",
      checkerbg_active: false,
      isButtonFrozen: false,
      INS_IS_INSPECTING: false,
      info_data: "",
      inspect_msgbox: "",
      load_has_error: false,
      metadata_settings: SETTINGS.image_metadata,
      inspect_image_menu_options: [
        {'id': 'copy_image', 'name': "Copy Image", 'callback': copyImage},
        {'id': 'share_image', 'name': "Share Image", 'callback': shareImage},
        {'id': 'send_to', 'name': 'Send To', 'callback': sendTo},
      ],
      inspect_info_menu_options: [
        {'name': "Copy Info", 'callback': copyInfo}
      ],
    };
  },
  methods: {
    loadImage() {
      let dialog_options = {
        filters: DIALOG_INSPECTING_EXT_FILTERS,
        properties: ["openFile"],
      };
      ipcRenderer.invoke('open-dialog', dialog_options).then((result) => {
      // dialog.showOpenDialog(mainWindow, options).then((result) => {
        console.log(result);
        let chosen_paths = result.filePaths;
        console.log(`chosen path: ${chosen_paths}`);
        if (chosen_paths === undefined || chosen_paths.length == 0) return;
        this._inspectImage(chosen_paths[0]);
      })
      .catch((err) => {
        console.log(err);
      });
    },
    _inspectImage (image_path) {
      this.INS_IS_INSPECTING = true;
      console.log(image_path);
      tridentEngine(["inspect_one", image_path], (error, res) => {
        if (error) {
          try {
            this.load_has_error = true;
            this.inspect_msgbox = error;
            clearImage(); 
            clearInfo();
          }
          catch (e) {
            // data.split_msgbox = error;
          }
        }
        else {
          if (res.data) {
            this.clearMsgBox();
            let res_data = res.data;
            this.info_data = res_data;
            // if (res_data.general_info || res_data.animation_info) {
            // data.img_path = `${
            //   res_data.general_info.absolute_url.value
            // }?timestamp=${randString()}`;
            let localPath = res_data.general_info.absolute_url.value;
            // To allow loading images with percent signs on their name.
            this.img_path = localPath;
            // }
            this._addExtraCtxOptions([{'id': 'format', 'name': 'Format', 'callback': formatShouter}])
          }
        }
        this.INS_IS_INSPECTING = false;
      });
    },
    clearButton() {
      this._clearImage(); 
      this._clearInfo();
      this.clearMsgBox();
    },
    _clearInfo() {
      this.info_data = "";
    },
    _clearImage() {
      this.img_path = "";
      this._removeExtraCtxOptions(['format']);
      webFrame.clearCache();
    },
    clearMsgBox() {
      this.load_has_error = false;
      this.inspect_msgbox = "";
    },
    _addExtraCtxOptions(payloads) {
      let combined_payload = this.inspect_image_menu_options.concat(payloads);
      this.inspect_image_menu_options = combined_payload;
    },
    _removeExtraCtxOptions(ids) {
      let filtered_payloads = this.inspect_image_menu_options.filter(payload => !ids.includes(payload.id));
      this.inspect_image_menu_options = filtered_payloads;
    },
    toggleCheckerBG() {
      this.checkerbg_active = !this.checkerbg_active;
      console.log("now checkerbg is", this.checkerbg_active);
    },
    varToSpaceUpper: varToSpaceUpper,
    roundPrecise: roundPrecise,
    escapeLocalPath: escapeLocalPath,
    helidropFile(e) {
      let droppedFiles = e.dataTransfer.files;
      console.log({"droppedFiles": droppedFiles})
      if (!droppedFiles || droppedFiles.length == 0) return;
      else if (droppedFiles.length > 1) console.error("error");
      else {
        let file = droppedFiles[0];
        console.log({a: INSPECTING_IMG_EXTS, r: file.type, b: mime.extension(file.type)});
        if (INSPECTING_IMG_EXTS.includes(mime.extension(file.type))) {
          console.log({exttee: file});
          this._inspectImage(file.path);
        }
        else {
          this.load_has_error = true;
          this.inspect_msgbox = "File is not an image, try loading a valid image file.";
        }
      }
    },
  },
};
export default vm;
</script>
