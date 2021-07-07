<template>
  <div id="buildsprite_panel" class="container" style="display: none; padding:10px;">
    <table class="table is-borderless" style="padding: 5px;" width="100%">
      <tr>
        <td
          id="BSPR_sequence_cell"
          class="silver-bordered is-paddingless"
          style="width: 500px; height: 320px;"
        >
          <div style="display: block;">
            <table class="sequence-grid is-paddingless" width="100%">
              <tbody>
                <tr v-for="(quintjson, row) in BSPRQuintcellLister" v-bind:key="row">
                  <!-- <template v-for="(item, i) in quintjson"> -->
                    <!-- <template v-if="item == '_CONTROL_CELL'">
                      <td v-bind:key="i" class="force-center">
                        <table class="intracell-table" width="100%">
                          <tr>
                            <td width="50%" class="">
                              <a v-on:click="alert('ok')" class="button square-button is-medium flex-expand is-neon-emerald neon-borderless">
                                <span class="icon is-small">
                                  <i class="fas fa-image"></i>
                                </span>
                              </a>
                            </td>
                            <td class="">
                              <a v-on:click="alert('ok')" class="button square-button is-medium flex-expand is-neon-emerald neon-borderless">
                                <span class="icon is-small">
                                  <i class="fas fa-images"></i>
                                </span>
                              </a>
                            </td>
                          </tr>
                          <tr>
                            <td width="100%" colspan="2" class="">
                              <label class="label" title="The frame number in which new frames will be inserted after. Leave blank as default (insert new ones after the last on the existing sequence)">
                                Insert on</label>
                              <input class="input is-block-grey" title="The frame number in which new frames will be inserted after. Leave blank as default (insert new ones after the last on the existing sequence)"
                              type="text" placeholder="Type frame number"/>
                            </td>
                          </tr>
                        </table>
                      </td>
                    </template>
                    <template v-else> -->
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
                          <span class="index-anchor">
                            {{ parseInt(row) * 5 + parseInt(i) + 1 }}
                          </span>
                          <a class="del-anchor">
                            <span class="icon" v-on:click="removeFrame(parseInt(row) * 5 + parseInt(i))">
                              <i class="fas fa-minus-circle del-icon" v-on:click="removeFrame(parseInt(row) * 5 + parseInt(i))"></i>
                            </span>
                          </a>
                        </div>
                      </td>
                    <!-- </template> -->
                  <!-- </template> -->
                </tr>
              </tbody>
            </table>
          </div>
          <div
            class="force-center"
            style="display: none; vertical-align: middle;"
          >
            <div class="crt-aimg-container">
              <span class="aimg-helper"></span>
              <img/>
            </div>
          </div>
        </td>
        <td
          id="create_spritesheet_cell"
          class="silver-bordered force-center is-paddingless"
          style="width: 320px; height: 320px;"
          v-bind:class="{'has-checkerboard-bg': checkerbg_active}"
        >
          <div v-if="preview_info" v-bind:title="
            `Dimensions: ${preview_info.width.value} x ${preview_info.height.value}\n` +
            `File size: ${preview_info.fsize_hr.value}\n` +
            `Format: ${preview_info.format.value}\n` +
            `Mode: ${preview_info.color_mode.value}`
          " class="prev-spritesheet-container">
            <img v-bind:src="preview_path_cb" />
          </div>
        </td>
      </tr>
      <tr>
        <td class="is-hpaddingless">
          <nav class="level">
            <div class="level-left">
              <div class="level-item has-text-centered">
                <div class="field is-horizontal">
                  <div class="field-body">
                    <div class="field">
                      <div class="control">
                        <div class="select is-neon-cyan">
                          <select v-model="input_format">
                            <option value="sequence">Sequence</option>
                            <!-- <option value="aimg">From GIF/APNG</option> -->
                          </select>
                        </div>
                      </div>
                    </div>
                    <div class="field force-vcenter">
                      <a v-on:click="loadInput('insert')" class="button is-neon-emerald" v-bind:class="{'is-loading': BSPR_INSERT_LOAD, 'is-static': isButtonFrozen}"
                        title="Adds a new sequence of images">
                        <span class="icon is-small">
                          <i class="fas fa-plus"></i>
                        </span>
                        <span>Add</span>
                      </a>
                      <a v-on:click="loadInput('smart_insert')" class="button is-neon-emerald" v-bind:class="{'is-loading': BSPR_SMARTINSERT_LOAD, 'is-static': isButtonFrozen}"
                        title="Adds a new sequence of images from selecting a single image">
                        <span class="icon is-small">
                          <i class="fas fa-plus-circle"></i>
                        </span>
                        <span>Smart</span>
                      </a>
                      <div class="dualine-label">
                        <span>Insert<br/>after</span>
                      </div>
                      <input v-model="insert_index" v-on:keydown="numConstrain($event, true, true)" class="input is-neon-white" type="number" min="0" style="width: 70px;"
                      title="The frame number at which new sequence of images will be inserted after. Setting 0 will add the new sequence before the first frame, and leaving
                      this field empty is the default operation (append the new sequence after the last one)"/>
                      <a v-on:click="loadInput('replace')" class="button is-neon-emerald" v-bind:class="{'is-loading': BSPR_REPLACE_LOAD, 'is-static': isButtonFrozen}"
                      title="Loads multiple static images to create an animated image. This replaces the current sequence above">
                        <span class="icon is-small">
                          <i class="fas fa-times"></i>
                        </span>
                        <span>Load</span>
                      </a>
                      <a v-on:click="clearInfo" class="button is-neon-crimson" v-bind:class="{'is-static': isButtonFrozen}"
                      title="Clears the entire sequence">
                        <span class="icon is-small">
                          <i class="fas fa-times"></i>
                        </span>
                        <span>Clear</span>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
              <!-- <div class="level-item has-text-centered">
                <span class="force-vcenter">
                  {{ sequenceCounter }}
                </span>
              </div> -->
            </div>
          </nav>
        </td>
        <td class="is-hpaddingless">
          <nav class="level">
            <div class="level-item has-text-centered">
              <div>
              <a v-on:click="previewSheet" class="button is-neon-cyan" v-bind:class="{'is-loading': BSPR_IS_PREVIEWING, 'is-static': isButtonFrozen}">
                <span class="icon is-medium">
                  <i class="far fa-eye"></i>
                </span>
                <span>Preview</span>
              </a>
              
              <a v-on:click="BSPRToggleCheckerBG" class="button is-neon-white" v-bind:class="{'is-active': checkerbg_active}">
                <span class="icon is-medium">
                  <i class="fas fa-chess-board"></i>
                </span>
              </a>
              </div>
            </div>
            <!-- <div class="level-item has-text-centered">
              <div>
                <p v-if="sequence_count">{{ sequence_count }} images</p>
              </div>
            </div>
            <div class="level-item has-text-right">
              <div>
                <span v-if="sheetDimensions">Sheet dimensions: {{ sheetDimensions }}</span>
              </div>
            </div> -->
          </nav>
        </td>
      </tr>
      <tr>
        <td id="BSPR_create_control_table" class="silver-bordered is-paddingless" colspan="2">
          <div class="bspr-control-container">
            <table class="table spr-control-table" width="100%">
              <tr>
                <td width="20%">
                  <div class="field">
                    <label class="label">Name</label>
                    <div class="control">
                      <input v-model="name" class="input is-neon-white" type="text" />
                    </div>
                  </div>
                </td>
                <td width="20%">
                  <div class="field">
                    <label class="label">Tile Width</label>
                    <div class="control">
                      <input
                        v-bind:value="tile_width" v-on:keydown="wholeNumConstrain($event, true, true)" v-on:input="widthHandler(tile_width, $event)"
                        class="input is-neon-white"
                        type="number" 
                        min="1" step="1"/>
                    </div>
                  </div>
                </td>
                <td width="20%">
                  <div class="field">
                    <label class="label">Tile Height</label>
                    <div class="control">
                      <input
                        v-bind:value="tile_height" v-on:keydown="numConstrain($event, true, true)" v-on:input="heightHandler(tile_width, $event)"
                        class="input is-neon-white"
                        type="number"
                        min="1" step="1"
                      />
                    </div>
                  </div>
                </td>

                <td width="20%" style="vertical-align: bottom;">
                  <div class="field">
                    <label class="label">Max tiles per row</label>
                    <div class="control">
                      <input
                        v-model="tile_row"
                        class="input is-neon-white"
                        type="number"
                        min="1"
                        step="1"
                      />
                    </div>
                  </div>
                </td>

                <td width="20%">
                  <label class="checkbox">
                    <input v-model="lock_aspect_ratio" type="checkbox"/>
                    Lock aspect ratio
                  </label>
                  <br/>
                    <template v-if="aspect_ratio && aspect_ratio.text">
                      <input v-model="aspect_ratio.text" class="input is-border-colorless is-paddingless" style="height: 1.5em;" readonly="readonly"/>
                    </template>
                    <template v-else>&nbsp;</template>
                </td>
              </tr>
              <tr>
                
                <td>
                  <div class="field">
                    <label class="label">Offset X</label>
                    <div class="control">
                      <input
                        v-model="offset_x"
                        class="input is-neon-white"
                        type="number"
                        step="1"
                      />
                    </div>
                  </div>
                </td>

                <td>
                  <div class="field">
                    <label class="label">Offset Y</label>
                    <div class="control">
                      <input
                        v-model="offset_y"
                        class="input is-neon-white"
                        type="number"
                        step="1"
                      />
                    </div>
                  </div>
                </td>

                <td>
                  <div class="field">
                    <label class="label">Padding X</label>
                    <div class="control">
                      <input
                        v-model="padding_x"
                        class="input is-neon-white"
                        type="number"
                        step="1"
                      />
                    </div>
                  </div>
                </td>

                <td>
                  <div class="field">
                    <label class="label">Padding Y</label>
                    <div class="control">
                      <input
                        v-model="padding_y"
                        class="input is-neon-white"
                        type="number"
                        step="1"
                      />
                    </div>
                  </div>
                </td>

              </tr>
              <tr>
                <td colspan="3" style="padding-top: 15px;">
                  <div class="field has-addons">
                    <div class="control">
                      <a v-on:click="chooseOutDir" class="button is-neon-cyan">
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
                <td colspan="1" style="padding-top: 15px;">
                  <div class="field has-text-centered">
                    <div class="control">
                      <a v-on:click="buildSpritesheet" class="button is-neon-cyan" v-bind:class="{'is-loading': BSPR_IS_BUILDING, 'is-static': isButtonFrozen}">
                        Build Spritesheet
                      </a>
                    </div>
                  </div>
                </td>
                <td style="padding-top: 5px; line-height: 20px;">
                  <template v-if="sheetDimensions">
                    <span>Sheet dimensions</span>
                    <input v-model="sheetDimensions" class="input is-border-colorless is-paddingless" readonly="readonly"/>
                  </template>
                </td>
              </tr>
              <tr>
                <td colspan="5" class="has-text-left" style="vertical-align: middle;">
                  <input v-model="bspr_msgbox" type="text" class="input is-paddingless is-border-colorless" readonly="readonly"/>
                </td>
              </tr>
            </table>
          </div>
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
// const { client } = require("./Client.vue");
import { quintcellLister, GIF_DELAY_DECIMAL_PRECISION, randString, gcd, wholeNumConstrain,
  numConstrain, validateFilename, fileExists } from './api/utility';

