console.log("SettingsFragment.js loaded!");
const { remote, shell } = require('electron');
const dialog = remote.dialog;
const session = remote.getCurrentWebContents().session;
const { client, ImageViewer } = require('./Client.js');
const { quintcell_generator, escapeHtml } = require('./Utils.js');
const { mboxClear, mboxError, mboxSuccess } = require('./MessageBox.js');


let github_button = document.getElementById('github_button');
let donate_button = document.getElementById('donate_button');

github_button.addEventListener("click", () => {
    shell.openExternal("https://github.com/StahlFerro/TridentFrame");
    console.log('called');
});

donate_button.addEventListener("click", () => {
    shell.openExternal("https://en.liberapay.com/StahlFerro");
});
