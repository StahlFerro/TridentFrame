console.log("splitfragment.js loaded!");
const { dialog } = require('electron').remote
const { client } = require("./renderer.js");

let open_image_button = document.querySelector('#open_image_button')
let target_dir_button = document.querySelector('#target_dir_button')
let split_button = document.querySelector('#split_button')

let image_stage = document.querySelector('#image_stage')
let image_path = document.querySelector('#image_path')

let target_path = document.querySelector('#target_path')

let info_header = document.querySelector('#info_header')
let td_fname = document.querySelector('#td_fname')
let td_dimens = document.querySelector('#td_dimens')
let td_fsize = document.querySelector('#td_fsize')
let td_fcount = document.querySelector('#td_fcount')
let td_fps = document.querySelector('#td_fps')
let td_loopdur = document.querySelector('#td_loopdur')

let td_message_box = document.querySelector('#td_message_box')


let extension_filters = [
    { name: 'Images', extensions: ['png', 'gif'] },
]

let file_dialog_prop = ['openfile']
let dir_dialog_prop = ['openDirectory']


// function registerListeners() {
//     open_image_button.addEventListener("click", openImage);
//     console.log("registerListener called");
// }

open_image_button.addEventListener("click", () => {
    var chosen_path = dialog.showOpenDialog({ filters: extension_filters, properties: file_dialog_prop })
    console.log(`chosen path: ${chosen_path}`)
    if (chosen_path === undefined) {return}
    client.invoke("inspect_image", chosen_path[0], (error, res) => {
        if (error) {
            console.error(error)
            td_message_box.innerHTML = error
            td_message_box.classList.add("has-text-danger")
        } else {
            console.log(res)
            td_fname.innerHTML = res.name
            info_header.innerHTML = `${res.extension} Information`
            td_fsize.innerHTML = `${res.fsize}`
            td_fcount.innerHTML = res.frame_count
            td_fps.innerHTML = res.fps
            td_dimens.innerHTML = `${res.width} x ${res.height}`
            td_loopdur.innerHTML = `${res.loop_duration} seconds`
            image_stage.src = res.absolute_url
            image_path.value = res.absolute_url
        }
    })
    console.log('registered!');
});

target_dir_button.addEventListener('click', () => {
    var choosen_dir = dialog.showOpenDialog({ properties: dir_dialog_prop });
    console.log(`Chosen dir: ${choosen_dir}`);
    if (choosen_dir === undefined) {return}
    target_path.innerHTML = choosen_dir;
    td_message_box.classList.remove('has-text-danger');
    td_message_box.innerHTML = "";
});

split_button.addEventListener('click', () => {
    var img_path = image_path.value;
    var out_path = target_path.innerHTML;
    console.log(`${image_path} ${out_path}`);
    if (out_path === undefined || img_path === undefined) {return}
    client.invoke('split_image', img_path, out_path, (error, res) => {
        if (error || !res){
            console.log(error);
            td_message_box.innerHTML = error;
            td_message_box.classList.add("has-text-danger");
        } else {
            if (res){
                td_message_box.innerHTML = "Success!";
            }
        }
    })
});

// module.exports.registerListeners = registerListeners;