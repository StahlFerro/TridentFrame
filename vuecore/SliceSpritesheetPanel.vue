<template>
  <div id="slicesprite_panel" class="container" style="display: none; padding: 10px;">
    <table class="table is-borderless" style="padding: 5px;" width="100%">
      <tr>
        <td
          class="slicegrid-cell silver-bordered force-center is-paddingless is-marginless"
          v-bind:class="{'has-checkerboard-bg': checkerbg_active }"
        >
          <!-- <div class="spl-aimg-container"> -->
          <div class="slicegrid-container">
            <!-- <span class="aimg-helper"></span> -->
            <img ref="slicegrid_image" v-bind:src="sheet_path_cb" v-on:load="sheetHandler($event)"/>
            <canvas ref="slicegrid_canvas" class="slicegrid-canvas" v-show="show_canvas"
             v-bind:width="el_width" v-bind:height="el_height"></canvas>
          </div>
          <!-- </div> -->
        </td>
        <td class="sliceinfo-cell silver-bordered is-paddingless">
          <table width="100%">
            <thead>
              <tr>
                <th colspan="2">
                  <p class="is-white-d">Sheet information</p>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="is-cyan force-vcenter">Name</td>
                <td class="">
                  <input class="input is-neon-white" type="text" v-model="name"/>
                  <!-- <span v-if="name">{{ name }}</span>
                  <span v-else>-</span> -->
                </td>
              </tr>
              <tr>
                <td class="is-cyan force-vcenter">Dimensions</td>
                <td class="">
                  <input class="input is-border-colorless" type="text" v-model="dimensionsText" readonly="readonly"/>
                </td>
              </tr>
              <tr>
                <td class="is-cyan force-vcenter">File Size</td>
                <td class="">
                  <input class="input is-border-colorless" type="text" v-model="file_size_hr" readonly="readonly"/>
                </td>
              </tr>
            </tbody>
          </table>
          
          <table class="slicecontrol-cell" width="100%">
            <tr>
              <td>
                <div class="field">
                  <label class="label">Tile Width</label>
                  <div class="control">
                    <input
                      v-bind:value="tile_width" v-on:keydown="wholeNumConstrain($event)" v-on:input="tileWidthHandler(tile_width, $event)"
                      class="input is-neon-white"
                      type="number" 
                      min="1" step="1"/>
                  </div>
                </div>
              </td>
              <td>
                <div class="field">
                  <label class="label">Tile Height</label>
                  <div class="control">
                    <input
                      v-bind:value="tile_height" v-on:keydown="wholeNumConstrain($event)" v-on:input="tileHeightHandler(tile_height, $event)"
                      class="input is-neon-white"
                      type="number" 
                      min="1" step="1"/>
                  </div>
                </div>
              </td>
            </tr>
            <tr>
              <td>
                <label class="checkbox" title="Preserve alpha on tiles that have their width or height cut-off on the edges">
                  <input v-model="is_edge_alpha" type="checkbox" />
                  Edge Alpha
                </label>
              </td>
            </tr>
          </table>

        </td>
      </tr>
      <tr>
        <td colspan="2" class="is-hpaddingless">
          <a v-on:click="loadSheet" class="button is-neon-emerald" v-bind:class="{'is-loading': SSPR_IS_LOADING, 'is-static': isButtonFrozen}">
            <span class="icon is-small">
              <i class="fas fa-plus"></i>
            </span>
            <span>Load Spritesheet</span>
          </a>
          <a v-on:click="clearSheet" class="button is-neon-crimson">
            <span class="icon is-small">
              <i class="fas fa-trash-alt"></i>
            </span>
            <span>Clear</span>
          </a>
          <a
            v-on:click="toggleCheckerBG"
            class="button is-neon-white"
            v-bind:class="{'is-active': checkerbg_active}"
          >
            <span class="icon is-medium">
              <i class="fas fa-chess-board"></i>
            </span>
          </a>
          <a v-on:click="toggleGridView" class="button is-neon-white"
            v-bind:class="{'is-active': show_canvas}">
            <span class="icon is-medium">
              <i class="fas fa-th"></i>
            </span>
            <span>Preview Grid</span>
          </a>
        </td>
        <td></td>
      </tr>
      <tr>
        <td class="is-paddingless">
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
        <td class="has-text-centered is-paddingless">
          <a v-on:click="sliceSheet" class="button is-neon-cyan" v-bind:class="{'is-loading': SSPR_IS_SLICING, 'is-static': isButtonFrozen}">
            Slice to Folder</a>
        </td>
      </tr>
      <tr>
        <td colspan="2" class="is-paddingless" style="vertical-align: middle;">
          <input v-model="sspr_msgbox" type="text" class="input is-paddingless is-border-colorless" readonly="readonly"/>
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
const { randString, wholeNumConstrain, posWholeNumConstrain, gcd } = require("./Utility.vue");

