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
              <tbody id="CRT_sequence_body"></tbody>
            </table>
          </td>
          <td
            id="create_aimg_cell"
            class="silver-bordered force-center is-paddingless"
            style="width: 320px; height: 320px;"
          >
            <div class="crt-aimg-container">
              <span class="aimg-helper"></span>
              <img id="CRT_aimg_stage" src />
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
                    <a id="CRT_load_imgs_button" class="button is-neon-cyan">
                      <span class="icon is-small">
                        <i class="fas fa-plus"></i>
                      </span>
                      <span>Load Images</span>
                    </a>
                    <a id="CRT_clear_imgs_button" class="button is-neon-white">
                      <span class="icon is-small">
                        <i class="fas fa-trash-alt"></i>
                      </span>
                      <span>Clear</span>
                    </a>
                  </div>
                </div>
                <div class="level-item has-text-right">
                  <div>
                    <p id="CRT_sequence_counter"></p>
                  </div>
                </div>
              </div>
            </nav>
          </td>
          <td class="has-text-left is-paddingless" style="vertical-align: middle;">
            <nav class="level">
              <div class="level-item has-text-centered">
                <div>
                  <a id="CRT_bgprev_button" class="button is-neon-white">
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
                      <input id="create_name" class="input is-neon-white" type="text" />
                    </div>
                  </div>
                </td>
                <td>
                  <div class="field">
                    <label class="label">Duration</label>
                    <div class="control">
                      <input id="create_duration" class="input is-neon-white" type="number" />
                    </div>
                  </div>
                </td>
                <td>
                  <div class="field">
                    <label class="label">Frame rate</label>
                    <div class="control">
                      <input
                        id="create_fps"
                        class="input is-neon-white"
                        type="number"
                        min="1"
                        max="50"
                      />
                    </div>
                  </div>
                </td>
                <td style="vertical-align: bottom;">
                  <label class="checkbox">
                    <input id="is_disposed" type="checkbox" />
                    Preserve Transparency
                  </label>
                  <br />
                  <label class="checkbox">
                    <input id="is_reversed" type="checkbox" />
                    Reversed
                  </label>
                </td>
              </tr>
              <tr>
                <td>
                  <div class="field">
                    <label class="label">Width</label>
                    <div class="control">
                      <input id="create_width" class="input is-neon-white" type="number" />
                    </div>
                  </div>
                </td>
                <td>
                  <div class="field">
                    <label class="label">Height</label>
                    <div class="control">
                      <input id="create_height" class="input is-neon-white" type="number" />
                    </div>
                  </div>
                </td>
                <td></td>
                <td style="vertical-align: bottom;">
                  <label class="checkbox">
                    <input id="flip_horizontal" type="checkbox" />
                    Flip Horizontally
                  </label>
                  <br />
                  <label class="checkbox">
                    <input id="flip_vertical" type="checkbox" />
                    Flip Vertically
                  </label>
                </td>
              </tr>
              <tr>
                <td colspan="2" style="padding-top: 25px;">
                  <div class="field has-addons">
                    <div class="control">
                      <a class="button is-neon-cyan" id="choose_aimg_outdir_button">
                        <span class="icon is-small">
                          <i class="fas fa-folder-open"></i>
                        </span>
                        <span>Save to</span>
                      </a>
                    </div>
                    <div class="control is-expanded">
                      <input
                        id="create_outdir"
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
                        <select id="CRT_out_format">
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
                      <a v-on:click="testlog" class="button is-neon-cyan">Create</a>
                    </div>
                  </div>
                </td>
              </tr>
              <tr>
                <td colspan="4">
                  <div id="create_msgbox" class="create-msgbox"></div>
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
export default {
  methods: {
    testlog: function() {
      client.invoke("test", (error, res) => {
        console.log("error", error);
        console.log("res", res);
      });
      console.log("pressed!");
    }
  }
};
</script>
