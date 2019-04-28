const remote = require("electron").remote;
window.$ = window.jQuery = require('jquery');

let create_button = document.querySelector('#create_button')
let split_button = document.querySelector('#split_button');
let exit_button = document.querySelector('#exit_button');

$(create_button).click(function() {
    console.log('yes');
});

exit_button.addEventListener('click', () => {
    var window = remote.getCurrentWindow();
    window.close();
})


