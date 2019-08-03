console.log("SettingsFragment.js loaded!");
const remote = require('electron').remote;
const dialog = remote.dialog;
const session = remote.getCurrentWebContents().session;
const { client, ImageViewer } = require('./Client.js');
const { quintcell_generator, escapeHtml } = require('./Utils.js');
const { mboxClear, mboxError, mboxSuccess } = require('./MessageBox.js');

let refresh_button = document.getElementById('refresh_button');

refresh_button.addEventListener("click", () => {
    remote.getCurrentWindow().reload();
    session.clearCache(testcallback);
});

function testcallback(){
    console.log("cache cleared!!1");
}
