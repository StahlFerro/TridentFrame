import os
import io
import string
import shutil
import math
import time
import subprocess
import tempfile
from random import choices
from pprint import pprint
from urllib.parse import urlparse
from typing import List, Dict, Tuple
from datetime import datetime

from PIL import Image
from apng import APNG, PNG
from hurry.filesize import size, alternative

from .config import IMG_EXTS, ANIMATED_IMG_EXTS, STATIC_IMG_EXTS, CreationCriteria, SplitCriteria, SpritesheetBuildCriteria, SpritesheetSliceCriteria, ABS_CACHE_PATH, gifsicle_exec
from .utility import _mk_temp_dir


def _create_gifragments(image_paths: List, out_path: str, criteria: CreationCriteria, absolute_paths=True) -> Tuple[str, List[str]]:
    """ Generate a sequence of GIFs created from the input sequence with the specified criteria, before compiling them into a single animated GIF"""
    disposal = 0
    if criteria.reverse:
        image_paths.reverse()
    temp_gifs = []
    for index, ipath in enumerate(image_paths):
        yield f"Processing frames ({index}/{len(image_paths)})..."
        with Image.open(ipath) as im:
            orig_width, orig_height = im.size
            must_resize = criteria.resize_width != orig_width or criteria.resize_height != orig_height
            alpha = None
            if criteria.flip_h:
                im = im.transpose(Image.FLIP_LEFT_RIGHT)
            if criteria.flip_v:
                im = im.transpose(Image.FLIP_TOP_BOTTOM)
            if must_resize:
                im = im.resize((round(criteria.resize_width) , round(criteria.resize_height)))
            fragment_name = os.path.splitext(os.path.basename(ipath))[0]
            save_path = f'{os.path.join(out_path, fragment_name)}.gif'
            if im.mode == 'RGBA' and criteria.transparent:
                alpha = im.getchannel('A')
                # alpha.show(title='alpha')
                im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
                # im.show('im first convert')
                mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
                # mask.show('mask')
                im.paste(255, mask)
                # im.show('masked im')
                im.info['transparency'] = 255
                im.save(save_path)
            elif im.mode == 'RGB' or not criteria.transparent:
                im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE)
                im.save(save_path)
            elif im.mode == 'P':
                im.save(save_path, transparency=im.info['transparency'])
            if absolute_paths:
                temp_gifs.append(save_path)
            else:
                temp_gifs.append(os.path.relpath(save_path, os.getcwd()))


def _build_gif(image_paths: List, out_full_path: str, criteria: CreationCriteria):
    gifragment_dir = _mk_temp_dir(prefix_name="tmp_gifrags")
    yield from _create_gifragments(image_paths, gifragment_dir, criteria, absolute_paths=False)
    executable = gifsicle_exec()
    colors = 256
    delay = 2
    optimization = "--unoptimize"
    disposal = "background"
    loopcount = "--loopcount"
    globstar_path = os.path.join(gifragment_dir, "*.gif")
    args = [executable, f"--colors={colors}", optimization, f"--delay={delay}", f"--disposal={disposal}", loopcount, globstar_path, "--output", out_full_path]
    # pprint(args)
    cmd = ' '.join(args)
    # print(cmd) 
    yield "Combining frames..."
    subprocess.run(cmd, shell=True)
    shutil.rmtree(gifragment_dir)
    yield "Finished!"


def _build_apng(image_paths, criteria: CreationCriteria) -> APNG:
    if criteria.reverse:
        image_paths.reverse()
    apng = APNG()
    first_width, first_height = Image.open(image_paths[0]).size
    first_must_resize = criteria.resize_width != first_width or criteria.resize_height != first_height
    if criteria.flip_h or criteria.flip_v or first_must_resize:
        for ipath in image_paths:
            # bytebox = io.BytesIO()
            with io.BytesIO() as bytebox:
                im = Image.open(ipath)
                orig_width, orig_height = im.size
                must_resize = criteria.resize_width != orig_width or criteria.resize_height != orig_height
                if must_resize:
                    im = im.resize((round(criteria.resize_width), round(criteria.resize_height)))
                if criteria.flip_h:
                    im = im.transpose(Image.FLIP_LEFT_RIGHT)
                if criteria.flip_v:
                    im = im.transpose(Image.FLIP_TOP_BOTTOM)
                im.save(bytebox, "PNG", optimize=True)
                apng.append(PNG.from_bytes(bytebox.getvalue()), delay=criteria.duration)
        return apng
    else:
        return APNG.from_files(image_paths, delay=criteria.duration)


def create_aimg(image_paths: List[str], out_dir: str, filename: str, criteria: CreationCriteria):
    """ Umbrella function for creating animated images from a sequence of images """
    abs_image_paths = [os.path.abspath(ip) for ip in image_paths if os.path.exists(ip)]
    img_paths = [f for f in abs_image_paths if str.lower(os.path.splitext(f)[1][1:]) in STATIC_IMG_EXTS]
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

    if criteria.extension == 'gif':
        out_full_path = os.path.join(out_dir, f"{filename}.gif")
        filename = f"{filename}.gif"
        return _build_gif(image_paths, out_full_path, criteria)
    
    elif criteria.extension == 'apng':
        out_full_path = os.path.join(out_dir, f"{filename}.png")
        apng = _build_apng(img_paths, criteria)
        return apng.save(out_full_path)

    return out_dir
