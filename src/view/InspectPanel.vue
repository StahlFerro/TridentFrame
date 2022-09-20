<template>
  <div id="inspect_panel">
    <div class="inspect-panel-root">
      <div class="inspect-panel-main-view">
        <div
          v-cloak class="inspect-panel-viewbox silver-bordered" 
          :class="{'has-checkerboard-bg': checkerBGIsActive }"
          @contextmenu="$emit('right-click', $event, imageContextMenuOptions)" 
          @drop.prevent="helidropFile" @dragenter.prevent @dragover.prevent
        >
          <div v-if="imageFilePath === ''" class="inspect-panel-hint">
            <h2 :class="[checkerBGIsActive? 'is-white-d' : 'is-white-d', 'is-border-colorless']">
              <span class="icon is-large"><font-awesome-icon icon="file-upload" size="2x" /></span>
            </h2>
            <p :class="[checkerBGIsActive? 'is-white-d' : 'is-white-d', 'is-border-colorless']">
              Drop your image here
            </p>
          </div>
          <div v-else class="inspect-panel-image">
            <img :src="escapeLocalPath(imageFilePath)" />
          </div>
        </div>
        <div class="inspect-panel-info silver-bordered-no-left">
          <table v-if="imageInfo" class="table ins-info-table is-paddingless" width="100%">
            <template v-for="attr_group in INSPECT_PANEL_SETTINGS.image_attributes">
              <!-- <template v-for="(meta_list, meta_categ) in imageInfo"> -->
              <!-- <span v-bind:key="key"/> -->
              <template v-if="imageInfo[attr_group.category]">
                <tr :key="attr_group.category">
                  <td colspan="2" class="is-cyan">
                    {{ attr_group.label }}
                  </td>
                </tr>
                <!-- <tr v-if="meta_categ == 'general_info'" :key="'general_info_' + meta_categ">
                  <td colspan="2" class="is-cyan">GENERAL INFO</td>
                </tr>
                <tr v-if="meta_categ == 'animation_info'" :key="'animation_info_' + meta_categ">
                  <td colspan="2" class="is-cyan">ANIMATION INFO</td>
                </tr> -->
                <tr
                  v-for="attribute in attr_group.attributes" 
                  :key="'Attribute$' + attr_group.category + '_' + attribute"
                  :set="attr_field = imageInfo[attr_group.category][attribute]"
                >
                  <td style="width: 123px">
                    <strong><span class="is-white-d">
                      {{ $t(`image_metadata.${attribute}`) }}
                    </span></strong>
                  </td>
                  <template v-if="attribute == 'loop_count' && attr_field.value == 0">
                    <td style="max-width: 369px; word-wrap: break-all">
                      Infinite
                    </td>
                  </template>
                  <!-- <template v-else-if="attribute == 'is_animated'">
                    <td style="max-width: 369px; word-wrap: break-all">{{ metadata_field.value? "Yes" : "No" }}</td>
                  </template>
                  <template v-else-if="attribute == 'delays_are_even'">
                    <td style="max-width: 369px; word-wrap: break-all">{{ delays_are_even.value? "Yes" : "No" }}</td>
                  </template> -->
                  <template v-else-if="typeof attr_field.value == 'boolean'">
                    <td style="max-width: 369px; word-wrap: break-all">
                      {{ attr_field.value? "Yes" : "No" }}
                    </td>
                  </template>
                  <template v-else-if="typeof attr_field.value == 'number'">
                    <td style="max-width: 369px; word-wrap: break-all">
                      {{ roundPrecise(attr_field.value, 3) }}
                    </td>
                  </template>
                  <template v-else>
                    <!-- <td style="max-width: 369px; word-wrap: break-all" @contextmenu="$emit('inspect-ctxmenu', $event, infoContextMenuOptions)"> -->
                    <td style="max-width: 369px; word-wrap: break-all">
                      {{ attr_field.value }}
                    </td>
                  </template>
                </tr>
              </template>
            </template>
          </table>
        </div>
      </div>
      <div class="inspect-panel-controls">
        <a
          class="button is-neon-emerald" :class="{
            'is-loading': INS_IS_INSPECTING,
            'non-interactive': isButtonFrozen,
          }"
          @click="loadImage"
        >
          <span class="icon is-small">
            <font-awesome-icon icon="plus" />
            <!-- <i class="fas fa-plus"></i> -->
          </span>
          <span>Load Image</span>
        </a>
        <a class="button is-neon-crimson" :class="{'non-interactive': isButtonFrozen}" @click="clearButton">
          <span class="icon is-small">
            <font-awesome-icon icon="times" />
            <!-- <i class="fas fa-times"></i> -->
          </span>
          <span>Clear</span>
        </a>
        <a
          class="button is-neon-white"
          :class="{ 'is-active': checkerBGIsActive }"
          @click="toggleCheckerBG"
          @click.middle.prevent="toggleCheckerBG"
          @contextmenu.prevent="toggleCheckerBG"
        >
          <span class="icon is-medium">
            <font-awesome-icon icon="chess-board" />
            <!-- <i class="fas fa-chess-board"></i> -->
          </span>
        </a>
      </div>
      <div class="inspect-panel-bottom-bar">
        <StatusBar :status-bar-id="statusBarId" />
      </div>
    </div>
  </div>
