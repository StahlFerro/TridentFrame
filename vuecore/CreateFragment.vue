<template>
  <div id="create_panel" class="container" style="padding:10px;">
    <div class="content">
      <table class="table is-borderless" style="padding: 5px;" width="100%">
        <tr>
          <td
            id="CRT_sequence_cell"
            class="silver-bordered is-paddingless"
            style="width: 500px; height: 320px;"
          >
            <table class="sequence-grid is-paddingless" width="100%">
              <tbody>
                <tr v-for="(paths, row) in CRTQuintcellLister" v-bind:key="row">
                  <td v-for="path in paths" v-bind:key="path">
                    <div class="seqdiv">
                      <img v-bind:src="path"/>
                      <a class="del-anchor">
                        <span class="icon"><i class="fas fa-minus-circle del-icon"></i></span>
                      </a>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </td>
          <td
            id="create_aimg_cell"
            class="silver-bordered force-center is-paddingless"
            style="width: 320px; height: 320px;"
            v-bind:class="{'has-checkerboard-bg': checkerbg_active}">
            <div class="crt-aimg-container">
              <span class="aimg-helper"></span>
              <img v-bind:src="preview_path"/>
            </div>
          </td>
        </tr>
        <tr>
          <td class="is-hpaddingless">
            <nav class="level">
              <div class="level-left">
                <div class="level-item has-text-centered">
                  <div>
                    <a v-on:click="loadImages" class="button is-neon-cyan" v-bind:class="{'is-loading': CRT_IS_LOADING, 'is-static': isButtonFrozen}">
                      <span class="icon is-small">
                        <i class="fas fa-plus"></i>
                      </span>
                      <span>Load Images</span>
                    </a>
                    <a v-on:click="CRTClearAIMG" class="button is-neon-white">
                      <span class="icon is-small">
                        <i class="fas fa-trash-alt"></i>
                      </span>
                      <span>Clear</span>
                    </a>
                  </div>
                </div>
                <div class="level-item has-text-right">
                  <div>
                    <p>{{ sequence_counter }}</p>
                  </div>
                </div>
              </div>
            </nav>
          </td>
          <td class="has-text-left is-paddingless" style="vertical-align: middle;">
            <nav class="level">
              <div class="level-item has-text-centered">
                <div>
                  <a v-on:click="previewAIMG" class="button is-neon-white">
                    <span class="icon is-medium">
                      <i id="autoprev_icon" class="far fa-eye"></i>
                    </span>
                    <span>Preview</span>
                  </a>
                  <a v-on:click="CRTToggleCheckerBG" class="button is-neon-white" v-bind:class="{'is-active': checkerbg_active}">
                    <span class="icon is-medium">
                      <i class="fas fa-chess-board"></i>
                    </span>
                  </a>
                </div>
              </div>
            </nav>
          </td>
        </tr>
        <tr>
          <td id="CRT_control_cell" class="is-paddingless" colspan="2">
            <table class="table crt-control-table" width="100%">
              <tr>
                <td>
                  <div class="field">
                    <label class="label">Name</label>
                    <div class="control">
                      <input v-model="name" class="input is-neon-white" type="text" />
                    </div>
                  </div>
                </td>
                <td>
                  <div class="field">
                    <label class="label">Delay (seconds)</label>
                    <div class="control">
                      <input v-model="delay" v-on:input="delayConstrain" class="input is-neon-white" type="number" />
                    </div>
                  </div>
                </td>
                <td>
                  <div class="field">
                    <label class="label">Frame rate</label>
                    <div class="control">
                      <input v-model="fps" v-on:input="fpsConstrain" class="input is-neon-white" type="number" min="1" max="50" step="0.01"/>
                    </div>
                  </div>
                </td>
                <td style="vertical-align: bottom;">
                  <label class="checkbox" title="Preserve transparent pixels">
                    <input v-model="is_transparent" type="checkbox" />
                    Preserve Alpha
                  </label>
                  <br />
                  <label class="checkbox" title="Reverse the animation">
                    <input v-model="is_reversed" type="checkbox" />
                    Reversed
                  </label>
                </td>
              </tr>
              <tr>
                <td>
                  <div class="field">
                    <label class="label">Width</label>
                    <div class="control">
                      <input v-model="width" class="input is-neon-white" type="number" />
                    </div>
                  </div>
                </td>
                <td>
                  <div class="field">
                    <label class="label">Height</label>
                    <div class="control">
                      <input v-model="height" class="input is-neon-white" type="number" />
                    </div>
                  </div>
                </td>
                <td></td>
                <td style="vertical-align: bottom;">
                  <label class="checkbox">
                    <input v-model="flip_x" type="checkbox" />
                    Flip Horizontally
                  </label>
                  <br />
                  <label class="checkbox">
                    <input v-model="flip_y" type="checkbox" />
                    Flip Vertically
                  </label>
                </td>
              </tr>
              <tr>
                <td colspan="2" style="padding-top: 25px;">
                  <div class="field has-addons">
                    <div class="control">
                      <a class="button is-neon-cyan" v-on:click="CRTChooseOutdir">
                        <span class="icon is-small">
                          <i class="fas fa-folder-open"></i>
                        </span>
                        <span>Save to</span>
                      </a>
                    </div>
                    <div class="control is-expanded">
                      <input
                        v-model="outdir"
                        class="input is-neon-white"
                        type="text"
                        placeholder="Output folder"
                        readonly
                      />
                    </div>
                  </div>
                </td>
                <td colspan="1" style="padding-top: 25px;">
                  <div class="field">
                    <!-- <label class="label">Format</label> -->
                    <div class="control">
                      <div class="select is-neon-cyan">
                        <select v-model="format">
                          <option value="gif">GIF</option>
                          <option value="apng">APNG</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </td>
                <td colspan="1" style="padding-top: 25px;">
                  <div class="field has-text-centered">
                    <div class="control">
                      <a v-on:click="CRTCreateAIMG" class="button is-neon-cyan" 
                        v-bind:class="{'is-loading': CRT_IS_CREATING == true, 'is-static': isButtonFrozen}">Create</a>
                    </div>
                  </div>
                </td>
              </tr>
              <tr>
                <td colspan="4">
                  <div class="create-msgbox">
                    <span>{{ create_msgbox }}</span>
                  </div>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
