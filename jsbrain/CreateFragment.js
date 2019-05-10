console.log("splitfragment.js loaded!");
const { dialog } = require('electron').remote
const { client } = require("./Client.js");
const { mboxClear, mboxError, mboxSuccess } = require('./MessageBox.js')
window.$ = window.jQuery = require('jquery');

// let sequence_carousel = document.getElementById('sequence_carousel')
let sequences = null;
var sequence_body = document.getElementById('sequence_body')
let load_imgs_button = document.getElementById('load_imgs_button')
let clear_imgs_button = document.getElementById('clear_imgs_button')

let extension_filters = [
    { name: 'Images', extensions: ['png', 'gif'] },
]
let imgs_dialog_props = ['openfile', 'multiSelections', 'createDirectory']

load_imgs_button.addEventListener("click", () => {
    var img_paths = dialog.showOpenDialog({ filters: extension_filters, properties: imgs_dialog_props })
    console.log(`chosen path: ${img_paths}`)
    if (img_paths === undefined) { return }
    console.log(img_paths);
    client.invoke("inspect_sequence", img_paths, (error, res) => {
        if (error) {
            console.error(error);
            mboxError(error);
        } else {
            sequences = res.sequences;
            console.log("obtained sequences", sequences);
            quintcell_generator(sequences);
            console.log(res);
            mboxClear();
        }
    })
});

clear_imgs_button.addEventListener('click', () => {
    sequence_body.innerHTML = '';
});

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