function clearInfo() {
  data.image_paths = [],
  data.sequence_info = [];
  data.sequence_count = 0;
  // data.sequence_size = "";
  data.name = "";
  data.old_tile_width = "";
  data.tile_width = "";
  data.old_tile_height = "";
  data.tile_height = "";
  data.tile_row = "";
  data.outdir = "";
  data.bspr_msgbox = "";
  data.preview_path = "";
  data.preview_path_cb = "";
  data.preview_info = "";
  let ARData = {
    "w_ratio": "",
    "h_ratio": "",
    "text": "",
  };
  data.aspect_ratio = ARData;
}

var data = {
  image_paths: [],
  sequence_info: [],
  sequence_count: 0,
  insert_index: "",
  // sequence_size: "",
  input_format: "sequence",
  name: "",
  old_tile_width: "",
  tile_width: "",
  old_tile_height: "",
  tile_height: "",
  tile_row: "",
  outdir: "",
  offset_x: "",
  offset_y: "",
  padding_x: "",
  padding_y: "",
  preserve_alpha: true,
  preview_path: "",
  preview_path_cb: "",
  preview_info: "",
  aspect_ratio: "",
  lock_aspect_ratio: false,
  checkerbg_active: false,
  bspr_msgbox: "",
  BSPR_INSERT_LOAD: false,
  BSPR_SMARTINSERT_LOAD: false,
  BSPR_REPLACE_LOAD: false,
  BSPR_IS_LOADING: false,
  BSPR_IS_PREVIEWING: false,
  BSPR_IS_BUILDING: false,
};

