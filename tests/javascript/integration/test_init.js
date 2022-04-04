// // const { Application } = require('spectron');
// //! PLAYWRIGHT CURRENTLY NOT WORKING PROPERLY

// const { _electron } = require('playwright');
// const { test } = require('@playwright/test');

// test('launch app', async () => {
//   const electronApp = await _electron.launch({ args: ['main.js'] })
//   // close app
//   await electronApp.close()
// })

import { _electron } from 'playwright';
import { env } from "process";
import assert from 'assert';
import path from 'path';
import { expect } from 'chai';  // Using Expect style
import { should } from 'chai';  // Using Should style
// import { expect } from 'chai';


let _tridentFrame;
let _appPath;
let _windowTitle;


before(async() => {
  _tridentFrame = await _electron.launch({ args: [path.join(__dirname, '../../../main.js')] });
  _appPath = await _tridentFrame.evaluate(({ app }) => {
    // This runs in the main Electron process, parameter here is always
    // the result of the require('electron') in the main app script.
    return app.getAppPath();
  });
  console.log(_appPath);
  // const window = await _tridentFrame.windows();
  // const w = window.map( ww => ww.title)
  // _windowTitle = await window.title();
});

after(async () => {
  await _tridentFrame.close();
});
// let page;
// beforeEach(async() => {
//   page = await _tridentFrame.newPage();
// });
// afterEach(async () => {
//   await _tridentFrame.close();
// });

describe("Application launch", function () {
  it('should initialize windows', async() => {
    const windows = await _tridentFrame.windows();
    // console.log(windows.filter(w => w.title));
    if (env.DEPLOY_ENV == "DEV"){
      assert.equal(windows.length, 2);
    }
    else{
      assert.equal(windows.length, 1);
    }
    // assert.equal(await _tridentFrame.first, 'TridentFrame');
  });
  
  it('should have correct windows based on DEPLOY_ENV', async() => {
    const windows = await _tridentFrame.windows();
    const windows_titles = await Promise.all(windows.map(async (w) => { return await w.title(); }));
    // console.log(windows_titles);
    if (env.DEPLOY_ENV == "DEV"){
      // assert.deepStrictEqual(['TridentFrame', 'DevTools'], windows_titles);
      expect(windows_titles).to.include('TridentFrame');
      expect(windows_titles).to.include('DevTools');
    }
    else{
      expect(windows_titles).to.include('TridentFrame');
      // assert.deepStrictEqual(['TridentFrame'], windows_titles);
    }
    // assert.equal(await _tridentFrame.first, 'TridentFrame');
  });
});

// const { test } = 
// const assert = require('assert');
// const { env, platform, electron } = require("process");
// const electronPath = require('electron');
// // var wtf = require('wtfnode');
// // wtf.dump();

// let appPath;
// if (env.DEPLOY_ENV == "DEV")
//   appPath = electronPath;
// else {
//   if (platform == "win32")
//     appPath = path.join(__dirname, "../../../release/tridentframe/win-unpacked/TridentFrame.exe");
//   else if (platform == "linux")
//     appPath = path.join(__dirname, "../../../release/tridentframe/linux-unpacked/tridentframe");
// }

// // const app = new Application({
// //   path: appPath,
// //   args: [path.join(__dirname, '../../../')],
// //   chromeDriverArgs: ['remote-debugging-port=9222']
// // })

// // (async () => {
// //   const electronApp = await _electron.launch({
// //     args: [path.join(__dirname, '../../../main.js')],
// //   });
  
// //   const appPath = await electronApp.evaluate(async ({ app }) => {
// //     return app.getAppPath();  
// //   });
// //   // console.log(electronApp);
// //   console.log(appPath);
// //   console.log('2');
// //   const window = await electronApp.firstWindow();
// //   console.log(await window.title());
// //   await electronApp.close();
// // })();

// // console.log(path.join(__dirname, '../../../'));
// let electronApp, windows, titles;

// console.log(path.join(__dirname, '../../../'));
// console.log(appPath);

// describe('Application launch', function () {
//   this.timeout(10000);

//   beforeEach(async () => {
//     // return app.start();
//     electronApp = await _electron.launch({
//       args: [path.join(__dirname, '../../../')],
//       // executablePath: appPath,
//     });
//     // windows = electronApp.windows();
//     // titles = windows.filter(async function (page){
//     //   return await page.title() != "DevTools";
//     // }).map(async function (page) {return await page.title();})
//     // let window = await electronApp.firstWindow();
//     // let d = await window.innerHTML();
//     // console.log(d);
//   })

//   afterEach(async () => {
//     electronApp.close();
//   })

//   it('Has the TridentFrame title', async () => {
//     return assert.strictEqual(titles, ['ok']);
//     return assert.strictEqual(title, "TridentFrame");
//   })

//   // // it('shows an initial window', function() {
//   // //     return app.client.getWindowCount().then(function (count) {
//   // //         let windowCount = process.env.DEPLOY_ENV == "DEV"? 2 : 1;
//   // //         assert.strictEqual(count, windowCount);
//   // //     });
//   // // })

//   // it('shows an initial window', async () => {
//   //   let windowCount = env.DEPLOY_ENV == "DEV" ? 2 : 1;
//   //   let actualWindowCount = await app.client.getWindowCount();
//   //   return assert.strictEqual(actualWindowCount, windowCount);
//   // })

//   // it('has the correct title', async () => {
//   //   let title = await app.client.getTitle();
//   //   return assert.strictEqual(title, 'TridentFrame');
//   // })

//   // it('shows dev tool if running with DEV environment', async () => {
//   //   let isDev = env.DEPLOY_ENV == "DEV";
//   //   const isDevToolOpened = await app.client.browserWindow.isDevToolsOpened();
//   //   return assert.strictEqual(isDevToolOpened, isDev);
//   // })

//   // it('has a global right-click popper menu', async () => {
//   //   let rClickMenu = await app.client.$('#generalRClickMenu');
//   //   return assert.strictEqual(await rClickMenu.isExisting(), true);
//   // })

//   // it('on startup must have first panel visible and the others invisible', async () => {
//   //   let childPanels = await app.client.$$('.root-panel > div');
//   //   let panelVisibilities = [];
//   //   let expectedVisibilities = Array.from(Array(childPanels.length), (x, index) => index == 0 ? true : false);
//   //   for (const panel of childPanels) {
//   //     panelVisibilities.push(await panel.isDisplayed());
//   //     // console.log(panelVisibilities);
//   //   }
//   //   return assert.deepStrictEqual(panelVisibilities, expectedVisibilities);
//   // })

//   // it('has the same number of panel buttons as there are panels', async () => {
//   //   let panelButtons = await app.client.$$('ul.menu-list > li.menu-item');
//   //   let childPanels = await app.client.$$('.root-panel > div');
//   //   return assert.strictEqual(panelButtons.length, childPanels.length);
//   // })

//   // it('should switch to corresponding panel based on same id, for every panel button click', async () => {
//   //   let panelButtons = await app.client.$$('ul.menu-list > li.menu-item > a');
//   //   for (const btn of panelButtons) {
//   //     let btnId = await btn.getAttribute('id');
//   //     btn.click();
//   //     let panel = await app.client.$(`.root-panel > div#${btnId}`);
//   //     assert.strictEqual(await panel.isDisplayed(), true);
//   //   }
//   // })
// })
