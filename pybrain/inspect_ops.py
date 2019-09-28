import os
import string
import math
from random import choices
from pprint import pprint
from typing import List
from urllib.parse import urlparse

from PIL import Image, ExifTags, ImageFile
from apng import APNG
from hurry.filesize import size, alternative

from .config import IMG_EXTS, STATIC_IMG_EXTS, ANIMATED_IMG_EXTS
from .utility import _filter_images


def inspect_general(image_path):
    """ Handler function from InspectPanel """
    abspath = os.path.abspath(image_path)
    filename = str(os.path.basename(abspath))
    base_fname, ext = os.path.splitext(filename)
    ext = ext.lower()
    if ext == '.gif':
        try:
            gif: Image = Image.open(abspath)
        except Exception:
            raise Exception(f'The chosen file ({filename}) is not a valid GIF image')
        if gif.format == 'GIF':
            if gif.is_animated:
                return _inspect_agif(image_path, gif)
            else:
                return _inspect_image(image_path)
    elif ext == '.png':
        try:
            apng: APNG = APNG.open(abspath)
        except Exception:
            raise Exception(f'The chosen file ({filename}) is not a valid PNG image')
        frames = apng.frames
        frame_count = len(frames)
        if frame_count > 1:
            return _inspect_apng(image_path)
        else:
            return _inspect_image(image_path)
    else:
        return _inspect_image(image_path)


def _inspect_image(image):
    """ Returns general and EXIF info from static image. Static GIFs will not display EXIF (they don't support it) """
    img_metadata = {}
    if image.__class__.__bases__[0] is ImageFile.ImageFile:
        im = image
    else:
        im = Image.open(image)
    info = im.info
    fmt = im.format
    if fmt.upper() != "GIF":
        exif = im._getexif()
    else:
        exif = None
    width, height = im.size
    path = im.filename
    fsize = size(os.stat(path).st_size, system=alternative)
    img_metadata = {
        "general_info": {
            "name": {"value": os.path.basename(path), "label": "Name"},
            "width": {"value": width, "label": "Width"},
            "height": {"value": height, "label": "Height"},
            "fsize": {"value": fsize, "label": "File size"},
            "absolute_url": {"value": path, "label": "Path"},
            "format": {"value": fmt, "label": "Format"},
            "comments": {"value": info.get("comment", ""), "label": "Comments"},
            "color_mode": {"value": im.mode, "label": "Color Mode"},
            "exif": {"value": exif, "label": "EXIF"},
        }
    }
    return img_metadata


