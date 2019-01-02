# ImagoWerkzeuge

A personal collection of various python CLI tools made to assist on GIF splitting, sequential file 
renaming, and perhaps more tools in the future

### Available tools
1. `renamer.py`  
    Renames multiple images with incrementing sequence numbers, in the same folder it's executed.
    
2.  `gifsplitter.py`  
    Splits an animated GIF into a directory of PNG frames.  
    Example:  
    ```
    python3.7 gifsplitter.py sodis.gif
    ```
    The directory will be created in the same folder containing the gif

3.  `gifcomposer.py`  
    Creates an animated GIF out of a directory of PNG frames.  
    Example:  
    ```
    python3.7 gifcomposer.py animation/
    ```
    Where `animation` is the name of the directory containing the image frames. The resulting GIF 
    will have its frames ordered from their names alphabetically.

### Built with
*   [Click](http://click.palletsprojects.com/en/7.x/) : CLI interface
*   [Pillow](https://python-pillow.org/) : Image parsing library
