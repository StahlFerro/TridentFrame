<template>
  <div id="buildsprite_panel" class="container" style="display: none; padding:10px;">
    <div class="content">
      <table class="table is-borderless" style="padding: 5px;" width="100%">
        <tr>
          <td
            id="BSPR_sequence_cell"
            class="silver-bordered is-paddingless"
            style="width: 500px; height: 320px;"
          >
            <div id="BSPR_from_sequence_subpanel" style="display: block;">
              <table class="sequence-grid is-paddingless" width="100%">
                <tbody>
                  <tr v-for="(paths, row) in BSPRQuintcellLister" v-bind:key="row">
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
            </div>
            <div
              id="BSPR_from_aimg_subpanel"
              class="force-center"
              style="display: none; vertical-align: middle;"
            >
              <div class="crt-aimg-container">
                <span class="aimg-helper"></span>
                <img id="BSPR_aimg_stage" src />
              </div>
              <input id="BSPR_aimg_path" name="BSPR_aimg_path_field" type="hidden" value />
            </div>
          </td>
          <td
            id="create_spritesheet_cell"
            class="silver-bordered force-center is-paddingless"
            style="width: 320px; height: 320px;"
          >
            <div class="prev-spritesheet-container">
              <span class="spritesheet-helper"></span>
              <img id="BSPR_prev_spritesheet_stage" src />
            </div>
            <input
              id="BSPR_prev_spritesheet_path"
              name="BSPR_prev_spritesheet_path_field"
              type="hidden"
              value
            />
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
                              <option value="sequence">From Sequence</option>
                              <!-- <option value="aimg">From GIF/APNG</option> -->
                            </select>
                          </div>
                        </div>
                      </div>
                      <div class="field">
                        <a v-on:click="loadInput" class="button is-neon-cyan" v-bind:class="{'is-loading': BSPR_IS_LOADING, 'is-static': isButtonFrozen}">
                          <span class="icon is-small">
                            <i class="fas fa-plus"></i>
                          </span>
                          <span>Add</span>
                        </a>
                        <a v-on:click="clearInfo" class="button is-neon-white">
                          <span class="icon is-small">
                            <i class="fas fa-trash-alt"></i>
                          </span>
                          <span>Clear</span>
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </nav>
          </td>
          <td class="is-hpaddingless">
            <nav class="level">
              <div class="level-item has-text-centered">
                <div>
                  <p v-if="sequence_count">{{ sequence_count }} images</p>
                </div>
              </div>
              <div class="level-item has-text-right">
                <div>
                  <span v-if="sheetDimensions">Sheet dimensions: {{ sheetDimensions }}</span>
                </div>
              </div>
            </nav>
          </td>
        </tr>
        <tr>
          <td id="BSPR_create_control_table" class="is-paddingless" colspan="2">
            <table class="table spr-control-table" width="100%">
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
                    <label class="label">Tile Width</label>
                    <div class="control">
                      <input v-model="tile_width" class="input is-neon-white" type="number" />
                    </div>
                  </div>
                </td>
                <td>
                  <div class="field">
                    <label class="label">Tile Height</label>
                    <div class="control">
                      <input
                        v-model="tile_height"
                        class="input is-neon-white"
                        type="number"
                        min="1"
                        max="50"
                      />
                    </div>
                  </div>
                </td>
                <td>
                  <div class="field">
                    <label class="label">Max tiles per row</label>
                    <div class="control">
                      <input
                        v-model="tile_row"
                        class="input is-neon-white"
                        type="number"
                        min="1"
                        max="50"
                      />
                    </div>
                  </div>
                </td>
              </tr>
              <tr>
                <td colspan="2" style="padding-top: 25px;">
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
                <td colspan="2" style="padding-top: 25px;">
                  <div class="field has-text-centered">
                    <div class="control">
                      <a v-on:click="buildSpritesheet" class="button is-neon-cyan" v-bind:class="{'is-loading': BSPR_IS_BUILDING, 'is-static': isButtonFrozen}">
                        Create
                      </a>
                    </div>
                  </div>
                </td>
              </tr>
              <tr>
                <td colspan="4" class="has-text-left" style="vertical-align: middle;">
                  <span>{{ bspr_msgbox }}</span>
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
import { quintcellLister, GIF_DELAY_DECIMAL_PRECISION } from './Utility.vue';