let extension_filters = [{ name: "Spritesheet image", extensions: ["png", "jpg"] }];
let file_dialog_props = ["openfile"];
let dir_dialog_props = ["openDirectory", "createDirectory"];
let slicegrid_image = null;
let slicegrid_canvas = null;
let canvas_context = null;

let data = {
  sheet_path: "",
  sheet_path_cb: "",
  name: "",
  sheet_width: "",
  sheet_height: "",
  old_tile_width: "",
  old_tile_height: "",
  tile_width: "",
  tile_height: "",
  offset_x: "",
  offset_y: "",
  padding_x: "",
  padding_y: "",
  is_edge_alpha: false,
  file_size: "",
  file_size_hr: "",
  aspect_ratio: "",
  lock_aspect_ratio: false,
  checkerbg_active: false,
  show_canvas: false,
  SSPR_IS_LOADING: false,
  SSPR_IS_SLICING: false,
  sspr_msgbox: "",
  el_width: 0,
  el_height: 0,
  wprev_ratio: 0,
  hprev_ratio: 0,
  outdir: "",
}

function mountElements() {
  // slicegrid_image = document.getElementById('slicegrid_image');
  // slicegrid_canvas = document.getElementById('slicegrid_canvas');
  console.log(this.$refs);
  slicegrid_image = this.$refs['slicegrid_image'];
  slicegrid_canvas = this.$refs['slicegrid_canvas'];
  canvas_context = slicegrid_canvas.getContext("2d");
  console.log("MOUNTED!");
  console.log(slicegrid_image);
  console.log(slicegrid_canvas);
}

function loadSheet() {
  let options = {
    filters: extension_filters,
    properties: file_dialog_props
  };
  dialog.showOpenDialog(mainWindow, options, (chosen_path) => {
    console.log(`chosen path: ${chosen_path}`);
    if (chosen_path === undefined || chosen_path.length == 0) {
      return;
    }
    data.SSPR_IS_LOADING = true;
    client.invoke("inspect_one", chosen_path[0], "static", (error, res) => {
      if (error) {
        console.error(error);
        data.sspr_msgbox = error;
        data.SSPR_IS_LOADING = false;
      } else {
        console.log(res);
        let geninfo = res.general_info
        data.name = geninfo.base_fname.value;
        data.file_size_hr = geninfo.fsize_hr.value;
        data.sheet_path = geninfo.absolute_url.value;
        data.sheet_width = geninfo.width.value;
        data.sheet_height = geninfo.height.value;
        sheetPathCacheBreaker();
        // for (const [key, value] of Object.entries(slicegrid_image.attributes)) {
        //   console.log(`${key}: ${value}`);
        // }
        data.SSPR_IS_LOADING = false;
      }
    });
  });
}

function sheetHandler(event) {
  let img = event.target;
  console.log(img);
  data.el_width = img.clientWidth;
  data.el_height = img.clientHeight;
  console.log(img.clientWidth, img.clientHeight);
  computePreviewRatio();
  autoDrawCanvasGrid();
}

function boxCountEstimation() {
  if (data.tile_width && data.tile_height && data.sheet_width && data.sheet_height) {

  }
}

function computePreviewRatio() {
  if (data.el_width && data.sheet_width) {
    data.wprev_ratio = data.el_width / data.sheet_width;
  }
  if (data.el_height && data.sheet_height) {
    data.hprev_ratio = data.el_height / data.sheet_height;
  }
}

function autoDrawCanvasGrid() {
  console.log('autodraw', data.tile_width, data.tile_height)
  if (data.tile_width > 0 && data.tile_height > 0 && data.el_width > 0 && data.el_height && data.sheet_width > 0 && data.sheet_height > 0) {
    console.log("CANVAS REDRAWING....")
    clearGrid();
    drawGrid();
  }
}

function toggleGridView() {
  data.show_canvas = !data.show_canvas;
  autoDrawCanvasGrid();
}

function drawGrid() {
  console.log("Draw GRID...");
  let wprev_ratio = data.wprev_ratio
  let hprev_ratio = data.hprev_ratio;
  let prev_tile_width = parseInt(data.tile_width) * wprev_ratio;
  let prev_tile_height = parseInt(data.tile_height) * hprev_ratio;
  console.log('prevratios', wprev_ratio, hprev_ratio);
  console.log(data.el_width, data.el_height, prev_tile_width, prev_tile_height);
  let xlines = 0;
  let ylines = 0;
  canvas_context.beginPath();
  for (let x = 0; x <= data.el_width; x += prev_tile_width) {
    canvas_context.moveTo(x, 0);
    canvas_context.lineTo(x, data.el_height);
    xlines++;
  }
  for (let x = 0; x <= data.el_height; x += prev_tile_height) {
    canvas_context.moveTo(0, x);
    canvas_context.lineTo(data.el_width, x);
    ylines++;
  }
  canvas_context.strokeStyle = "black";
  canvas_context.stroke();
  canvas_context.closePath();
  console.log("X and Y segments:", xlines, ylines);
}

