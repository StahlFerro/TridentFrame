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
from colorama import init, deinit
from hurry.filesize import size, alternative

from .config import IMG_EXTS, ANIMATED_IMG_EXTS, STATIC_IMG_EXTS, CreationCriteria, SplitCriteria, SpritesheetBuildCriteria, SpritesheetSliceCriteria


def _build_gif(image_paths: List, out_full_path: str, criteria: CreationCriteria):
    frames = []
    disposal = 0
    if criteria.reverse:
        image_paths.reverse()
    for ipath in image_paths:
        im = Image.open(ipath)
        orig_width, orig_height = im.size
        must_resize = criteria.resize_width != orig_width or criteria.resize_height != orig_height
        alpha = None
        if criteria.flip_h:
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        if criteria.flip_v:
            im = im.transpose(Image.FLIP_TOP_BOTTOM)
        if must_resize:
            im = im.resize((round(criteria.resize_width) , round(criteria.resize_height)))
        try: 
            alpha = im.getchannel('A')
        except Exception:
            alpha = False
        if criteria.transparent and alpha:
            disposal = 2
            # alpha.show(title='alpha')
            im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
            # im.show('im first convert')
            mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
            # mask.show('mask')
            im.paste(255, mask)
            # im.show('masked im')
            im.info['transparency'] = 255
        else:
            im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=256)
        frames.append(im)
    frames[0].save(out_full_path, optimize=False,
        save_all=True, append_images=frames[1:], duration=criteria.duration, loop=0, disposal=disposal)


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
    abs_image_paths = [os.path.abspath(ip) for ip in image_paths if os.path.exists(ip)]
    img_paths = [f for f in abs_image_paths if str.lower(os.path.splitext(f)[1][1:]) in STATIC_IMG_EXTS]
    # workpath = os.path.dirname(img_paths[0])
    init()
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
        _build_gif(image_paths, out_full_path, criteria)
        
    elif criteria.extension == 'apng':
        out_full_path = os.path.join(out_dir, f"{filename}.png")
        apng = _build_apng(img_paths, criteria)
        apng.save(out_full_path)

    deinit()
    return out_full_path


def split_aimg(image_path: str, out_dir: str, criteria: SplitCriteria):
    abspath = os.path.abspath(image_path)
    init()
    if not os.path.isfile(image_path):
        raise Exception("Oi skrubman the path here seems to be a bloody directory, should've been a file")
    filename = str(os.path.basename(abspath))
    workpath = os.path.dirname(abspath)

    if os.getcwd() != workpath:
        os.chdir(workpath)

    # Custom output dirname and frame names if specified on the cli
    if '.' not in filename:
        raise Exception('Where the fuk is the extension mate?!')

    fname, ext = os.path.splitext(filename)
    ext = str.lower(ext[1:])
    # raise Exception(fname, ext)
    if ext not in ANIMATED_IMG_EXTS:
        return
        # raise ClickException('Only supported extensions are gif and apng. Sry lad')

    # Create directory to contain all the frames if does not exist
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
        print(f"Creating directory {out_dir}...")
    else:
        print(f"Directory {out_dir} already exists, replacing the PNGs inside it...")

    # Image processing
    if ext == 'gif':
        try:
            gif: Image = Image.open(filename)
        except Exception:
            raise Exception(filename, "M8 I don't even think this file is even an image file in the first place")

        if gif.format != 'GIF' or not gif.is_animated:
            raise Exception(filename, "Sorry m9, the image you specified is not a valid animated GIF")

        # click.secho(f"{filename} ({gif.n_frames} frames). Splitting GIF...", fg='cyan')
        pad_count = max(len(str(gif.n_frames)), 3)
        frame_nums = list(range(0, gif.n_frames))

        # with click.progressbar(frame_nums, empty_char=" ", fill_char="█", show_percent=True, show_pos=True) as frames:
        pad_count: int = 3 if (not criteria.pad_count or criteria.pad_count <= 0) else criteria.pad_count
        durations = []
        for f in frame_nums:
            gif.seek(f)
            durations.append(gif.info['duration'])
        min_duration = min(durations)
        if criteria.is_duration_sensitive:
            multipliers = [dur//min_duration for dur in durations]
        else:
            multipliers = [1 for dur in durations]
        frame_multipliers = list(zip(frame_nums, multipliers))
        seq_no = 0
        for index, multiplier in frame_multipliers:
            gif.seek(index)
            for n in range(0, multiplier):
                gif.save(os.path.join(out_dir, f"{fname}_{str.zfill(str(seq_no), pad_count)}.png"), 'PNG')
                seq_no += 1

    elif ext == 'png':
        img: APNG = APNG.open(filename)
        iframes = img.frames
        pad_count = max(len(str(len(iframes))), 3)
        # print('frames', [(png, control.__dict__) for (png, control) in img.frames][0])
        # with click.progressbar(iframes, empty_char=" ", fill_char="█", show_percent=True, show_pos=True) as frames:
        for index, (png, control) in enumerate(iframes):
            png.save(os.path.join(out_dir, f"{fname}_{str.zfill(str(index), pad_count)}.png"))

    deinit()
    return True


# if __name__ == "__main__":
#     pprint(_inspect_sequence(""))

def _delete_temp_images():
    # raise Exception(os.getcwd())
    temp_dir = os.path.abspath('temp')
    # raise Exception(os.getcwd(), temp_dir)
    # raise Exception(image_name, path)
    # os.remove(path)
    temp_aimgs = [os.path.join(temp_dir, i) for i in os.listdir(temp_dir)]
    for ta in temp_aimgs:
        os.remove(ta)
    return True
