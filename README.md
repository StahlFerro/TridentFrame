<div align="center">
  <a href="https://stahlferro.pages.dev/softwares/tridentframe">
    <img width="200" height="200" src="https://stahlferro.pages.dev/logos/TridentFrame_logo.svg">
  </a>
  <h1>TridentFrame</h1>
</div>

The cross-platform desktop swiss-army knife for GIFs, APNGs and spritesheets. Create, split, convert or alter GIFs and animated PNGs as well as quickly making spritesheets, all with easy-to-use-but-powerful-when-needed controls.

TridentFrame consists of two main parts. The python backend handling image processing, and the web frontend (HTML-CSS-JS) for the UI, image previews and input controls.

## Powered by

* [Electron](https://electronjs.org/) : Cross-platform GUI.
* [Vue](https://vuejs.org/) : Frontend framework.
* [Pillow](https://python-pillow.org/) : Image preprocessing and spritesheet handling.
* [ImageMagick](https://imagemagick.org/index.php) : GIF manipulation.
* [Gifsicle](https://www.lcdf.org/gifsicle/) : GIF creation and splitting.
* [pyAPNG](https://github.com/eight04/pyAPNG) : APNG creation & splitting.
* [apngdis](http://apngdis.sourceforge.net/) : APNG disassembler.
* [apngopt](https://sourceforge.net/projects/apng/files/APNG_Optimizer/) : APNG modification.
* [Bulma](https://bulma.io/) : For the clean UI.
* [Sass](https://sass-lang.com/) : Modifying bulma's styles.
* [Font Awesome](https://fontawesome.com/) : Icons.

# Setup for development

## Prerequisites

Make sure to have the following installed:

* Python 3.7 (or above)
* Pipenv (optional)
* Node.js 14 (or above)


## Project setup

* Clone repository:

    ```
    $ git clone https://github.com/StahlFerro/TridentFrame.git
    ```

* [Optional] Setup python virtual environment, install Pipfile dependencies and activate the environment (this example uses pipenv):

    ```
    $ pipenv install --dev
    $ pipenv shell
    ```

* Install node dependencies:

    ```
    $ npm i
    ```

## Running the app in development

Perform each of these commands in separate terminal windows:

1. Start Sass to monitor changes in .scss files:

    ```
    $ npm run css-watch
    ```
  
2. Then start up webpack dev server:

    ```
    $ npm run wpserve
    ```

3. Finally start Electron:

    ```
    $ npm run dev
    ```


## Building the app as distributables

**NOTE**: If using a python virtual environment, make sure to activate it before running these commands.

* Windows:

    ```
    $ npm run release-windows
  ```

* Linux:

    ```
    $ npm run release-linux
    ```
