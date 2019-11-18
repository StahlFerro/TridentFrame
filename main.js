const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const path = require('path');
const deploy_env = process.env.DEPLOY_ENV;
let pyProc = null;
let pyPort = null;
let appath = app.getAppPath();
console.log("DIRNAME", __dirname);
console.log("APP PATH", appath);

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
        icon: path.join(__dirname, 'imgs/TridentFrame_logo_256x256.ico'),
        webPreferences: {
            webSecurity: false,
            nodeIntegration: true,
        },
    });
    mainWindow.setMenu(null);
    if (deploy_env && deploy_env == "DEV") { // Development environment
        console.log("------ DEVELOPMENT VERSION ------");
        mainWindow.loadURL("http://localhost:8080/");
    }
    else {
        console.log("------ PRODUCTION VERSION ------");
        // Production environment
        mainWindow.loadURL(require('url').format({
            pathname: path.join(__dirname, './dist/index.html'),
            protocol: 'file:',
            slashes: true
        }));
    }

    // if (deploy_env && deploy_env == 'DEV') {
        mainWindow.webContents.openDevTools({detach: true});
    // }
    mainWindow.focus();
    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

app.on('ready', () => {
    createPyProc();
    createWindow();
});
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
    pyPort = 42069;
    return pyPort;
}

const createPyProc = () => {
    let port = '' + selectPort();
    if (deploy_env && (deploy_env == 'DEV' || deploy_env == 'PROD')) {
        let script = path.join(__dirname, 'main.py');
        pyProc = require('child_process').spawn('python', [script]);
        if (pyProc != null) {
          console.log('development child process success');
        }
    }
    else {
        let script = "";
        if (process.platform == 'win32') {
            script = path.join(__dirname, 'engine/windows/main.exe');
        }
        else if (process.platform == 'linux') {
            script = path.join(__dirname, 'engine/linux/main');
        }
        console.log(`Obtained python path script: \n${script}`);
        try {
            pyProc = require('child_process').spawn(script);
        }
        catch (error) {
            console.log(error);
        }
        if (pyProc != null) {
          console.log('production child process success');
        }
    }
}

const exitPyProc = (event) => {
    // console.log(event);
    if (pyProc) { pyProc.kill(); }
    pyProc = null;
    pyPort = null;
}

app.on('ready', createPyProc);
app.on('will-quit', exitPyProc);
app.on('window-all-closed', exitPyProc);
app.on('quit', exitPyProc);
app.on('session-end', exitPyProc);
app.on('shutdown', exitPyProc);