let img_dialog_props = ["openfile"];
let sequence_dialog_props = ['openfile', 'multiSelections', 'createDirectory'];
let dir_dialog_props = ['openDirectory', 'createDirectory'];
let extension_filters = [{ name: 'Images', extensions: ['png', 'gif'] }];


function toggleLoadButtonAnim(ops, state=false) {
  if (ops == 'insert') {
    data.BSPR_INSERT_LOAD = state;
  }
  else if (ops == 'smart_insert') {
    data.BSPR_SMARTINSERT_LOAD = state;
  }
  else if (ops == 'replace') {
    data.BSPR_REPLACE_LOAD = state;
  }
}


function loadInput(ops) {
  console.log("bspr load image with ops:", ops);
  let props = ops == 'smart_insert'? img_dialog_props : sequence_dialog_props;
  let options = {
    filters: extension_filters,
    properties: props,
  }
  dialog.showOpenDialog(mainWindow, options, (img_paths) => {
    if (img_paths === undefined || img_paths.length == 0) { return; }
    if (data.input_format == "sequence") {
      loadSequence(img_paths, ops);
    }
  });
}

function loadSequence(img_paths, ops) {
  console.log('loading sequences...');
  data.BSPR_IS_LOADING = true;
  toggleLoadButtonAnim(ops, true);
  let pymethod = ops == 'smart_insert'? "inspect_smart" : "inspect_many";
  let paths = ops == 'smart_insert'? img_paths[0] : img_paths;
  client.invoke(pymethod, paths, (error, res) => {
    if (error) {
      console.error(error);
      data.bspr_msgbox = error;
      data.BSPR_IS_LOADING = false;
      toggleLoadButtonAnim(ops, false);
    }
    else {
      if (res && res.msg) {
        console.log('msg executed');
        data.bspr_msgbox = res.msg;
      }
      else if (res && res.data) { 
        let info = res.data;
        renderSequence(info, {operation: ops});
        // data.image_paths = info.sequence;
        // data.sequence_info = info.sequence_info;
        // data.sequence_size = `${info.total} image${info.total > 1 ? "s" : ""} (${info.size})`;
        data.name = info.name;
        data.tile_width = info.width;
        data.tile_height = info.height;
        data.tile_row = 5;
        data.sequence_count = info.total;
        updateAspectRatio(data.tile_width, data.tile_height);
        data.bspr_msgbox = "";
        data.BSPR_IS_LOADING = false;
        toggleLoadButtonAnim(ops, false);
      }
    }
  });
}

