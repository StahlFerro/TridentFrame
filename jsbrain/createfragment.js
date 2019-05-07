console.log("splitfragment.js loaded!");
const { dialog } = require('electron').remote
const { client } = require("./renderer.js");

let sequence_carousel = document.getElementById('sequence_carousel')
let load_imgs_button = document.getElementById('load_imgs_button')
let sequence_dir = document.getElementById("sequence_dir")

let extension_filters = [
    { name: 'Images', extensions: ['png', 'gif'] },
]
let imgs_dialog_props = ['openfile', 'multiSelections', 'createDirectory']

load_imgs_button.addEventListener("click", () => {
    var img_paths = dialog.showOpenDialog({  filters: extension_filters, properties: imgs_dialog_props })
    console.log(`chosen path: ${img_paths}`)
    if (img_paths === undefined) {return}
    sequence_dir.value = img_paths;
    console.log(img_paths);
    client.invoke("inspect_sequence", img_paths, (error, res) => {
        if (error) {
            console.error(error);
        } else {
            carousel_tags = ''
            for (const ipath of img_paths){
                console.log(ipath)
                carousel_tags += `<div class="carousel-slide">
                <img class="carousel-img" src="${ipath}" width="150px" height="150px"/>
            </div>`
            }
            sequence_carousel.innerHTML = carousel_tags;
            console.log(res);
        }
    })
    // msg_clear();
});
