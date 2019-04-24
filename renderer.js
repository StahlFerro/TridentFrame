const zerorpc = require("zerorpc")
const { dialog } = require('electron').remote

let client = new zerorpc.Client()
client.connect("tcp://127.0.0.1:4242")

let load_image_button = document.querySelector('#load_image_button')
let image_stage = document.querySelector('#image_stage')
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

let dialog_properties = ['openfile']

load_image_button.addEventListener('click', () => {
    var chosen_path = dialog.showOpenDialog({ filters: extension_filters, properties: dialog_properties })
    console.log(`chosen path: ${chosen_path}`)
    client.invoke("inspect_image", chosen_path[0], (error, res) => {
    if (error) {
        console.error(error)
    } else {
        console.log(res)
        td_fname.innerHTML = res.name
        td_fsize.innerHTML = `${res.size} bytes`
        td_fcount.innerHTML = res.frame_count
        td_fps.innerHTML = res.fps
        td_dimens.innerHTML = `${res.width} x ${res.height}`
        td_loopdur.innerHTML = `${res.loop_duration} seconds`
        image_stage.src = res.absolute_url
    }
    })
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


