<template>
  <div id="split_panel">
    <div class="split-panel-root">
      <div class="split-panel-display">
        <div class="split-panel-image silver-bordered" 
          v-bind:class="{'has-checkerboard-bg': checkerbg_active }">
          <img v-bind:src="escapeLocalPath(preview_path_cb)" />
        </div>
        <div class="split-panel-info silver-bordered-no-left">
          <table class="table spl-info-table" width="100%">
            <thead>
              <tr>
                <th colspan="2">
                  <p class="is-white-d">{{ info_header }}</p>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="spl-info-label is-cyan">Name</td>
                <td class="spl-info-data">
                  <span v-if="name">{{ name }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
              </tr>
              <tr>
                <td class="spl-info-label is-cyan">Dimensions</td>
                <td class="spl-info-data">
                  <span v-if="dimensions">{{ dimensions }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
              </tr>
              <tr>
                <td class="spl-info-label is-cyan">File Size</td>
                <td class="spl-info-data">
                  <span v-if="file_size">{{ file_size_hr }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
              </tr>
              <tr>
                <td class="spl-info-label is-cyan">Has Transparency</td>
                <td class="spl-info-data">
                  <span v-if="has_transparency">{{ has_transparency? "Yes" : "No" }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
              </tr>
              <tr>
                <td class="spl-info-label is-cyan">Total frames</td>
                <td class="spl-info-data">
                  <span v-if="frame_count">{{ frame_count }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
              </tr>
              <!-- <tr>
                <td class="spl-info-label is-cyan">Total frames (DS)</td>
                <td class="spl-info-data">
                  <span v-if="frame_count_ds">{{ frame_count_ds }}</span>
                  <span v-else>-</span>
                </td>
              </tr> -->
              <tr>
                <td class="spl-info-label is-cyan">Average delay (ms)</td>
                <td class="spl-info-data">                  
                  <span v-if="average_delay">{{ roundPrecise(average_delay, 3) }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
              </tr>
              <tr>
                <td class="spl-info-label is-cyan">Delays are even</td>
                <td class="spl-info-data">                  
                  <span v-if="delays">{{ delays_are_even? "Yes" : "No" }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
              </tr>
              <tr>
                <td class="spl-info-label is-cyan">Delays</td>
                <td class="spl-info-data">                  
                  <span v-if="delays">{{ delays }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
              </tr>
              <tr>
                <td class="spl-info-label is-cyan">Frame rate (FPS)</td>
                <td class="spl-info-data">
                  <span v-if="fps">{{ fps }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
              </tr>
              <tr>
                <td class="spl-info-label is-cyan">Loop duration</td>
                <td class="spl-info-data">
                  <span v-if="loop_duration">{{ loop_duration }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
              </tr>
              <tr>
                <td class="spl-info-label is-cyan">Loop count</td>
                <td class="spl-info-data">
                    <template v-if="preview_path">
                      <span v-if="loop_count == 0">Infinite</span>
                      <span v-else>{{ loop_count }}</span>
                    </template>
                    <!-- <template v-else>-</template> -->
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="split-panel-middlebar">
        <div class="spl-control-btn">
          <a v-on:click="loadImage" class="button is-neon-emerald" v-bind:class="{'is-loading': SPL_IS_LOADING, 'non-interactive': isButtonFrozen}">
            <span class="icon is-small">
              <i class="fas fa-plus"></i>
            </span>
            <span>Load GIF/APNG</span>
          </a>
        </div>
        <div class="spl-control-btn">
          <a v-on:click="clearImage" class="button is-neon-crimson" v-bind:class="{'non-interactive': isButtonFrozen}">
            <span class="icon is-small">
              <i class="fas fa-times"></i>
            </span>
            <span>Clear</span>
          </a>
        </div>
        <div class="spl-control-btn">
          <a v-on:click="toggleCheckerBG" class="button is-neon-white" v-bind:class="{'is-active': checkerbg_active}">
            <span class="icon is-medium">
              <i class="fas fa-chess-board"></i>
            </span>
          </a>
        </div>
      </div>
      <div class="split-panel-controls">
        <table width="100%">
          <tr>
            <td width="20%">
              <div class="field">
                <label class="label">Rename sequence</label>
                <div class="control">
                  <input
                    v-model="criteria.new_name"
                    class="input is-neon-white"
                  />
                </div>
              </div>
            </td>
            <td width="20%">
              <div class="field">
                <label class="label">Pad count</label>
                <div class="control">
                  <input
                    v-model="criteria.pad_count"
                    class="input is-neon-white"
                    type="number"
                    min="0"
                    max="6"
                    v-on:keydown="numConstrain($event, true, true)"
                  />
                </div>
              </div>
            </td>
            <td width="20%" style="vertical-align: middle;">
              <!-- <label class="checkbox" title="Split the GIF into more frames, calculated from frames has higher delay than others">
                <input v-model="criteria.is_duration_sensitive" type="checkbox" />
                Duration-sensitive
              </label> -->
              <label class="checkbox" title="Reconstructs the original image of each frame. Use on optimized GIFs">
                <input v-model="criteria.is_unoptimized" type="checkbox" />
                Unoptimize
              </label>
              <br/>
              <label class="checkbox" title="Convert each frame into a PNG with RGBA color mode">
                <input v-model="criteria.convert_to_rgba" type="checkbox" />
                Convert to RGBA
              </label>
              <br/>
              <label class="checkbox" title="Generate a file containing the delay information of each frame">
                <input v-model="criteria.extract_delay_info" type="checkbox" />
                Extract frame delays
              </label>
              <!-- <label class="checkbox">
                <input v-model="is_reduced_color" type="checkbox" />
                Reduce Colors
              </label> -->
            </td>
            <td width="20%" style="vertical-align: middle;">
              <br/>
            </td>
            <td width="20%" style="vertical-align: middle;">
              <br/>
            </td>
          </tr>
          <tr>
            <td colspan="4">
              <div class="field has-addons">
                <div class="control">
                  <a v-on:click="chooseOutDir" class="button is-neon-cyan">
                    <span class="icon is-small">
                      <i class="fas fa-save"></i>
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
            <td class="has-text-centered">
              <a v-on:click="splitImage" class="button is-neon-cyan" v-bind:class="{'is-loading': SPL_IS_SPLITTING, 'non-interactive': isButtonFrozen}">
                Split to folder</a>
            </td>
          </tr>
          <tr>
            <td colspan="5">
              <input
                v-model="split_msgbox"
                type="text"
                class="input is-left-paddingless is-border-colorless"
                readonly="readonly"
              />
            </td>
          </tr>
        </table>
      </div>
    </div>
  </div>
</template>



<script>

const { ipcRenderer } = require("electron");
const { randString, numConstrain, roundPrecise, validateFilename } = require('./modules/utility');
const { escapeLocalPath } = require("./modules/formatters");
const { tridentEngine } = require("./modules/tridentEngine");

let extension_filters = [{ name: "Images", extensions: ["png", "gif"] }];
let file_dialog_props = ["openfile"];
let dir_dialog_props = ["openDirectory", "createDirectory"];

var defaults = {
  info_header: "Information",
  name: "",
  new_name: "",
  dimensions: "",
  file_size: "",
  file_size_hr: "",
  frame_count: "",
  frame_count_ds: "",
  fps: "",
  average_delay: "",
  delays: "",
  delays_are_even: "",
  loop_duration: "",
  loop_count: "",
  has_transparency: "",
  preview_path: "",
  preview_path_cb: "",
  split_msgbox: ""
};

var data = {
  info_header: "Information",
  name: "",
  criteria: {
    new_name: "",
    pad_count: "",
    color_space: "",
    is_duration_sensitive: false,
    is_unoptimized: false,
    convert_to_rgba: false,
    extract_delay_info: false,
  },
  dimensions: "",
  file_size: "",
  file_size_hr: "",
  frame_count: "",
  frame_count_ds: "",
  fps: "",
  average_delay: "",
  delays_are_even: "",
  delays: "",
  loop_duration: "",
  loop_count: "",
  has_transparency: "",
  preview_path: "",
  preview_path_cb: "",
  checkerbg_active: false,
  is_reduced_color: false,
  outdir: "",
  split_msgbox: "",
  SPL_IS_LOADING: false,
  SPL_IS_SPLITTING: false,
};

function loadImage() {
  console.log("spl load iamge");
  var options = {
    filters: extension_filters,
    properties: file_dialog_props
  };
  ipcRenderer.invoke('open-dialog', options).then((result) => {
    let chosen_path = result.filePaths;
    console.log(`chosen path: ${chosen_path}`);
    if (chosen_path === undefined || chosen_path.length == 0) {
      console.debug('chosen path undefined/null. returning...')
      return;
    }
    data.SPL_IS_LOADING = true;
    console.log(chosen_path);
    tridentEngine(["inspect_one", chosen_path[0], "animated"], (error, res) => {
      if (error) {        
        try {
          data.split_msgbox = error;
        }
        catch (e) {
          data.split_msgbox = error;
        }
        // mboxError(split_msgbox, error);
        data.SPL_IS_LOADING = false;
      } else if (res) {
        if (res && res.msg) {
          data.split_msgbox = res.msg;
        } else if (res && res.data) {
          let info = res.data;
          var geninfo = info.general_info;
          var ainfo = info.animation_info;
          data.name = geninfo.name.value;
          data.dimensions = `${geninfo.width.value} x ${geninfo.height.value}`;
          data.info_header = `${geninfo.format.value} Information`;
          data.file_size = geninfo.fsize.value;
          data.file_size_hr = geninfo.fsize_hr.value;
          data.has_transparency = geninfo.has_transparency.value;
          data.frame_count = `${ainfo.frame_count.value} frames`;
          // data.frame_count_ds = `${ainfo.frame_count_ds.value} frames`
          data.fps = `${ainfo.fps.value} fps`;
          // let delay_info = `${ainfo.avg_delay.value} seconds`;
          // if (ainfo.delay_is_even.value) {
          //   delay_info += ` (even)`;
          // }
          // data.delay = delay_info;
          data.average_delay = ainfo.average_delay.value;
          data.delays_are_even = ainfo.delays_are_even.value;
          data.delays = ainfo.delays.value;
          data.loop_duration = `${ainfo.loop_duration.value} seconds`;
          data.loop_count = ainfo.loop_count.value;
          data.preview_path = geninfo.absolute_url.value;
          data.criteria.pad_count = 3;
          if (data.is_reduced_color) {
            data.criteria.color_space - 256;
          }
          data.split_msgbox = "";
          data.SPL_IS_LOADING = false;
          previewPathCacheBreaker();
          // loadAIMG(res);
          // SPL_pad_count.value = 3;
          // if (SPL_is_reduced_color.checked) { SPL_color_space.value = 256; }
        }
      }
    });
  });
}

function clearImage() {
  Object.assign(data, defaults);
}


function previewPathCacheBreaker() {
  let cb_url = data.preview_path;
  // let cb_url = `${data.preview_path}?cachebreaker=${randString()}`;
  console.log("Cache breaker url", cb_url);
  data.preview_path_cb = cb_url;
}


function toggleCheckerBG() {
  data.checkerbg_active = !data.checkerbg_active;
  console.log("now checkerbg is", data.checkerbg_active);
}

function chooseOutDir() {
  var options = { properties: dir_dialog_props };
  ipcRenderer.invoke('open-dialog', options).then((result) => {
    let out_dirs = result.filePaths;
    console.log(out_dirs);
    if (out_dirs && out_dirs.length > 0) { 
      data.outdir = out_dirs[0];
    }
    data.split_msgbox = "";
  });
}

function splitImage() {
  let validator = validateFilename(data.criteria.new_name);
  if (!validator.valid) {
    console.error(validator.msg);
    data.split_msgbox = validator.msg;
    return;
  }
  data.SPL_IS_SPLITTING = true;
  // freezeButtons();
  // console.log(`in path: ${in_path} out path: ${out_path}`);
  var color_space = data.criteria.color_space;
  if (!data.is_reduced_color || color_space == "") {
    color_space = 0;
  }
  console.log(data);
  tridentEngine(["split_image", data.preview_path, data.outdir, data.criteria], (error, res) => {
    if (error) {
      try {
        data.split_msgbox = error;
      }
      catch (e) {
        data.split_msgbox = error;
      }
      data.SPL_IS_SPLITTING = false;
    } else if (res) {
      if (res.msg) {
        data.split_msgbox = res.msg;
      }
    }
  },
  () => {
    data.split_msgbox = "All frames successfully split!"
    data.SPL_IS_SPLITTING = false;
  });
}

function isButtonFrozen() {
  if (data.SPL_IS_LOADING || data.SPL_IS_SPLITTING) return true;
  else return false;
}

export default {
  data: function() {
    return data;
  },
  computed: {
    isButtonFrozen: isButtonFrozen,
  },
  methods: {
    loadImage: loadImage,
    clearImage: clearImage,
    toggleCheckerBG: toggleCheckerBG,
    chooseOutDir: chooseOutDir,
    splitImage: splitImage,
    numConstrain: numConstrain,
    escapeLocalPath: escapeLocalPath,
    roundPrecise: roundPrecise,
  }
};
</script>
