# ImagoWerkzeuge

A personal collection of various python CLI tools made to assist on GIF splitting, sequential file 
renaming, and perhaps more tools in the future

### Available tools
1. `renamer.py`  
    Name says it all, a simple tool for batch-renaming multiple images into files with incrementing 
    sequence numbers.
2.  `gifsplitter.py`  
    Splits an animated GIF into a directory of PNG frames
3.  `gifcomposer.py`  
    Opposite of gifsplitter, creates an animated GIF out of a directory of PNG frames

### Built with
*   [Click](http://click.palletsprojects.com/en/7.x/) : CLI interface
*   [Pillow](https://python-pillow.org/) : Image parsing library
