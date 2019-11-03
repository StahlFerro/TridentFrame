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
            <img ref="slicegrid_image" v-bind:src="sheet_path_cb" v-on:load="sheetElementDimensions($event)"/>
            <canvas ref="slicegrid_canvas" class="slicegrid-canvas" v-bind:width="el_width" v-bind:height="el_height"></canvas>
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
                <td class="is-cyan">Name</td>
                <td class="">
                  <span v-if="name">{{ name }}</span>
                  <span v-else>-</span>
                </td>
              </tr>
              <tr>
                <td class="is-cyan">Dimensions</td>
                <td class="">
                  <span v-if="dimensions">{{ dimensions }}</span>
                  <span v-else>-</span>
                </td>
              </tr>
              <tr>
                <td class="is-cyan">File Size</td>
                <td class="">
                  <span v-if="file_size_hr">{{ file_size_hr }}</span>
                  <span v-else>-</span>
                </td>
              </tr>
            </tbody>
          </table>
        </td>
      </tr>
      <tr>
        <td class="is-hpaddingless">
          <a v-on:click="loadSheet" class="button is-neon-cyan" v-bind:class="{'is-loading': SSPR_IS_LOADING, 'is-static': isButtonFrozen}">
            <span class="icon is-small">
              <i class="fas fa-plus"></i>
            </span>
            <span>Load Spritesheet</span>
          </a>
          <a v-on:click="clearSheet" class="button is-neon-white">
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
        </td>
        <td></td>
      </tr>
      <tr>
        <td class="is-hpaddingless is-toppaddingless">
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
        <td class="has-text-centered is-toppaddingless">
          <a v-on:click="sliceSheet" class="button is-neon-cyan" v-bind:class="{'is-loading': SSPR_IS_SLICING, 'is-static': isButtonFrozen}">
            Slice to Folder</a>
        </td>
      </tr>
      <tr>
        <td colspan="2" class="has-text-left" style="vertical-align: middle;">
          <span>{{ sspr_msgbox }}</span>
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
const { randString } = require("./Utility.vue");

let extension_filters = [{ name: "Spritesheet image", extensions: ["png", "jpg"] }];
let file_dialog_props = ["openfile"];
let dir_dialog_props = ["openDirectory", "createDirectory"];
let slicegrid_image = null;
let slicegrid_canvas = null;

let data = {
  sheet_path: "",
  sheet_path_cb: "",
  name: "",
  width: "",
  height: "",
  file_size: "",
  file_size_hr: "",
  checkerbg_active: false,
  SSPR_IS_LOADING: false,
  SSPR_IS_SLICING: false,
  sspr_msgbox: "",
  el_width: 0,
  el_height: 0,
  outdir: "",
}

function mountElements() {
  // slicegrid_image = document.getElementById('slicegrid_image');
  // slicegrid_canvas = document.getElementById('slicegrid_canvas');
  console.log(this.$refs);
  slicegrid_image = this.$refs['slicegrid_image'];
  slicegrid_canvas = this.$refs['slicegrid_canvas'];
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
        data.sheet_path = geninfo.absolute_url.value;
        sheetPathCacheBreaker();
        // for (const [key, value] of Object.entries(slicegrid_image.attributes)) {
        //   console.log(`${key}: ${value}`);
        // }
        data.SSPR_IS_LOADING = false;
      }
    });
  });
}

function sheetElementDimensions(event) {
  let img = event.target;
  console.log(img);
  data.el_width = img.clientWidth;
  data.el_height = img.clientHeight;
  console.log(img.clientWidth, img.clientHeight);
}

function drawGrid() {
  let context = slicegrid_canvas.getContext("2d");
  let grid_width = data.el_width;
  let grid_height = data.el_height;
  for (let x = 0; x <= grid_width; x += 100) {

  }
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
  data.sheet_path = "";
  data.sheet_path_cb = "";
  data.name = "";
  data.width = "";
  data.height = "";
  data.file_size = "";
  data.file_size_hr = "";
  data.sspr_msgbox = "";
  data.el_width = 0;
  data.el_height = 0;
}

function sheetPathCacheBreaker() {
  let cb_url = `${data.sheet_path}?cachebreaker=${randString()}`;
  console.log("Cache breaker url", cb_url);
  data.sheet_path_cb = cb_url;
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

function dimensions() {
  if (data.width && data.height) {
    return `${data.width}  ${data.height}`;
  }
  else{
    return "";
  }
}

function overlayGrid() {
}

function sliceSheet() {
    
}

export default {
  data: function() {
    return data;
  },
  computed: {
    isButtonFrozen: isButtonFrozen,
    dimensions: dimensions,
  },
  mounted: mountElements,
  methods: {
    loadSheet: loadSheet,
    clearSheet: clearSheet,
    chooseOutDir: chooseOutDir,
    toggleCheckerBG: toggleCheckerBG,
    sheetElementDimensions: sheetElementDimensions,
    sliceSheet: sliceSheet,
  },
}
</script>
