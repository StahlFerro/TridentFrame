const electron = require('electron');
const protocol = electron.protocol;
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const dialog = electron.dialog;
const ipcMain = electron.ipcMain;
const path = require('path');
const deploy_env = process.env.DEPLOY_ENV;

const SettingsStore = require("./src/store/settingsStore.js");
const PresetsStore = require("./src/store/presetsStore.js");

let SETTINGS;
// let PRESETS;

console.log('DIRNAME', __dirname);
console.log('APP PATH', app.getAppPath());

if (deploy_env && deploy_env == 'DEV') {
	var wtf = require('wtfnode');
	wtf.dump();
}

let mainWindow = null;
let onceReload = 0;

const createWindow = () => {
	console.log('Creating window...');
	mainWindow = new BrowserWindow({
		title: 'TridentFrame',
		width: 1000,
		height: 700,
		minWidth: 1016,
		minHeight: 759,
		center: true,
		// frame: false,
		darkTheme: true,
		fullscreen: false,
		// resizable: false,
		icon: path.join(__dirname, 'src/assets/icons/TridentFrame_logo_256x256.ico'),
		webPreferences: {
			webSecurity: false,
			nodeIntegration: true,
			enableRemoteModule: true,
			contextIsolation: false,
		}
	});
	mainWindow.setMenu(null);
	if (deploy_env && deploy_env == 'DEV') {
		// Development environment
		console.debug('------ DEVELOPMENT VERSION ------');
		mainWindow.loadURL('http://localhost:8705/');
	} else {
		console.debug('------ PRODUCTION VERSION ------');
		// Production environment
		mainWindow.loadURL(
			require('url').format({
				pathname: path.join(__dirname, './dist/index.html'),
				protocol: 'file:',
				slashes: true
			})
		);
	}
	if ((deploy_env && deploy_env == 'DEV') || SETTINGS.startup.open_devtools)
		mainWindow.webContents.openDevTools({
			mode: 'detach'
		});
	mainWindow.focus();
	console.log(JSON.stringify(SETTINGS, null, 4));
	if (SETTINGS.startup.fullscreen) {
		mainWindow.maximize();
	}
	mainWindow.on('closed', () => {
		mainWindow = null;
	});
};

app.on('ready', () => {
	// createPyProc();
	console.log("[Ready] Initialize settings");
	SETTINGS = SettingsStore.initialize();
	PRESETS = PresetsStore.initialize();
	console.log("[Ready] Creating window...");
	createWindow();
	mainWindow.reload();
});

app.on('window-all-closed', () => {
	if (process.platform !== 'darwin') {
		app.quit();
	}
});
app.on('activate', () => {
	if (mainWindow === null) {
		createWindow();
	}
});

app.whenReady().then(() => {
	protocol.registerFileProtocol('file', (request, callback) => {
		const pathname = decodeURIComponent(request.url.replace('file:///', ''));
		callback(pathname);
	});
});

ipcMain.handle('open-dialog', async (event, args) => {
	return dialog.showOpenDialog(mainWindow, args);
});

ipcMain.handle('choose-dir-dialog', async (event, args) => {
	return "";
});

ipcMain.handle('IPC-SHOW-SAVE-DIALOG', async (event, args) => {
	return dialog.showSaveDialog(mainWindow, args);
});

ipcMain.on('get-app-path-sync', function (event, args) {
	event.returnValue = app.getAppPath();
});

ipcMain.on("IPC-SHOW-MESSAGE-BOX-SYNC", function (event, args) {
	event.returnValue = dialog.showMessageBoxSync(args);
})

ipcMain.handle("IPC-SHOW-MESSAGE-BOX", async (event, args) => {
	return dialog.showMessageBox(mainWindow, args);
})

ipcMain.handle('reload-window', async (event, args) => {
	reloadWindow();
});

ipcMain.handle("relaunch-application", async (event, args) => {
	app.relaunch();
	app.exit();
});

function reloadWindow() {
	mainWindow.reload();
	mainWindow.webContents.session.clearCache(() => {});
}

ipcMain.handle('reload-window-once', async (event, args) => {
	if (process.platform == 'linux' && onceReload == 0) {
		onceReload = 1;
		reloadWindow();
	}
});

ipcMain.handle('open-inspector', async (event, args) => {
	mainWindow.webContents.openDevTools({
		mode: 'detach'
	});
	var devtools = mainWindow.devToolsWebContents;
	if (devtools) {
		devtools.focus();
	}
});

// const selectPort = () => {
// 	pyPort = 42069;
// 	return pyPort;
// };

// const createPyProc = () => {
// 	// console.log(deploy_env);
// 	console.log('Starting python engine...');
// 	let port = '' + selectPort();
// 	if (deploy_env && deploy_env == 'DEV') {
// 		let script = path.join(__dirname, 'main.py');
// 		console.log(`Obtained python path script: \n${script}`);
// 		pyProc = require('child_process').spawn('python', [script]);
// 		if (pyProc != null) {
// 			console.log('development child process success');
// 		}
// 	} else {
// 		let script = '';
// 		if (process.platform == 'win32') {
// 			script = path.join(__dirname, 'engine/windows/main.exe');
// 		} else if (process.platform == 'linux') {
// 			script = path.join(__dirname, 'engine/linux/main');
// 		}
// 		console.log(`Obtained python path script: \n${script}`);
// 		try {
// 			pyProc = require('child_process').spawn(script, {
// 				detached: true,
// 				windowsHide: true
// 			});
// 		} catch (error) {
// 			console.log(error);
// 		}
// 		if (pyProc != null) {
// 			console.log('production child process success');
// 		}
// 	}
// };

// const exitPyProc = (event) => {
// 	// console.log(event);
// 	if (pyProc) {
// 		pyProc.kill();
// 	}
// 	pyProc = null;
// 	pyPort = null;
// };

// app.on('will-quit', exitPyProc);
// app.on('window-all-closed', exitPyProc);
// app.on('quit', exitPyProc);
// app.on('session-end', exitPyProc);
// app.on('shutdown', exitPyProc);