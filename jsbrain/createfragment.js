console.log("splitfragment.js loaded!");
const { dialog } = require('electron').remote
const { client } = require("./renderer.js");

let load_dir_button = document.getElementById('load_dir_button')
let sequence_dir = document.getElementById("sequence_dir")

let extension_filters = [
    { name: 'Images', extensions: ['png', 'gif'] },
]
let file_dialog_prop = ['openfile', 'multiSelections']

load_dir_button.addEventListener("click", () => {
    var chosen_path = dialog.showOpenDialog({  filters: extension_filters, properties: file_dialog_prop })
    console.log(`chosen path: ${chosen_path}`)
    if (chosen_path === undefined) {return}
    sequence_dir.value = chosen_path;
    client.invoke("inspect_sequence", chosen_path[0], (error, res) => {
        if (error) {
            console.error(error);
        } else {
            console.log(res);
        }
    })
    // msg_clear();
});
