const uri2path = require('file-uri-to-path');


function allowDrop(ev) {
    console.log("allowDrop called");
    ev.preventDefault();
}

function drag(ev) {
    console.log("drag called");
    console.log("data", ev.target.src)
    console.log("data", uri2path(ev.target.src))
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
    console.log("drop called");
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    console.log("data", data)
    console.log(data)
    ev.target.appendChild(document.getElementById(data));
}
