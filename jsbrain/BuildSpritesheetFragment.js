console.log("splitfragment.js loaded!");
const remote = require('electron').remote;
const dialog = remote.dialog;
const session = remote.getCurrentWebContents().session;
const { client, ImageViewer } = require('./Client.js');
const { quintcell_generator, escapeHtml } = require('./Utils.js');
const { mboxClear, mboxError, mboxSuccess } = require('./MessageBox.js');
let bspr_msgbox = document.getElementById('bspr_msgbox');

let bspr_sequence_list = null;
let bspr_aimg_path_list = null;
let BSPR_sequence_body = document.getElementById('BSPR_sequence_body');
let BSPR_sequence_counter = document.getElementById('BSPR_sequence_counter');
let BSPR_sequence_counter_label = document.getElementById('BSPR_sequence_counter_label')
let BSPR_input_button = document.getElementById('BSPR_input_button');
let BSPR_clear_imgs_button = document.getElementById('BSPR_clear_imgs_button'); 
let BSPR_outdir_button = document.getElementById('BSPR_outdir_button');
let BSPR_outdir_path = document.getElementById('BSPR_outdir_path');
let BSPR_create_button = document.getElementById('BSPR_create_button');
let BSPR_prev_spritesheet_stage = document.getElementById('BSPR_prev_spritesheet_stage');
let BSPR_prev_spritesheet_path = document.getElementById('BSPR_prev_spritesheet_path');

let BSPR_create_name = document.getElementById('BSPR_create_name');
let BSPR_tile_width = document.getElementById("BSPR_tile_width");
let BSPR_tile_height = document.getElementById("BSPR_tile_height");
let BSPR_tile_row = document.getElementById("BSPR_tile_row");

let BSPR_final_dimens = document.getElementById('BSPR_final_dimens');

let BSPR_in_format = document.getElementById('BSPR_in_format');
let BSPR_from_sequence_subpanel = document.getElementById('BSPR_from_sequence_subpanel');
let BSPR_from_aimg_subpanel = document.getElementById('BSPR_from_aimg_subpanel');
let BSPR_aimg_stage = document.getElementById('BSPR_aimg_stage');
let BSPR_aimg_path = document.getElementById('BSPR_aimg_path');

let autobuild_active = false;


let extension_filters = [
    { name: 'Images', extensions: ['png', 'gif'] },
];
let aimg_dialog_props = ['openfile'];
let sequence_dialog_props = ['openfile', 'multiSelections', 'createDirectory'];
let dir_dialog_props = ['openDirectory', 'createDirectory'];

function activateButtons () {
    BSPR_input_button.classList.remove('is-static');
    BSPR_clear_imgs_button.classList.remove('is-static');
}
function deactivateButtons () {
    BSPR_input_button.classList.add('is-static');
    BSPR_clear_imgs_button.classList.add('is-static');
}

BSPR_tile_width.addEventListener("change", displayFinalSheetDimensions);
BSPR_tile_height.addEventListener("change", displayFinalSheetDimensions);
BSPR_tile_row.addEventListener("change", displayFinalSheetDimensions);
BSPR_in_format.addEventListener("change", change_spritesheet_input);

function update_BSPR_create_count(count) {
    console.log("fucking called");
    BSPR_sequence_counter.value = count;
    BSPR_sequence_counter_label.innerHTML = `${count} images`;
}



function change_spritesheet_input(){
    console.log('in format changed');
    var format = BSPR_in_format.value;
    if (format == 'sequence') {
        hideAll();
        BSPR_from_sequence_subpanel.style.display = 'block';
    }
    else if (format == 'aimg') {
        hideAll();
        BSPR_from_aimg_subpanel.style.display = 'block';
    }
    smartLoadInput();
}

function hideAll() {
    BSPR_from_sequence_subpanel.style.display = 'none';
    BSPR_from_aimg_subpanel.style.display = 'none';
}


function reloadTempSpritesheet() {
    console.log("reloadTempSpritesheet called!")
    if (autobuild_active) {
        deleteTempSpritesheet();
        createTempSpritesheet();
    }
    if (BSPR_sequence_counter.value) {
        displayFinalSheetDimensions();
    }
}

BSPR_outdir_button.addEventListener('click', () => {
    var choosen_dir = dialog.showOpenDialog({ properties: dir_dialog_props });
    console.log(`Chosen dir: ${choosen_dir}`);
    if (choosen_dir === undefined) {return}
    BSPR_outdir_path.value = choosen_dir;
    mboxClear(bspr_msgbox);
});

function createTempSpritesheet() {
    if (bspr_sequence_list == null){ console.log('no sequences, exiting...'); return; }
    deactivateButtons();
    client.invoke('build_spritesheet', bspr_sequence_list, 'temp/', Date.now().toString(), (error, res) => {
        console.log('createfragment fps', create_fps.value);
        if (error) {
            console.error(error);
        } else {
            BSPR_prev_spritesheet_stage.src = res;
            BSPR_prev_spritesheet_path.value = res;
        }
        activateButtons();
    });
}

BSPR_input_button.addEventListener("click", () => {
    if (BSPR_in_format.value == 'sequence') {
        var img_paths = dialog.showOpenDialog({ filters: extension_filters, properties: sequence_dialog_props }); 
        if (img_paths === undefined) { return; }
        bspr_sequence_list = img_paths;
    }
    else if (BSPR_in_format.value == 'aimg') {
        var img_paths = dialog.showOpenDialog({ filters: extension_filters, properties: aimg_dialog_props }); 
        if (img_paths === undefined) { return; }
        bspr_aimg_path_list = img_paths;
    }
    smartLoadInput();
});

