import json
import platform
import hashlib
from pathlib import Path
from typing import List
from PIL import Image


__FILE__PATH__ = Path(__file__).resolve()

PROJECT_DIR = __FILE__PATH__.parents[2]
SOURCE_IMG = PROJECT_DIR.joinpath("src/assets/imgs/TridentFrame_logo_512x512.png")
TARGET_ICONS_DIR = PROJECT_DIR.joinpath("build/icons")
FORMAT_SIZES = {
    "png": [16, 32, 48, 64, 96, 128, 192, 256, 512, 720],
    "ico": [256],
    "icns": [256]
}

im = Image.open(SOURCE_IMG)

for fmt, sizes in FORMAT_SIZES.items():
    for size in sizes:
        new_im = im.resize((size, size), resample=Image.BICUBIC)
        fname = f'{size}x{size}.{fmt}'
        save_path = TARGET_ICONS_DIR.joinpath(fname)
        new_im.save(save_path, format=fmt.upper())