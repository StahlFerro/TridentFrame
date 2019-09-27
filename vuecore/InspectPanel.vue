<template>
  <div id="inspect_panel" class="container" style="padding:10px;">
    <table class="table is-borderless" style="padding: 5px;" width="100%">
      <tr>
        <td class="silver-bordered force-center is-paddingless" width="45%" style="height: 380px;">
            <img v-bind:src="img_path"/>
        </td>
        <td width="55%" class="is-paddingless silver-bordered">
            <table class="table" width="100%">
            </table>
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
var data = {
    img_path: "",
    checkerbg_active: false,
    isButtonFrozen: false,
    INS_IS_INSPECTING: false,
};
function loadImage() {

}
function clearImage() {

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
