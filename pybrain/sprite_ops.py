import os
import io
import string
import shutil
import math
from random import choices
from pprint import pprint
from urllib.parse import urlparse
from typing import List

from PIL import Image
from apng import APNG, PNG
from hurry.filesize import size, alternative

from .config import IMG_EXTS, ANIMATED_IMG_EXTS, STATIC_IMG_EXTS
from .criterion import SpritesheetBuildCriteria, SpritesheetSliceCriteria


def _build_spritesheet(image_paths: List, out_dir: str, filename: str, criteria: SpritesheetBuildCriteria):
    abs_image_paths = [os.path.abspath(ip) for ip in image_paths if os.path.exists(ip)]
    img_paths = [f for f in abs_image_paths if str.lower(os.path.splitext(f)[1][1:]) in set(STATIC_IMG_EXTS + ANIMATED_IMG_EXTS)]
    # workpath = os.path.dirname(img_paths[0])
    # Test if inputted filename has extension, then remove it from the filename
    fname, ext = os.path.splitext(filename)
    if ext:
        filename = fname
    if not out_dir:
        raise Exception("No output folder selected, please select it first")
    out_dir = os.path.abspath(out_dir)
    if not os.path.exists(out_dir):
        raise Exception("The specified absolute out_dir does not exist!")
    input_mode = criteria.input_format
    frames = []
    if input_mode == 'sequence':
        frames = [Image.open(i) for i in img_paths]
    elif input_mode == 'aimg':
        aimg = img_paths[0]
        ext = os.path.splitext(aimg)[1][1:]
        if ext.lower() == 'gif':
            gif: Image = Image.open(aimg)
            for cr in range(0, gif.n_frames):
                gif.seek(cr)
                bytebox = io.BytesIO()
                gif.save(bytebox, "PNG", optimize=True)
                frames.append(Image.open(bytebox))
                yield {"msg": f'Splitting GIF... ({cr + 1}/{gif.n_frames})'}
        elif ext.lower() == 'png':
            raise Exception('APNG!')
        else:
            raise Exception('Unknown image format!')
    else:
        raise Exception('Unknown input image mode!')

    tile_width = frames[0].size[0]
    tile_height = frames[0].size[1]

    max_frames_row = criteria.tiles_per_row
    if len(frames) > max_frames_row:
        spritesheet_width = tile_width * max_frames_row
        required_rows = math.ceil(len(frames)/max_frames_row)
        print('required rows', required_rows)
        spritesheet_height = tile_height * required_rows
    else:
        spritesheet_width = tile_width * len(frames)
        spritesheet_height = tile_height

    spritesheet = Image.new("RGBA", (int(spritesheet_width), int(spritesheet_height)))
    # spritesheet.save(os.path.join(out_dir,"Ok.png"), "PNG")
    boxes = []
    for index, fr in enumerate(frames):
        top = tile_height * math.floor(index / max_frames_row)
        left = tile_width * (index % max_frames_row)
        bottom = top + tile_height
        right = left + tile_width

        box = (left, top, right, bottom)
        box = [int(b) for b in box]

        cut_frame = fr.crop((0, 0, tile_width, tile_height))
        spritesheet.paste(cut_frame, box)
        yield {"msg": f'Placing frames to sheet... ({index + 1}/{len(frames)})'}
        boxes.append(box)
    outfilename = f"{filename}.png"
    final_path = os.path.join(out_dir, outfilename)
    yield {"msg": f'Saving the file...'}
    spritesheet.save(final_path, "PNG")
    yield {"preview_path": final_path}
    if input_mode == 'sequence':
        for f in frames:
            f.close()
            # yield {"msg": f"{f} closed!"}
    yield {"msg": 'Finished!'}
    # raise Exception(boxes)
    