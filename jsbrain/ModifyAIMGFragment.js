console.log('ConvertFragment.js loaded!');
const remote = require('electron').remote;
const dialog = remote.dialog;
const session = remote.getCurrentWebContents().session;
const { client } = require('./Client.js');
const { mboxClear, mboxError, mboxSuccess } = require('./MessageBox.js');
const { escapeHtml } = require('./Utils.js')

let MOD_load_aimg_button = document.getElementById('MOD_load_aimg_button');
let MOD_clear_aimg_button = document.getElementById('MOD_clear_aimg_button');
let MOD_orig_bgprev_button = document.getElementById('MOD_orig_bgprev_button');
let MOD_orig_cell = document.getElementById('MOD_orig_cell');
let MOD_orig_stage = document.getElementById('MOD_orig_stage');
let MOD_orig_path = document.getElementById('MOD_orig_path');

// let MOD_in_name = document.getElementById('MOD_in_name');
// let MOD_in_format = document.getElementById('MOD_in_format');
// let MOD_in_dimensions = document.getElementById('MOD_in_dimensions');
// let MOD_in_duration = document.getElementById('MOD_in_duration');
// let MOD_in_fps = document.getElementById('MOD_in_fps');
let MOD_orig_name = document.getElementById('MOD_orig_name');
let MOD_orig_dimensions = document.getElementById('MOD_orig_dimensions');
let MOD_orig_framecount = document.getElementById('MOD_orig_framecount');
let MOD_orig_fps = document.getElementById('MOD_orig_fps');
let MOD_orig_delay = document.getElementById('MOD_orig_delay');
let MOD_orig_loopduration = document.getElementById('MOD_orig_loopduration');
let MOD_orig_format = document.getElementById('MOD_orig_format');

let MOD_new_name = document.getElementById('MOD_new_name');
let MOD_new_width = document.getElementById('MOD_new_width');
let MOD_new_fps = document.getElementById('MOD_new_fps');
let MOD_new_height = document.getElementById('MOD_new_height');
let MOD_new_delay = document.getElementById('MOD_new_delay');
let MOD_new_format = document.getElementById('MOD_new_format');


let mod_orig_checkerbg_active = false;

MOD_orig_bgprev_button.addEventListener('click', () => {
    if (!mod_orig_checkerbg_active) {
        MOD_orig_cell.style.background = "url('./imgs/Transparency500.png')";
        MOD_orig_bgprev_button.classList.add('is-active');
        mod_orig_checkerbg_active = true;
    } else {
        MOD_orig_cell.style.background = ''
        MOD_orig_bgprev_button.classList.remove('is-active');
        mod_orig_checkerbg_active = false;
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
            clearOrigFields();
            clearNewFields();
            fillOrigData(res);
            fillNewData(res);
            // if (SPL_is_reduced_color.checked) { SPL_color_space.value = 256; }
        }
    })
    console.log('registered!');
});

function fillOrigData(res) {
    MOD_orig_name.innerHTML = escapeHtml(res.name);
    MOD_orig_dimensions.innerHTML = `${res.width} x ${res.height}`;
    MOD_orig_framecount.innerHTML = `${res.frame_count} (${res.frame_count_ds})`;
    MOD_orig_format.innerHTML = res.extension;
    let delay_info = `${res.avg_duration} seconds`
    if (res.duration_is_uneven) {
        delay_info += ` (uneven)`
    }
    MOD_orig_delay.innerHTML = res.delay_info
    MOD_orig_loopduration.innerHTML = `${res.loop_duration} seconds`;
    MOD_orig_stage.src = res.absolute_url;
    MOD_orig_path.value = res.absolute_url;
}

function fillNewData(res) {
    MOD_new_name.value = res.name;
    MOD_new_format.value = res.extension;
    MOD_new_width.value = res.width;
    MOD_new_height.value = res.height;
    MOD_new_delay.value = res.height;
    MOD_new_fps.value = res.fps;
}

MOD_clear_aimg_button.addEventListener('click', modClearAIMG);

function modClearAIMG() {
    clearOrigFields();
    clearNewFields();
    session.clearCache(() => {});
    session.clearStorageData(['appcache', 'cookies', 'filesystem', 'indexdb', 'localstorage', 'shadercache', 'websql', 'serviceworkers', 'cachestorage']);
    console.log('session cleared');
}

// function clearInFields() {
//     MOD_orig_name
// }

function clearOrigFields() {
    MOD_orig_name.innerHTML = '-';
    MOD_orig_dimensions.innerHTML = '-';
    MOD_orig_framecount.innerHTML = '-';
    MOD_orig_fps.innerHTML = '-';
    MOD_orig_delay.innerHTML = '-';
    MOD_orig_loopduration.innerHTML = '-';
    MOD_orig_format.innerHTML = '-';
}

function clearNewFields() {
    MOD_new_name.value = '';
    MOD_new_format.value = '';
    MOD_new_width.value = '';
    MOD_new_height.value = '';
    MOD_new_delay.value = '';
    MOD_new_fps.value = '';
    MOD_new_stage.src = '';
    MOD_new_path.value = '';
}