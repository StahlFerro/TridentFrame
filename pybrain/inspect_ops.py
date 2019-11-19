import os
import string
import math
from random import choices
from pprint import pprint
from typing import List, Dict
from urllib.parse import urlparse

from PIL import Image, ExifTags, ImageFile
# from PIL.GifImagePlugin import GifImageFile
Image.MAX_IMAGE_PIXELS = None
from apng import APNG
from hurry.filesize import size, alternative

from .config import IMG_EXTS, STATIC_IMG_EXTS, ANIMATED_IMG_EXTS
from .utility import _filter_images, read_filesize, shout_indices


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
    """ Returns general and EXIF info from a static image. Static GIFs will not display EXIF (GIFs don't support it)

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
    filename = str(os.path.basename(path))
    base_fname, ext = os.path.splitext(filename)
    fsize = os.stat(path).st_size
    fsize_hr = read_filesize(fsize)
    color_mode = im.mode
    transparency = im.info.get('transparency', "No")
    # alpha = im.getchannel('A')
    comment = im.info.get('comment')
    # fsize = size(os.stat(path).st_size, system=alternative)
    img_metadata = {
        "general_info": {
            "name": {"value": filename, "label": "Name"},
            "base_fname": {"value": base_fname, "label": "Base Name"},
            "width": {"value": width, "label": "Width"},
            "height": {"value": height, "label": "Height"},
            "fsize": {"value": fsize, "label": "File size (bytes)"},
            "fsize_hr": {"value": fsize_hr, "label": "File size "},
            "absolute_url": {"value": path, "label": "Path"},
            "format": {"value": fmt, "label": "Format"},
            "comments": {"value": comment, "label": "Comments"},
            "color_mode": {"value": color_mode, "label": "Color Mode"},
            "transparency": {"value": transparency, "label": "Has Transparency"},
            # "alpha": {"value": alpha, "label": "Has Alpha"},
            "exif": {"value": exif, "label": "EXIF"},
            "is_animated": {"value": False, "label": "Is Animated"},
        }
    }
    im.close()
    return img_metadata


def _inspect_agif(abspath: str, gif: Image):
    filename = str(os.path.basename(abspath))
    base_fname, ext = os.path.splitext(filename)
    width, height = gif.size
    frame_count = gif.n_frames
    fsize = os.stat(abspath).st_size
    fsize_hr = read_filesize(fsize)
    loop_info = gif.info.get('loop')
    if loop_info == None:
        loop_count = 1
    elif loop_info == 0:
        loop_count = 0
    else:
        loop_count = loop_info + 1
    delays = []
    comments = []
    for f in range(0, gif.n_frames):
        gif.seek(f)
        delays.append(gif.info['duration'])
        comments.append(gif.info.get('comment', ""))
    min_duration = min(delays)
    if min_duration == 0:
        frame_count_ds = frame_count
    else:
        frame_count_ds = sum([delay//min_duration for delay in delays])
    # raise Exception(delays)
    delay_is_uneven = len(set(delays)) > 1
    avg_delay = sum(delays) / len(delays) if sum(delays) != 0 else 0
    fps = round(1000.0 / avg_delay, 3) if avg_delay != 0 else 0
    loop_duration = round(frame_count / fps, 3) if fps != 0 else 0
    fmt = 'GIF'
    full_format = str(gif.info.get('version') or "")
    transparency = gif.info.get('transparency', "No")
    # alpha = gif.getchannel('A')
    image_info = {
        "general_info": {
            "name": {"value": filename, "label": "Name"},
            "base_fname": {"value": base_fname, "label": "Base Name"},
            "width": {"value": width, "label": "Width"},
            "height": {"value": height, "label": "Height"},
            "fsize": {"value": fsize, "label": "File size (bytes)"},
            "fsize_hr": {"value": fsize_hr, "label": "File size "},
            "absolute_url": {"value": abspath, "label": "Path"},
            "format": {"value": fmt, "label": "Format"},
            "format_version": {"value": full_format, "label": "Full format"},
            "transparency": {"value": transparency, "label": "Has Transparency"},
            # "alpha": {"value": alpha, "label": "Has Alpha"},
            "comments": {"value": comments, "label": "Comments"},
            "is_animated": {"value": True, "label": "Is Animated"},
        },
        "animation_info": {
            "fps": {"value": fps, "label": "FPS"},
            "avg_delay": {"value": round(avg_delay / 1000, 3), "label": "Average Delay"},
            "delay_is_uneven": {"value": delay_is_uneven, "label": "Delays are uneven"},
            "delays": {"value": delays, "label": "Delays (milliseconds)"},
            "frame_count": {"value": frame_count, "label": "Frame count"},
            "frame_count_ds": {"value": frame_count_ds, "label": "Frame count (DS)"},
            "loop_duration": {"value": loop_duration, "label": "Loop duration (seconds)"},
            "loop_count": {"value": loop_count, "label": "Loop count"},
        }
    }
    gif.close()
    return image_info


def _inspect_apng(abspath, apng: APNG):  
    filename = str(os.path.basename(abspath))
    base_fname, ext = os.path.splitext(filename)      
    frames = apng.frames
    frame_count = len(frames)
    loop_count = apng.num_plays
    png_one, controller_one = frames[0]
    fmt = 'PNG'
    fsize = os.stat(abspath).st_size
    fsize_hr = read_filesize(fsize)
    width = png_one.width
    height = png_one.height
    delays = [f[1].delay for f in frames]
    min_duration = min(delays)
    if min_duration == 0:
        frame_count_ds = frame_count
    else:
        frame_count_ds = sum([delay//min_duration for delay in delays])
    delay_is_uneven = len(set(delays)) > 1
    avg_delay = sum(delays) / frame_count if sum(delays) != 0 else 0
    fps = round(1000.0 / avg_delay, 3) if avg_delay != 0 else 0
    loop_duration = round(frame_count / fps, 3) if fps != 0 else 0

    image_info = {
        "general_info": {
            "name": {"value": filename, "label": "Name"},
            "base_fname": {"value": base_fname, "label": "Base Name"},
            "width": {"value": width, "label": "Width"},
            "height": {"value": height, "label": "Height"},
            "fsize": {"value": fsize, "label": "File size (bytes)"},
            "fsize_hr": {"value": fsize_hr, "label": "File size "},
            "absolute_url": {"value": abspath, "label": "Path"},
            "format": {"value": fmt, "label": "Format"},
            "is_animated": {"value": True, "label": "Is Animated"},
            # "comments": {"value": comments, "label": "Comments"},
        },
        "animation_info": {
            "fps": {"value": fps, "label": "FPS"},
            "avg_delay": {"value": round(avg_delay / 1000, 3), "label": "Average Delay"},
            "delay_is_uneven": {"value": delay_is_uneven, "label": "Delays are uneven"},
            "delays": {"value": delays, "label": "Delays (milliseconds)"},
            "frame_count": {"value": frame_count, "label": "Frame count"},
            "frame_count_ds": {"value": frame_count_ds, "label": "Frame count (DS)"},
            "loop_duration": {"value": loop_duration, "label": "Loop duration (seconds)"},
            "loop_count": {"value": loop_count, "label": "Loop count"},
        }
    }
    return image_info


def inspect_sequence(image_paths):
    """Returns information of a selected sequence of static images"""
    abs_image_paths = [os.path.abspath(ip) for ip in image_paths if os.path.exists(ip)]
    sequence_info = []
    perc_skip = 5
    shout_nums = shout_indices(len(abs_image_paths), perc_skip)
    for index, path in enumerate(abs_image_paths):
        if shout_nums.get(index):
            yield {"msg": f'Loading images... ({shout_nums.get(index)})'}
        info = inspect_general(path, filter_on="static", skip=True)
        if info:
            gen_info = info['general_info']
            sequence_info.append(gen_info)
    if not sequence_info:
        raise Exception("No images selected. Make sure the path to them are correct and they are static images")
    static_img_paths = [si['absolute_url']['value'] for si in sequence_info]
    # print("imgs count", len(static_img_paths))
    first_img_name = os.path.splitext(os.path.basename(static_img_paths[0]))[0]
    # filename = first_img_name.split('_')[0] if '_' in first_img_name else first_img_name
    sequence_count = len(static_img_paths)
    sequence_filesize = read_filesize(sum([os.stat(i).st_size for i in static_img_paths]))
    # im = Image.open(static_img_paths[0])
    # width, height = im.size
    # im.close()
    yield {
        "data": {
            "name": sequence_info[0]['base_fname']['value'],
            "total": sequence_count,
            "sequence": static_img_paths,
            "sequence_info": sequence_info,
            "size": sequence_filesize,
            "width": sequence_info[0]['width']['value'],
            "height": sequence_info[0]['height']['value'],
        }
    }