const remote = require("electron").remote;
const dialog = remote.dialog;
const mainWindow = remote.getCurrentWindow();
const session = remote.getCurrentWebContents().session;
const { client } = require("./Client.vue");
import { quintcellLister, validateFilename, GIF_DELAY_DECIMAL_PRECISION } from "./Utility.vue";

var data = {
  image_paths: [],
  name: "",
  fps: "",
  orig_width: "",
  orig_height: "",
  width: "",
  height: "",
  delay: "",
  is_transparent: false,
  is_reversed: false,
  flip_x: false,
  flip_y: false,
  format: "gif",
  outdir: "",
  preview_path: "",
  create_msgbox: "",
  sequence_counter: "",
  checkerbg_active: false,
  CRT_IS_LOADING: false,
  CRT_IS_PREVIEWING: false,
  CRT_IS_CREATING: false,
}

let extension_filters = [{ name: "Images", extensions: ["png", "gif"] }];
let imgs_dialog_props = ["openfile", "multiSelections", "createDirectory"];
let dir_dialog_props = ["openDirectory", "createDirectory"];

function loadImages() {
  console.log("crt load image")
  var options = {
    filters: extension_filters,
    properties: imgs_dialog_props
  }
  dialog.showOpenDialog(mainWindow, options, (img_paths) => {
    console.log(img_paths);
    if (img_paths === undefined || img_paths.length == 0) { return; }
    data.CRT_IS_LOADING = true;
    client.invoke("inspect_sequence", img_paths, (error, res) => {
      if (error) {
        console.error(error);
        data.create_msgbox = error;
      } else {
        data.image_paths = res.sequence;
        data.name = res.name;
        data.sequence_counter = `${res.total} image${res.total > 1 ? "s" : ""} (${res.size} total)`;
        data.orig_width = res.width;
        data.width = res.width;
        data.orig_height = res.height;
        data.height = res.height;
        data.fps = 50;
        data.delay = 0.02;
        data.create_msgbox = "";
      }
      data.CRT_IS_LOADING = false;
    });
  });
}

