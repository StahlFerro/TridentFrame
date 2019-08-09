console.log("splitfragment.js loaded!");
const remote = require('electron').remote;
const dialog = remote.dialog;
const session = remote.getCurrentWebContents().session;
const { client, ImageViewer } = require('./Client.js');
const { quintcell_generator, escapeHtml } = require('./Utils.js');
const { mboxClear, mboxError, mboxSuccess } = require('./MessageBox.js');
let spr_msgbox = document.getElementById('spr_msgbox');

let SPR_sequence_paths = null;
let SPR_sequence_body = document.getElementById('SPR_sequence_body');
let SPR_sequence_counter = document.getElementById('SPR_sequence_counter');
let SPR_input_button = document.getElementById('SPR_input_button');
let SPR_input_button_text = document.getElementById('SPR_input_button_text');
let SPR_clear_imgs_button = document.getElementById('SPR_clear_imgs_button'); 
let SPR_outdir_button = document.getElementById('SPR_outdir_button');
let SPR_outdir_path = document.getElementById('SPR_outdir_path');
let SPR_create_button = document.getElementById('SPR_create_button');
let SPR_in_format = document.getElementById('SPR_in_format');
let prev_spritesheet_stage = document.getElementById('prev_spritesheet_stage');
let prev_spritesheet_path = document.getElementById('prev_spritesheet_path');

let spr_create_name = document.getElementById('spr_create_name');
let spr_tile_width = document.getElementById("spr_tile_width");
let spr_tile_height = document.getElementById("spr_tile_height");
let spr_tile_row = document.getElementById("spr_tile_row");

let SPR_final_dimens = document.getElementById('SPR_final_dimens');

let spr_from_sequence_stage = document.getElementById('spr_from_sequence_stage');
let spr_from_aimg_stage = document.getElementById('spr_from_aimg_stage');

let autobuild_active = false;


let extension_filters = [
    { name: 'Images', extensions: ['png', 'gif'] },
];
let imgs_dialog_props = ['openfile', 'multiSelections', 'createDirectory'];
let dir_dialog_props = ['openDirectory', 'createDirectory'];

function activateButtons () {
    SPR_input_button.classList.remove('is-static');
    SPR_clear_imgs_button.classList.remove('is-static');
}
function deactivateButtons () {
    SPR_input_button.classList.add('is-static');
    SPR_clear_imgs_button.classList.add('is-static');
}

spr_tile_width.addEventListener("change", () => display_final_sheet_dimensions(SPR_sequence_counter.value));
spr_tile_height.addEventListener("change", () => display_final_sheet_dimensions(SPR_sequence_counter.value));
spr_tile_row.addEventListener("change", () => display_final_sheet_dimensions(SPR_sequence_counter.value));
SPR_in_format.addEventListener("change", () => change_spritesheet_input(SPR_in_format.value));

function change_spritesheet_input(format){
    if (format == 'sequence') {
        showSequenceStage();
    }
    else if (format == 'aimg') {
        showAIMGStage();
    }
}

function hideAll() {
    spr_from_sequence_stage.style.display = 'none';
    spr_from_aimg_stage.style.display = 'none';
}

function showSequenceStage() {
    hideAll();
    spr_from_sequence_stage.style.display = 'block';
}

function showAIMGStage() {
    hideAll();
    spr_from_aimg_stage.style.display = 'block';
}


function reloadTempSpritesheet() {
    console.log("reloadTempSpritesheet called!")
    if (autobuild_active) {
        deleteTempSpritesheet();
        createTempSpritesheet();
    }
    if (SPR_sequence_counter.innerHTML) {
        display_final_sheet_dimensions(SPR_sequence_counter.value);
    }
}

SPR_outdir_button.addEventListener('click', () => {
    var choosen_dir = dialog.showOpenDialog({ properties: dir_dialog_props });
    console.log(`Chosen dir: ${choosen_dir}`);
    if (choosen_dir === undefined) {return}
    SPR_outdir_path.value = choosen_dir;
    mboxClear(spr_msgbox);
});

function createTempSpritesheet() {
    if (SPR_sequence_paths == null){ console.log('no sequences, exiting...'); return; }
    deactivateButtons();
    client.invoke('build_spritesheet', SPR_sequence_paths, 'temp/', Date.now().toString(), (error, res) => {
        console.log('createfragment fps', create_fps.value);
        if (error) {
            console.error(error);
        } else {
            prev_spritesheet_stage.src = res;
            prev_spritesheet_path.value = res;
        }
        activateButtons();
    });
}

