import os
import string
from random import choices
from pprint import pprint
from urllib.parse import urlparse

from PIL import Image
from apng import APNG
from colorama import init, deinit
from hurry.filesize import size, alternative

from .config import IMG_EXTS, STATIC_IMG_EXTS, ANIMATED_IMG_EXTS


def _inspect_image(image_path):
    filename = str(os.path.basename(image_path))
    abspath = os.path.abspath(image_path)
    workpath = os.path.dirname(abspath)
    ext = str.lower(os.path.splitext(filename)[1])

    if os.getcwd() != workpath:
        os.chdir(workpath)

    frame_count = 0
    fps = 0
    duration = 0
    fsize = size(os.stat(filename).st_size, system=alternative)
    # fsize = 0
    width = height = 0
    loop_duration = 0
    extension = ''

    if ext == '.gif':
        try:
            gif: Image = Image.open(filename)
        except Exception:
            return
        if gif.format != 'GIF' or not gif.is_animated:
            raise Exception(f"The chosen GIF ({filename}) is not an animated GIF!")
        width, height = gif.size
        frame_count = gif.n_frames
        # pprint(gif.info)
        durations = []
        for f in range(0, gif.n_frames):
            gif.seek(f)
            durations.append(gif.info['duration'])
        duration = sum(durations) / len(durations)
        fps = 1000.0 / duration
        loop_duration = frame_count / fps
        extension = 'GIF'

    elif ext == '.png':
        try:
            apng: APNG = APNG.open(filename)
        except Exception:
            pass
        frames = apng.frames
        frame_count = len(frames)
        if frame_count <= 1:
            raise Exception(f"The chosen PNG ({filename}) is not an APNG!")
        png_one, controller_one = frames[0]
        # pprint(png_one.__dict__)
        # pprint(controller_one.__dict__)
        extension = 'APNG'
        width = png_one.width
        height = png_one.height
        duration = controller_one.delay
        fps = 1000.0 / duration
        loop_duration = frame_count / fps

    image_info = {
        "name": filename,
        "fps": fps,
        "duration": duration,
        "fsize": fsize,
        "extension": extension,
        "frame_count": frame_count,
        "absolute_url": abspath,
        "width": width,
        "height": height,
        "loop_duration": loop_duration,
    }
    return image_info


def _inspect_sequence(dir_path):
    abspath = os.path.abspath(dir_path)

    print("absolute sequence path", abspath)
    if os.getcwd() != abspath:
        os.chdir(abspath)

    print(os.listdir("."))
    imgs = [f for f in os.listdir('.') if '.' in f and str.lower(f.split('.')[-1]) in STATIC_IMG_EXTS]
    if not imgs:
        raise Exception("Directory does not contain any PNG/JPG images!")
    first_img = imgs[0].split('.')[0]
    filename = first_img.split('_')[0] if '_' in first_img else first_img.split('.')[0]

    sequence_info = {
        "name": filename,
        "total": len(imgs),
    }
    return sequence_info


if __name__ == "__main__":
    pprint(_inspect_sequence("../test"))

