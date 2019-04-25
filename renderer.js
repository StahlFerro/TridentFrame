const zerorpc = require("zerorpc")
const { dialog } = require('electron').remote

let client = new zerorpc.Client()
client.connect("tcp://127.0.0.1:4242")

let open_image_button = document.querySelector('#open_image_button')
let target_dir_button = document.querySelector('#target_dir_button')
let image_stage = document.querySelector('#image_stage')
let target_path = document.querySelector('#target_path')
let info_header = document.querySelector('#info_header')
let td_fname = document.querySelector('#td_fname')
let td_dimens = document.querySelector('#td_dimens')
let td_fsize = document.querySelector('#td_fsize')
let td_fcount = document.querySelector('#td_fcount')
let td_fps = document.querySelector('#td_fps')
let td_loopdur = document.querySelector('#td_loopdur')


let extension_filters = [
    { name: 'Images', extensions: ['png', 'gif'] },
//    { name: 'Movies', extensions: ['mkv', 'avi', 'mp4'] },
//    { name: 'Custom File Type', extensions: ['as'] },
//    { name: 'All Files', extensions: ['*'] }
]

let file_dialog_prop = ['openfile']
let dir_dialog_prop = ['openDirectory']

open_image_button.addEventListener('click', () => {
    var chosen_path = dialog.showOpenDialog({ filters: extension_filters, properties: file_dialog_prop })
    console.log(`chosen path: ${chosen_path}`)
    if (chosen_path === undefined) {return}
    client.invoke("inspect_image", chosen_path[0], (error, res) => {
    if (error) {
        console.error(error)
    } else {
        console.log(res)
        td_fname.innerHTML = res.name
        info_header.innerHTML = `${res.extension} Information`
        td_fsize.innerHTML = `${res.fsize}`
        td_fcount.innerHTML = res.frame_count
        td_fps.innerHTML = res.fps
        td_dimens.innerHTML = `${res.width} x ${res.height}`
        td_loopdur.innerHTML = `${res.loop_duration} seconds`
        image_stage.src = res.absolute_url
    }
    })
})

target_dir_button.addEventListener('click', () => {
    var choosen_dir = dialog.showOpenDialog({ properties: dir_dialog_prop })
    console.log(`Chosen dir: ${choosen_dir}`)
    if (choosen_dir === undefined) {return}
    target_path.innerHTML = choosen_dir
})


//formula.addEventListener('input', () => {
//  console.log(formula.value)
//  client.invoke("calc", formula.value, (error, res) => {
//    if(error) {
//      console.error(error)
//    } else {
//      result.textContent = res
//    }
//  })
//})

//formula.dispatchEvent(new Event('input'))


