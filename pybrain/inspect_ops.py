import os
import string
import math
from random import choices
from pprint import pprint
from typing import List, Dict
from urllib.parse import urlparse

from PIL import Image, ExifTags, ImageFile
from apng import APNG
from hurry.filesize import size, alternative

from .config import IMG_EXTS, STATIC_IMG_EXTS, ANIMATED_IMG_EXTS
from .utility import _filter_images, read_filesize


def inspect_general(image_path, filter_on="", skip=False) -> Dict:
    """ Main single image inspection handler function.
    :param `image_path`: Input path.
    :param `filter_on`: "" no filter, "static": "Throws error on detecting an animated image", "animated": "Throws error on detecting a static image"
    :param `skip`: Returns an empty dict instead of throwing an error. Used in conjuntion with fitler_on
    """
    abspath = os.path.abspath(image_path)
    filename = str(os.path.basename(abspath))
    base_fname, ext = os.path.splitext(filename)
    ext = ext.lower()
    if ext == '.gif':
        try:
            gif: Image = Image.open(abspath)
        except Exception:
            raise Exception(f'The chosen file ({filename}) is not a valid GIF image')
            
        # raise Exception(gif.is_animated, filter_on, skip)
        if gif.format == 'GIF':
            if gif.is_animated:
                if filter_on == "static":
                    if skip:
                        return {}
                    else:
                        raise Exception(f"The GIF {base_fname} is not static!")
                else:
                    return _inspect_agif(image_path, gif)
            else:
                if filter_on == "animated":
                    if skip:
                        return {}
                    else:
                        raise Exception(f"The GIF {base_fname} is not animated!")
                else:
                    return _inspect_simg(image_path)
    elif ext == '.png':
        try:
            apng: APNG = APNG.open(abspath)
        except Exception:
            raise Exception(f'The chosen file ({filename}) is not a valid PNG image')
        frames = apng.frames
        frame_count = len(frames)
        if frame_count > 1:
            if filter_on == "static":
                if skip:
                    return {}
                else:
                    raise Exception(f"The APNG ({filename}) is not static!")
            else:
                return _inspect_apng(image_path, apng)
        else:
            if filter_on == "animated":
                if skip:
                    return {}
                else:
                    raise Exception(f"The PNG {base_fname} is not animated!")
            else:
                return _inspect_simg(image_path)
    else:
        return _inspect_simg(image_path)


def _inspect_simg(image):
    """ Returns general and EXIF info from a static image. Static GIFs will not display EXIF (they don't support it)

    Keyword arguments:
    image -- Path or Pillow Image
    """
    img_metadata = {}
    if image.__class__.__bases__[0] is ImageFile.ImageFile:
        im = image
    else:
        im = Image.open(image)
    fmt = im.format
    exif = "-"
    if fmt.upper() != "GIF":
        exif_raw = im._getexif()
        if exif_raw:
            exif = {
                ExifTags.TAGS[k]: v
                for k, v in exif_raw.items()
                if k in ExifTags.TAGS
            }
    width, height = im.size
    path = im.filename
    fsize = read_filesize(os.stat(path).st_size)
    color_mode = im.mode
    transparency = im.info.get('transparency', "No")
    # alpha = im.getchannel('A')
    comment = im.info.get('comment')
    # fsize = size(os.stat(path).st_size, system=alternative)
    img_metadata = {
        "general_info": {
            "name": {"value": os.path.basename(path), "label": "Name"},
            "width": {"value": width, "label": "Width"},
            "height": {"value": height, "label": "Height"},
            "fsize": {"value": fsize, "label": "File size"},
            "absolute_url": {"value": path, "label": "Path"},
            "format": {"value": fmt, "label": "Format"},
            "comments": {"value": comment, "label": "Comments"},
            "color_mode": {"value": color_mode, "label": "Color Mode"},
            "transparency": {"value": transparency, "label": "Has Transparency"},
            # "alpha": {"value": alpha, "label": "Has Alpha"},
            "exif": {"value": exif, "label": "EXIF"},
        }
    }
    im.close()
    return img_metadata


