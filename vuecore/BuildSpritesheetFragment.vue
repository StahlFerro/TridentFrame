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
                <tbody id="BSPR_sequence_body"></tbody>
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
                            <select id="BSPR_in_format">
                              <option value="sequence">From Sequence</option>
                              <!-- <option value="aimg">From GIF/APNG</option> -->
                            </select>
                          </div>
                        </div>
                      </div>
                      <div class="field">
                        <a id="BSPR_input_button" class="button is-neon-cyan">
                          <span class="icon is-small">
                            <i class="fas fa-plus"></i>
                          </span>
                          <span id="BSPR_input_button_text">Add</span>
                        </a>
                        <a id="BSPR_clear_imgs_button" class="button is-neon-white">
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
                  <p id="BSPR_sequence_counter_label"></p>
                </div>
                <input
                  id="BSPR_sequence_counter"
                  name="BSPR_sequence_counter_field"
                  type="hidden"
                  value
                />
              </div>
              <div class="level-item has-text-right">
                <div>
                  <span id="BSPR_final_dimens"></span>
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
                      <input id="BSPR_create_name" class="input is-neon-white" type="text" />
                    </div>
                  </div>
                </td>
                <td>
                  <div class="field">
                    <label class="label">Tile Width</label>
                    <div class="control">
                      <input id="BSPR_tile_width" class="input is-neon-white" type="number" />
                    </div>
                  </div>
                </td>
                <td>
                  <div class="field">
                    <label class="label">Tile Height</label>
                    <div class="control">
                      <input
                        id="BSPR_tile_height"
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
                        id="BSPR_tile_row"
                        class="input is-neon-white"
                        type="number"
                        min="1"
                        max="50"
                      />
                    </div>
                  </div>
                </td>
              </tr>
              <!-- <tr>
                                                <td>
                                                    <div class="field">
                                                        <label class="label">Name</label>
                                                        <div class="control"><input id="BSPR_create_name" class="input is-neon-white" type="text"/></div>
                                                    </div>
                                                </td>
                                                <td>
                                                    <div class="field">
                                                        <label class="label">Sheet Columns</label>
                                                        <div class="control"><input id="spr_sheet_columns" class="input is-neon-white" type="number"/></div>
                                                    </div>
                                                </td>
                                                <td>
                                                    <div class="field">
                                                        <label class="label">Sheet Rows</label>
                                                        <div class="control"><input id="spr_sheet_rows" class="input is-neon-white" type="number" min="1" max="50"/></div>
                                                    </div>
                                                </td>
                                                <td>
                                                </td>
              </tr>-->
              <tr>
                <td colspan="2" style="padding-top: 25px;">
                  <div class="field has-addons">
                    <div class="control">
                      <a id="BSPR_outdir_button" class="button is-neon-cyan">
                        <span class="icon is-small">
                          <i class="fas fa-folder-open"></i>
                        </span>
                        <span>Save to</span>
                      </a>
                    </div>
                    <div class="control is-expanded">
                      <input
                        id="BSPR_outdir_path"
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
                      <a id="BSPR_create_button" class="button is-neon-cyan">Create</a>
                    </div>
                  </div>
                </td>
              </tr>
              <tr>
                <td
                  colspan="4"
                  class="has-text-left"
                  style="vertical-align: middle;"
                  id="bspr_msgbox"
                ></td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>