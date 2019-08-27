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

let MOD_orig_name = document.getElementById('MOD_orig_name');
let MOD_orig_dimensions = document.getElementById('MOD_orig_dimensions');
let MOD_orig_framecount = document.getElementById('MOD_orig_framecount');
let MOD_orig_fps = document.getElementById('MOD_orig_fps');
let MOD_orig_delay = document.getElementById('MOD_orig_delay');
let MOD_orig_loopduration = document.getElementById('MOD_orig_loopduration');
let MOD_orig_format = document.getElementById('MOD_orig_format');

let MOD_new_bgprev_button = document.getElementById('MOD_new_bgprev_button');
let MOD_new_cell = document.getElementById('MOD_new_cell');
let MOD_new_name = document.getElementById('MOD_new_name');
let MOD_new_width = document.getElementById('MOD_new_width');
let MOD_new_fps = document.getElementById('MOD_new_fps');
let MOD_new_height = document.getElementById('MOD_new_height');
let MOD_new_delay = document.getElementById('MOD_new_delay');
let MOD_new_format = document.getElementById('MOD_new_format');
let MOD_new_reversed = document.getElementById('MOD_new_reversed');
let MOD_new_preserve_alpha = document.getElementById('MOD_new_preserve_alpha');
let MOD_new_is_optimized = document.getElementById('MOD_new_is_optimized');
let MOD_new_optimization_level = document.getElementById('MOD_new_optimization_level');
let MOD_new_is_lossy = document.getElementById('MOD_new_is_lossy');
let MOD_new_lossy_value = document.getElementById('MOD_new_lossy_value');
let MOD_new_reduced_color = document.getElementById('MOD_new_reduced_color');
let MOD_color_space = document.getElementById('MOD_color_space');

let MOD_general_control_panel = document.getElementById('MOD_general_control_panel');
let MOD_gif_control_panel = document.getElementById('MOD_gif_control_panel');
let MOD_menu_general = document.getElementById('MOD_menu_general');
let MOD_box_general = document.getElementById('MOD_box_general');
let MOD_menu_gif = document.getElementById('MOD_menu_gif');
let MOD_box_gif = document.getElementById('MOD_box_gif');

function hideMODPanels() {
    MOD_general_control_panel.style.display = 'none';
    MOD_gif_control_panel.style.display = 'none';
}

function deselectMODMenus() {
    MOD_box_general.classList.remove('is-selected');
    MOD_box_gif.classList.remove('is-selected');
}

function showMODGeneralPanel() {
    hideMODPanels();
    deselectMODMenus();
    MOD_box_general.classList.add('is-selected');
    MOD_general_control_panel.style.display = 'block';
}
function showMODGIFPanel() {
    hideMODPanels();
    deselectMODMenus();
    MOD_box_gif.classList.add('is-selected');
    MOD_gif_control_panel.style.display = 'block';
}

MOD_menu_general.addEventListener('click', showMODGeneralPanel);
MOD_menu_gif.addEventListener('click', showMODGIFPanel);


let MOD_modify_aimg_button = document.getElementById('MOD_modify_aimg_button');

let modify_msgbox = document.getElementById("modify_msgbox");


let mod_orig_checkerbg_active = false;
let mod_new_checkerbg_active = false;

MOD_orig_bgprev_button.addEventListener("click", () => {
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

MOD_new_bgprev_button.addEventListener("click", () => {
    if (!mod_new_checkerbg_active) {
        MOD_new_cell.style.background = "url('./imgs/Transparency500.png')";
        MOD_new_bgprev_button.classList.add('is-active');
        mod_new_checkerbg_active = true;
    } else {
        MOD_new_cell.style.background = ''
        MOD_new_bgprev_button.classList.remove('is-active');
        mod_new_checkerbg_active = false;
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
            mboxError(modify_msgbox, error);
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
    MOD_orig_delay.innerHTML = delay_info
    MOD_orig_loopduration.innerHTML = `${res.loop_duration} seconds`;
    MOD_orig_stage.src = res.absolute_url;
    MOD_orig_path.value = res.absolute_url;
}

function fillNewData(res) {
    MOD_new_name.value = escapeHtml(res.base_fname);
    console.log(res.extension);
    if (res.extension == "GIF") { MOD_new_format.selectedIndex = "0"; }
    else if (res.extension == "APNG") { MOD_new_format.selectedIndex = "1"; }
    MOD_new_width.value = res.width;
    MOD_new_height.value = res.height;
    MOD_new_delay.value = res.height;
    MOD_new_fps.value = res.fps;
}


MOD_clear_aimg_button.addEventListener('click', modClearAIMG);

function modClearAIMG() {
    mboxClear(modify_msgbox);
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
    MOD_orig_stage.src = '';
    MOD_orig_path.value = '';
}

function clearNewFields() {
    MOD_new_name.value = '';
    MOD_new_width.value = '';
    MOD_new_height.value = '';
    MOD_new_delay.value = '';
    MOD_new_fps.value = '';
    MOD_new_stage.src = '';
    MOD_new_path.value = '';
    MOD_new_reversed.checked = false;
    MOD_new_preserve_alpha.checked = false;
    MOD_new_reduced_color.checked = false;
}

MOD_new_reduced_color.addEventListener("click", () => {
    if (MOD_new_reduced_color.checked) {
        MOD_color_space.disabled = false;
    }
    else {
        MOD_color_space.disabled = true;
    }
});

MOD_new_is_lossy.addEventListener("click", () => {
    if (MOD_new_is_lossy.checked) {
        MOD_new_lossy_value.disabled = false;
    }
    else {
        MOD_new_lossy_value.disabled = true;
    }
})


MOD_new_is_optimized.addEventListener("click", () => {
    if (MOD_new_is_optimized.checked) {
        MOD_new_optimization_level.disabled = false;
    }
    else {
        MOD_new_optimization_level.disabled = true;
    }
})



MOD_modify_aimg_button.addEventListener("click", () => {
    client.invoke("", "", (error, res) => {
        
    });

})
