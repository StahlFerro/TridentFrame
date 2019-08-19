console.log('ConvertFragment.js loaded!');
const remote = require('electron').remote;
const dialog = remote.dialog;
const session = remote.getCurrentWebContents().session;
const { client } = require('./Client.js');
const { mboxClear, mboxError, mboxSuccess } = require('./MessageBox.js');
const { escapeHtml } = require('./Utils.js')

let CON_load_aimg_button = document.getElementById('CON_load_aimg_button');
let CON_clear_aimg_button = document.getElementById('CON_clear_aimg_button');
let CON_bgprev_button = document.getElementById('CON_bgprev_button');
let CON_in_cell = document.getElementById('CON_in_cell');

let CON_in_name = document.getElementById('CON_in_name');
let CON_in_format = document.getElementById('CON_in_format');
let CON_in_dimensions = document.getElementById('CON_in_dimensions');
let CON_in_stage = document.getElementById('CON_in_stage');
let CON_in_path = document.getElementById('CON_in_path');

let convert_checkerbg_active = false;

CON_bgprev_button.addEventListener('click', () => {
    if (!convert_checkerbg_active) {
        CON_in_cell.style.background = "url('./imgs/Transparency500.png')";
        CON_bgprev_button.classList.add('is-active');
        convert_checkerbg_active = true;
    } else {
        CON_in_cell.style.background = ''
        CON_bgprev_button.classList.remove('is-active');
        convert_checkerbg_active = false;
    }
});

let extension_filters = [
    { name: 'Images', extensions: ['png', 'gif'] },
];
let file_dialog_props = ['openfile'];
let dir_dialog_props = ['openDirectory', 'createDirectory'];

CON_load_aimg_button.addEventListener("click", () => {
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
    CON_in_name.innerHTML = escapeHtml(res.name);
    CON_in_format.innerHTML = res.extension;
    CON_in_dimensions.innerHTML = `${res.width} x ${res.height}`;
    CON_in_stage.src = res.absolute_url;
    CON_in_path.value = res.absolute_url;
}

CON_clear_aimg_button.addEventListener('click', conClearAIMG);

function conClearAIMG() {
    CON_in_name.innerHTML = '-';
    CON_in_format.innerHTML = '-';
    CON_in_dimensions.innerHTML = '-';
    CON_in_stage.src = '';
    CON_in_path.value = '';
    session.clearCache(() => {});
    session.clearStorageData(['appcache', 'cookies', 'filesystem', 'indexdb', 'localstorage', 'shadercache', 'websql', 'serviceworkers', 'cachestorage']);
    console.log('session cleared');
}