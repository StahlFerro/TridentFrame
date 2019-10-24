<template>
  <div id="modify_panel" class="container" style="display: none; padding:10px;">
    <!-- <div class="content"> -->
    <table class="table is-borderless" style="padding: 5px;" width="100%">
      <tr>
        <!-- <td width="3%"></td> -->
        <td width="35%"
          colspan="3"
          class="silver-bordered force-center is-paddingless"
          v-bind:class="{'has-checkerboard-bg': orig_checkerbg_active}"
          style="height: 250px;">
          <div class="mod-aimg-container">
            <span class="aimg-helper"></span>
            <img v-bind:src="orig_path" />
          </div>
          <!-- <input id="MOD_orig_path" name="MOD_orig_path_field" type="hidden" value /> -->
        </td>
        <!-- <td width="3%"></td> -->

        <td width="6%"></td>
        <td width="9%"></td>
        <td width="35%"
          class="silver-bordered force-center is-paddingless"
          v-bind:class="{'has-checkerboard-bg': new_checkerbg_active}"
          style="height: 250px;">
          <div class="mod-aimg-container">
            <span class="aimg-helper"></span>
            <img v-bind:src="preview_path" />
          </div>
        </td>
        <td colspan="2" width="15%">
          <span v-if="preview_size">
            Preview size:<br/>{{ preview_size_hr }}<br/>
            ({{ previewSizePercentage }}% of original)
            </span>
        </td>
      </tr>
      <tr>
        <td colspan="3" class="has-text-centered is-hpaddingless">
          <a v-on:click="loadImage" class="button is-neon-cyan" v-bind:class="{'is-loading': MOD_IS_LOADING, 'is-static': buttonIsFrozen}">
            <span class="icon is-small">
              <i class="fas fa-plus"></i>
            </span>
            <span>Load GIF/APNG</span>
          </a>
          <a v-on:click="clearImage" class="button is-neon-white">
            <span class="icon is-small">
              <i class="fas fa-trash-alt"></i>
            </span>
            <span>Clear</span>
          </a>
          <a v-on:click="toggleOrigCheckerBG" class="button is-neon-white"
            v-bind:class="{'is-active': orig_checkerbg_active}">
            <span class="icon is-medium">
              <i class="fas fa-chess-board"></i>
            </span>
          </a>
        </td>
        <td colspan="2">
        </td>
        <td class="has-text-centered is-hpaddingless">
          <a v-on:click="previewModImg" class="button is-neon-cyan" v-bind:class="{'is-loading': MOD_IS_PREVIEWING, 'is-static': buttonIsFrozen}">
            <span class="icon is-small">
              <i class="fas fa-eye"></i>
            </span>
            <span>Preview</span>
          </a>
          <a v-on:click="clearPrevImage" class="button is-neon-white">
            <span class="icon is-small">
              <i class="fas fa-trash-alt"></i>
            </span>
            <span>Clear</span>
          </a>
          <a v-on:click="toggleNewCheckerBG" class="button is-neon-white"
            v-bind:class="{'is-active': new_checkerbg_active}">
            <span class="icon is-medium">
              <i class="fas fa-chess-board"></i>
            </span>
          </a>
        </td>
        <td colspan="2">
        </td>
      </tr>
      <tr>
        <td style="width: 285px; height: 275px;" colspan="3" class="is-paddingless silver-bordered">
          <div class="mod-orig-info-container">
            <table class="table mod-orig-info-table is-hpaddingless">
              <tbody>
                <tr>
                  <td class="mod-info-label is-cyan">Name</td>
                  <td class="mod-info-data">{{ orig_name }}</td>
                </tr>
                <tr>
                  <td class="mod-info-label is-cyan">Dimensions</td>
                  <td class="mod-info-data">{{ origDimensions }}</td>
                </tr>
                <tr>
                  <td class="mod-info-label is-cyan">File size</td>
                  <td class="mod-info-data">{{ orig_file_size_hr }}</td>
                </tr>
                <tr>
                  <td class="mod-info-label is-cyan">Format</td>
                  <td class="mod-info-data">{{ orig_format }}</td>
                </tr>
                <tr>
                  <td class="mod-info-label is-cyan">Total frames</td>
                  <td class="mod-info-data">{{ orig_frame_count }}</td>
                </tr>
                <tr>
                  <td class="mod-info-label is-cyan">Frame rate</td>
                  <td class="mod-info-data">{{ orig_fps }}</td>
                </tr>
                <tr>
                  <td class="mod-info-label is-cyan">Frame delay</td>
                  <td class="mod-info-data">{{ orig_delay_info }}</td>
                </tr>
                <tr>
                  <td class="mod-info-label is-cyan">Loop duration</td>
                  <td class="mod-info-data">{{ orig_loop_duration }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </td>
        <td style="width: 581px; height: 275px;" colspan="5"
          class="has-text-centered is-right-paddingless silver-bordered-left-thicc">
          <table class="table is-paddingless is-marginless" width="100%">
            <tr>
              <td width="10%" class="mod-menu-cell is-paddingless">
                <div class="mod-left-menu">
                  <aside class="menu has-text-centered" style="margin: 0;">
                    <ul class="menu-list mod-left-menu">
                      <li id="MOD_box_general" class="mod-menu-item"
                        v-bind:class="{'is-selected': mod_menuselection == 0}">
                        <a id="MOD_menu_general" v-on:click="mod_menuselection = 0">
                          <span class="icon is-large">
                            <i class="fas fa-image fa-2x fa-inverse"></i>
                          </span>
                          <p class="is-white-d">General</p>
                        </a>
                      </li>
                      <li id="MOD_box_gif" class="mod-menu-item"
                        v-bind:class="{'is-selected': mod_menuselection == 1}">
                        <a id="MOD_menu_gif" v-on:click="mod_menuselection = 1">
                          <span class="icon is-large">
                            <i class="far fa-images fa-2x fa-inverse"></i>
                          </span>
                          <p class="is-white-d is-large">GIF</p>
                        </a>
                      </li>
                    </ul>
                  </aside>
                </div>
              </td>
              <td width="90%" class="is-paddingless">
                <div v-show="mod_menuselection == 0">
                  <table class="table mod-new-control-table is-hpaddingless" width="100%">
                    <tr>
                      <td width="40%" colspan="2">
                        <div class="field">
                          <label class="label">Name</label>
                          <div class="control">
                            <input v-model="name" class="input is-neon-white" type="text" />
                          </div>
                        </div>
                      </td>
                      <td width="20%">
                        <div class="field">
                          <label class="label">Width</label>
                          <div class="control">
                            <input v-model="width" class="input is-neon-white" type="text" />
                          </div>
                        </div>
                      </td>
                      <td width="20%">
                        <div class="field">
                          <label class="label">Height</label>
                          <div class="control">
                            <input v-model="height" class="input is-neon-white" type="text" />
                          </div>
                        </div>
                      </td>
                      <td width="20%">
                        <div class="field">
                          <label class="label">Rotation</label>
                          <div class="control">
                            <input v-model="rotation" class="input is-neon-white" type="number" />
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td width="20%">
                        <div class="field">
                          <label class="label">FPS</label>
                          <div class="control">
                            <input v-model="fps" v-on:input="fpsConstrain" class="input is-neon-white" type="number" />
                          </div>
                        </div>
                      </td>
                      <td width="20%">
                        <div class="field">
                          <label class="label">Delay</label>
                          <div class="control">
                            <input v-model="delay" v-on:input="delayConstrain" class="input is-neon-white" type="number" />
                          </div>
                        </div>
                      </td>
                      <td width="20%">
                        <div class="field">
                          <label class="label">Skip Frames</label>
                          <div class="control">
                            <input v-model="skip_frame" class="input is-neon-white" type="number" min="0"/>
                          </div>
                        </div>
                      </td>
                      <td width="20%"></td>
                      <td width="20%">
                        <div class="field">
                          <label class="label">Format</label>
                          <div class="control">
                            <div class="select is-neon-cyan">
                              <select v-model="format">
                                <option value="GIF">GIF</option>
                                <option value="APNG">APNG</option>
                              </select>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td width="20%" class="force-vcenter">
                        <label class="checkbox" title="Flip the image horizontally">
                          <input v-model="flip_x" type="checkbox" />
                          Flip X
                        </label>
                        <label class="checkbox" title="Flip the image vertically">
                          <input v-model="flip_y" type="checkbox" />
                          Flip Y
                        </label>
                      </td>
                      <td width="40%" class="force-vcenter" colspan="2">
                        <label class="checkbox" title="Reverse the animation">
                          <input v-model="is_reversed" type="checkbox" />
                          Reversed
                        </label>
                        <label class="checkbox" title="Preserve transparent pixels">
                          <input v-model="preserve_alpha" type="checkbox" />
                          Preserve Alpha
                        </label>
                      </td>
                    </tr>
                    <tr>
                      <td colspan="4">
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
                            <input v-model="outdir"
                              class="input is-neon-white"
                              type="text"
                              placeholder="Output folder"
                              readonly
                            />
                          </div>
                        </div>
                      </td>
                      <td>
                        <a v-on:click="modifyImage" class="button is-neon-cyan"  v-bind:class="{'is-loading': MOD_IS_MODIFYING, 'is-static': buttonIsFrozen}">
                          MODIFY</a>
                      </td>
                    </tr>
                  </table>
                </div>
                <div v-show="mod_menuselection == 1">
                  <GIFOptimizationTable 
                    :is_optimized.sync="is_optimized"
                    :optimization_level.sync="optimization_level"
                    :is_lossy.sync="is_lossy"
                    :lossy_value.sync="lossy_value"
                    :is_reduced_color.sync="is_reduced_color"
                    :color_space.sync="color_space"
                  />
                </div>
              </td>
            </tr>
          </table>
        </td>
      </tr>
      <tr>
        <td colspan="8" class="has-text-left" style="vertical-align: middle;">
          {{ modify_msgbox }}
        </td>
      </tr>
    </table>
    <!-- </div> -->
  </div>
</template>

<script>

const remote = require('electron').remote;
const dialog = remote.dialog;
const mainWindow = remote.getCurrentWindow();
const session = remote.getCurrentWebContents().session;
const { client } = require('./Client.vue');
const { GIF_DELAY_DECIMAL_PRECISION, ticks } = require("./Utility.vue");
import GIFOptimizationTable from "./vueshards/GIFOptimizationTable.vue";


var data = {
  orig_name: "-",
  orig_width: "",
  orig_height: "",
  orig_frame_count: "-",
  orig_fps: "-",
  orig_delay: "",
  orig_delay_info: "-",
  orig_loop_duration: "-",
  orig_file_size: "",
  orig_file_size_hr: "-",
  orig_format: "-",
  orig_path: "",
  name: "",
  width: "",
  height: "",
  rotation: "",
  fps: "",
  delay: "",
  format: "GIF",
  skip_frame: "",
  flip_x: false,
  flip_y: false,
  is_reversed: false,
  preserve_alpha: false,
  is_optimized: false,
  optimization_level: "1",
  is_lossy: false,
  lossy_value: "",
  is_reduced_color: false,
  color_space: "",
  preview_path: "",
  outdir: "",
  preview_size: "",
  preview_size_hr: "",
  mod_menuselection: 0,
  orig_checkerbg_active: false,
  new_checkerbg_active: false,
  MOD_IS_LOADING: false,
  MOD_IS_MODIFYING: false,
  MOD_IS_PREVIEWING: false,
  modify_msgbox: "",
};

function clearOrigFields() {
  data.orig_name = "-";
  data.orig_width = "";
  data.orig_height = "";
  data.orig_frame_count = "-";
  data.orig_fps = "-";
  data.orig_delay = "";
  data.orig_delay_info = "-";
  data.orig_loop_duration = "-";
  data.orig_file_size = "-";
  data.orig_format = "-";
  data.orig_path = "";
}

function clearNewFields() {
  data.name = "";
  data.width = "";
  data.height = "";
  data.rotation = "";
  data.fps = "";
  data.delay = "";
  data.skip_frame = "";
  data.preview_path = "";  
}

function toggleOrigCheckerBG() {
  data.orig_checkerbg_active = !data.orig_checkerbg_active;
  console.log("orig checkerbg is", data.orig_checkerbg_active);
}

function toggleNewCheckerBG() {
  data.new_checkerbg_active = !data.new_checkerbg_active;
  console.log("new checkerbg is", data.new_checkerbg_active);
}

let extension_filters = [
    { name: 'Images', extensions: ['png', 'gif'] },
];
let file_dialog_props = ['openfile'];
let dir_dialog_props = ['openDirectory', 'createDirectory'];

function loadImage() {
  console.log("mod load image called");
  var options = {
    filters: extension_filters,
    properties: file_dialog_props
  };
  dialog.showOpenDialog(mainWindow, options, (chosen_path) => {
    console.log(`chosen path: ${chosen_path}`);
    if (chosen_path === undefined || chosen_path.length == 0) {
      return;
    }
    data.MOD_IS_LOADING = true;
    client.invoke("inspect_one", chosen_path[0], "animated", (error, res) => {
      if (error) {
        console.error(error);
        data.modify_msgbox = error;
        // mboxError(modify_msgbox, error);
      } else {
        loadOrigInfo(res);
        loadNewInfo(res);
        data.modify_msgbox = "";
      }
      data.MOD_IS_LOADING = false;
    });
    console.log("registered!");
  });
}

function loadOrigInfo(res) {
  let geninfo = res.general_info;
  let ainfo = res.animation_info;
  data.orig_name = geninfo.name.value;
  data.orig_width = geninfo.width.value;
  data.orig_height = geninfo.height.value;
  data.orig_fps = `${ainfo.fps.value} fps`;
  data.orig_frame_count= `${ainfo.frame_count.value} (${ainfo.frame_count_ds.value} DS)`;
  data.orig_format = geninfo.format.value;
  let delay_info = `${ainfo.avg_delay.value} seconds`;
  if (ainfo.delay_is_uneven) {
      delay_info += ` (uneven)`;
  }
  data.orig_delay = ainfo.avg_delay.value;
  data.orig_delay_info = delay_info;
  data.orig_loop_duration = `${ainfo.loop_duration.value} seconds`;
  data.orig_path = geninfo.absolute_url.value;
  data.orig_file_size = geninfo.fsize.value;
  data.orig_file_size_hr = geninfo.fsize_hr.value;
}

function loadNewInfo(res) {
  var geninfo = res.general_info;
  var ainfo = res.animation_info;
  console.log(geninfo);
  console.log(ainfo);
  data.name = geninfo.base_fname.value;
  data.format = geninfo.format.value;
  data.width = geninfo.width.value;
  data.height = geninfo.height.value;
  data.delay = ainfo.avg_delay.value;
  data.fps = ainfo.fps.value;
}


function clearImage() {
  console.log(data);
  clearOrigFields();
  clearNewFields();
}

function clearPrevImage() {
  data.preview_path = "";
  data.preview_size = "";
  data.preview_size_hr = "";
}

function chooseOutDir() {
  var options = { properties: dir_dialog_props };
  dialog.showOpenDialog(mainWindow, options, (chosen_dir) => {
    console.log(chosen_dir);
    if (chosen_dir && chosen_dir.length > 0) { 
      data.outdir = chosen_dir[0];
    }
  });
}

function modifyImage() {
  data.MOD_IS_MODIFYING = true;
  client.invoke("modify_image", data.orig_path, data.outdir, data, (error, res) => {
    if (error) {
      console.error(error);
      data.modify_msgbox = error;
      data.MOD_IS_MODIFYING = false;
    }
    else if (res) {
      console.log(res);
      if (res.msg) {
        data.modify_msgbox = res.msg;
        if (res.msg == "Finished!") {
          data.MOD_IS_MODIFYING = false;
        }
      }
    }
  });
}

function previewModImg() {
  data.MOD_IS_PREVIEWING = true;
  client.invoke("modify_image", data.orig_path, "./temp", data, (error, res) => {
    if (error) {
      console.error(error);
      data.modify_msgbox = error;
      data.MOD_IS_PREVIEWING = false;
    }
    else if (res) {
      console.log(res);
      if (res.msg) {
        data.modify_msgbox = res.msg;
      }
      if (res.preview_path) {
        data.preview_path = `${res.preview_path}?timestamp=${ticks()}`;
        console.log(res.preview_path);
        client.invoke("inspect_one", res.preview_path, "animated", (error, info) => {
          if (error) {
            console.error(error);
          } else {
            console.log(info);
            if (info && info.general_info) {
              data.preview_size = info.general_info.fsize.value;
              data.preview_size_hr = info.general_info.fsize_hr.value;
            }
          }
        });
      }
      if (res.msg == "Finished!") {
        data.MOD_IS_PREVIEWING = false;
        var orig_path = data.orig_path;
      }
    }
  });
}

function buttonIsFrozen() {
  if (data.MOD_IS_LOADING || data.MOD_IS_MODIFYING || data.MOD_IS_PREVIEWING) return true;
  else return false;
}

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

function origDimensions() {
  if (data.orig_width && data.orig_height) {
    return `${data.orig_width} x ${data.orig_height}`;
  }
  else {
    return "-";
  }
}

function previewSizePercentage() {
  let oldsize = data.orig_file_size
  let prevsize = data.preview_size;
  console.log(oldsize, prevsize);
  let redux = Math.round((prevsize / oldsize) * 100);
  return redux;
}


export default {
  data: function() {
    return data;
  },
  components: {
    GIFOptimizationTable,
  },
  methods: {
    loadImage: loadImage,
    clearImage: clearImage,
    clearPrevImage: clearPrevImage,
    chooseOutDir: chooseOutDir,
    previewModImg: previewModImg,
    modifyImage: modifyImage,
    toggleOrigCheckerBG: toggleOrigCheckerBG,
    toggleNewCheckerBG: toggleNewCheckerBG,
    delayConstrain: delayConstrain,
    fpsConstrain: fpsConstrain,
  },
  computed: {
    origDimensions: origDimensions,
    buttonIsFrozen: buttonIsFrozen,
    previewSizePercentage: previewSizePercentage,
  }
};
</script>
