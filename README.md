# TridentFrame

The cross-platform desktop swiss-army knife for GIFs, APNGs and spritesheets. Create, split, convert or alter GIFs and animated PNGs as well as quickly making spritesheets, all with easy-to-use-but-powerful-when-needed controls.

```
⚠️ WARNING ⚠️
The app is currently under rigorous daily development and is incomplete. Clone it at your own risk. All feedbacks are appreciated!
```

TridentFrame consists of two main parts. The python backend handling image processing, and the web frontend (HTML-CSS-JS) for the UI, image previews and input controls.

### Powered by:
*   [Electron](https://electronjs.org/) : Cross-platform GUI
*   [Pillow](https://python-pillow.org/) : Image preprocessing
*   [Gifsicle](https://www.lcdf.org/gifsicle/) : GIF creation and splitting
*   [pyAPNG](https://github.com/eight04/pyAPNG) : APNG creation & splitting
*   [zeroRPC](https://www.zerorpc.io/) : Connecting the python backend to the electron frontend
*   [Bulma](https://bulma.io/) : For the pretty and clean UI
*   [Sass](https://sass-lang.com/) : Modifying bulma's styles
*   [Font Awesome](https://fontawesome.com/) : Icons

Devnotes: 

ZeroMQ fix: `npm rebuild zeromq --runtime=electron --target=1.8.8`