function renderSequence(pyinfo, options) {
  let operation = options.operation;
  if (operation == 'replace') {
    data.image = pyinfo.sequence;
    data.sequence_info = pyinfo.sequence_info;
    console.log("AA");
  }
  else if (['insert', 'smart_insert'].includes(operation)) {
    console.log("BB");
    if (data.insert_index) {
      data.image_paths.splice(data.insert_index, 0, ...pyinfo.sequence);
      data.sequence_info.splice(data.insert_index, 0, ...pyinfo.sequence_info);
    }
    else {
      data.image_paths.push(...pyinfo.sequence);
      data.sequence_info.push(...pyinfo.sequence_info);
    }
  }
}

function removeFrame(index) {
  data.image_paths.splice(index, 1);
  data.sequence_info.splice(index, 1);
}

function sequenceCounter() {
  if (data.sequence_info.length > 0) {
    return `${data.sequence_info.length} images`;
  }
  else return "";
}

function widthHandler(tile_width, event) {
  data.old_tile_width = parseInt(tile_width);
  console.log(event);
  let newWidth = event.target.value;
  data.tile_width = newWidth;
  if (data.lock_aspect_ratio && data.aspect_ratio.h_ratio > 0) { // Change height if lock_aspect_ratio is true and height is not 0
    console.log('sync aspect ratio');
    let raHeight = Math.round(newWidth / data.aspect_ratio.w_ratio * data.aspect_ratio.h_ratio);
    data.tile_height = raHeight > 0? raHeight : "";
  }
  else {
    updateAspectRatio(data.tile_width, data.tile_height);
  }
}