function smartLoadInput()  {
    console.log('invoking...');
    if (BSPR_in_format.value == 'sequence') {
        if (bspr_sequence_list == null) { return; }
        deactivateButtons();
        BSPR_input_button.classList.add("is-loading");
        client.invoke("inspect_sequence", bspr_sequence_list, (error, res) => {
            console.log("spritesheet load sequence");
            if (error) {
                bspr_sequence_list = null;
                console.error(error);
                mboxError(bspr_msgbox, error);
            } else {
                bspr_sequence_list = res.sequence; // Write to bspr_sequence_list again just in case if any of the images in the sequences are not static
                console.log("obtained sequences", bspr_sequence_list);
                quintcell_generator(bspr_sequence_list, BSPR_sequence_body);
                console.log(res);
                mboxClear(bspr_msgbox);
                reloadTempSpritesheet();
                BSPR_create_name.value = escapeHtml(res.name);
                BSPR_tile_width.value = res.width;
                BSPR_tile_height.value = res.height;
                BSPR_tile_row.value = 5;
                update_BSPR_create_count(res.total);
                displayFinalSheetDimensions();
            }
            BSPR_input_button.classList.remove('is-loading');
            activateButtons();
        });
    }
    else if (BSPR_in_format.value == 'aimg') {
        if (bspr_aimg_path_list == null) { return; }
        deactivateButtons();
        BSPR_input_button.classList.add("is-loading");
        client.invoke("inspect_aimg", bspr_aimg_path_list[0], (error, res) => {
            console.log("spritesheet load aimg");
            if (error) {
                bspr_aimg_path_list = null;
                console.log(error);
                mboxError(bspr_msgbox, error);
            } else {
                BSPR_create_name.value = escapeHtml(res.name);
                BSPR_tile_width.value = res.width;
                BSPR_tile_height.value = res.height;
                BSPR_tile_row.value = 5;
                BSPR_aimg_stage.src = res.absolute_url;
                BSPR_aimg_path.value = res.absolute_url;
                update_BSPR_create_count(res.frame_count);
                displayFinalSheetDimensions();
            }
            BSPR_input_button.classList.remove('is-loading');
            activateButtons();
        });
    }
    mboxClear(bspr_msgbox);
}

BSPR_clear_imgs_button.addEventListener('click', () => {
    // sequence_body.innerHTML = '';
    if (BSPR_in_format.value == 'sequence') {
        bspr_sequence_list = null;
        while (BSPR_sequence_body.hasChildNodes()){
            BSPR_sequence_body.removeChild(BSPR_sequence_body.firstChild);
        }
    }
    else if (BSPR_in_format.value == 'aimg') {
        bspr_aimg_path_list = null;
        BSPR_aimg_stage.src = '';
        BSPR_aimg_path.value = '';
    }
    BSPR_create_name.value = '';
    BSPR_tile_width.value = '';
    BSPR_tile_height.value = '';
    BSPR_tile_row.value = '';
    BSPR_sequence_counter.value = 0;
    BSPR_sequence_counter_label.innerHTML = '';
    BSPR_final_dimens.innerHTML = '';
    mboxClear(bspr_msgbox);
    deleteTempSpritesheet();
    session.clearCache(testcallback);
});


function testcallback(){
    console.log("cache cleared!!1");
}

BSPR_create_button.addEventListener('click', () => {
    mboxClear(bspr_msgbox);
    BSPR_create_button.classList.add('is-loading');
    // build_aimg(sequence_paths, create_outdir.value, create_name.value, parseInt(create_fps.value), CRT_out_format.value, false, is_disposed.checked);
    var paths = null;
    if (BSPR_in_format.value == 'sequence') { paths = bspr_sequence_list; }
    else if (BSPR_in_format.value == 'aimg') { paths = bspr_aimg_path_list; }
    client.invoke("build_spritesheet", paths, BSPR_in_format.value, BSPR_outdir_path.value, BSPR_create_name.value, 
    BSPR_tile_width.value, BSPR_tile_height.value, BSPR_tile_row.value, 0, 0, 0, 0, true, (error, res) => {
        if (error) {
            console.error(error);
            mboxError(bspr_msgbox, error);
        } else {
            if (res) {
                console.log(res);
                mboxSuccess(bspr_msgbox, res);
            }
            // console.log('res', res);
            // console.log("SUCCESS!");
            // mboxSuccess(bspr_msgbox, 'Spritesheet successfully built!!1, check out the output directory');
        }
        BSPR_create_button.classList.remove('is-loading');
    });
});


function displayFinalSheetDimensions() {
    console.log('displayFinalSheetDimensions called!')
    var image_count = BSPR_sequence_counter.value;
    var x_count = Math.min(image_count, BSPR_tile_row.value);
    var y_count = Math.ceil(image_count / BSPR_tile_row.value);
    console.log('xcount', x_count);
    console.log('ycount', y_count);
    var sheet_width = BSPR_tile_width.value * x_count;
    var sheet_height = BSPR_tile_height.value * y_count;
    BSPR_final_dimens.innerHTML = `Sheet dimensions: ${sheet_width}x${sheet_height}`;
    // var dimensions = {"width": }
}

function deleteTempSpritesheet() {
    BSPR_prev_spritesheet_stage.src = '';
    abstempath = '';
    // client.invoke('delete_temp_images', (error, res) => {
    //     if (error) {
    //         console.error(error);
    //     } else {
    //         console.log(res);
    //     }
    // });
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
