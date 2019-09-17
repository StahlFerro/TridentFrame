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
            v-bind:class="{'has-checkerboard-bg': CRT_checkerbg_active}">
            <div class="crt-aimg-container">
              <span class="aimg-helper"></span>
              <img id="CRT_aimg_stage"/>
            </div>
            <input id="CRT_aimg_path" name="CRT_aimg_path_field" type="hidden" value />
          </td>
        </tr>
        <tr>
          <td class="is-hpaddingless">
            <nav class="level">
              <div class="level-left">
                <div class="level-item has-text-centered">
                  <div>
                    <a v-on:click="loadImage" class="button is-neon-cyan" v-bind:class="{'is-loading': CRT_IS_LOADING, 'is-static': isButtonFrozen}">
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
                  <a v-on:click="CRTToggleCheckerBG" class="button is-neon-white" v-bind:class="{'is-active': CRT_checkerbg_active}">
                    <span class="icon is-medium">
                      <i class="fas fa-chess-board"></i>
                    </span>
                  </a>
                  <a id="CRT_autoprev_button" class="button is-neon-white">
                    <span class="icon is-medium">
                      <i id="autoprev_icon" class="far fa-eye-slash"></i>
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
                      <input v-model="create_name" class="input is-neon-white" type="text" />
                    </div>
                  </div>
                </td>
                <td>
                  <div class="field">
                    <label class="label">Delay (seconds)</label>
                    <div class="control">
                      <input v-model="create_delay" v-on:input="delayConstrain" class="input is-neon-white" type="number" />
                    </div>
                  </div>
                </td>
                <td>
                  <div class="field">
                    <label class="label">Frame rate</label>
                    <div class="control">
                      <input v-model="create_fps" v-on:input="fpsConstrain" class="input is-neon-white" type="number" min="1" max="50" step="0.01"/>
                    </div>
                  </div>
                </td>
                <td style="vertical-align: bottom;">
                  <label class="checkbox">
                    <input v-model="is_disposed" type="checkbox" />
                    Preserve Transparency
                  </label>
                  <br />
                  <label class="checkbox">
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
                      <input v-model="create_width" class="input is-neon-white" type="number" />
                    </div>
                  </div>
                </td>
                <td>
                  <div class="field">
                    <label class="label">Height</label>
                    <div class="control">
                      <input v-model="create_height" class="input is-neon-white" type="number" />
                    </div>
                  </div>
                </td>
                <td></td>
                <td style="vertical-align: bottom;">
                  <label class="checkbox">
                    <input v-model="flip_horizontal" type="checkbox" />
                    Flip Horizontally
                  </label>
                  <br />
                  <label class="checkbox">
                    <input v-model="flip_vertical" type="checkbox" />
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
                        v-model="create_outdir"
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
                        <select v-model="CRT_out_format">
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
const session = remote.getCurrentWebContents().session;
const { client } = require("./Client.vue");
import { quintcellLister, GIF_DELAY_DECIMAL_PRECISION } from "./Utility.vue";

var data = {
  sequence_paths: [],
  create_name: "",
  create_fps: "",
  create_width: "",
  create_height: "",
  create_delay: "",
  is_disposed: false,
  is_reversed: false,
  flip_horizontal: false,
  flip_vertical: false,
  CRT_out_format: "gif",
  create_outdir: "",
  CRT_aimg_stage: "",
  CRT_aimg_path: "",
  create_msgbox: "",
  sequence_counter: "",
  CRT_checkerbg_active: false,
  CRT_IS_LOADING: false,
  CRT_IS_CREATING: false,
}

let extension_filters = [{ name: "Images", extensions: ["png", "gif"] }];
let imgs_dialog_props = ["openfile", "multiSelections", "createDirectory"];
let dir_dialog_props = ["openDirectory", "createDirectory"];

function loadImage() {
  console.log("crt load image")
  var options = {
    filters: extension_filters,
    properties: imgs_dialog_props
  }
  dialog.showOpenDialog(options, (img_paths) => {
    console.log(img_paths);
    if (img_paths === undefined || img_paths.length == 0) { return; }
    data.CRT_IS_LOADING = true;
    client.invoke("inspect_sequence", img_paths, (error, res) => {
      if (error) {
        console.error(error);
        data.create_msgbox = error;
      } else {
        data.sequence_paths = res.sequence;
        data.create_name = res.name;
        data.sequence_counter = `${res.total} image${res.total > 1 ? "s" : ""} (${res.size} total)`;
        data.create_width = res.width;
        data.create_height = res.height;
        data.create_fps = 50;
        data.create_delay = 0.02;
        data.create_msgbox = "";
      }
      data.CRT_IS_LOADING = false;
    });
  });
}

function CRTChooseOutdir() {
  dialog.showOpenDialog({ properties: dir_dialog_props }, (choosen_dir) => {
    console.log(`Chosen dir: ${choosen_dir}`);
    if (choosen_dir === undefined) {return}
    data.create_outdir = choosen_dir[0];
    data.create_msgbox = "";
  });
  // mboxClear(create_msgbox);
}

function CRTClearAIMG() {
  data.sequence_paths = [];
  data.create_name = "";
  data.create_delay = "";
  data.create_fps = "";
  data.create_width = "";
  data.create_height = "";
  data.CRT_sequence_counter = "";
  data.create_msgbox = "";
  data.sequence_counter = "";
  // mboxClear(create_msgbox);
  // deleteTempAIMG();
  // session.clearCache(testcallback);
}

function CRTCreateAIMG() {
  data.create_msgbox = "";
  console.log('console log', data.is_disposed);
  // create_aimg_button.classList.add('is-loading');
  // freezeButtons();
  data.CRT_IS_CREATING = true;
  // build_aimg(sequence_paths, create_outdir.value, create_name.value, parseInt(create_fps.value), CRT_out_format.value, false, is_disposed.checked);
  console.log('data before create');
  console.log(data);
  // console.log(getFPS());
  client.invoke("combine_image", data.sequence_paths, data.create_outdir, data.create_name, data.create_fps, 
    data.CRT_out_format, data.create_width, data.create_height, data.is_reversed, data.is_disposed, data.flip_horizontal, data.flip_vertical, (error, res) => {
    // console.log('createfragment fps', data.create_fps);
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
  data.CRT_checkerbg_active = !data.CRT_checkerbg_active;
  console.log('now checkerbg is', data.CRT_checkerbg_active);
}

function isButtonFrozen() {
  if (data.CRT_IS_LOADING || data.CRT_IS_CREATING) return true;
  else return false;
}

// function getFPS() {
//   return Math.round(1/data.create_delay * 1000) / 1000;
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
      data.create_delay = `${numdec[0]}.${twodecs}`;
    }
  }
  data.create_fps = Math.round(1000 / data.create_delay) / 1000;
}

function fpsConstrain (event) {
  console.log("fps event", event);
  var value = event.target.value;
  if (value) {
    data.create_delay = Math.round(100 / data.create_fps) / 100;
  }
}

function CRTQuintcellLister() {
  return quintcellLister(data.sequence_paths);
}

export default {
  data: function() {
    return data;
  },
  methods: {
    loadImage: loadImage,
    CRTClearAIMG: CRTClearAIMG,
    CRTChooseOutdir: CRTChooseOutdir,
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
