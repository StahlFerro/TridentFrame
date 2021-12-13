<template>
  <!-- <table class="table root-table is-borderless" v-on:click="whatClicked($event)">
    <thead> -->
  <!-- <tr class="has-background-dark-2 frame-title-bar">
        <td width="10%" class="is-paddingless" style="vertical-align: middle;">
          <span style="padding-left: 10px;" class="is-white-d">TridentFrame</span>
        </td>
        <td width="90%" class="is-paddingless">
          <nav class="level is-marginless">
            <div class="level-left"></div>
            <div class="level-right has-text-centered">
              <div class="level-item">
                <a v-on:click="minimizeWindow" class="minimize-button">
                  <span class="icon is-medium">
                    <i class="far fa-window-minimize fa-inverse"></i>
                  </span>
                </a>
                <a v-on:click="maximizeWindow" class="exit-button">
                  <span class="icon is-medium">
                    <i class="fas fa-window-maximize fa-inverse"></i>
                  </span>
                </a>
                <a v-on:click="exitApp" class="exit-button">
                  <span class="icon is-medium">
                    <i class="fas fa-times fa-inverse"></i>
                  </span>
                </a>
              </div>
            </div>
          </nav>
        </td>
      </tr>
    </thead> -->
  <!-- <tbody>
      <tr> -->
  <div class="root-container">
    <div class="root-sidebar">
      <div class="left-menu">
        <aside class="menu has-text-centered" style="margin: 0">
          <ul class="menu-list left-menu">
            <li
              id="create_box"
              class="menu-item"
              v-bind:class="{ 'is-selected': menuselection == 'create_panel' }"
            >
              <a id="create_panel" v-on:click="menuselection = 'create_panel'">
                <span class="icon is-large">
                  <font-awesome-icon icon="image" size="2x" inverse/>
                  <!-- <i class="fas fa-image fa-2x fa-inverse"></i> -->
                </span>
                <p class="is-white-d">Create AIMG</p>
              </a>
            </li>
            <li
              id="split_box"
              class="menu-item"
              v-bind:class="{ 'is-selected': menuselection == 'split_panel' }"
            >
              <a id="split_panel" v-on:click="menuselection = 'split_panel'">
                <span class="icon is-large">
                  <font-awesome-icon icon="images" size="2x" inverse/>
                  <!-- <i class="far fa-images fa-2x fa-inverse"></i> -->
                </span>
                <p class="is-white-d">Split AIMG</p>
              </a>
            </li>
            <li
              id="modify_box"
              class="menu-item"
              v-bind:class="{ 'is-selected': menuselection == 'modify_panel' }"
            >
              <a id="modify_panel" v-on:click="menuselection = 'modify_panel'">
                <span class="icon is-large">
                  <font-awesome-icon icon="exchange-alt" size="2x" inverse/>
                  <!-- <i class="fas fa-exchange-alt fa-2x fa-inverse"></i> -->
                </span>
                <p class="is-white-d">Modify AIMG</p>
              </a>
            </li>
            <!-- <li
              id="buildsprite_box"
              class="menu-item"
              v-bind:class="{ 'is-selected': menuselection == 'buildspritesheet_panel' }"
            >
              <a
                id="buildsprite_menu"
                v-on:click="menuselection = 'buildspritesheet_panel'"
              >
                <span class="icon is-large">
                  <i class="fas fa-border-all fa-2x fa-inverse"></i>
                </span>
                <p class="is-white-d">Build Spritesheet</p>
              </a>
            </li>
            <li
              id="slicesprite_box"
              class="menu-item"
              v-bind:class="{ 'is-selected': menuselection == 'slicespritesheet_panel' }"
            >
              <a
                id="slicesprite_menu"
                v-on:click="menuselection = 'slicespritesheet_panel'"
              >
                <span class="icon is-large">
                  <i class="fas fa-th fa-2x fa-inverse"></i>
                </span>
                <p class="is-white-d">Slice Spritesheet</p>
              </a>
            </li> -->
            <li
              id="inspect_box"
              class="menu-item"
              v-bind:class="{ 'is-selected': menuselection == 'inspect_panel' }"
            >
              <a id="inspect_panel" v-on:click="menuselection = 'inspect_panel'">
                <span class="icon is-large">
                  <font-awesome-icon icon="search" size="2x" inverse/>
                  <!-- <i class="fas fa-search fa-2x fa-inverse"></i> -->
                </span>
                <p class="is-white-d">Inspect Image</p>
              </a>
            </li>
            <!-- <li
              id="tile_box"
              class="menu-item"
              v-bind:class="{ 'is-selected': menuselection == 'tiles_panel' }"
            >
              <a id="tile_menu" v-on:click="menuselection = 'tiles_panel'">
                <span class="icon is-large">
                  <i class="fas fa-search fa-2x fa-inverse"></i>
                </span>
                <p class="is-white-d">Tiles Panel</p>
              </a>
            </li> -->
            <li
              id="settings_box"
              class="menu-item"
              v-bind:class="{ 'is-selected': menuselection == 'settings_panel' }"
            >
              <a id="settings_panel" v-on:click="menuselection = 'settings_panel'">
                <span class="icon is-large">
                  <font-awesome-icon icon="cog" size="2x" inverse/>
                  <!-- <i class="fas fa-cog fa-2x fa-inverse"></i> -->
                </span>
                <p class="is-white-d">Settings</p>
              </a>
            </li>
            <!-- <li
              id="about_box"
              class="menu-item"
              v-bind:class="{ 'is-selected': menuselection == 'about_panel' }"
            >
              <a id="about_panel" v-on:click="menuselection = 'about_panel'">
                <span class="icon is-large">
                  <font-awesome-icon icon="info-circle" size="2x" inverse/>
                </span>
                <p class="is-white-d">About</p>
              </a>
            </li> -->
          </ul>
        </aside>
      </div>
    </div>
    <div class="root-panel">
      <!-- $refs.ctxmenu.open($event, 'Payload') -->
        <CreatePanel v-show="menuselection == 'create_panel'" />
        <SplitPanel v-show="menuselection == 'split_panel'" />
        <ModifyPanel v-show="menuselection == 'modify_panel'" />
        <!-- <BuildSpritesheetPanel v-show="menuselection == 'buildspritesheet_panel'" /> -->
        <!-- <SliceSpritesheetPanel v-show="menuselection == 'slicespritesheet_panel'" /> -->
        <InspectPanel v-show="menuselection == 'inspect_panel'" @open-root-ctxmenu="openRootContextMenu" @close-root-ctxmenu="closeRootContextMenu"/>
        <!-- <TilesPanel v-show="menuselection == 'tiles_panel'" /> -->
        <SettingsPanel v-show="menuselection == 'settings_panel'" />
        <!-- <AboutPanel v-show="menuselection == 'about_panel'" /> -->
    </div>
    <div>
      <ContextMenu ref="ctxmenu">
        <template slot-scope="{ contextData }">
          <ContextMenuItem v-for="(ctxData, ctxIndex) in contextData" v-bind:key="ctxIndex" 
            @click.native="$refs.ctxmenu.callOptionFunction(ctxData.callback);">
              {{ ctxData.name }}
          </ContextMenuItem>
        </template>
      </ContextMenu>
    </div>
  </div>

  <!-- </td>
      </tr>
    </tbody> -->
  <!-- </table> -->
