<template>
  <table class="table root-table is-borderless">
    <thead>
      <tr class="has-background-dark-2 frame-title-bar" style="height: 30px;">
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
    </thead>
    <tbody>
      <tr>
        <td width="10%" id="left_menu_panel" class="has-background-dark-2">
          <div class="left-menu">
            <aside class="menu has-text-centered" style="margin: 0;">
              <ul class="menu-list left-menu">
                <li
                  id="create_box"
                  class="menu-item"
                  v-bind:class="{'is-selected': menuselection == 'create_panel'}"
                >
                  <a id="create_menu" v-on:click="menuselection = 'create_panel'">
                    <span class="icon is-large">
                      <i class="fas fa-image fa-2x fa-inverse"></i>
                    </span>
                    <p class="is-white-d">Create AIMG</p>
                  </a>
                </li>
                <li
                  id="split_box"
                  class="menu-item"
                  v-bind:class="{'is-selected': menuselection == 'split_panel'}"
                >
                  <a id="split_menu" v-on:click="menuselection = 'split_panel'">
                    <span class="icon is-large">
                      <i class="far fa-images fa-2x fa-inverse"></i>
                    </span>
                    <p class="is-white-d">Split AIMG</p>
                  </a>
                </li>
                <li
                  id="modify_box"
                  class="menu-item"
                  v-bind:class="{'is-selected': menuselection == 'modify_panel'}"
                >
                  <a id="modify_menu" v-on:click="menuselection = 'modify_panel'">
                    <span class="icon is-large">
                      <i class="fas fa-exchange-alt fa-2x fa-inverse"></i>
                    </span>
                    <p class="is-white-d">Modify AIMG</p>
                  </a>
                </li>
                <li
                  id="buildsprite_box"
                  class="menu-item"
                  v-bind:class="{'is-selected': menuselection == 'buildspritesheet_panel'}"
                >
                  <a id="buildsprite_menu" v-on:click="menuselection = 'buildspritesheet_panel'">
                    <span class="icon is-large">
                      <i class="fas fa-border-all fa-2x fa-inverse"></i>
                    </span>
                    <p class="is-white-d">Build Spritesheet</p>
                  </a>
                </li>
                <li
                  id="slicesprite_box"
                  class="menu-item"
                  v-bind:class="{'is-selected': menuselection == 'slicespritesheet_panel'}"
                >
                  <a id="slicesprite_menu" v-on:click="menuselection = 'slicespritesheet_panel'">
                    <span class="icon is-large">
                      <i class="fas fa-th fa-2x fa-inverse"></i>
                    </span>
                    <p class="is-white-d">Slice Spritesheet</p>
                  </a>
                </li>
                <li
                  id="settings_box"
                  class="menu-item"
                  v-bind:class="{'is-selected': menuselection == 'settings_panel'}"
                >
                  <a id="settings_menu" v-on:click="menuselection = 'settings_panel'">
                    <span class="icon is-large">
                      <i class="fas fa-cog fa-2x fa-inverse"></i>
                    </span>
                    <p class="is-white-d">Settings</p>
                  </a>
                </li>
                <li
                  id="about_box"
                  class="menu-item"
                  v-bind:class="{'is-selected': menuselection == 'about_panel'}"
                >
                  <a id="about_menu" v-on:click="menuselection = 'about_panel'">
                    <span class="icon is-large">
                      <i class="fas fa-info-circle fa-2x fa-inverse"></i>
                    </span>
                    <p class="is-white-d">About</p>
                  </a>
                </li>
              </ul>
            </aside>
          </div>
        </td>
        <td width="90%" id="panel_container">
          <CreatePanel v-show="menuselection == 'create_panel'" />
          <SplitPanel v-show="menuselection == 'split_panel'" />
          <ModifyPanel v-show="menuselection == 'modify_panel'" />
          <BuildSpritesheetPanel v-show="menuselection == 'buildspritesheet_panel'" />
          <SliceSpritesheetPanel v-show="menuselection == 'slicespritesheet_panel'" />
          <SettingsPanel v-show="menuselection == 'settings_panel'" />
          <AboutPanel v-show="menuselection == 'about_panel'" />
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
const remote = require("electron").remote;
const session = remote.getCurrentWebContents().session;

import { client, ImageViewer } from "./vuecore/Client.vue";
import CreatePanel from "./vuecore/CreatePanel.vue";
import SplitPanel from "./vuecore/SplitPanel.vue";
import ModifyPanel from "./vuecore/ModifyPanel.vue";
import BuildSpritesheetPanel from "./vuecore/BuildSpritesheetPanel.vue";
import SliceSpritesheetPanel from "./vuecore/SliceSpritesheetPanel.vue";
import SettingsPanel from "./vuecore/SettingsPanel.vue";
import AboutPanel from "./vuecore/AboutPanel.vue";

var data = {
  menuselection: "create_panel",
};

export default {
  name: "app",
  data: function() {
    return data;
  },
  components: {
    CreatePanel,
    SplitPanel,
    ModifyPanel,
    BuildSpritesheetPanel,
    SliceSpritesheetPanel,
    SettingsPanel,
    AboutPanel
  },
  methods: {
    minimizeWindow: function () {
      var window = remote.getCurrentWindow();
      window.minimize();
    },
    exitApp: function() {
      var window = remote.getCurrentWindow();
      window.close();
    }
  }
};
</script>
