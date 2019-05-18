# TridentFrame

The cross-platform desktop swiss-army knife for GIFs and APNGs. Create, split, convert or alter GIFs and animated PNGs with easy-to-use-but-powerful-when-needed controls.

```
⚠️ WARNING ⚠️
The app is currently under rigorous daily development and is incomplete. Clone it at your own risk. All feedbacks are appreciated
```

TridentFrame consists of two main parts. The python backend handling image processing, and the web frontend (HTML-CSS-JS) for the UI, image previews and input controls.

### Built with
*   [Electron](https://electronjs.org/) : Main framework
*   [Pillow](https://python-pillow.org/) : GIF parsing
*   [pyAPNG](https://github.com/eight04/pyAPNG) : APNG parsing
*   [zeroRPC](https://www.zerorpc.io/) : Connecting the python backend to the electron frontend
*   [Bulma](https://bulma.io/) : For the pretty and clean UI
*   [Sass](https://sass-lang.com/) : Modifying bulma's styles
*   [Font Awesome](https://fontawesome.com/) : Icons

Devnotes: 

ZeroMQ fix: `npm rebuild zeromq --runtime=electron --target=1.8.8`