</template>

<script>

// import { client } from "./src/Client.vue";
// import { client, ImageViewer } from "./src/Client.vue";
// const { tridentEngine } = require("./src/modules/streams/trident_engine")
import ContextMenu from './view/components/ContextMenu/ContextMenu.vue';
import ContextMenuItem from './view/components/ContextMenu/ContextMenuItem.vue';

import CreatePanel from "./view/CreatePanel.vue";
import SplitPanel from "./view/SplitPanel.vue";
import ModifyPanel from "./view/ModifyPanel.vue";
// import BuildSpritesheetPanel from "./src/BuildSpritesheetPanel.vue";
// import SliceSpritesheetPanel from "./src/SliceSpritesheetPanel.vue";
import InspectPanel from "./view/InspectPanel.vue";
// import TilesPanel from "./src/TilesPanel.vue";
import SettingsPanel from "./view/SettingsPanel.vue";
// import AboutPanel from "./view/AboutPanel.vue";


export default {
  created() {
    window.addEventListener("resize", this.closeRootContextMenu);
  },
  destroyed() {
    window.removeEventListener("resize", this.closeRootContextMenu);
  },
  name: "app",
  data: function () {
    return {
      menuselection: "create_panel",
    };
  },
  components: {
    CreatePanel,
    SplitPanel,
    ModifyPanel,
    // BuildSpritesheetPanel,
    // SliceSpritesheetPanel,
    InspectPanel,
    // TilesPanel,
    SettingsPanel,
    // AboutPanel,
    ContextMenu,
    ContextMenuItem,
  },
  methods: {
    openRootContextMenu(event, payload) {
      console.log("openContextMenu");
      console.log(event);
      console.log(payload);
      this.$refs.ctxmenu.openPopper(event, payload);
    },
    closeRootContextMenu(event){
      this.$refs.ctxmenu.closePopper();
    },
    whatClicked(event) {
      console.log(`CLICK!!!`);
      console.log(event);
    },
  },
};
</script>