SPR_input_button.addEventListener("click", () => {
    var img_paths = dialog.showOpenDialog({ filters: extension_filters, properties: imgs_dialog_props })
    console.log(`chosen path: ${img_paths}`);
    if (img_paths === undefined) { return }
    console.log(img_paths);
    deactivateButtons();
    SPR_input_button.classList.add("is-loading");
    console.log('invoking...');
    if (SPR_in_format.value == 'sequence') {
        client.invoke("inspect_sequence", img_paths, (error, res) => {
            if (error) {
                console.error(error);
                mboxError(spr_msgbox, error);
            } else {
                SPR_sequence_paths = res.sequence;
                console.log("obtained sequences", SPR_sequence_paths);
                quintcell_generator(SPR_sequence_paths, SPR_sequence_body);
                console.log(res);
                mboxClear(spr_msgbox);
                reloadTempSpritesheet();
                spr_create_name.value = escapeHtml(res.name);
                spr_tile_width.value = res.width;
                spr_tile_height.value = res.height;
                spr_tile_row.value = 5;
                SPR_sequence_counter.innerHTML = `${res.total} images`;
            }
            display_final_sheet_dimensions(res.total);
            SPR_input_button.classList.remove('is-loading');
            activateButtons();
        });
    }
    else if (SPR_in_format.value == 'aimg') {
        client.invoke("inspect_aimg", img_paths, (error, res) => {
            
        });
    }
});

SPR_clear_imgs_button.addEventListener('click', () => {
    // sequence_body.innerHTML = '';
    while (SPR_sequence_body.hasChildNodes()){
        SPR_sequence_body.removeChild(SPR_sequence_body.firstChild);
    }
    SPR_sequence_paths = null;
    spr_create_name.value = '';
    spr_tile_width.value = '';
    spr_tile_height.value = '';
    spr_tile_row.value = '';
    SPR_sequence_counter.innerHTML = '';
    SPR_final_dimens.innerHTML = '';
    mboxClear(spr_msgbox);
    deleteTempSpritesheet();
    session.clearCache(testcallback);
});


function testcallback(){
    console.log("cache cleared!!1");
}

SPR_create_button.addEventListener('click', () => {
    mboxClear(spr_msgbox);
    SPR_create_button.classList.add('is-loading');
    // build_aimg(sequence_paths, create_outdir.value, create_name.value, parseInt(create_fps.value), CRT_out_format.value, false, is_disposed.checked);
    client.invoke("build_spritesheet", SPR_sequence_paths, SPR_outdir_path.value, spr_create_name.value, 
    spr_tile_width.value, spr_tile_height.value, spr_tile_row.value, 0, 0, 0, 0, true, (error, res) => {
        if (error) {
            console.error(error);
            mboxError(spr_msgbox, error);
        } else {
            console.log("SUCCESS!");
            mboxSuccess(spr_msgbox, 'Spritesheet successfully built!!1, check out the output directory');
        }
        SPR_create_button.classList.remove('is-loading');
    });
});


function display_final_sheet_dimensions(image_count) {
    var x_count = Math.min(image_count, spr_tile_row.value);
    var y_count = Math.ceil(image_count / spr_tile_row.value);
    console.log('xcount', x_count);
    console.log('ycount', y_count);
    var sheet_width = spr_tile_width.value * x_count;
    var sheet_height = spr_tile_height.value * y_count;
    SPR_final_dimens.innerHTML = `Sheet dimensions: ${sheet_width}x${sheet_height}`;
    // var dimensions = {"width": }
}

function deleteTempSpritesheet() {
    prev_spritesheet_stage.src = '';
    abstempath = '';
    client.invoke('delete_temp_images', (error, res) => {
        if (error) {
            console.error(error);
        } else {
            console.log(res);
        }
    });
}

// autobuild_toggle_button.addEventListener('click', () => {
//     if (!autobuild_active) {
//         autoprev_icon.classList.remove('fa-eye-slash');
//         autoprev_icon.classList.add('fa-eye');
//         autobuild_active = true;
//         reloadTempAIMG();
//     } else {
//         autoprev_icon.classList.remove('fa-eye');
//         autoprev_icon.classList.add('fa-eye-slash');
//         autobuild_active = false;
//         deleteTempAIMG();
//     }
// });
