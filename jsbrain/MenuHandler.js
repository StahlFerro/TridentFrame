const remote = require("electron").remote;
const session = remote.getCurrentWebContents().session;

let create_menu = document.getElementById('create_menu');
let create_box = document.getElementById('create_box');
let split_menu = document.getElementById('split_menu');
let split_box = document.getElementById('split_box');
let convert_menu = document.getElementById('convert_menu');
let convert_box = document.getElementById('convert_box')
let sprsheet_menu = document.getElementById('sprsheet_menu');
let sprsheet_box = document.getElementById('sprsheet_box')

let create_panel = document.getElementById('create_panel');
let split_panel = document.getElementById('split_panel');
let convert_panel = document.getElementById('convert_panel');
let sprsheet_panel = document.getElementById('sprsheet_panel');

let minimize_button = document.getElementById('minimize_button');
let exit_button = document.getElementById('exit_button');
let display_panel = document.getElementById('display_panel');

// window.addEventListener("load", show_create_panel);

function hideAll() {
    create_panel.style.display = 'none';
    split_panel.style.display = 'none';
    convert_panel.style.display = 'none';
    sprsheet_panel.style.display = 'none';
}
function unselect_all_menus() {
    create_box.classList.remove('is-selected');
    split_box.classList.remove('is-selected');
    convert_box.classList.remove('is-selected');
    sprsheet_box.classList.remove('is-selected');
}
function show_create_panel() {
    console.log("create called")
    hideAll();
    unselect_all_menus();
    create_box.classList.add('is-selected');
    create_panel.style.display = 'block';
    session.clearStorageData(['appcache', 'cookies', 'filesystem', 'indexdb', 'localstorage', 'shadercache', 'websql', 'serviceworkers', 'cachestorage']);
}
function show_split_panel() {
    console.log("split called");
    hideAll();
    unselect_all_menus();
    split_box.classList.add('is-selected');
    split_panel.style.display = 'block';
    session.clearStorageData(['appcache', 'cookies', 'filesystem', 'indexdb', 'localstorage', 'shadercache', 'websql', 'serviceworkers', 'cachestorage']);
}
function show_convert_panel() {
    console.log("convert called");
    hideAll();
    unselect_all_menus();
    convert_box.classList.add('is-selected');
    convert_panel.style.display = 'block';
    session.clearStorageData(['appcache', 'cookies', 'filesystem', 'indexdb', 'localstorage', 'shadercache', 'websql', 'serviceworkers', 'cachestorage']);
}
function show_sprsheet_panel() {
    console.log("sprsheet called");
    hideAll();
    unselect_all_menus();
    sprsheet_box.classList.add('is-selected');
    sprsheet_panel.style.display = 'block';
    session.clearStorageData(['appcache', 'cookies', 'filesystem', 'indexdb', 'localstorage', 'shadercache', 'websql', 'serviceworkers', 'cachestorage']);
}

minimize_button.addEventListener("click", () => {
    var window = remote.getCurrentWindow();
    window.minimize();
});

exit_button.addEventListener("click", () => {
    var window = remote.getCurrentWindow();
    window.close();
});

create_menu.addEventListener('click', show_create_panel);
split_menu.addEventListener('click', show_split_panel);
convert_menu.addEventListener('click', show_convert_panel);
sprsheet_menu.addEventListener('click', show_sprsheet_panel);
