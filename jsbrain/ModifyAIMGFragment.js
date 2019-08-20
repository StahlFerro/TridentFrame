console.log('ConvertFragment.js loaded!');
const remote = require('electron').remote;
const dialog = remote.dialog;
const session = remote.getCurrentWebContents().session;
const { client } = require('./Client.js');
const { mboxClear, mboxError, mboxSuccess } = require('./MessageBox.js');
const { escapeHtml } = require('./Utils.js')

let MOD_load_aimg_button = document.getElementById('MOD_load_aimg_button');
let MOD_clear_aimg_button = document.getElementById('MOD_clear_aimg_button');
let MOD_bgprev_button = document.getElementById('MOD_bgprev_button');
let MOD_in_cell = document.getElementById('MOD_in_cell');
let MOD_in_stage = document.getElementById('MOD_in_stage');
let MOD_in_path = document.getElementById('MOD_in_path');

let MOD_in_name = document.getElementById('MOD_in_name');
let MOD_in_format = document.getElementById('MOD_in_format');
let MOD_in_dimensions = document.getElementById('MOD_in_dimensions');
let MOD_in_duration = document.getElementById('MOD_in_duration');
let MOD_in_fps = document.getElementById('MOD_in_fps');


let convert_checkerbg_active = false;

MOD_bgprev_button.addEventListener('click', () => {
    if (!convert_checkerbg_active) {
        MOD_in_cell.style.background = "url('./imgs/Transparency500.png')";
        MOD_bgprev_button.classList.add('is-active');
        convert_checkerbg_active = true;
    } else {
        MOD_in_cell.style.background = ''
        MOD_bgprev_button.classList.remove('is-active');
        convert_checkerbg_active = false;
    }
});

let extension_filters = [
    { name: 'Images', extensions: ['png', 'gif'] },
];
let file_dialog_props = ['openfile'];
let dir_dialog_props = ['openDirectory', 'createDirectory'];

MOD_load_aimg_button.addEventListener("click", () => {
    var chosen_path = dialog.showOpenDialog({ filters: extension_filters, properties: file_dialog_props });
    console.log(`chosen path: ${chosen_path}`);
    if (chosen_path === undefined) {return}
    client.invoke("inspect_aimg", chosen_path[0], (error, res) => {
        if (error) {
            console.error(error);
            mboxError(split_msgbox, error);
        } else {
            conLoadAIMG(res);
            // if (SPL_is_reduced_color.checked) { SPL_color_space.value = 256; }
        }
    })
    console.log('registered!');
});

function conLoadAIMG(res) {
    console.log(res);
    conClearAIMG();
    MOD_in_name.innerHTML = escapeHtml(res.name);
    MOD_in_format.innerHTML = res.extension;
    MOD_in_dimensions.innerHTML = `${res.width} x ${res.height}`;
    MOD_in_duration.innerHTML = `${res.avg_duration} seconds`;
    MOD_in_fps.innerHTML = `${res.fps} fps`;
    MOD_in_stage.src = res.absolute_url;
    MOD_in_path.value = res.absolute_url;
}

MOD_clear_aimg_button.addEventListener('click', conClearAIMG);

function conClearAIMG() {
    MOD_in_name.innerHTML = '-';
    MOD_in_format.innerHTML = '-';
    MOD_in_dimensions.innerHTML = '-';
    MOD_in_duration.innerHTML = '-';
    MOD_in_fps.innerHTML = '-';
    MOD_in_stage.src = '';
    MOD_in_path.value = '';
    session.clearCache(() => {});
    session.clearStorageData(['appcache', 'cookies', 'filesystem', 'indexdb', 'localstorage', 'shadercache', 'websql', 'serviceworkers', 'cachestorage']);
    console.log('session cleared');
}