def _inspect_agif(abspath: str, gif: Image):
    filename = str(os.path.basename(abspath))
    base_fname, ext = os.path.splitext(filename)
    width, height = gif.size
    frame_count = gif.n_frames
    fsize = size(os.stat(abspath).st_size, system=alternative)
    durations = []
    comments = []
    for f in range(0, gif.n_frames):
        gif.seek(f)
        durations.append(gif.info['duration'])
        comments.append(gif.info.get('comment', ""))
    min_duration = min(durations)
    frame_count_ds = sum([dur//min_duration for dur in durations])
    # raise Exception(delays)
    duration_is_uneven = len(set(durations)) > 1
    avg_duration = sum(durations) / len(durations)
    fps = round(1000.0 / avg_duration, 3)
    loop_duration = round(frame_count / fps, 3)
    fmt = 'GIF'
    image_info = {
        "general_info": {
            "name": {"value": filename, "label": "Name"},
            "width": {"value": width, "label": "Width"},
            "height": {"value": height, "label": "Height"},
            "fsize": {"value": fsize, "label": "File size"},
            "absolute_url": {"value": abspath, "label": "Path"},
            "format": {"value": fmt, "label": "Format"},
            "comments": {"value": comments, "label": "Comments"},
        },
        "animation_info": {
            "fps": {"value": fps, "label": "FPS"},
            "avg_duration": {"value": round(avg_duration / 1000, 3), "label": "Average Delay"},
            "duration_is_uneven": {"value": duration_is_uneven, "label": "Uneven Delay"},
            "frame_count": {"value": frame_count, "label": "Frame count"},
            "frame_count_ds": {"value": frame_count_ds, "label": "Frame count (Delay sensitive)"},
            "loop_duration": {"value": loop_duration, "label": "Loop"},
        }
    }
    return image_info


def _inspect_apng(abspath, apng: APNG):  
    filename = str(os.path.basename(abspath))
    base_fname, ext = os.path.splitext(filename)      
    frames = apng.frames
    frame_count = len(frames)
    png_one, controller_one = frames[0]
    fmt = 'APNG'
    fsize = size(os.stat(abspath).st_size, system=alternative)
    width = png_one.width
    height = png_one.height
    durations = [f[1].delay for f in frames]
    min_duration = min(durations)
    frame_count_ds = sum([dur//min_duration for dur in durations])

    duration_is_uneven = len(set(durations)) > 1
    avg_duration = sum(durations) / frame_count
    fps = round(1000.0 / avg_duration, 3)
    loop_duration = round(frame_count / fps, 3)

    image_info = {
        "general_info": {
            "name": {"value": filename, "label": "Name"},
            "width": {"value": width, "label": "Width"},
            "height": {"value": height, "label": "Height"},
            "fsize": {"value": fsize, "label": "File size"},
            "absolute_url": {"value": abspath, "label": "Path"},
            "format": {"value": fmt, "label": "Format"},
            # "comments": {"value": comments, "label": "Comments"},
        },
        "animation_info": {
            "fps": {"value": fps, "label": "FPS"},
            "avg_duration": {"value": round(avg_duration / 1000, 3), "label": "Average Delay"},
            "duration_is_uneven": {"value": duration_is_uneven, "label": "Uneven Delay"},
            "frame_count": {"value": frame_count, "label": "Frame count"},
            "frame_count_ds": {"value": frame_count_ds, "label": "Frame count (Delay sensitive)"},
            "loop_duration": {"value": loop_duration, "label": "Loop"},
        }
    }
    return image_info


def _inspect_aimg(animage_path):
    """ Returns information of an animated GIF/APNG """
    abspath = os.path.abspath(animage_path)
    filename = str(os.path.basename(abspath))
    base_fname, ext = os.path.splitext(filename)
    ext = ext.lower()
    frame_count = 0  # Actual number of frames
    frame_count_ds = 0  # Duration-sensitive frame-count
    fps = 0
    avg_duration = 0
    fsize = size(os.stat(abspath).st_size, system=alternative)
    # fsize = 0
    width = height = 0
    loop_duration = 0
    extension = ''
    duration_is_uneven = False
    comment = ''

    if ext == '.gif':
        try:
            gif: Image = Image.open(abspath)
        except Exception:
            raise Exception(f'The chosen file ({filename}) is not a valid GIF image')
        if gif.format != 'GIF' or not gif.is_animated:
            raise Exception(f"The chosen GIF ({filename}) is not an animated GIF!")
        width, height = gif.size
        frame_count = gif.n_frames
        # pprint(gif.info)
        durations = []
        for f in range(0, gif.n_frames):
            gif.seek(f)
            durations.append(gif.info['duration'])
        min_duration = min(durations)
        frame_count_ds = sum([dur//min_duration for dur in durations])
        # raise Exception(delays)
        duration_is_uneven = len(set(durations)) > 1
        avg_duration = sum(durations) / len(durations)
        fps = round(1000.0 / avg_duration, 3)
        loop_duration = round(frame_count / fps, 3)
        extension = 'GIF'
        # comment = gif.comment

    elif ext == '.png':
        try:
            apng: APNG = APNG.open(abspath)
        except Exception:
            raise Exception(f'The chosen file ({filename}) is not a valid PNG image')
        frames = apng.frames
        frame_count = len(frames)
        if frame_count <= 1:
            raise Exception(f"The chosen PNG ({filename}) is not an animated PNG!")
        png_one, controller_one = frames[0]
        # pprint(png_one.__dict__)
        # pprint(controller_one.__dict__)
        extension = 'APNG'
        width = png_one.width
        height = png_one.height
        durations = [f[1].delay for f in frames]
        min_duration = min(durations)
        frame_count_ds = sum([dur//min_duration for dur in durations])

        duration_is_uneven = len(set(durations)) > 1
        avg_duration = sum(durations) / frame_count
        fps = round(1000.0 / avg_duration, 3)
        loop_duration = round(frame_count / fps, 3)

    image_info = {
        "name": filename,
        "base_fname": base_fname,
        "fps": fps,
        "avg_duration": round(avg_duration / 1000, 3),
        "duration_is_uneven": duration_is_uneven,
        "fsize": fsize,
        "extension": extension,
        "frame_count": frame_count,
        "frame_count_ds": frame_count_ds,
        "absolute_url": abspath,
        "width": width,
        "height": height,
        "loop_duration": loop_duration,
        "comment": comment,
    }
    return image_info


def _inspect_sequence(image_paths):
    """Returns information of a selected sequence of static images"""
    abs_image_paths = [os.path.abspath(ip) for ip in image_paths if os.path.exists(ip)]
    static_imgs, static_img_paths = zip(*_filter_images(abs_image_paths, "static"))
    print("imgs count", len(static_img_paths))
    if not static_img_paths:
        raise Exception("No images selected. Make sure the path to them are correct and they are static images")
    first_img_name = os.path.splitext(os.path.basename(static_img_paths[0]))[0]
    filename = first_img_name.split('_')[0] if '_' in first_img_name else first_img_name
    sequence_count = len(static_img_paths)
    sequence_filesize = size(sum([os.stat(i).st_size for i in static_img_paths]), system=alternative)
    if not static_img_paths:
        raise Exception("The images choosen must be static images, not animted GIFs or PNGs!")
    width, height = Image.open(static_img_paths[0]).size
    sequence_info = [_inspect_image(si)['general_info'] for si in static_imgs]
    # sequence_info = _get_sequence_metadata(static_img_paths)
    data = {
        "name": sequence_info[0]['name']['value'],
        "total": sequence_count,
        "sequence": static_img_paths,
        "sequence_info": sequence_info,
        "size": sequence_filesize,
        "width": sequence_info[0]['width']['value'],
        "height": sequence_info[0]['width']['value'],
    }
    return data


def _get_sequence_metadata(sequence_paths: List):
    sequence_metadata = []
    for index, path in enumerate(sequence_paths):
        with Image.open(path) as im:
            info = im.info
            ext = im.format
            if ext.upper() != "GIF":
                exif = im._getexif()
            else:
                exif = None
            width, height = im.size
            sequence_metadata.append({
                "index": index,
                "name": os.path.basename(path),
                "format": ext,
                "path": path,
                "color_mode": im.mode,
                "comment": info.get("comment", ""),
                "exif": exif,
                "width": width,
                "height": height,
            })
    return sequence_metadata
