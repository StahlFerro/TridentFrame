const remote = require("electron").remote;
const session = remote.getCurrentWebContents().session;

let create_menu = document.getElementById('create_menu');
let create_box = document.getElementById('create_box');
let split_menu = document.getElementById('split_menu');
let split_box = document.getElementById('split_box');
let convert_menu = document.getElementById('convert_menu');
let convert_box = document.getElementById('convert_box')
let buildsprite_menu = document.getElementById('buildsprite_menu');
let buildsprite_box = document.getElementById('buildsprite_box')
let slicesprite_menu = document.getElementById('slicesprite_menu');
let slicesprite_box = document.getElementById('slicesprite_box')
let settings_menu = document.getElementById('settings_menu');
let settings_box = document.getElementById('settings_box')
let about_menu = document.getElementById('about_menu');
let about_box = document.getElementById('about_box')

let create_panel = document.getElementById('create_panel');
let split_panel = document.getElementById('split_panel');
let convert_panel = document.getElementById('convert_panel');
let buildsprite_panel = document.getElementById('buildsprite_panel');
let slicesprite_panel = document.getElementById('slicesprite_panel');
let settings_panel = document.getElementById('settings_panel');
let about_panel = document.getElementById('about_panel');

let minimize_button = document.getElementById('minimize_button');
let exit_button = document.getElementById('exit_button');
let display_panel = document.getElementById('display_panel');

// window.addEventListener("load", show_create_panel);

function hideAll() {
    create_panel.style.display = 'none';
    split_panel.style.display = 'none';
    convert_panel.style.display = 'none';
    buildsprite_panel.style.display = 'none';
    slicesprite_panel.style.display = 'none';
    settings_panel.style.display = 'none';
    about_panel.style.display = 'none';
}
function unselect_all_menus() {
    create_box.classList.remove('is-selected');
    split_box.classList.remove('is-selected');
    convert_box.classList.remove('is-selected');
    buildsprite_box.classList.remove('is-selected');
    slicesprite_box.classList.remove('is-selected');
    settings_box.classList.remove('is-selected');
    about_box.classList.remove('is-selected');
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
function show_buildsprite_panel() {
    console.log("buildsprite called");
    hideAll();
    unselect_all_menus();
    buildsprite_box.classList.add('is-selected');
    buildsprite_panel.style.display = 'block';
    session.clearStorageData(['appcache', 'cookies', 'filesystem', 'indexdb', 'localstorage', 'shadercache', 'websql', 'serviceworkers', 'cachestorage']);
}
function show_slicesprite_panel() {
    console.log("slicesprite called");
    hideAll();
    unselect_all_menus();
    slicesprite_box.classList.add('is-selected');
    slicesprite_panel.style.display = 'block';
    session.clearStorageData(['appcache', 'cookies', 'filesystem', 'indexdb', 'localstorage', 'shadercache', 'websql', 'serviceworkers', 'cachestorage']);
}
function show_settings_panel() {
    console.log("settings called");
    hideAll();
    unselect_all_menus();
    settings_box.classList.add('is-selected');
    settings_panel.style.display = 'block';
    session.clearStorageData(['appcache', 'cookies', 'filesystem', 'indexdb', 'localstorage', 'shadercache', 'websql', 'serviceworkers', 'cachestorage']);
}
function show_about_panel() {
    console.log("about called");
    hideAll();
    unselect_all_menus();
    about_box.classList.add('is-selected');
    about_panel.style.display = 'block';
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
buildsprite_menu.addEventListener('click', show_buildsprite_panel);
slicesprite_menu.addEventListener('click', show_slicesprite_panel);
settings_menu.addEventListener('click', show_settings_panel);
about_menu.addEventListener('click', show_about_panel);
