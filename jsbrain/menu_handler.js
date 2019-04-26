const remote = require('electron').remote;

let split_button = document.querySelector('#split_button')
let exit_button = document.querySelector('#exit_button')

exit_button.addEventListener('click', () => {
    var window = remote.getCurrentWindow();
    window.close();
})