function CRTChooseOutdir() {
  var options = { properties: dir_dialog_props };
  dialog.showOpenDialog(mainWindow, options, (out_dirs) => {
    console.log(out_dirs)
    if (out_dirs && out_dirs.length > 0) {
      console.log("folder selected");
      data.outdir = out_dirs[0];
      data.create_msgbox = "";
    }
  });
  // mboxClear(create_msgbox);
}

function CRTClearAIMG() {
  data.image_paths = [];
  data.name = "";
  data.delay = "";
  data.fps = "";
  data.orig_width = "";
  data.width = "";
  data.orig_height = "";
  data.height = "";
  data.CRT_sequence_counter = "";
  data.create_msgbox = "";
  data.sequence_counter = "";
  // mboxClear(create_msgbox);
  // deleteTempAIMG();
  // session.clearCache(testcallback);
}

function previewAIMG() {
  data.create_msgbox = "";
  var validator = validateFilename(data.name);
  if (!validator.valid) {
    console.error(validator.msg);
    data.create_msgbox = validator.msg;
    return;
  }
  client.invoke("combine_image", data, (error, res) => {

  });
}

function CRTCreateAIMG() {
  data.create_msgbox = "";
  var validator = validateFilename(data.name);
  if (!validator.valid) {
    console.error(validator.msg);
    data.create_msgbox = validator.msg;
    return;
  }
  data.CRT_IS_CREATING = true;
  // console.log(getFPS());
  client.invoke("combine_image", data.image_paths, data.outdir, data.name, data, (error, res) => {
    // console.log('createfragment fps', data.fps);
    if (error) {
      console.error(error);
      data.create_msgbox = error;
      // create_aimg_button.classList.remove('is-loading');
      data.CRT_IS_CREATING = false;
      // unfreezeButtons();
    } else {
      if (res) {
        if ("msg" in res) {
          console.log(res["msg"])
          data.create_msgbox = res["msg"]
            // mboxSuccess(create_msgbox, res["msg"]);
        }
        if (res["msg"] == "Finished!") {
            // create_aimg_button.classList.remove('is-loading');
            // unfreezeButtons();
          data.CRT_IS_CREATING = false;
        }
      }
    }
  });
}

function CRTToggleCheckerBG() {
  data.checkerbg_active = !data.checkerbg_active;
  console.log('now checkerbg is', data.checkerbg_active);
}

function isButtonFrozen() {
  if (data.CRT_IS_LOADING || data.CRT_IS_CREATING) return true;
  else return false;
}

// function getFPS() {
//   return Math.round(1/data.delay * 1000) / 1000;
// }

function delayConstrain (event) {
  console.log("delay event", event);
  var value = event.target.value;
  if (value && value.includes(".")) {
    var numdec = value.split(".");
    console.log("numdec", numdec);
    if (numdec[1].length > GIF_DELAY_DECIMAL_PRECISION) {
      var twodecs = numdec[1].substring(0, GIF_DELAY_DECIMAL_PRECISION);
      console.log("twodecs limit triggered", twodecs);
      data.delay = `${numdec[0]}.${twodecs}`;
    }
  }
  data.fps = Math.round(1000 / data.delay) / 1000;
}

function fpsConstrain (event) {
  console.log("fps event", event);
  var value = event.target.value;
  if (value) {
    data.delay = Math.round(100 / data.fps) / 100;
  }
}

function CRTQuintcellLister() {
  return quintcellLister(data.image_paths);
}

export default {
  data: function() {
    return data;
  },
  methods: {
    loadImages: loadImages,
    CRTClearAIMG: CRTClearAIMG,
    CRTChooseOutdir: CRTChooseOutdir,
    previewAIMG: previewAIMG,
    CRTCreateAIMG: CRTCreateAIMG,
    CRTToggleCheckerBG: CRTToggleCheckerBG,
    delayConstrain: delayConstrain,
    fpsConstrain: fpsConstrain,
  },
  computed: {
    CRTQuintcellLister: CRTQuintcellLister,
    isButtonFrozen: isButtonFrozen,
  },
};
</script>
