<template>
  <table
    id="main_table"
    class="table is-borderless is-desktop"
    style="width: 950px;height: 700px;table-layout: fixed; margin: 0;"
    width="100%"
  >
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
                <a id="minimize_button" class="minimize-button">
                  <span class="icon is-medium">
                    <i class="far fa-window-minimize fa-inverse"></i>
                  </span>
                </a>
                <a id="exit_button" class="exit-button">
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
                  v-bind:class="{'is-selected': menuselection == 0}"
                >
                  <a id="create_menu" v-on:click="menuselection = 0">
                    <span class="icon is-large">
                      <i class="fas fa-image fa-2x fa-inverse"></i>
                    </span>
                    <p class="is-white-d">Create AIMG</p>
                  </a>
                </li>
                <li
                  id="split_box"
                  class="menu-item"
                  v-bind:class="{'is-selected': menuselection == 1}"
                >
                  <a id="split_menu" v-on:click="menuselection = 1">
                    <span class="icon is-large">
                      <i class="far fa-images fa-2x fa-inverse"></i>
                    </span>
                    <p class="is-white-d">Split AIMG</p>
                  </a>
                </li>
                <li
                  id="modify_box"
                  class="menu-item"
                  v-bind:class="{'is-selected': menuselection == 2}"
                >
                  <a id="modify_menu" v-on:click="menuselection = 2">
                    <span class="icon is-large">
                      <i class="fas fa-exchange-alt fa-2x fa-inverse"></i>
                    </span>
                    <p class="is-white-d">Modify AIMG</p>
                  </a>
                </li>
                <li
                  id="buildsprite_box"
                  class="menu-item"
                  v-bind:class="{'is-selected': menuselection == 3}"
                >
                  <a id="buildsprite_menu" v-on:click="menuselection = 3">
                    <span class="icon is-large">
                      <i class="fas fa-border-all fa-2x fa-inverse"></i>
                    </span>
                    <p class="is-white-d">Build Spritesheet</p>
                  </a>
                </li>
                <li
                  id="slicesprite_box"
                  class="menu-item"
                  v-bind:class="{'is-selected': menuselection == 4}"
                >
                  <a id="slicesprite_menu" v-on:click="menuselection = 4">
                    <span class="icon is-large">
                      <i class="fas fa-th fa-2x fa-inverse"></i>
                    </span>
                    <p class="is-white-d">Slice Spritesheet</p>
                  </a>
                </li>
                <li
                  id="settings_box"
                  class="menu-item"
                  v-bind:class="{'is-selected': menuselection == 5}"
                >
                  <a id="settings_menu" v-on:click="menuselection = 5">
                    <span class="icon is-large">
                      <i class="fas fa-cog fa-2x fa-inverse"></i>
                    </span>
                    <p class="is-white-d">Settings</p>
                  </a>
                </li>
                <li
                  id="about_box"
                  class="menu-item"
                  v-bind:class="{'is-selected': menuselection == 6}"
                >
                  <a id="about_menu" v-on:click="menuselection = 6">
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
          <CreateFragment v-show="menuselection == 0" />
          <SplitFragment v-show="menuselection == 1" />
          <ModifyFragment v-show="menuselection == 2" />
          <BuildSpritesheetFragment v-show="menuselection == 3" />
          <SliceSpritesheetFragment v-show="menuselection == 4" />
          <SettingsFragment v-show="menuselection == 5" />
          <AboutFragment v-show="menuselection == 6" />
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import { client, ImageViewer } from "./vuecore/Client.vue";
import CreateFragment from "./vuecore/CreateFragment.vue";
import SplitFragment from "./vuecore/SplitFragment.vue";
import ModifyFragment from "./vuecore/ModifyFragment.vue";
import BuildSpritesheetFragment from "./vuecore/BuildSpritesheetFragment.vue";
import SliceSpritesheetFragment from "./vuecore/SliceSpritesheetFragment.vue";
import SettingsFragment from "./vuecore/SettingsFragment.vue";
import AboutFragment from "./vuecore/AboutFragment.vue";

var data = {
  menuselection: 0,
  message: "Hi!"
};

export default {
  name: "app",
  data: function() {
    return data;
  },
  components: {
    CreateFragment,
    SplitFragment,
    ModifyFragment,
    BuildSpritesheetFragment,
    SliceSpritesheetFragment,
    SettingsFragment,
    AboutFragment
  },
  methods: {
    switchem: function() {
      console.log("YO!");
      if (data.menuselection == 0) {
        data.menuselection = 1;
      } else {
        data.menuselection = 0;
      }
      console.log("menuselection", data.menuselection);
    },
    testlog: function() {
      console.log("pressed!");
    }
  }
};
</script>
