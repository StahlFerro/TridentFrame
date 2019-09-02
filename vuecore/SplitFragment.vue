<template>
  <div id="split_panel" class="container" style="display: none; padding:10px;">
    <div class="content">
      <table class="table is-borderless" style="padding: 5px;" width="100%">
        <tr>
          <td
            id="split_aimg_cell"
            class="silver-bordered force-center is-paddingless"
            width="45%"
            style="height: 380px;"
          >
            <div class="spl-aimg-container">
              <span class="aimg-helper"></span>
              <img id="SPL_aimg_stage" src />
            </div>
            <input id="SPL_aimg_path" name="SPL_aimg_path_field" type="hidden" value />
          </td>
          <td width="55%" class="is-paddingless silver-bordered">
            <table class="table spl-aimg-info-table" width="100%">
              <thead>
                <tr>
                  <th colspan="2">
                    <p id="info_header" class="is-white-d">Information</p>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="spl-info-label is-cyan">Name</td>
                  <td class="spl-info-data" id="aimg_name">-</td>
                </tr>
                <tr>
                  <td class="spl-info-label is-cyan">Dimensions</td>
                  <td class="spl-info-data" id="aimg_dimens">-</td>
                </tr>
                <tr>
                  <td class="spl-info-label is-cyan">File Size</td>
                  <td class="spl-info-data" id="aimg_file_size">-</td>
                </tr>
                <tr>
                  <td class="spl-info-label is-cyan">Total frames</td>
                  <td class="spl-info-data" id="aimg_frame_count">-</td>
                </tr>
                <tr>
                  <td class="spl-info-label is-cyan">Total frames (DS)</td>
                  <td class="spl-info-data" id="aimg_frame_count_ds">-</td>
                </tr>
                <tr>
                  <td class="spl-info-label is-cyan">Frame rate</td>
                  <td class="spl-info-data" id="aimg_fps">-</td>
                </tr>
                <tr>
                  <td class="spl-info-label is-cyan">Frame delay</td>
                  <td class="spl-info-data" id="aimg_frame_delay">-</td>
                </tr>
                <tr>
                  <td class="spl-info-label is-cyan">Loop duration</td>
                  <td class="spl-info-data" id="aimg_duration">-</td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
        <tr>
          <td class="is-hpaddingless">
            <a class="button is-neon-cyan" id="SPL_load_aimg_button">
              <span class="icon is-small">
                <i class="fas fa-plus"></i>
              </span>
              <span>Load GIF/APNG</span>
            </a>
            <a class="button is-neon-white" id="SPL_clear_aimg_button">
              <span class="icon is-small">
                <i class="fas fa-trash-alt"></i>
              </span>
              <span>Clear</span>
            </a>
            <a class="button is-neon-white" id="SPL_bgprev_button">
              <span class="icon is-medium">
                <i class="fas fa-chess-board"></i>
              </span>
            </a>
          </td>
          <td></td>
        </tr>
        <tr>
          <td id="SPL_control_cell" class="is-paddingless" colspan="2">
            <table class="table control-table" width="100%">
              <tr>
                <td width="20%">
                  <div class="field">
                    <label class="label">Pad count</label>
                    <div class="control">
                      <input
                        id="SPL_pad_count"
                        class="input is-neon-white"
                        type="number"
                        min="1"
                        max="6"
                      />
                    </div>
                  </div>
                </td>
                <td width="25%">
                  <div class="field">
                    <label class="label">Color space</label>
                    <div class="control">
                      <input
                        id="SPL_color_space"
                        class="input is-neon-white"
                        type="number"
                        min="2"
                        max="256"
                        disabled
                      />
                    </div>
                  </div>
                </td>
                <td width="25%" style="vertical-align: middle;">
                  <label class="checkbox">
                    <input id="is_duration_sensitive" type="checkbox" />
                    Duration-sensitive
                  </label>
                  <label class="checkbox">
                    <input id="SPL_is_reduced_color" type="checkbox" />
                    Reduce Colors
                  </label>
                </td>
                <td width="30%" style="vertical-align: middle;"></td>
              </tr>
              <tr>
                <td colspan="3">
                  <div class="field has-addons">
                    <div class="control">
                      <a class="button is-neon-cyan" id="choose_seq_outdir_button">
                        <span class="icon is-small">
                          <i class="fas fa-folder-open"></i>
                        </span>
                        <span>Save to</span>
                      </a>
                    </div>
                    <div class="control is-expanded">
                      <input
                        id="target_seq_path"
                        class="input is-neon-white"
                        type="text"
                        placeholder="Output folder"
                        readonly
                      />
                    </div>
                  </div>
                </td>
                <td class="has-text-centered">
                  <a class="button is-neon-cyan" id="SPL_split_aimg_button">Split to folder</a>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td colspan="2" class="has-text-left" style="vertical-align: middle;" id="split_msgbox"></td>
        </tr>
      </table>
    </div>
  </div>
</template>