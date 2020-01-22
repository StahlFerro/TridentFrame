<template>
  <div id="about_panel" class="container has-text-centered" style="display: none; padding:10px;">
    <div class="about-content">
      <table class="table about-table" width="100%">
        <tr>
          <td class="has-text-centered">
            <img v-bind:src="logo" width="200px;" height="200px;" />
          </td>
        </tr>
        <tr>
          <td class="has-text-centered is-vcentered">
            <h1 class="title is-1">TridentFrame</h1>
            <p class="subtitle is-4">v1.0.0</p>
          </td>
        </tr>
        <tr>
          <td class="has-text-centered is-vcentered">
            <p>Developed by Andreas Pangestu</p>
            <!-- <div class="field is-grouped is-grouped-centered">
              <p class="control">
                <a v-on:click="warpGithub" class="button is-neon-cyan is-medium">
                  <span class="icon">
                    <i class="fab fa-github"></i>
                  </span>
                  <span>Github</span>
                </a>
              </p>
              <p class="control">
                <a v-on:click="warpDonate" class="button is-neon-cyan is-medium">
                  <span class="icon">
                    <i class="fas fa-heart"></i>
                  </span>
                  <span>Donate</span>
                </a>
              </p>
            </div> -->
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
const { remote, shell } = require('electron');
const dialog = remote.dialog;
const session = remote.getCurrentWebContents().session;
const logo = require('../imgs/TridentFrame_logo_512x512.png');

function warpGithub() {
  shell.openExternal("https://github.com/StahlFerro/TridentFrame");
}

function warpDonate() {
  shell.openExternal("https://en.liberapay.com/StahlFerro");
}

let data = {
  logo: logo,
}

export default {
  data: function() {
    return data;
  },
  methods: {
    warpGithub: warpGithub,
    warpDonate: warpDonate,
  }
}
</script>
