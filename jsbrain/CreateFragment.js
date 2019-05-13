console.log("splitfragment.js loaded!");
const remote = require('electron').remote;
const dialog = remote.dialog;
const session = remote.getCurrentWebContents().session;
const { client } = require('./Client.js');
const { mboxClear, mboxError, mboxSuccess } = require('./MessageBox.js');
window.$ = window.jQuery = require('jquery');

console.log(`session ${session}`);
console.log(`session ${session.defaultSession}`);
setInterval(() => {
    session.getCacheSize((num) => {
        console.log(`session size: ${num}`);
    });
}, 3000);


// let sequence_carousel = document.getElementById('sequence_carousel')
let load_imgs_button = document.getElementById('load_imgs_button');
let clear_imgs_button = document.getElementById('clear_imgs_button');
let choose_outdir_button = document.getElementById('choose_outdir_button');
let create_aimg_button = document.getElementById('create_aimg_button');

var sequence_body = document.getElementById('sequence_body');
let sequence_paths = null;
let create_name = document.getElementById('create_name');
let create_fps = document.getElementById('create_fps');
let is_disposed = document.getElementById('is_disposed')
let create_format = document.getElementById('create_format');
let create_outdir = document.getElementById('create_outdir');


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
    deactivate_buttons();
    load_imgs_button.classList.add("is-loading");
    client.invoke("inspect_sequence", img_paths, (error, res) => {
        if (error) {
            console.error(error);
            mboxError(error);
        } else {
            sequence_paths = res.sequences;
            console.log("obtained sequences", sequence_paths);
            quintcell_generator(sequence_paths);
            create_name.value = res.name;
            create_fps.value = 50;
            console.log(res);
            mboxClear();
        }
        load_imgs_button.classList.remove('is-loading');
        activate_buttons();
    })
});

clear_imgs_button.addEventListener('click', () => {
    // sequence_body.innerHTML = '';
    while (sequence_body.hasChildNodes()){
        sequence_body.removeChild(sequence_body.firstChild);
    }
    sequence_paths = null;
    session.clearCache(testcallback);
});

choose_outdir_button.addEventListener('click', () => {
    var choosen_dir = dialog.showOpenDialog({ properties: dir_dialog_props });
    console.log(`Chosen dir: ${choosen_dir}`);
    if (choosen_dir === undefined) {return}
    create_outdir.value = choosen_dir;
    mboxClear();
});

create_aimg_button.addEventListener('click', () => {
    console.log(sequence_paths, create_outdir.value, create_name.value, parseInt(create_fps.value), 
    create_format.value, false, is_disposed.checked);
    console.log('console log', is_disposed.checked);
    client.invoke("combine_image", sequence_paths, create_outdir.value, create_name.value, parseInt(create_fps.value), 
        create_format.value, false, is_disposed.checked, (error, res) => {
        if (error) {
            console.error(error);
        } else {
            console.log("SUCCESS!");
        }
    });
});

function testcallback(){
    console.log("cache cleared!!1");
}

function activate_buttons () {
    load_imgs_button.classList.remove('is-static');
    clear_imgs_button.classList.remove('is-static');
}

function deactivate_buttons () {
    load_imgs_button.classList.add('is-static');
    clear_imgs_button.classList.add('is-static');
    
}

function quintcell_generator(paths) {
    sequence_body.innerHTML = '';
    for (var row = 0; row < Math.ceil(paths.length / 5); row++) {
        var tr = document.createElement('TR');
        for (var c = 0; c < 5; c++) {
            const index = (row * 5) + c;
            const data = paths[index];
            if (data === undefined) {continue;}
            var td = document.createElement('TD');
            var img = document.createElement('IMG');
            img.src = data;
            td.appendChild(img);
            tr.appendChild(td);
        }
        sequence_body.appendChild(tr);
    }
}
