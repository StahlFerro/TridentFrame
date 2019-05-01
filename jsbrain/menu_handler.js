const remote = require("electron").remote;
window.$ = window.jQuery = require('jquery');

let create_fragment_menu = document.querySelector('#create_fragment_menu')
let split_fragment_menu = document.querySelector('#split_fragment_menu');
let exit_button = document.querySelector('#exit_button');
let display_panel = document.getElementById('display_panel');

var observer = new MutationObserver(function (mutationrecords){
    console.log("mutation observed");
    console.log(display_panel.nodeName);
    const { registerListeners } = require("./splitfragment.js");
    console.log(registerListeners);
    registerListeners();
});
observer.observe(display_panel, {childList: true});

$(create_fragment_menu).click(function() {
    console.log('create button pressed');
    $(display_panel).load("htfragments/createfragment.html");
});

$(split_fragment_menu).click(function () {
    console.log('split button pressed');
    $(display_panel).load("htfragments/splitfragment.html");
});

exit_button.addEventListener('click', () => {
    var window = remote.getCurrentWindow();
    window.close();
});
