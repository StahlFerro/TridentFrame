console.log("splitfragment.js loaded!");
const remote = require('electron').remote;
const dialog = remote.dialog;
const session = remote.getCurrentWebContents().session;
const { client } = require('./Client.js');
const { quintcell_generator, escapeHtml } = require('./Utils.js');
const { mboxClear, mboxError, mboxSuccess } = require('./MessageBox.js');


console.log(`session ${session}`);
console.log(`session ${session.defaultSession}`);
setInterval(() => {
    session.getCacheSize((num) => {
        console.log(`session size: ${num}`);
    });
}, 3000);


let create_msgbox = document.getElementById('create_msgbox');
// let sequence_carousel = document.getElementById('sequence_carousel')
let CRT_load_imgs_button = document.getElementById('CRT_load_imgs_button');
let CRT_clear_imgs_button = document.getElementById('CRT_clear_imgs_button');
let choose_aimg_outdir_button = document.getElementById('choose_aimg_outdir_button');
let CRT_bgprev_button = document.getElementById('CRT_bgprev_button');
let CRT_autoprev_button = document.getElementById('CRT_autoprev_button');
let autoprev_icon = document.getElementById('autoprev_icon')
let create_aimg_cell = document.getElementById('create_aimg_cell');
let create_aimg_button = document.getElementById('create_aimg_button');
let create_checkerbg_active = false;
let autoprev_active = false;

var CRT_sequence_body = document.getElementById('CRT_sequence_body');
let sequence_paths = null;
let CRT_sequence_counter = document.getElementById('CRT_sequence_counter');
let create_name = document.getElementById('create_name');
let create_fps = document.getElementById('create_fps');
let create_width = document.getElementById('create_width');
let create_height = document.getElementById('create_height');
let create_duration = document.getElementById('create_duration');
let is_disposed = document.getElementById('is_disposed');
let is_reversed = document.getElementById('is_reversed');
let flip_horizontal = document.getElementById('flip_horizontal');
let flip_vertical = document.getElementById('flip_vertical');
let CRT_out_format = document.getElementById('CRT_out_format');
let create_outdir = document.getElementById('create_outdir');
let CRT_aimg_stage = document.getElementById('CRT_aimg_stage');
let CRT_aimg_path = document.getElementById('CRT_aimg_path');


let extension_filters = [
    { name: 'Images', extensions: ['png', 'gif'] },
];
let imgs_dialog_props = ['openfile', 'multiSelections', 'createDirectory'];
let dir_dialog_props = ['openDirectory', 'createDirectory'];

CRT_load_imgs_button.addEventListener("click", () => {
    var img_paths = dialog.showOpenDialog({ filters: extension_filters, properties: imgs_dialog_props })
    console.log(`chosen path: ${img_paths}`);
    if (img_paths === undefined) { return }
    console.log(img_paths);
    freezeButtons();
    CRT_load_imgs_button.classList.add("is-loading");
    client.invoke("inspect_sequence", img_paths, (error, res) => {
        if (error) {
            console.error(error);
            mboxError(create_msgbox, error);
        } else {
            sequence_paths = res.sequence;
            console.log("obtained sequences", sequence_paths);
            quintcell_generator(sequence_paths, CRT_sequence_body);
            create_name.value = escapeHtml(res.name);
            if (create_fps.value === undefined || create_fps.value == null || create_fps.value == "") {
                create_fps.value = 50;
                create_duration = 0.02;
            }
            CRT_sequence_counter.innerHTML = `${res.total} image${res.total > 1? "s": ""} (${res.size} total)`;
            create_width.value = res.width;
            create_height.value = res.height;
            console.log(res);
            mboxClear(create_msgbox);
            reloadTempAIMG();
        }
        CRT_load_imgs_button.classList.remove('is-loading');
        unfreezeButtons();
    });
});


CRT_clear_imgs_button.addEventListener('click', () => {
    // sequence_body.innerHTML = '';
    while (CRT_sequence_body.hasChildNodes()){
        CRT_sequence_body.removeChild(CRT_sequence_body.firstChild);
    }
    sequence_paths = null;
    create_name.value = '';
    create_fps.value = '';
    create_width.value = '';
    create_height.value = '';
    CRT_sequence_counter.innerHTML = '';
    mboxClear(create_msgbox);
    deleteTempAIMG();
    session.clearCache(testcallback);
});

