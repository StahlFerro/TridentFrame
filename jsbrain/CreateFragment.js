console.log("splitfragment.js loaded!");
const remote = require('electron').remote;
const dialog = remote.dialog;
const session = remote.getCurrentWebContents().session;
const { client } = require('./Client.js');
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
let load_imgs_button = document.getElementById('load_imgs_button');
let clear_imgs_button = document.getElementById('clear_imgs_button');
let choose_aimg_outdir_button = document.getElementById('choose_aimg_outdir_button');
let background_button = document.getElementById('background_button')
let create_aimg_button = document.getElementById('create_aimg_button');

var sequence_body = document.getElementById('sequence_body');
let sequence_paths = null;
let sequence_counter = document.getElementById('sequence_counter');
let create_name = document.getElementById('create_name');
let create_fps = document.getElementById('create_fps');
let is_disposed = document.getElementById('is_disposed');
let is_reversed = document.getElementById('is_reversed');
let flip_horizontal = document.getElementById('flip_horizontal');
let flip_vertical = document.getElementById('flip_vertical');
let create_format = document.getElementById('create_format');
let create_outdir = document.getElementById('create_outdir');
let prev_aimg_stage = document.getElementById('prev_aimg_stage');
let prev_aimg_path = document.getElementById('prev_aimg_path');


let extension_filters = [
    { name: 'Images', extensions: ['png', 'gif'] },
];
let imgs_dialog_props = ['openfile', 'multiSelections', 'createDirectory'];
let dir_dialog_props = ['openDirectory', 'createDirectory'];

load_imgs_button.addEventListener("click", () => {
    var img_paths = dialog.showOpenDialog({ filters: extension_filters, properties: imgs_dialog_props })
    console.log(`chosen path: ${img_paths}`)
    if (img_paths === undefined) { return }
    console.log(img_paths);
    deactivateButtons();
    load_imgs_button.classList.add("is-loading");
    client.invoke("inspect_sequence", img_paths, (error, res) => {
        if (error) {
            console.error(error);
            mboxError(create_msgbox, error);
        } else {
            sequence_paths = res.sequences;
            console.log("obtained sequences", sequence_paths);
            quintcell_generator(sequence_paths);
            create_name.value = res.name;
            if (create_fps.value === undefined || create_fps.value == null || create_fps.value == "") {
                create_fps.value = 50;
            }
            sequence_counter.innerHTML = `${res.total} image${res.total > 1? "s": ""} (${res.size} total)`;
            console.log(res);
            mboxClear(create_msgbox);
            createTempAIMG();
        }
        load_imgs_button.classList.remove('is-loading');
        activateButtons();
    });
});


clear_imgs_button.addEventListener('click', () => {
    // sequence_body.innerHTML = '';
    while (sequence_body.hasChildNodes()){
        sequence_body.removeChild(sequence_body.firstChild);
    }
    sequence_paths = null;
    create_name.value = '';
    create_fps.value = '';
    sequence_counter.innerHTML = '';
    mboxClear(create_msgbox);
    deleteTempAIMG();
    session.clearCache(testcallback);
});

create_fps.addEventListener('input', reloadTempAIMG);
is_disposed.addEventListener('click', reloadTempAIMG);
is_reversed.addEventListener('click', reloadTempAIMG);
create_format.addEventListener('change', reloadTempAIMG);
flip_horizontal.addEventListener('click', reloadTempAIMG);
flip_vertical.addEventListener('click', reloadTempAIMG);

function reloadTempAIMG() {
    deleteTempAIMG();
    createTempAIMG();
    if (create_format.value == 'gif') {
        flip_horizontal.disabled = false;
        flip_vertical.disabled = false;
    }
    else {
        flip_horizontal.disabled = true;
        flip_vertical.disabled = true;        
    }
}

function createTempAIMG() {
    if (sequence_paths == null){ console.log('no sequences, exiting...'); return; }
    deactivateButtons();

    client.invoke('combine_image', sequence_paths, 'temp/', Date.now().toString(), parseFloat(create_fps.value), 
        create_format.value, is_reversed.checked, is_disposed.checked, flip_horizontal.checked, flip_vertical.checked, (error, res) => {
        if (error) {
            console.error(error);
        } else {
            prev_aimg_stage.src = res;
            prev_aimg_path.value = res;
        }
        activateButtons();
    });
}

function deleteTempAIMG() {
    prev_aimg_stage.src = '';
    abstempath = '';
    client.invoke('delete_temp_images', (error, res) => {
        if (error) {
            console.error(error);
        } else {
            console.log(res);
        }
    });
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
    create_format.value, false, is_disposed.checked);
    console.log('console log', is_disposed.checked);
    create_aimg_button.classList.add('is-loading');
    // build_aimg(sequence_paths, create_outdir.value, create_name.value, parseInt(create_fps.value), create_format.value, false, is_disposed.checked);
    client.invoke("combine_image", sequence_paths, create_outdir.value, create_name.value, parseFloat(create_fps.value), 
        create_format.value, false, is_disposed.checked, flip_horizontal.checked, flip_vertical.checked, (error, res) => {
        if (error) {
            console.error(error);
            mboxError(create_msgbox, error);
        } else {
            console.log("SUCCESS!");
            mboxSuccess(create_msgbox, 'GIF/APNG successfully created!!1, check out the output directory');
        }
        create_aimg_button.classList.remove('is-loading');
    });
});

function testcallback(){
    console.log("cache cleared!!1");
}

function activateButtons () {
    load_imgs_button.classList.remove('is-static');
    clear_imgs_button.classList.remove('is-static');
}

function deactivateButtons () {
    load_imgs_button.classList.add('is-static');
    clear_imgs_button.classList.add('is-static');
}

function quintcell_generator(paths) {
    sequence_body.innerHTML = '';
    for (var row = 0; row < Math.ceil(paths.length / 5); row++) {
        var tr = document.createElement('TR');
        for (var c = 0; c < 5; c++) {
            const index = (row * 5) + c;
            const img_path = paths[index];
            if (img_path === undefined) {continue;}
            var td = document.createElement('TD');
            var div = document.createElement('DIV');
            div.classList.add('seqdiv');
            var img = document.createElement('IMG');
            img.src = img_path;
            var i = document.createElement('I');
            i.className = 'fas fa-minus-circle del-icon';
            i.onclick = del_frame;

            var span = document.createElement('SPAN');
            span.classList.add('icon');
            span.appendChild(i);

            var a = document.createElement('A');
            a.className = 'del-anchor';
            a.append(span);

            div.appendChild(img);
            div.appendChild(a);
            td.appendChild(div);
            tr.appendChild(td);
        }
        sequence_body.appendChild(tr);
    }
}

function del_frame() {
    console.log("delet");
}