function clearGrid() {
  console.log('Clearing GRID...')
  canvas_context.clearRect(0, 0, slicegrid_canvas.width, slicegrid_canvas.height);
}

// function resizeCanvas() {
//   if (data.el_width && data.el_height) {
//     slicegrid_canvas.style.width = data.el_width;
//     slicegrid_canvas.style.height = data.el_height;
//   }
//   else {
//     slicegrid_canvas.style.width = 0;
//     slicegrid_canvas.style.height = 0;
//   }
//   console.log("slice grid canvas", slicegrid_canvas);
// }

function clearSheet() {
  clearGrid();
  data.sheet_path = "";
  data.sheet_path_cb = "";
  data.name = "";
  data.sheet_width = "";
  data.sheet_height = "";
  data.tile_width = "";
  data.tile_height = "";
  data.offset_x = "",
  data.offset_y = "",
  data.padding_x = "",
  data.padding_y = "",
  data.is_edge_alpha = false;
  data.file_size = "";
  data.file_size_hr = "";
  data.sspr_msgbox = "";
  data.el_width = 0;
  data.el_height = 0;
  data.sspr_msgbox = "";
  let ARData = {
    "w_ratio": "",
    "h_ratio": "",
    "text": "",
  };
  data.aspect_ratio = ARData;
}

function tileWidthHandler(tile_width, event) {
  data.old_tile_width = parseInt(tile_width);
  console.log(event);
  let newWidth = event.target.value;
  data.tile_width = newWidth;
  if (data.lock_aspect_ratio && data.aspect_ratio.h_ratio > 0) { // Change height if lock_aspect_ratio is true and height is not 0
    let raHeight = Math.round(newWidth / data.aspect_ratio.w_ratio * data.aspect_ratio.h_ratio);
    data.tile_height = raHeight > 0? raHeight : "";
  }
  else {
    updateAspectRatio(data.tile_width, data.tile_height);
  }
  autoDrawCanvasGrid();
}

function tileHeightHandler(tile_height, event) {
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
  autoDrawCanvasGrid();
}

function sheetPathCacheBreaker() {
  let cb_url = `${data.sheet_path}?cachebreaker=${randString()}`;
  console.log("Cache breaker url", cb_url);
  data.sheet_path_cb = cb_url;
}

function updateAspectRatio(tile_width, tile_height) {
  if (data.tile_width && data.tile_height) {
    console.log('uAR', tile_width, tile_height);
    let divisor = gcd(tile_width, tile_height);
    let w_ratio = tile_width / divisor;
    let h_ratio = tile_height / divisor;
    let ARData = {
      "w_ratio": w_ratio,
      "h_ratio": h_ratio,
      "text": `${w_ratio}:${h_ratio}`,
    };
    console.log(ARData);
    data.aspect_ratio = ARData;
  }
}

function toggleCheckerBG() {
  data.checkerbg_active = !data.checkerbg_active;
  console.log("now checkerbg is", data.checkerbg_active);
}

function chooseOutDir() {
  var options = { properties: dir_dialog_props };
  dialog.showOpenDialog(mainWindow, options, (out_dirs) => {
    console.log(out_dirs);
    if (out_dirs && out_dirs.length > 0) { 
      data.outdir = out_dirs[0];
    }
    data.split_msgbox = "";
  });
}

function isButtonFrozen() {
  if (data.SSPR_IS_LOADING) return true;
  else return false;
}

function dimensionsText() {
  if (data.sheet_width && data.sheet_height) {
    return `${data.sheet_width} x ${data.sheet_height}`;
  }
  else {
    return "";
  }
}

function overlayGrid() {
}

function sliceSheet() {
  data.SSPR_IS_SLICING = true;
  client.invoke("slice_spritesheet", data.sheet_path, data.outdir, data.name, data, (error, res) => {
    if (error) {
      console.error(error);
      data.sspr_msgbox = error;
      data.SSPR_IS_SLICING = false;
    }
    else {
      if (res) {
        console.log(res);
        if (res.msg) {
          data.sspr_msgbox = res.msg;
        }
        if (res.CONTROL == "SSPR_FINISH") {
          data.sspr_msgbox = "Spritesheet built!";
          data.SSPR_IS_SLICING = false;
        }
      }
    }
  });
}

export default {
  data: function() {
    return data;
  },
  computed: {
    isButtonFrozen: isButtonFrozen,
    dimensionsText: dimensionsText,
  },
  mounted: mountElements,
  methods: {
    loadSheet: loadSheet,
    clearSheet: clearSheet,
    chooseOutDir: chooseOutDir,
    drawGrid: drawGrid,
    clearGrid: clearGrid,
    toggleGridView: toggleGridView,
    toggleCheckerBG: toggleCheckerBG,
    sheetHandler: sheetHandler,
    sliceSheet: sliceSheet,
    wholeNumConstrain: wholeNumConstrain,
    tileWidthHandler: tileWidthHandler,
    tileHeightHandler: tileHeightHandler,
  },
}
</script>