function heightHandler(tile_height, event) {
  data.old_tile_height = parseInt(tile_height);
  let newHeight = event.target.value;
  data.tile_height = newHeight;
  if (data.lock_aspect_ratio && data.aspect_ratio.w_ratio > 0) {
    let raWidth = Math.round(newHeight / data.aspect_ratio.h_ratio * data.aspect_ratio.w_ratio);
    console.log(raWidth);
    data.tile_width = raWidth > 0? raWidth : "";
  }
  else {
    updateAspectRatio(data.tile_width, data.tile_height);
  }
}

function updateAspectRatio(width, height) {
  if (data.tile_width && data.tile_height) {
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

function sheetDimensions() {
  console.log('compute final dimens called');
  let image_count = data.sequence_count;
  let x_count = Math.min(image_count, data.tile_row);
  let y_count = data.tile_row? Math.ceil(image_count / data.tile_row) : 0;
  let padding_x = data.padding_x? parseInt(data.padding_x) : 0;
  let padding_y = data.padding_y? parseInt(data.padding_y) : 0;
  let offset_x = data.offset_x? parseInt(data.offset_x) : 0;
  let offset_y = data.offset_y? parseInt(data.offset_y) : 0;
  console.log('xcount', x_count);
  console.log('ycount', y_count);
  let total_pad_x = x_count * 2 * padding_x - ((x_count + 1) * padding_x);
  let total_pad_y = y_count * 2 * padding_y - ((y_count + 1) * padding_y);
  console.log(data.tile_width, data.tile_height);
  console.log(total_pad_x, total_pad_y);
  let sheet_width = data.tile_width * x_count + offset_x + total_pad_x;
  let sheet_height = data.tile_height * y_count + offset_y + total_pad_y;
  console.log(sheet_width, sheet_height);
  if (sheet_width && sheet_height) {
    return `${sheet_width}x${sheet_height}`;
  }
  else return "";
}

function chooseOutDir() {
  var options = { properties: dir_dialog_props };
  dialog.showOpenDialog(mainWindow, options, (out_dirs) => {
    console.log(out_dirs);
    if (out_dirs && out_dirs.length > 0) {
      data.outdir = out_dirs[0];
    }
    data.bspr_msgbox = "";
  });
}

function BSPRQuintcellLister() {
  return quintcellLister(data.sequence_info);
}

function isButtonFrozen() {
  if (data.BSPR_IS_LOADING || data.BSPR_IS_PREVIEWING || data.BSPR_IS_BUILDING) return true;
  else return false;
}

function previewSheet() {
  data.BSPR_IS_PREVIEWING = true;
  let paths = null;
  if (data.input_format == 'sequence') { paths = data.image_paths; }
  console.log('paths...');
  console.log(paths);
  client.invoke("build_spritesheet", paths, './temp', data.name, data, (error, res) => {
    if (error) {
      console.error(error);
      data.bspr_msgbox = error;
      data.BSPR_IS_PREVIEWING = false;
      // mboxError(bspr_msgbox, error);
    } else {
      if (res) {
        console.log(res);
        if (res.msg) {
          data.bspr_msgbox = res.msg;
        }
        if (res.preview_path) {
          data.bspr_msgbox = "Obtaining preview spritesheet information...";
          console.log("Obtaining preview spritesheet information...");
          data.preview_path = res.preview_path;
          previewPathCacheBreaker();
        }
        if (res.CONTROL == "BSPR_FINISH") {
          console.log('timeout exhausted, invoking zerorpc...');
          client.invoke("inspect_one", data.preview_path, "static", (error, info) => {
            if (error) {
              console.error(error);
            } else {
              console.log("preview inspect");
              console.log(info);
              data.preview_info = info.general_info;
              data.bspr_msgbox = "Previewed!";
              data.BSPR_IS_PREVIEWING = false;
            }
          });
        }
      }
    }
  });
}

function buildSpritesheet() {
  let proceed_build = true;

  data.bspr_msgbox = "";
  var validator = validateFilename(data.name);
  if (!validator.valid) {
    console.error(validator.msg);
    data.bspr_msgbox = validator.msg;
    return;
  }

  if (fileExists(data.outdir, `${data.name}.png`)) {
    let WINDOW = remote.getCurrentWindow();
    let options = {
      buttons: ["Yes", "Cancel"],
      message: "A file with the same name already exists in the output folder. Do you want to override it?"
    };
    let response = dialog.showMessageBoxSync(WINDOW, options);
    if (response == 1) proceed_build = false;
  }

  if (proceed_build) {
    data.BSPR_IS_BUILDING = true;
    let paths = null;
    if (data.input_format == 'sequence') { paths = data.image_paths; }
    // else if (data.input_format == 'aimg') { paths = bspr_aimg_path_list; }
    client.invoke("build_spritesheet", paths, data.outdir, data.name, data, (error, res) => {
      if (error) {
        console.error(error);
        data.bspr_msgbox = error;
        data.BSPR_IS_BUILDING = false;
        // mboxError(bspr_msgbox, error);
      } else {
        if (res) {
          console.log(res);
          if (res.msg) {
            data.bspr_msgbox = res.msg;
          }
          if (res.CONTROL == "BSPR_FINISH") {
            data.bspr_msgbox = "Spritesheet built!";
            data.BSPR_IS_BUILDING = false;
          }
        }
      }
    });
  }
}

function BSPRToggleCheckerBG() {
  data.checkerbg_active = !data.checkerbg_active;
  console.log('now checkerbg is', data.checkerbg_active);
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
    loadInput: loadInput,
    chooseOutDir: chooseOutDir,
    removeFrame: removeFrame,
    clearInfo: clearInfo,
    previewSheet, previewSheet,
    wholeNumConstrain: wholeNumConstrain,
    numConstrain: numConstrain,
    widthHandler: widthHandler,
    heightHandler: heightHandler,
    buildSpritesheet: buildSpritesheet,
    BSPRToggleCheckerBG: BSPRToggleCheckerBG,
  },
  computed: {
    sequenceCounter: sequenceCounter,
    BSPRQuintcellLister: BSPRQuintcellLister,
    sheetDimensions: sheetDimensions,
    isButtonFrozen: isButtonFrozen,
  }
}
</script>