create_fps.addEventListener('input', reloadTempAIMG);
is_disposed.addEventListener('click', reloadTempAIMG);
is_reversed.addEventListener('click', reloadTempAIMG);
CRT_out_format.addEventListener('change', reloadTempAIMG);
create_width.addEventListener('change', reloadTempAIMG);
create_height.addEventListener('change', reloadTempAIMG);
flip_horizontal.addEventListener('click', reloadTempAIMG);
flip_vertical.addEventListener('click', reloadTempAIMG);

function reloadTempAIMG() {
    console.log("reloadTempAIMG called!")
    if (autoprev_active) {
        deleteTempAIMG();
        createTempAIMG();
    }
    // if (CRT_out_format.value == 'gif') {
    //     flip_horizontal.disabled = false;
    //     flip_vertical.disabled = false;
    // }
    // else {
    //     flip_horizontal.disabled = true;
    //     flip_vertical.disabled = true;        
    // }
}

function createTempAIMG() {
    if (sequence_paths == null){ console.log('no sequences, exiting...'); return; }
    freezeButtons();
    client.invoke('combine_image', sequence_paths, 'temp/', Date.now().toString(), parseFloat(create_fps.value), 
        CRT_out_format.value, create_width.value, create_height.value, is_reversed.checked, is_disposed.checked, 
        flip_horizontal.checked, flip_vertical.checked, (error, res) => {
        console.log('createfragment fps', create_fps.value);
        if (error) {
            console.error(error);
        } else {
            CRT_aimg_stage.src = res;
            CRT_aimg_path.value = res;
        }
        unfreezeButtons();
    });
}

function deleteTempAIMG() {
    CRT_aimg_stage.src = '';
    abstempath = '';
    // client.invoke('delete_temp_images', (error, res) => {
    //     if (error) {
    //         console.error(error);
    //     } else {
    //         console.log(res);
    //     }
    // });
}

choose_aimg_outdir_button.addEventListener('click', () => {
    var choosen_dir = dialog.showOpenDialog({ properties: dir_dialog_props });
    console.log(`Chosen dir: ${choosen_dir}`);
    if (choosen_dir === undefined) {return}
    create_outdir.value = choosen_dir;
    mboxClear(create_msgbox);
});

create_aimg_button.addEventListener('click', () => {
    mboxClear(create_msgbox);
    console.log(sequence_paths, create_outdir.value, create_name.value, parseFloat(create_fps.value), 
    CRT_out_format.value, false, is_disposed.checked);
    console.log('console log', is_disposed.checked);
    create_aimg_button.classList.add('is-loading');
    freezeButtons();
    // build_aimg(sequence_paths, create_outdir.value, create_name.value, parseInt(create_fps.value), CRT_out_format.value, false, is_disposed.checked);
    client.invoke("combine_image", sequence_paths, create_outdir.value, create_name.value, parseFloat(create_fps.value), 
        CRT_out_format.value, create_width.value, create_height.value, is_reversed.checked, is_disposed.checked, flip_horizontal.checked, flip_vertical.checked, (error, res) => {
        console.log('createfragment fps', create_fps.value);
        if (error) {
            console.error(error);
            mboxError(create_msgbox, error);
            create_aimg_button.classList.remove('is-loading');
            unfreezeButtons();
        } else {
            if (res) {
                console.log('res', res);
                mboxSuccess(create_msgbox, res);
                if (res == "Finished!") {
                    create_aimg_button.classList.remove('is-loading');
                    unfreezeButtons();
                }
            }
        }
    });
});

function testcallback(){
    console.log("cache cleared!!1");
}

function unfreezeButtons () {
    CRT_load_imgs_button.classList.remove('is-static');
    CRT_clear_imgs_button.classList.remove('is-static');
}
function freezeButtons () {
    CRT_load_imgs_button.classList.add('is-static');
    CRT_clear_imgs_button.classList.add('is-static');
}

CRT_bgprev_button.addEventListener('click', () => {
    if (!create_checkerbg_active) {
        create_aimg_cell.style.background = "url('./imgs/Transparency500.png')";
        CRT_bgprev_button.classList.add('is-active');
        create_checkerbg_active = true;
    } else {
        create_aimg_cell.style.background = ''
        CRT_bgprev_button.classList.remove('is-active');
        create_checkerbg_active = false;
    }
});

CRT_autoprev_button.addEventListener('click', () => {
    if (!autoprev_active) {
        autoprev_icon.classList.remove('fa-eye-slash');
        autoprev_icon.classList.add('fa-eye');
        autoprev_active = true;
        reloadTempAIMG();
    } else {
        autoprev_icon.classList.remove('fa-eye');
        autoprev_icon.classList.add('fa-eye-slash');
        autoprev_active = false;
        deleteTempAIMG();
    }
});

