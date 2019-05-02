const remote = require("electron").remote;
window.$ = window.jQuery = require('jquery');

let create_menu = document.getElementById('create_menu');
let split_menu = document.getElementById('split_menu');
let create_panel = document.getElementById('create_panel');
let split_panel = document.getElementById('split_panel');

let minimize_button = document.getElementById('minimize_button');
let exit_button = document.getElementById('exit_button');
let display_panel = document.getElementById('display_panel');

// window.addEventListener("load", show_create_panel);

function hideAll() {
    $(create_panel).hide();
    $(split_panel).hide();
}
function show_create_panel() {
    console.log("create called")
    hideAll();
    $(create_panel).show();
}
function show_split_panel() {
    console.log("split called");
    hideAll();
    $(split_panel).show();
}

$(create_menu).click(show_create_panel);
$(split_menu).click(show_split_panel);

minimize_button.addEventListener("click", () => {
    var window = remote.getCurrentWindow();
    window.minimize();
})

exit_button.addEventListener("click", () => {
    var window = remote.getCurrentWindow();
    window.close();
});
