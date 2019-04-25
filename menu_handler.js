const remote = require('electron').remote;

let exit_button = document.querySelector('#exit_button')

exit_button.addEventListener('click', () => {
    var window = remote.getCurrentWindow();
    window.close();
})