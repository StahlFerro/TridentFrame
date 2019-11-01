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
    fcount = len(frames)
    max_frames_row = criteria.tiles_per_row
    if fcount > max_frames_row:
        spritesheet_width = tile_width * max_frames_row + criteria.offset_x
        required_rows = math.ceil(fcount/max_frames_row)
        # print('required rows', required_rows)
        spritesheet_height = tile_height * required_rows + criteria.offset_y
    else:
        spritesheet_width = tile_width * fcount
        spritesheet_height = tile_height

    spritesheet = Image.new("RGBA", (int(spritesheet_width), int(spritesheet_height)))
    # spritesheet.save(os.path.join(out_dir,"Ok.png"), "PNG")
    # boxes = []
    yield {"msg": "Placing frames to sheet..."}
    shout_indices = [round(fcount / 10 * mult) for mult in range(0, 10)]
    # yield {"msg": shout_indices}
    # raise Exception(shout_indices)
    for index, fr in enumerate(frames):

        orig_width, orig_height = fr.size
        must_resize = criteria.tile_width != orig_width or criteria.tile_height
        if must_resize:
            fr = fr.resize((round(criteria.resize_width) , round(criteria.resize_height))) != orig_height
        top = tile_height * math.floor(index / max_frames_row) + criteria.offset_y
        left = tile_width * (index % max_frames_row) + criteria.offset_x
        bottom = top + tile_height
        right = left + tile_width

        box = (left, top, right, bottom)
        box = [int(b) for b in box]

        cut_frame = fr.crop((0, 0, tile_width, tile_height))
        spritesheet.paste(cut_frame, box)
        cut_frame.close()
        if index in shout_indices:
            yield {"msg": f'Placing frames to sheet... ({round(index / fcount, 1) * 100}%)'}
        # boxes.append(box)
        fr.close()
    outfilename = f"{filename}.png"
    final_path = os.path.join(out_dir, outfilename)
    yield {"msg": f'Saving the file...'}
    spritesheet.MAX_IMAGE_PIXELS = None
    spritesheet.save(final_path, "PNG")
    yield {"msg": "closing up images..."}
    # if input_mode == 'sequence':
    #     for f in frames:
    #         f.close()
    spritesheet.close()
    yield {"preview_path": final_path}
    yield {"CONTROL": "BSPR_FINISH"}
    # raise Exception('yo')
    