def _inspect_agif(abspath: str, gif: Image):
    filename = str(os.path.basename(abspath))
    base_fname, ext = os.path.splitext(filename)
    width, height = gif.size
    frame_count = gif.n_frames
    fsize = read_filesize(os.stat(abspath).st_size)
    durations = []
    comments = []
    for f in range(0, gif.n_frames):
        gif.seek(f)
        durations.append(gif.info['duration'])
        comments.append(gif.info.get('comment', ""))
    min_duration = min(durations)
    if min_duration == 0:
        frame_count_ds = frame_count
    else:
        frame_count_ds = sum([dur//min_duration for dur in durations])
    # raise Exception(delays)
    delay_is_uneven = len(set(durations)) > 1
    avg_delay = sum(durations) / len(durations) if sum(durations) != 0 else 0
    fps = round(1000.0 / avg_delay, 3) if avg_delay != 0 else 0
    loop_duration = round(frame_count / fps, 3) if fps != 0 else 0
    fmt = 'GIF'
    transparency = gif.info.get('transparency', "No")
    # alpha = gif.getchannel('A')
    image_info = {
        "general_info": {
            "name": {"value": filename, "label": "Name"},
            "base_fname": {"value": base_fname, "label": "Base Name"},
            "width": {"value": width, "label": "Width"},
            "height": {"value": height, "label": "Height"},
            "fsize": {"value": fsize, "label": "File size"},
            "absolute_url": {"value": abspath, "label": "Path"},
            "format": {"value": fmt, "label": "Format"},
            "transparency": {"value": transparency, "label": "Has Transparency"},
            # "alpha": {"value": alpha, "label": "Has Alpha"},
            "comments": {"value": comments, "label": "Comments"},
        },
        "animation_info": {
            "fps": {"value": fps, "label": "FPS"},
            "avg_delay": {"value": round(avg_delay / 1000, 3), "label": "Average Delay"},
            "delay_is_uneven": {"value": delay_is_uneven, "label": "Delays are uneven"},
            "frame_count": {"value": frame_count, "label": "Frame count"},
            "frame_count_ds": {"value": frame_count_ds, "label": "Frame count (DS)"},
            "loop_duration": {"value": loop_duration, "label": "Loop"},
        }
    }
    gif.close()
    return image_info


def _inspect_apng(abspath, apng: APNG):  
    filename = str(os.path.basename(abspath))
    base_fname, ext = os.path.splitext(filename)      
    frames = apng.frames
    frame_count = len(frames)
    png_one, controller_one = frames[0]
    fmt = 'APNG'
    fsize = read_filesize(os.stat(abspath).st_size)
    width = png_one.width
    height = png_one.height
    durations = [f[1].delay for f in frames]
    min_duration = min(durations)
    if min_duration == 0:
        frame_count_ds = frame_count
    else:
        frame_count_ds = sum([dur//min_duration for dur in durations])
    delay_is_uneven = len(set(durations)) > 1
    avg_delay = sum(durations) / frame_count if sum(durations) != 0 else 0
    fps = round(1000.0 / avg_delay, 3) if avg_delay != 0 else 0
    loop_duration = round(frame_count / fps, 3) if fps != 0 else 0

    image_info = {
        "general_info": {
            "name": {"value": filename, "label": "Name"},
            "base_fname": {"value": base_fname, "label": "Base Name"},
            "width": {"value": width, "label": "Width"},
            "height": {"value": height, "label": "Height"},
            "fsize": {"value": fsize, "label": "File size"},
            "absolute_url": {"value": abspath, "label": "Path"},
            "format": {"value": fmt, "label": "Format"},
            # "comments": {"value": comments, "label": "Comments"},
        },
        "animation_info": {
            "fps": {"value": fps, "label": "FPS"},
            "avg_delay": {"value": round(avg_delay / 1000, 3), "label": "Average Delay"},
            "delay_is_uneven": {"value": delay_is_uneven, "label": "Delays are uneven"},
            "frame_count": {"value": frame_count, "label": "Frame count"},
            "frame_count_ds": {"value": frame_count_ds, "label": "Frame count (DS)"},
            "loop_duration": {"value": loop_duration, "label": "Loop"},
        }
    }
    return image_info


def inspect_sequence(image_paths):
    """Returns information of a selected sequence of static images"""
    abs_image_paths = [os.path.abspath(ip) for ip in image_paths if os.path.exists(ip)]
    sequence_info = []
    for path in abs_image_paths:
        info = inspect_general(path, filter_on="static", skip=True)
        if info:
            gen_info = info['general_info']
            sequence_info.append(gen_info)
            yield {"msg": f"Loading {gen_info['name']['value']}"}
    if not sequence_info:
        raise Exception("No images selected. Make sure the path to them are correct and they are static images")
    static_img_paths = [si['absolute_url']['value'] for si in sequence_info]
    # print("imgs count", len(static_img_paths))
    first_img_name = os.path.splitext(os.path.basename(static_img_paths[0]))[0]
    filename = first_img_name.split('_')[0] if '_' in first_img_name else first_img_name
    sequence_count = len(static_img_paths)
    sequence_filesize = read_filesize(sum([os.stat(i).st_size for i in static_img_paths]))
    width, height = Image.open(static_img_paths[0]).size
    yield {
        "data": {
            "name": sequence_info[0]['name']['value'],
            "total": sequence_count,
            "sequence": static_img_paths,
            "sequence_info": sequence_info,
            "size": sequence_filesize,
            "width": sequence_info[0]['width']['value'],
            "height": sequence_info[0]['height']['value'],
        }
    }
