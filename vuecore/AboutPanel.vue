<template>
  <div id="about_panel" class="container" style="display: none;">
    <div class="about-content">
      <div class="about-info">
        <img v-bind:src="logo" class="about-logo no-select-drag"/>
        <h1 class="about-software-name">TridentFrame</h1>
        <p class="about-software-version">v0.1.0-beta.7</p>
        <p class="about-software-author">Developed by StahlFerro</p>
      </div>
      <div class="about-buttons">
        <div class="field is-grouped is-grouped-centered">
          <p class="control">
            <a v-on:click="warpGithub" class="button is-neon-cyan is-medium">
              <span class="icon">
                <i class="fab fa-github"></i>
              </span>
              <span>Github</span>
            </a>
          </p>
          <!-- <p class="control">
            <a v-on:click="warpDonate" class="button is-neon-cyan is-medium">
              <span class="icon">
                <i class="fas fa-heart"></i>
              </span>
              <span>Donate</span>
            </a>
          </p> -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const { remote, shell } = require('electron');
const dialog = remote.dialog;
const session = remote.getCurrentWebContents().session;
const logo = require('../imgs/TridentFrame_logo_512x512.png');

let data = {
  logo: logo,
}

export default {
  data: function() {
    return {
      logo: logo,
    };
  },
  methods: {
    warpGithub() {
      shell.openExternal("https://github.com/StahlFerro/TridentFrame");
    },
    warpDonate() {
      shell.openExternal("https://en.liberapay.com/StahlFerro");
    },
  }
}
</script>
