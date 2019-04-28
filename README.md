# TridentFrame

A python command-line tool made to assist on GIF/APNG splitting/building, sequential file renaming, 
and perhaps more tools in the future.

A graphical UI is currently under development, and will replace it's command line interface once it's finished

### Available subcommands
1.  `rename`  
    Renames multiple images with incrementing sequence numbers, in the same folder it's executed.
    
2.  `split`  
    Splits an animated GIF into a directory of PNG frames.  
    Example:  
    ```
    python3.7 tridentframe.py split sodis.gif
    ```
    The directory will be created in the same folder containing the gif

3.  `compose`  
    Creates an animated GIF out of a directory of PNG frames.  
    Example:  
    ```
    python3.7 tridentframe.py compose animation/
    ```
    Where `animation` is the name of the directory containing the image frames. The resulting GIF 
    will have its frames ordered from their names alphabetically.

### Built with
*   [Click](http://click.palletsprojects.com/en/7.x/) : CLI interface
*   [Pillow](https://python-pillow.org/) : Image parsing library
*   [pyAPNG](https://github.com/eight04/pyAPNG) : APNG parsing

Note: `npm rebuild zeromq --runtime=electron --target=1.8.8`