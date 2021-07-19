const { Applcation, Application } = require('spectron');
const assert = require('assert');
const { env, platform } = require("process");
const electronPath = require('electron');
const path = require('path');
var wtf = require('wtfnode');
wtf.dump();

let appPath;
if (env.DEPLOY_ENV == "DEV")
    appPath = electronPath;
else {
    if (platform == "win32")
        appPath = path.join(__dirname,"../../../release/tridentframe/win-unpacked/TridentFrame.exe");
    else if (platform == "linux")
        appPath = path.join(__dirname,"../../../release/tridentframe/linux-unpacked/tridentframe");
}


const app = new Application({
    path: appPath,
    args: [path.join(__dirname, '../../../')],
    chromeDriverArgs: ['remote-debugging-port=9222']
})
console.log(electronPath);
console.log(path.join(__dirname, '../../../'));

describe('Application launch', function() {
    this.timeout(10000);

    beforeEach(function() {
        return app.start();
    })

    afterEach(function() {
        if (app && app.isRunning()) {
            app.stop();
        }
    })
    
    // it('shows an initial window', function() {
    //     return app.client.getWindowCount().then(function (count) {
    //         let windowCount = process.env.DEPLOY_ENV == "DEV"? 2 : 1;
    //         assert.strictEqual(count, windowCount);
    //     });
    // })

    it('shows an initial window', async () => {
        let windowCount = env.DEPLOY_ENV == "DEV"? 2 : 1;
        let actualWindowCount = await app.client.getWindowCount();
        return assert.strictEqual(actualWindowCount, windowCount);
    })

    it('has the correct title', async () => {
        let title = await app.client.getTitle();
        return assert.strictEqual(title, 'TridentFrame');
    })

    it('shows dev tool if running with DEV environment', async () => {
        let isDev = env.DEPLOY_ENV == "DEV";
        const isDevToolOpened = await app.client.browserWindow.isDevToolsOpened();
        return assert.strictEqual(isDevToolOpened, isDev);
    })

    it('has a global right-click popper menu', async () => {
        let rClickMenu = await app.client.$('#generalRClickMenu');
        return assert.strictEqual(await rClickMenu.isExisting(), true);
    })

    it('on startup must have first panel visible and the others invisible', async () => {
        let childPanels = await app.client.$$('.root-panel > div');
        let panelVisibilities = [];
        let expectedVisibilities = Array.from(Array(childPanels.length), (x, index) => index == 0? true : false);
        for (const panel of childPanels) {
            panelVisibilities.push(await panel.isDisplayed());
            // console.log(panelVisibilities);
        }
        return assert.deepStrictEqual(panelVisibilities, expectedVisibilities);
    })

    it('has the same number of panel buttons as there are panels', async () => {
        let panelButtons = await app.client.$$('ul.menu-list > li.menu-item');
        let childPanels = await app.client.$$('.root-panel > div');
        return assert.strictEqual(panelButtons.length, childPanels.length);
    })

    it('should switch to corresponding panel based on same id, for every panel button click', async () => {
        let panelButtons = await app.client.$$('ul.menu-list > li.menu-item > a');
        for (const btn of panelButtons) {
            let btnId = await btn.getAttribute('id');
            btn.click();
            let panel = await app.client.$(`.root-panel > div#${btnId}`);
            assert.strictEqual(await panel.isDisplayed(), true);
        }
    })


})
