<template>
  <div id="inspect_panel" class="container" style="padding:10px;">
    <table class="table is-borderless" style="padding: 5px;" width="100%">
      <tr>
        <td class="silver-bordered force-center is-paddingless" 
            style="width: 320px; height: 320px;">
          <div class="ins-img-container is-paddingless is-marginless">
            <span class="aimg-helper"></span>
            <img v-bind:src="img_path"/>
          </div>
        </td>
        <td class="is-paddingless silver-bordered"
            style="width: 500px; height: 320px;">
          <div class="is-paddingless is-marginless" style="height: 320px; overflow: auto;">
            <table class="table ins-info-table is-paddingless" width="100%">
              <template v-for="(item, key) in info_data">
                <tr v-if="key == 'general_info'">
                  <td colspan="2" class="is-cyan">GENERAL INFO</td>
                </tr>
                <tr v-if="key == 'animation_info'">
                  <td colspan="2" class="is-cyan">ANIMATION INFO</td>
                </tr>
                <tr v-for="(item, key, index) in item" v-bind:key="key">
                  <td style="width: 123px;">
                    <strong><span class="is-white-d">{{ item.label }}</span></strong>
                  </td>  
                  <td style="max-width: 369px; word-wrap: break-all;">{{ item.value }}</td>
                </tr>
              </template>
            </table>
          </div>
        </td>
      </tr>

      <tr>
        <td class="is-hpaddingless">
          <a
            v-on:click="loadImage"
            class="button is-neon-cyan"
            v-bind:class="{'is-loading': INS_IS_INSPECTING, 'is-static': isButtonFrozen}"
          >
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
    </table>
  </div>
</template>

<script>
const remote = require("electron").remote;
const dialog = remote.dialog;
const mainWindow = remote.getCurrentWindow();
const session = remote.getCurrentWebContents().session;
const { client } = require("./Client.vue");
const { ticks } = require("./Utility.vue");

let extension_filters = [{ name: "Images", extensions: ["png", "gif", "jpg"] }];
let file_dialog_props = ["openfile"];
let dir_dialog_props = ["openDirectory", "createDirectory"];

var data = {
    img_path: "",
    checkerbg_active: false,
    isButtonFrozen: false,
    INS_IS_INSPECTING: false,
    info_data: "",
};
function loadImage() {
  var options = {
    filters: extension_filters,
    properties: file_dialog_props
  };
  dialog.showOpenDialog(mainWindow, options, (chosen_path) => {
    console.log(`chosen path: ${chosen_path}`);
    if (chosen_path === undefined || chosen_path.length == 0) {
      return;
    }
    client.invoke("inspect_one", chosen_path[0], "", (error, res) => {
      if (error) {
        console.error(error);
      }
      else {
        data.info_data = res;
        data.img_path = `${res.general_info.absolute_url.value}?timestamp=${ticks()}`;;
        console.log(res);
      }
    })
  });
}
function clearImage() {
  data.img_path = "";
  data.info_data = "";
}
function toggleCheckerBG() {

}
export default {
  data: function() {
    return data;
  },
  methods: {
      loadImage: loadImage,
      clearImage: clearImage,
      toggleCheckerBG: toggleCheckerBG,
  }
};

</script>
