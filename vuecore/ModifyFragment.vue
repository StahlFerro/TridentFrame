<template>
  <div id="modify_panel" class="container" style="display: none; padding:10px;">
    <!-- <div class="content"> -->
    <table class="table is-borderless" style="padding: 5px;" width="100%">
      <tr>
        <!-- <td width="3%"></td> -->
        <td
          width="35%"
          colspan="3"
          id="MOD_orig_cell"
          class="silver-bordered force-center is-paddingless"
          style="height: 250px;"
        >
          <div class="mod-aimg-container">
            <span class="aimg-helper"></span>
            <img id="MOD_orig_stage" src />
          </div>
          <input id="MOD_orig_path" name="MOD_orig_path_field" type="hidden" value />
        </td>
        <!-- <td width="3%"></td> -->

        <td width="6%"></td>
        <td width="9%"></td>
        <td
          width="35%"
          id="MOD_new_cell"
          class="silver-bordered force-center is-paddingless"
          style="height: 250px;"
        >
          <div class="mod-aimg-container">
            <span class="aimg-helper"></span>
            <img id="MOD_new_stage" src />
          </div>
          <input id="MOD_new_path" name="MOD_new_path_field" type="hidden" value />
        </td>
        <td width="9%"></td>
        <td width="6%"></td>
      </tr>
      <tr>
        <td width="41%" colspan="3" class="has-text-centered is-hpaddingless">
          <a class="button is-neon-cyan" id="MOD_load_aimg_button">
            <span class="icon is-small">
              <i class="fas fa-plus"></i>
            </span>
            <span>Load GIF/APNG</span>
          </a>
          <a class="button is-neon-white" id="MOD_clear_aimg_button">
            <span class="icon is-small">
              <i class="fas fa-trash-alt"></i>
            </span>
            <span>Clear</span>
          </a>
          <a class="button is-neon-white" id="MOD_orig_bgprev_button">
            <span class="icon is-medium">
              <i class="fas fa-chess-board"></i>
            </span>
          </a>
        </td>
        <td width="59%" colspan="5" class="has-text-centered is-hpaddingless">
          <a class="button is-neon-cyan" id="MOD_prev_res_button">
            <span class="icon is-small">
              <i class="fas fa-eye"></i>
            </span>
            <span>Preview</span>
          </a>
          <a class="button is-neon-white" id="MOD_new_bgprev_button">
            <span class="icon is-medium">
              <i class="fas fa-chess-board"></i>
            </span>
          </a>
        </td>
      </tr>
      <tr>
        <td width="35%" colspan="3" class="is-paddingless silver-bordered">
          <table class="table mod-orig-info-table is-hpaddingless" width="100%">
            <tbody>
              <tr>
                <td class="mod-info-label is-cyan">Name</td>
                <td class="mod-info-data" id="MOD_orig_name">-</td>
              </tr>
              <tr>
                <td class="mod-info-label is-cyan">Dimensions</td>
                <td class="mod-info-data" id="MOD_orig_dimensions">-</td>
              </tr>
              <tr>
                <td class="mod-info-label is-cyan">Total frames</td>
                <td class="mod-info-data" id="MOD_orig_framecount">-</td>
              </tr>
              <tr>
                <td class="mod-info-label is-cyan">Frame rate</td>
                <td class="mod-info-data" id="MOD_orig_fps">-</td>
              </tr>
              <tr>
                <td class="mod-info-label is-cyan">Frame delay</td>
                <td class="mod-info-data" id="MOD_orig_delay">-</td>
              </tr>
              <tr>
                <td class="mod-info-label is-cyan">Loop duration</td>
                <td class="mod-info-data" id="MOD_orig_loopduration">-</td>
              </tr>
              <tr>
                <td class="mod-info-label is-cyan">Format</td>
                <td class="mod-info-data" id="MOD_orig_format">-</td>
              </tr>
            </tbody>
          </table>
        </td>
        <td
          width="65%"
          colspan="5"
          class="has-text-centered is-right-paddingless silver-bordered-left-thicc"
        >
          <table class="table is-paddingless is-marginless" width="100%">
            <tr>
              <td width="10%" class="mod-menu-cell is-paddingless">
                <div class="mod-left-menu">
                  <aside class="menu has-text-centered" style="margin: 0;">
                    <ul class="menu-list mod-left-menu">
                      <li id="MOD_box_general" class="mod-menu-item is-selected">
                        <a id="MOD_menu_general">
                          <span class="icon is-large">
                            <i class="fas fa-image fa-2x fa-inverse"></i>
                          </span>
                          <p class="is-white-d">General</p>
                        </a>
                      </li>
                      <li id="MOD_box_gif" class="mod-menu-item">
                        <a id="MOD_menu_gif">
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
                <div id="MOD_general_control_panel">
                  <table class="table mod-new-control-table is-hpaddingless" width="100%">
                    <tr>
                      <td width="40%" colspan="2">
                        <div class="field">
                          <label class="label">Name</label>
                          <div class="control">
                            <input id="MOD_new_name" class="input is-neon-white" type="text" />
                          </div>
                        </div>
                      </td>
                      <td width="20%">
                        <div class="field">
                          <label class="label">Width</label>
                          <div class="control">
                            <input id="MOD_new_width" class="input is-neon-white" type="text" />
                          </div>
                        </div>
                      </td>
                      <td width="20%">
                        <div class="field">
                          <label class="label">Height</label>
                          <div class="control">
                            <input id="MOD_new_height" class="input is-neon-white" type="text" />
                          </div>
                        </div>
                      </td>
                      <td width="20%">
                        <div class="field">
                          <label class="label">Rotation</label>
                          <div class="control">
                            <input id="MOD_new_rotation" class="input is-neon-white" type="number" />
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td width="20%">
                        <div class="field">
                          <label class="label">FPS</label>
                          <div class="control">
                            <input id="MOD_new_fps" class="input is-neon-white" type="number" />
                          </div>
                        </div>
                      </td>
                      <td width="20%">
                        <div class="field">
                          <label class="label">Duration</label>
                          <div class="control">
                            <input id="MOD_new_delay" class="input is-neon-white" type="number" />
                          </div>
                        </div>
                      </td>
                      <td width="20%">
                        <div class="field">
                          <label class="label">Skip Frames</label>
                          <div class="control">
                            <input
                              id="MOD_new_frame_skip"
                              class="input is-neon-white"
                              type="number"
                              min="0"
                            />
                          </div>
                        </div>
                      </td>
                      <td width="20%"></td>
                      <td width="20%">
                        <div class="field">
                          <label class="label">Format</label>
                          <div class="control">
                            <div class="select is-neon-cyan">
                              <select id="MOD_new_format">
                                <option value="gif">GIF</option>
                                <option value="apng">APNG</option>
                              </select>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td width="20%" class="force-vcenter">
                        <label class="checkbox">
                          <input id="MOD_new_flip_x" type="checkbox" />
                          Flip X
                        </label>
                        <label class="checkbox">
                          <input id="MOD_new_flip_y" type="checkbox" />
                          Flip Y
                        </label>
                      </td>
                      <td width="40%" class="force-vcenter" colspan="2">
                        <label class="checkbox">
                          <input id="MOD_new_reversed" type="checkbox" />
                          Reversed
                        </label>
                        <label class="checkbox">
                          <input id="MOD_new_preserve_alpha" type="checkbox" />
                          Preserve Transparency
                        </label>
                      </td>
                    </tr>
                    <tr>
                      <td colspan="4">
                        <div class="field has-addons">
                          <div class="control">
                            <a class="button is-neon-cyan" id="MOD_outdir_button">
                              <span class="icon is-small">
                                <i class="fas fa-folder-open"></i>
                              </span>
                              <span>Save to</span>
                            </a>
                          </div>
                          <div class="control is-expanded">
                            <input
                              id="MOD_outdir"
                              class="input is-neon-white"
                              type="text"
                              placeholder="Output folder"
                              readonly
                            />
                          </div>
                        </div>
                      </td>
                      <td>
                        <a class="button is-neon-cyan" id="MOD_modify_aimg_button">MODIFY</a>
                      </td>
                    </tr>
                  </table>
                </div>
                <div id="MOD_gif_control_panel" style="display: none;">
                  <table class="table mod-new-control-table is-hpaddingless" width="100%">
                    <tr>
                      <td class="force-vcenter" width="20%">
                        <label class="checkbox">
                          <input id="MOD_new_is_optimized" type="checkbox" />
                          Optimize
                        </label>
                      </td>
                      <td class="force-vcenter" width="20%">
                        <div class="field">
                          <!-- <label class="label">Optimization Level</label> -->
                          <div class="control">
                            <div class="select is-neon-cyan">
                              <select id="MOD_new_optimization_level" disabled>
                                <option value="opt_1">Level 1</option>
                                <option value="opt_2">Level 2</option>
                                <option value="opt_3">Level 3</option>
                              </select>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td class="force-vcenter" width="20%">
                        <label class="checkbox">
                          <input id="MOD_new_is_lossy" type="checkbox" />
                          Lossy-compress
                        </label>
                      </td>
                      <td class="force-vcenter" width="20%">
                        <div class="field">
                          <!-- <label class="label">Color space</label> -->
                          <div class="control">
                            <input
                              id="MOD_new_lossy_value"
                              class="input is-neon-white"
                              type="number"
                              min="30"
                              max="200"
                              value="30"
                              disabled
                            />
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td class="force-vcenter" width="20%">
                        <label class="checkbox">
                          <input id="MOD_new_reduced_color" type="checkbox" />
                          Reduce Colors
                        </label>
                      </td>
                      <td class="force-vcenter" width="20%">
                        <div class="field">
                          <!-- <label class="label">Color space</label> -->
                          <div class="control">
                            <input
                              id="MOD_color_space"
                              class="input is-neon-white"
                              type="number"
                              min="2"
                              max="256"
                              value="256"
                              disabled
                            />
                          </div>
                        </div>
                      </td>
                    </tr>
                  </table>
                </div>
              </td>
            </tr>
          </table>
        </td>
      </tr>
      <tr>
        <td colspan="8" class="has-text-left" style="vertical-align: middle;" id="modify_msgbox"></td>
      </tr>
    </table>
    <!-- </div> -->
  </div>
</template>