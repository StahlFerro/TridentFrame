import json
import platform
import hashlib
import os
from pathlib import Path
from typing import List, Tuple
from PIL import Image


__FILE__PATH__ = Path(__file__).resolve()

PROJECT_DIR = __FILE__PATH__.parents[2]
SOURCE_IMG = PROJECT_DIR.joinpath("src/assets/imgs/TridentFrame_logo_512x512.png")
TARGET_ICONS_DIR = PROJECT_DIR.joinpath("build/icons")

if not TARGET_ICONS_DIR.exists():
    os.makedirs(TARGET_ICONS_DIR)
    
FORMAT_SIZES = {
    "png": {
        "variants": [16, 32, 48, 64, 96, 128, 192, 256, 512, 720],
        "default": 256
    },
    "ico": {
        "default": 256
    },
    "icns": {
        "default": 256
    }
}

DEFAULT_ICON_PNG_SIZE = 256

im = Image.open(SOURCE_IMG)


def resize_and_save_image(im: Image.Image, name: str, width, height, format: str):
    new_im = im.resize((width, height), resample=Image.BICUBIC)
    filename = f'{name}.{fmt}'
    save_path = TARGET_ICONS_DIR.joinpath(filename)
    new_im.save(save_path, format=fmt.upper())
    

for fmt, size_info in FORMAT_SIZES.items():
    sizes = size_info.get("variants")
    if sizes:
        for size in sizes:
            resize_and_save_image(im, f"{size}x{size}", size, size, fmt)
            # new_im = im.resize((size, size), resample=Image.BICUBIC)
            # filename = f'{size}x{size}.{fmt}'
            # save_path = TARGET_ICONS_DIR.joinpath(filename)
            # new_im.save(save_path, format=fmt.upper())
            
    def_size = size_info["default"]
    resize_and_save_image(im, "icon", size, size, fmt)
    # new_im = im.resize((def_size, def_size), resample=Image.BICUBIC)
    # fname = f'icon.{fmt}'
    # save_path = TARGET_ICONS_DIR.joinpath(fname)
    # new_im.save(save_path, format=fmt.upper())
    