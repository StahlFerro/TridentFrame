import os
import string
import shutil
from random import choices
from pprint import pprint
from urllib.parse import urlparse
from typing import List

from PIL import Image
from apng import APNG
from colorama import init, deinit
from hurry.filesize import size, alternative

from .config import IMG_EXTS, ANIMATED_IMG_EXTS, STATIC_IMG_EXTS


def gify_images(images: List, transparent: bool=False):
    new_images = []
    for im in images:
        alpha = None
        try: 
            alpha = im.getchannel('A')
        except Exception as e:
            alpha = False
        if transparent and alpha:
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
        new_images.append(im)
    return new_images


def _combine_image(image_paths: List[str], out_dir: str, filename: str, fps: float, extension: str, reverse: bool, transparent: bool):
    abs_image_paths = [os.path.abspath(ip) for ip in image_paths if os.path.exists(ip)]
    img_paths = [f for f in abs_image_paths if str.lower(os.path.splitext(f)[1][1:]) in STATIC_IMG_EXTS]
    # workpath = os.path.dirname(img_paths[0])
    init()
    if not filename:
        raise Exception("Set the filename first!")
    # Test if inputted filename has extension, then remove it from the filename
    fname, ext = os.path.splitext(filename)
    if ext:
        filename = fname
    if not out_dir:
        raise Exception("No output folder selected, please select it first")

    out_dir = os.path.abspath(out_dir)
    if not os.path.exists(out_dir):
        raise Exception("The specified absolute out_dir does not exist!")

    duration = round(1000 / fps)
    if reverse:
        img_paths.reverse()
    if extension == 'gif':
        out_full_path = os.path.join(out_dir, f"{filename}.gif")
        frames = [Image.open(i) for i in img_paths]
        # if scale != 1.0:
            # frames = [f.resize((round(f.width * scale), round(f.height * scale))) for f in frames]
        # pprint(frames[0].filename)
        filename = f"{filename}.gif"
        disposal = 0
        frames = gify_images(frames, transparent=transparent)
        if transparent:
            disposal = 2
        frames[0].save(out_full_path, optimize=False,
                       save_all=True, append_images=frames[1:], duration=duration, loop=0, disposal=disposal)

    elif extension == 'apng':
        out_full_path = os.path.join(out_dir, f"{filename}.png")
        APNG.from_files(img_paths, delay=duration).save(out_full_path)

    deinit()
    return out_full_path


def _split_image(image_path: str, out_path: str):
    if not image_path and not out_path:
        raise Exception("Please load a GIF or APNG and choose the output folder!")
    elif not image_path:
        raise Exception("Please load a GIF or APNG!")
    elif not out_path:
        raise Exception("Please choose an output folder!")

    upath = urlparse(image_path)
    abspath = os.path.abspath(upath.path)
    init()
    if not os.path.isfile(abspath):
        raise Exception(abspath, upath.path, "Oi skrubman the path here seems to be a bloody directory, should've been a file")
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
    if not os.path.exists(out_path):
        os.mkdir(out_path)
        print(f"Creating directory {out_path}...")
    else:
        print(f"Directory {out_path} already exists, replacing the PNGs inside it...")

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
        for f in frame_nums:
            gif.seek(f)
            gif.save(os.path.join(out_path, f"{fname}_{str.zfill(str(f), pad_count)}.png"), 'PNG')

    elif ext == 'png':
        img: APNG = APNG.open(filename)
        iframes = img.frames
        pad_count = max(len(str(len(iframes))), 3)
        # print('frames', [(png, control.__dict__) for (png, control) in img.frames][0])
        # with click.progressbar(iframes, empty_char=" ", fill_char="█", show_percent=True, show_pos=True) as frames:
        for i, (png, control) in enumerate(iframes):
            png.save(os.path.join(out_path, f"{fname}_{str.zfill(str(i), pad_count)}.png"))

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
