const remote = require("electron").remote;
window.$ = window.jQuery = require('jquery');

let display_panel = document.getElementById('display_panel');

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
exit_button.addEventListener('click', () => {
    var window = remote.getCurrentWindow();
    window.close();
});
