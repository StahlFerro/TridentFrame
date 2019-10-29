<template>
  <div id="create_panel" class="container" style="padding:10px;">
    <table class="table is-borderless" style="padding: 5px;" width="100%">
      <tr>
        <td
          id="CRT_sequence_cell"
          class="silver-bordered is-paddingless"
          style="width: 500px; height: 320px;"
        >
          <table class="sequence-grid is-paddingless" width="100%">
            <tbody>
              <tr v-for="(quintjson, row) in CRTQuintcellLister" v-bind:key="row">
                <td v-for="(item, i) in quintjson" v-bind:key="i" v-bind:title="
                      `Name: ${item.name.value}\n` + 
                      `Dimensions: ${item.width.value} x ${item.height.value}\n` +
                      `Format: ${item.format.value}\n` +
                      `Mode: ${item.color_mode.value}\n` +
                      `Comment: ${item.comments.value || 'None'}`
                    ">
                  <div class="seqdiv">
                    <!-- <span>{{ i }}</span><br/> -->
                    <img v-bind:src="item.absolute_url.value"/>
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
          <div v-if="preview_info" class="crt-aimg-container">
            <div v-bind:title="
              `Dimensions: ${preview_info.general_info.width.value} x ${preview_info.general_info.height.value}\n` +
              `File size: ${preview_info.general_info.fsize_hr.value}\n` +
              `Format: ${preview_info.general_info.format.value}`
            ">
              <span class="aimg-helper"></span>
              <img v-bind:src="preview_path_cb"/>
            </div>
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
                  <a v-on:click="CRTClearAIMG" class="button is-neon-white" v-bind:class="{'is-static': isButtonFrozen}">
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
                <a v-on:click="previewAIMG" class="button is-neon-cyan" v-bind:class="{'is-loading': CRT_IS_PREVIEWING, 'is-static': isButtonFrozen}">
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
                    <input v-bind:value="width" v-on:keydown="wholeNumberConstrain($event)" v-on:input="widthHandler(width, $event)" 
                    class="input is-neon-white" type="number" min="1" step="1"/>
                  </div>
                </div>
              </td>
              <td>
                <div class="field">
                  <label class="label">Height</label>
                  <div class="control">
                    <input v-bind:value="height" v-on:keydown="wholeNumberConstrain($event)" v-on:input="heightHandler(height, $event)"
                    class="input is-neon-white" type="number" />
                  </div>
                </div>
              </td>
              <td style="vertical-align: bottom;">
                <label class="checkbox">
                  <input v-model="lock_aspect_ratio" type="checkbox"/>
                  Lock aspect ratio
                </label>

                <label class="label">
                  <span v-if="aspect_ratio && aspect_ratio.text">{{ aspect_ratio.text }}</span>
                  <span v-else>&nbsp;</span>
                </label>
              </td>
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
</template>

<script>
const remote = require("electron").remote;
const dialog = remote.dialog;
const mainWindow = remote.getCurrentWindow();
const session = remote.getCurrentWebContents().session;
const { client } = require("./Client.vue");
import { quintcellLister, validateFilename, GIF_DELAY_DECIMAL_PRECISION, APNG_DELAY_DECIMAL_PRECISION, randString, gcd } from "./Utility.vue";

