const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const path = require('path');
const deploy_env = process.env.DEPLOY_ENV;
let pyProc = null;
let pyPort = null;


let mainWindow = null
const createWindow = () => {
    mainWindow = new BrowserWindow({
        width: 950, height: 700,
        minWidth: 950, minHeight: 700,
        maxWidth: 950, maxHeight: 700,
        center: true, 
        frame: false,
        darkTheme: true,
        fullscreen: false,
        resizable: false,
        icon: path.join(__dirname, 'imgs/TridentFrame_Icon_200px.png'),
        webPreferences: {
            webSecurity: false,
            nodeIntegration: true,
        },
    });
    mainWindow.setMenu(null);
    if (deploy_env && deploy_env == "DEV") { // Development environment
        mainWindow.loadURL("http://localhost:8080/")
    }
    else {
        // Production environment
        mainWindow.loadURL(require('url').format({
            pathname: path.join(__dirname, './dist/index.html'),
            protocol: 'file:',
            slashes: true
        }));
    }
    mainWindow.webContents.openDevTools();
    mainWindow.focus();
    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

app.on('ready', createWindow);
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin'){
        app.quit();
    }
})
app.on('activate', () => {
    if (mainWindow === null){
        createWindow();
    }
})

const selectPort = () => {
    pyPort = 4242;
    return pyPort;
}

const createPyProc = () => {
    let port = '' + selectPort();
    let script = path.join(__dirname, 'main.py');
    pyProc = require('child_process').spawn('python', [script, port]);
    if (pyProc != null) {
      console.log('child process success');
    }
}

const exitPyProc = () => {
    console.log(lmao)
    pyProc.kill();
    pyProc = null;
    pyPort = null;
}

app.on('ready', createPyProc);
app.on('will-quit', exitPyProc);
