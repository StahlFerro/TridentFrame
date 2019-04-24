import os
import string
from random import choices
from pprint import pprint

from PIL import Image
from apng import APNG
from colorama import init, deinit


def _inspect_image(file_path):
    file = str(os.path.basename(file_path))
    abspath = os.path.abspath(file_path)
    workpath = os.path.dirname(abspath)
    ext = str.lower(os.path.splitext(file)[1])

    if os.getcwd() != workpath:
        os.chdir(workpath)

    frame_count = 0
    fps = 0
    duration = 0
    size = os.stat(file).st_size
    width = height = 0
    loop_duration = 0

    if ext == '.gif':
        try:
            gif: Image = Image.open(file)
        except Exception:
            return
        width, height = gif.size
        #     raise FileError(file, "M8 I don't even think this file is even an image file in the first place")
        #
        # if gif.format != 'GIF' or not gif.is_animated:
        #     raise FileError(file, "Sorry m9, the image you specified is not a valid animated GIF")
        frame_count = gif.n_frames
        pprint(gif.info)
        durations = []
        for f in range(0, gif.n_frames):
            gif.seek(f)
            durations.append(gif.info['duration'])
        duration = sum(durations) / len(durations)
        fps = 1000.0 / duration
        loop_duration = frame_count / fps

    image_info = {
        "name": file,
        "fps": fps,
        "duration": duration,
        "size": size,
        "extension": ext,
        "frame_count": frame_count,
        "absolute_url": abspath,
        "width": width,
        "height": height,
        "loop_duration": loop_duration,
    }
    return image_info