var data = {
  image_paths: [],
  sequence_info: [],
  name: "",
  fps: "",
  orig_width: "",
  old_width: "",
  orig_height: "",
  old_height: "",
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
  preview_path_cb: "",
  preview_info: "",
  aspect_ratio: "",
  lock_aspect_ratio: false,
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
    // console.log(img_paths);
    if (img_paths === undefined || img_paths.length == 0) { return; }
    data.CRT_IS_LOADING = true;
    client.invoke("inspect_many", img_paths, (error, res) => {
      if (error) {
        console.error(error);
        data.create_msgbox = error;
        data.CRT_IS_LOADING = false;
      } else {
        console.log(res);
        if (res && res.msg) {
          console.log('msg executed');
          data.create_msgbox = res.msg;
        }
        else if (res && res.data) {
          let info = res.data
          console.log('sequence info');
          console.log(info.sequence_info);
          data.image_paths = info.sequence;
          data.sequence_info = info.sequence_info;
          data.name = info.name;
          data.sequence_counter = `${info.total} image${info.total > 1 ? "s" : ""} (${info.size})`;
          data.orig_width = info.width;
          data.width = info.width;
          data.orig_height = info.height;
          data.height = info.height;
          data.fps = 50;
          data.delay = 0.02;
          data.create_msgbox = "";
          updateAspectRatio(data.width, data.height);
          data.CRT_IS_LOADING = false;
        }
      }
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
  data.sequence_info = [];
  data.preview_path = "";
  data.preview_path_cb = "";
  data.preview_info = "";
  data.name = "";
  data.delay = "";
  data.fps = "";
  data.orig_width = "";
  data.old_width = "";
  data.width = "";
  data.orig_height = "";
  data.old_height = "";
  data.height = "";
  data.CRT_sequence_counter = "";
  data.create_msgbox = "";
  data.sequence_counter = "";
  // mboxClear(create_msgbox);
  // deleteTempAIMG();
  // session.clearCache(testcallback);
}

function previewAIMG() {
  console.log("preview called");
  data.create_msgbox = "";
  var validator = validateFilename(data.name);
  if (!validator.valid) {
    console.error(validator.msg);
    data.create_msgbox = validator.msg;
    return;
  }
  data.CRT_IS_PREVIEWING = true;
  client.invoke("combine_image", data.image_paths, "./temp", data.name, data, (error, res) => {
    if (error) {
      console.error(error);
      data.create_msgbox = error;
      data.CRT_IS_PREVIEWING = false;
    } else {
      if (res) {
        if (res.msg) {
          console.log(res.msg);
          data.create_msgbox = res.msg;
        }
        if (res.preview_path) {
          data.preview_path = res.preview_path;
          previewPathCacheBreaker();
        }
        if (res.CONTROL == "FINISH") {
          setTimeout(function() {
            console.log('timeout exhausted, invoking zerorpc...');
            client.invoke("inspect_one", data.preview_path, "animated", (error, info) => {
              if (error) {
                console.error(error);
              } else {
                console.log("preview inspect");
                console.log(info);
                data.preview_info = info;
                data.create_msgbox = "Previewed!";
                data.BSPR_IS_PREVIEWING = false;
              }
            });
          });
          data.create_msgbox = "Previewed!"
          data.CRT_IS_PREVIEWING = false;
        }
      }
    }
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
  client.invoke("combine_image", data.image_paths, data.outdir, data.name, data, (error, res) => {
    if (error) {
      console.error(error);
      data.create_msgbox = error;
      data.CRT_IS_CREATING = false;
    } else {
      if (res) {
        console.log(res);
        if (res.msg) {
          data.create_msgbox = res.msg;
        }
        if (res.CONTROL == "FINISH") {
          data.create_msgbox = `${data.format.toUpperCase()} created!`;
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
  if (data.CRT_IS_LOADING || data.CRT_IS_PREVIEWING || data.CRT_IS_CREATING) return true;
  else return false;
}

// function getFPS() {
//   return Math.round(1/data.delay * 1000) / 1000;
// }

function wholeNumberConstrain(event) {
  console.log(event.key, event.key != ".");
  if (event.key != ".") {
    console.log("IS DIGIT!");
    return true;
  }
  else {
    console.log("IS NOT DIGIT!");
    event.preventDefault();
  }
}

function widthHandler(width, event) {
  data.old_width = parseInt(width);
  console.log(event);
  let newWidth = event.target.value;
  data.width = newWidth;
  if (data.lock_aspect_ratio && data.aspect_ratio.h_ratio > 0) { // Change height if lock_aspect_ratio is true and height is not 0
    let raHeight = Math.round(newWidth / data.aspect_ratio.w_ratio * data.aspect_ratio.h_ratio);
    data.height = raHeight > 0? raHeight : "";
  }
  else {
    updateAspectRatio(data.width, data.height);
  }
}

function heightHandler(height, $event) {
  data.old_height = parseInt(height);
  let newHeight = event.target.value;
  data.height = newHeight;
  if (data.lock_aspect_ratio && data.aspect_ratio.w_ratio > 0) {
    let raWidth = Math.round(newHeight / data.aspect_ratio.h_ratio * data.aspect_ratio.w_ratio);
    console.log(raWidth);
    data.width = raWidth > 0? raWidth : "";
  }
  else {
    updateAspectRatio(data.width, data.height);
  }
}

function updateAspectRatio(width, height) {
  if (data.width && data.height) {
    console.log('uAR', width, height);
    let divisor = gcd(width, height);
    let w_ratio = width / divisor;
    let h_ratio = height / divisor;
    let ARData = {
      "w_ratio": w_ratio,
      "h_ratio": h_ratio,
      "text": `${w_ratio}:${h_ratio}`,
    };
    console.log(ARData);
    data.aspect_ratio = ARData;
  }
}


function delayConstrain (event) {
  console.log("delay event", event);
  let value = event.target.value;
  if (value && value.includes(".")) {
    let numdec = value.split(".");
    console.log("numdec", numdec);
    let precision = 2;
    if (data.format == 'gif') {
      precision = GIF_DELAY_DECIMAL_PRECISION;
    }
    else if (data.format == 'apng') {
      precision = APNG_DELAY_DECIMAL_PRECISION;
    }
    if (numdec[1].length > precision) {
      let decs = numdec[1].substring(0, precision);
      console.log("decs limit triggered", decs);
      data.delay = `${numdec[0]}.${decs}`;
    }
  }
  data.fps = Math.round(1000 / data.delay) / 1000;
}

function fpsConstrain (event) {
  console.log("fps event", event);
  let value = event.target.value;
  if (value) {
    let mult = 100
    if (data.format == 'gif') { mult = 100; }
    else if (data.format == 'apng') { mult = 1000; }
    data.delay = Math.round(mult / data.fps) / mult;
  }
}

function CRTQuintcellLister() {
  return quintcellLister(data.sequence_info);
}

function previewPathCacheBreaker() {
  let cb_url = `${data.preview_path}?cachebreaker=${randString()}`;
  console.log("Cache breaker url", cb_url);
  data.preview_path_cb = cb_url;
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
    wholeNumberConstrain: wholeNumberConstrain,
    widthHandler: widthHandler,
    heightHandler: heightHandler,
    delayConstrain: delayConstrain,
    fpsConstrain: fpsConstrain,
  },
  computed: {
    CRTQuintcellLister: CRTQuintcellLister,
    isButtonFrozen: isButtonFrozen,
  },
};
</script>
