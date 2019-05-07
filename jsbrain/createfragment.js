console.log("splitfragment.js loaded!");
const { dialog } = require('electron').remote
const { client } = require("./renderer.js");
window.$ = window.jQuery = require('jquery');

let sequence_carousel = document.getElementById('sequence_carousel')
let sequences = null;
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
        } else {
            sequences = res.sequences;
            console.log("obtained sequences", sequences)
            // carousel_tags = ''
            // for (const [index, ipath] of img_paths.entries()) {
            //     console.log(ipath)
            //     carousel_tags += `<div class="carousel-slide" ondrop="drop(event)" ondragover="allowDrop(event)">
            //         ${index} <img class="carousel-img" src="${ipath}" width="150px" height="150px" draggable="true" ondragstart="drag(event)"/>
            //     </div>`
            // }
            // sequence_carousel.innerHTML = carousel_tags;
            console.log(res);
        }
    })
    // msg_clear();
});

clear_imgs_button.addEventListener('click', () => {
    // sequence_carousel.innerHTML = ''
});

// (function () {
//     function scrollHorizontally(e) {
//         e = window.event || e;
//         var delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)));
//         sequence_carousel.scrollLeft -= (delta * 40); // Multiplied by 40
//         e.preventDefault();
//     }
//     if (sequence_carousel.addEventListener) {
//         // IE9, Chrome, Safari, Opera
//         sequence_carousel.addEventListener("mousewheel", scrollHorizontally, false);
//         // Firefox
//         sequence_carousel.addEventListener("DOMMouseScroll", scrollHorizontally, false);
//     } else {
//         // IE 6/7/8
//         sequence_carousel.attachEvent("onmousewheel", scrollHorizontally);
//     }
// })();

