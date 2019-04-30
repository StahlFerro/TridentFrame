const remote = require("electron").remote;
window.$ = window.jQuery = require('jquery');

let create_button = document.querySelector('#create_button')
let split_button = document.querySelector('#split_button');
let exit_button = document.querySelector('#exit_button');
let display_panel = document.getElementById('display_panel');

$(create_button).click(function() {
    console.log('create button pressed');
    $(display_panel).html("<p>Lmao</p>");
});

$(split_button).click(function () {
    console.log('split button pressed');
    $(display_panel).html("<h1 class='title is-1'>follow me on microsoft excel</h1>");
});

exit_button.addEventListener('click', () => {
    var window = remote.getCurrentWindow();
    window.close();
})