</template>

<script>
import { webFrame, clipboard, ipcRenderer } from "electron";
// const { client } from ("./Client.vue");
import { roundPrecise } from "../modules/utility/calculations";
import { varToSpaceUpper } from "../modules/utility/stringutils";
import { escapeLocalPath } from "../modules/utility/pathutils";
import { tridentEngine } from "../modules/streams/trident_engine";
// import { SETTINGS } from "../common/paths";
import { DIALOG_INSPECTING_EXT_FILTERS, INSPECTING_IMG_EXTS } from "../modules/constants/images";
import { extension as mime_extension } from "mime-types";

import StatusBar from "./components/StatusBar.vue";
import { EnumStatusLogLevel } from "../modules/constants/loglevels";
import { logStatus } from "../modules/events/statusBarEmitter";


export default {
  components: {
    StatusBar
  },
  emits: ['right-click', 'close-root-ctxmenu'],
  data: function () {
    return {
      imageFilePath: "",
      checkerBGIsActive: false,
      // isButtonFrozen: false,
      INS_IS_INSPECTING: false,
      imageInfo: {},
      // inspect_msgbox: "",
      imageContextMenuOptions: [
        {id: 'copy_image', name: "Copy Image"},
        {id: 'share_image', name: "Share Image"},
        {id: 'send_to', name: 'Send To'},
      ],
      infoContextMenuOptions: [
        {id: 'copy_info', name: "Copy Info", callback: this.cmCopyInfo}
      ],
      INSPECT_PANEL_SETTINGS: {},
      statusBarId: "inspectPanelStatusBar",
    };
  },
  computed: {
    isButtonFrozen() {
      return this.INS_IS_INSPECTING;
    }
  },
  beforeMount: function () {
    // ipcRenderer.invoke('reload-window-once');
    const SETTINGS = ipcRenderer.sendSync("IPC-GET-SETTINGS");
    this.INSPECT_PANEL_SETTINGS = { ...SETTINGS.inspect_panel };
    console.log(this);
  },
  mounted() {
    this.emitter.on('global-ctx-option-click-[copy_image]', args => {
      console.log('global-ctx-option-click-[copy_image] triggered!');
      this.$emit('close-root-ctxmenu');
    });
    
    this.emitter.on('global-ctx-option-click-[share_image]', args => {
      console.log('global-ctx-option-click-[share_image] triggered!');
      this.$emit('close-root-ctxmenu');
    });

    this.emitter.on('global-ctx-option-click-[send_to]', args => {
      console.log('global-ctx-option-click-[send_to] triggered!');
      this.$emit('close-root-ctxmenu');
    });

    this.emitter.on('global-ctx-option-click-[copy_info]', args => {
      console.log('global-ctx-option-click-[copy_info] triggered!');
      this.$emit('close-root-ctxmenu');
    });
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
    _inspectImage(image_path) {
      this._logProcessing(`Loading image ${image_path}`);
      this.INS_IS_INSPECTING = true;
      console.log(image_path);
      tridentEngine(["inspect_one", image_path], (err, res) => {
        if (err) {
          if (err.error) {
            this._logError(err.error);
            this._clearImage(); 
            this._clearInfo();
          }
          else if (err.warning) {
            this._logWarning(err.warning);
          }
        }
        else {
          if (res.data) {
            this._logClear();
            this._logSuccess("Image loaded.");
            this.imageInfo = res.data;
            // if (res_data.general_info || res_data.animation_info) {
            // data.imageFilePath = `${
            //   res_data.general_info.absolute_url.value
            // }?timestamp=${randString()}`;
            let localPath = this.imageInfo.general_info.absolute_url.value;
            // To allow loading images with percent signs on their name.
            this.imageFilePath = localPath;
            // }
            this._addExtraCtxOptions([{id: 'format', name: 'Format', callback: this.cmFormatShouter}]);
          }
        }
        this.INS_IS_INSPECTING = false;
      });
    },
    clearButton() {
      this._clearImage(); 
      this._clearInfo();
      this._logClear();
    },
    _clearInfo() {
      this.imageInfo = "";
    },
    _clearImage() {
      this.imageFilePath = "";
      this._removeExtraCtxOptions(['format']);
      webFrame.clearCache();
    },
    /**
     * Add extra options on the right click context menu. Automatically updates ones that already exist by id
     */
    _addExtraCtxOptions(options) {
      // let existing_options = this.imageContextMenuOptions.filter()
      console.debug(options);
      console.debug(this.imageContextMenuOptions);
      for (let opt of options){
        let exist_opt = this.imageContextMenuOptions.find(o => o.id == opt.id);
        console.debug("exist opt:");
        console.debug(exist_opt);
        if (exist_opt){
          /** 
           * TODO: For now do nothing if attempting to add a new option with the same id. In the future option updating with the same id must be supported.
           */
          // exist_opt = opt
        }
        else{
          this.imageContextMenuOptions.push(opt);
        }
      }
      // this.imageContextMenuOptions = menu_options;
      // let combined_payload = this.imageContextMenuOptions.concat(options);
      // this.imageContextMenuOptions = combined_payload;
    },
    _removeExtraCtxOptions(ids) {
      let remaining_options = this.imageContextMenuOptions.filter(payload => !ids.includes(payload.id));
      this.imageContextMenuOptions = remaining_options;
    },
    toggleCheckerBG(e) {
      console.debug(e);
      if (e.button == 0){
        this.checkerBGIsActive = !this.checkerBGIsActive;
        console.log("now checkerbg is", this.checkerBGIsActive);
      }
    },
    varToSpaceUpper: varToSpaceUpper,
    roundPrecise: roundPrecise,
    escapeLocalPath: escapeLocalPath,
    dragEnter(e) {
      console.warn("dragEnter");
      console.warn(e);
    },
    dragOver(e) {
      console.warn("dragOver");
      console.warn(e);
    },
    helidropFile(e) {
      let droppedFiles = e.dataTransfer.files;
      console.log({"droppedFiles": droppedFiles})
      if (!droppedFiles || droppedFiles.length == 0) return;
      else if (droppedFiles.length > 1) console.error("error");
      else {
        let file = droppedFiles[0];
        if (!file.path || file.path == '') return; /** NOTE: Do nothing if image already on the view panel is dragged and dropped back to the panel again */
        console.log({a: INSPECTING_IMG_EXTS, r: file.type, b: mime_extension(file.type)});
        if (INSPECTING_IMG_EXTS.includes(mime_extension(file.type))) {
          console.log({exttee: file});
          this._inspectImage(file.path);
        }
        else {
          // this.load_has_error = true;
          this._logError("File is not an image, try loading a valid image file.");
        }
      }
    },
    _logClear() {
      logStatus(this.statusBarId, EnumStatusLogLevel.CLEAR, null);
    },
    _logInfo(message) {
      logStatus(this.statusBarId, EnumStatusLogLevel.INFO, message);
    },
    _logProcessing(message) {
      logStatus(this.statusBarId, EnumStatusLogLevel.PROCESSING, message);
    },
    _logSuccess(message) {
      logStatus(this.statusBarId, EnumStatusLogLevel.SUCCESS, message);
    },
    _logWarning(message) {
      logStatus(this.statusBarId, EnumStatusLogLevel.WARNING, message);
    },
    _logError(message) {
      logStatus(this.statusBarId, EnumStatusLogLevel.ERROR, message);
    },
    cmFormatShouter(event) {
      console.log("cmFormatShouter");
      let format = this.imageInfo.general_info.format.value;
      console.log(format);
    }, 
    cmCopyImage(event) {
      console.log("cmCopyImage");
      console.log(event);
    },
    cmShareImage(event) {
      console.log("cmShareImage")
    },
    cmSendTo(event) {
      console.log("cmSendTo");
    },
    cmCopyInfo(event) {
      console.log("cmCopyInfo");
      console.log(event);
      let text = event.srcElement.innerText;
      console.log(`text ${text}`);
      if (text)
        clipboard.writeText(text);
    }
  },
};
</script>