function clearInfo() {
  data.sequence_paths = [],
  data.sequence_count = 0;
  data.name = "";
  data.tile_width = "";
  data.tile_height = "";
  data.tile_row = "";
  data.outdir = "";
  data.bspr_msgbox = "";
}

var data = {
  sequence_paths: [],
  sequence_count: 0,
  input_format: "sequence",
  name: "",
  tile_width: "",
  tile_height: "",
  tile_row: "",
  outdir: "",
  bspr_msgbox: "",
  BSPR_IS_LOADING: false,
  BSPR_IS_BUILDING: false,
};

let sequence_dialog_props = ['openfile', 'multiSelections', 'createDirectory'];
let dir_dialog_props = ['openDirectory', 'createDirectory'];
let extension_filters = [{ name: 'Images', extensions: ['png', 'gif'] }];

function loadInput() {
  var img_paths = dialog.showOpenDialog({ filters: extension_filters, properties: sequence_dialog_props }); 
  if (img_paths === undefined) { return; }
  console.log(img_paths);
  data.BSPR_IS_LOADING = true;
  if (data.input_format == "sequence") {
    loadSequence(img_paths);
  }
}

function loadSequence(img_paths) {
  client.invoke("inspect_sequence", img_paths, (error, res) => {
    if (error || !res.sequence) {
      console.error(error);
      data.bspr_msgbox = error;
      data.BSPR_IS_LOADING = false;
    }
    else {
      data.sequence_paths = img_paths;
      data.name = res.name;
      data.tile_width = res.width;
      data.tile_height = res.height;
      data.tile_row = 5;
      data.sequence_count = res.total;
      data.bspr_msgbox = "";
      data.BSPR_IS_LOADING = false;
    }
  });
}

function sheetDimensions() {
  console.log('compute final dimens called');
  var image_count = data.sequence_count;
  var x_count = Math.min(image_count, data.tile_row);
  var y_count = Math.ceil(image_count / data.tile_row);
  // console.log('xcount', x_count);
  // console.log('ycount', y_count);
  var sheet_width = data.tile_width * x_count;
  var sheet_height = data.tile_height * y_count;
  if (sheet_width && sheet_height) {
    return `${sheet_width}x${sheet_height}`;
  }
  else return "";
}

function chooseOutDir() {
  var choosen_dir = dialog.showOpenDialog({ properties: dir_dialog_props });
  console.log(`Chosen dir: ${choosen_dir}`);
  if (choosen_dir === undefined) {return}
  data.outdir = choosen_dir[0];
  data.bspr_msgbox = "";
}

function BSPRQuintcellLister() {
  return quintcellLister(data.sequence_paths);
}

function isButtonFrozen() {
  if (data.BSPR_IS_LOADING || data.BSPR_IS_BUILDING) return true;
  else return false;
}

function buildSpritesheet() {
  data.BSPR_IS_BUILDING = true;
  var paths = null;
  if (data.input_format == 'sequence') { paths = data.sequence_paths; }
  // else if (data.input_format == 'aimg') { paths = bspr_aimg_path_list; }
  client.invoke("build_spritesheet", paths, data.input_format, data.outdir, data.name, 
  data.tile_width, data.tile_height, data.tile_row, 0, 0, 0, 0, true, (error, res) => {
      if (error) {
          console.error(error);
          data.bspr_msgbox = error;
          data.BSPR_IS_BUILDING = false;
          // mboxError(bspr_msgbox, error);
      } else {
          if (res) {
            console.log(res);
            data.bspr_msgbox = res;
            if (res == "Finished!") {
              data.BSPR_IS_BUILDING = false;
            }
          }
      }
  });
}

export default {
  data: function() {
    return data;
  },
  methods: {
    loadInput: loadInput,
    chooseOutDir: chooseOutDir,
    clearInfo: clearInfo,
    buildSpritesheet: buildSpritesheet,
  },
  computed: {
    BSPRQuintcellLister: BSPRQuintcellLister,
    sheetDimensions: sheetDimensions,
    isButtonFrozen: isButtonFrozen,
  }
}
</script>
