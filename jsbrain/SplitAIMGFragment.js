console.log('splitfragment.js loaded!');
const remote = require('electron').remote;
const dialog = remote.dialog;
const session = remote.getCurrentWebContents().session;
const { client } = require('./Client.js');
const { mboxClear, mboxError, mboxSuccess } = require('./MessageBox.js');
const { escapeHtml } = require('./Utils.js')
let split_msgbox = document.getElementById('split_msgbox');

let SPL_load_aimg_button = document.getElementById('SPL_load_aimg_button');
let SPL_clear_aimg_button = document.getElementById('SPL_clear_aimg_button');
let SPL_bgprev_button = document.getElementById('SPL_bgprev_button');
let choose_seq_outdir_button = document.getElementById('choose_seq_outdir_button');
let SPL_split_aimg_button = document.getElementById('SPL_split_aimg_button');

let split_aimg_cell = document.getElementById('split_aimg_cell');
let split_checkerbg_active = false;
let SPL_aimg_stage = document.getElementById('SPL_aimg_stage');
let SPL_aimg_path = document.getElementById('SPL_aimg_path');
let SPL_pad_count = document.getElementById('SPL_pad_count');
let SPL_is_reduced_color = document.getElementById('SPL_is_reduced_color');
let SPL_color_space = document.getElementById('SPL_color_space');
let is_duration_sensitive = document.getElementById('is_duration_sensitive');

let target_seq_path = document.getElementById('target_seq_path');

let info_header = document.querySelector('#info_header');
let aimg_name = document.querySelector('#aimg_name');
let aimg_dimens = document.querySelector('#aimg_dimens');
let aimg_file_size = document.querySelector('#aimg_file_size');
let aimg_frame_count = document.querySelector('#aimg_frame_count');
let aimg_frame_count_ds = document.querySelector('#aimg_frame_count_ds');
let aimg_fps = document.querySelector('#aimg_fps');
let aimg_frame_delay = document.querySelector('#aimg_frame_delay');
let aimg_duration = document.querySelector('#aimg_duration');

let extension_filters = [
    { name: 'Images', extensions: ['png', 'gif'] },
];

let file_dialog_props = ['openfile'];
let dir_dialog_props = ['openDirectory', 'createDirectory'];


// function registerListeners() {
//     SPL_load_aimg_button.addEventListener("click", openImage);
//     console.log("registerListener called");
// }

SPL_load_aimg_button.addEventListener("click", () => {
    var chosen_path = dialog.showOpenDialog({ filters: extension_filters, properties: file_dialog_props });
    console.log(`chosen path: ${chosen_path}`);
    if (chosen_path === undefined) {return}
    client.invoke("inspect_aimg", chosen_path[0], (error, res) => {
        if (error) {
            console.error(error);
            mboxError(split_msgbox, error);
        } else {
            loadAIMG(res);
            SPL_pad_count.value = 3;
            // if (SPL_is_reduced_color.checked) { SPL_color_space.value = 256; }
        }
    })
    console.log('registered!');
});

SPL_clear_aimg_button.addEventListener('click', clearAIMG);

function loadAIMG(res) {
    console.log(res);
    clearAIMG();
    aimg_name.innerHTML = escapeHtml(res.name);
    info_header.innerHTML = `${res.extension} Information`;
    aimg_file_size.innerHTML = `${res.fsize}`;
    aimg_frame_count.innerHTML = `${res.frame_count} frames`;
    aimg_frame_count_ds.innerHTML = `${res.frame_count_ds} frames`;
    aimg_fps.innerHTML = `${res.fps} fps`;
    aimg_dimens.innerHTML = `${res.width} x ${res.height}`;
    let delay_info = `${res.avg_duration} seconds`
    if (res.duration_is_uneven) {
        delay_info += ` (uneven)`
    }
    aimg_frame_delay.innerHTML = delay_info;
    aimg_duration.innerHTML = `${res.loop_duration} seconds`;
    SPL_aimg_stage.src = res.absolute_url;
    SPL_aimg_path.value = res.absolute_url;
    mboxClear(split_msgbox);
}

function clearAIMG() {
    aimg_name.innerHTML = '-';
    info_header.innerHTML = 'Information';
    aimg_file_size.innerHTML = '-';
    aimg_frame_count.innerHTML = '-';
    aimg_frame_count_ds.innerHTML = '-';
    aimg_fps.innerHTML = '-';
    aimg_dimens.innerHTML = '-';
    aimg_frame_delay.innerHTML = '-';
    aimg_duration.innerHTML = '-';
    SPL_aimg_stage.src = '';
    SPL_aimg_path.value = '';
    SPL_pad_count.value = '';
    SPL_color_space.value = '';
    mboxClear(split_msgbox);
    session.clearCache(() => {});
    session.clearStorageData(['appcache', 'cookies', 'filesystem', 'indexdb', 'localstorage', 'shadercache', 'websql', 'serviceworkers', 'cachestorage']);
    console.log('session cleared');
}

SPL_bgprev_button.addEventListener('click', () => {
    if (!split_checkerbg_active) {
        split_aimg_cell.style.background = "url('./imgs/Transparency500.png')";
        SPL_bgprev_button.classList.add('is-active');
        split_checkerbg_active = true;
    } else {
        split_aimg_cell.style.background = ''
        SPL_bgprev_button.classList.remove('is-active');
        split_checkerbg_active = false;
    }
});

choose_seq_outdir_button.addEventListener('click', () => {
    var choosen_dir = dialog.showOpenDialog({ properties: dir_dialog_props });
    console.log(`Chosen dir: ${choosen_dir}`);
    if (choosen_dir === undefined) {return}
    target_seq_path.value = choosen_dir;
    mboxClear(split_msgbox);
});

function unfreezeButtons () {
    SPL_load_aimg_button.classList.remove('is-static');
    SPL_clear_aimg_button.classList.remove('is-static');
    choose_seq_outdir_button.classList.remove('is-static');
    SPL_split_aimg_button.classList.remove('is-static');
}

function freezeButtons () {
    SPL_load_aimg_button.classList.add('is-static');
    SPL_clear_aimg_button.classList.add('is-static');
    choose_seq_outdir_button.classList.add('is-static');
    SPL_split_aimg_button.classList.add('is-static');
}


SPL_is_reduced_color.addEventListener("click", () => {
    if (SPL_is_reduced_color.checked) {
        SPL_color_space.disabled = false;
    }
    else {
        SPL_color_space.disabled = true;
    }
});

SPL_split_aimg_button.addEventListener('click', () => {
    mboxClear(split_msgbox);
    freezeButtons();
    SPL_split_aimg_button.classList.add("is-loading");
    // console.log(`in path: ${in_path} out path: ${out_path}`);
    var color_space = SPL_color_space.value;
    if (!SPL_is_reduced_color.checked || color_space === undefined) {
        color_space = 0;
    }
    client.invoke('split_image', SPL_aimg_path.value, target_seq_path.value, SPL_pad_count.value, color_space, is_duration_sensitive.checked, (error, res) => {
        if (error){
            console.log(error);
            mboxError(split_msgbox, error);
            unfreezeButtons();
            SPL_split_aimg_button.classList.remove("is-loading");
        } else {
            if (res){
                console.log('res', res);
                mboxSuccess(split_msgbox, res);
                if (res == "Finished!") {
                    SPL_split_aimg_button.classList.remove('is-loading');
                    unfreezeButtons();
                }
            }
        }
    })
});
