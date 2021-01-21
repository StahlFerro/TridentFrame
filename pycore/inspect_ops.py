import os
import io
import string
import math
import sys
import json
import pickle
from random import choices
from pprint import pprint
from typing import List, Dict
from urllib.parse import urlparse
from pprint import pprint

from PIL import Image, ExifTags, ImageFile
from PIL.PngImagePlugin import PngImageFile, PngInfo
# from PIL.GifImagePlugin import GifImageFile
Image.MAX_IMAGE_PIXELS = None
from apng import APNG

from .core_funcs.config import IMG_EXTS, STATIC_IMG_EXTS, ANIMATED_IMG_EXTS, set_bufferfile_content
from .core_funcs.utility import _filter_images, read_filesize, shout_indices, sequence_nameget
from .core_funcs.metadata_builder import ImageMetadata, AnimatedImageMetadata


def inspect_general(image_path, filter_on="", skip=False) -> Dict:
    """ Main single image inspection handler function.
    :param `image_path`: Input path.
    :param `filter_on`: "" no filter, "static": "Throws error on detecting an animated image", "animated": "Throws error on detecting a static image"
    :param `skip`: Returns an empty dict instead of throwing an error. Used in conjuntion with filter_on
    """
    abspath = os.path.abspath(image_path)
    filename = str(os.path.basename(abspath))
    base_fname, ext = os.path.splitext(filename)
    ext = ext.lower()
    if ext == '.gif':
        try:
            gif: Image = Image.open(abspath)
        except Exception:
            print({"error": f'The chosen file ({filename}) is not a valid GIF image'}, file=sys.stderr)
            
        # raise Exception(gif.is_animated, filter_on, skip)
        if gif.format == 'GIF':
            if gif.is_animated:
                if filter_on == "static":
                    if skip:
                        return {}
                    else:
                        print({"error": f"The GIF {base_fname} is not static!"}, file=sys.stderr)
                else:
                    return _inspect_agif(image_path, gif)
            else:
                if filter_on == "animated":
                    if skip:
                        return {}
                    else:
                        print({"error": f"The GIF {base_fname} is not animated!"}, file=sys.stderr)
                else:
                    return _inspect_simg(image_path)
    elif ext == '.png':
        try:
            apng: APNG = APNG.open(abspath)
        except Exception:
            print({"error": f'The chosen file ({filename}) is not a valid PNG image'}, file=sys.stderr)
            return
        frames = apng.frames
        frame_count = len(frames)
        if frame_count > 1:
            if filter_on == "static":
                if skip:
                    return {}
                else:
                    print({"error": f"The APNG ({filename}) is not static!"}, file=sys.stderr)
                    return
            else:
                return _inspect_apng(image_path, apng)
        else:
            if filter_on == "animated":
                if skip:
                    return {}
                else:
                    print({"error": f"The PNG {base_fname} is not animated!"}, file=sys.stderr)
                    return
            else:
                return _inspect_simg(image_path)
    else:
        return _inspect_simg(image_path)


def _inspect_simg(image):
    """ Returns general and EXIF info from a static image. Static GIFs will not display EXIF (GIFs don't support it)

    Keyword arguments:
    image -- Path or Pillow Image
    """
    image_info = {}
    im: Image = None
    try:
        if image.__class__.__bases__[0] is ImageFile.ImageFile:
            im = image
        else:
            im = Image.open(image)
    except Exception as e:
        print(json.dumps({"error": str(e).replace("\\\\", "/")}), file=sys.stderr)
        return
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
    base_fname = sequence_nameget(base_fname)
    fsize = os.stat(path).st_size
    fsize_hr = read_filesize(fsize)
    color_mode = im.mode
    transparency = im.info.get('transparency', "-")
    # alpha = im.getchannel('A')
    comment = im.info.get('comment')
    im.close()
    
    metadata = ImageMetadata({
        "name": filename, 
        "base_filename": base_fname,
        "width": width,
        "height": height,
        "format": fmt,
        "fsize": fsize,
        "absolute_url": path,
        "comments": str(comment),
        "color_mode": str(color_mode),    
        "transparency": str(transparency),
        "is_animated": False,
        "exif": str(exif),
    })
    return metadata.format_info()


def _inspect_agif(abspath: str, gif: Image):
    filename = str(os.path.basename(abspath))
    base_fname, ext = os.path.splitext(filename)
    base_fname = sequence_nameget(base_fname)
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
    fmt = 'GIF'
    full_format = str(gif.info.get('version') or "")
    transparency = gif.info.get('transparency', "-")
    gif.close()
    metadata = AnimatedImageMetadata({
        "name": filename, 
        "base_filename": base_fname,
        "width": width,
        "height": height,
        "format": fmt,
        "format_version": full_format,
        "fsize": fsize,
        "absolute_url": abspath,
        "comments": comments,
        "transparency": transparency,
        "is_animated": True,
        "frame_count": frame_count,
        "delays": delays,
        "loop_count": loop_count
    })
    return metadata.format_info()


def _inspect_apng(abspath, apng: APNG):  
    filename = str(os.path.basename(abspath))
    base_fname, ext = os.path.splitext(filename)
    base_fname = sequence_nameget(base_fname)
    frames = apng.frames
    frame_count = len(frames)
    loop_count = apng.num_plays
    png_one, controller_one = frames[0]
    fmt = 'PNG'
    fsize = os.stat(abspath).st_size
    fsize_hr = read_filesize(fsize)
    width = png_one.width
    height = png_one.height
    # raise Exception(frames)
    delays = [f[1].delay if f[1] else 0 for f in frames]
    min_duration = min(delays)
    if min_duration == 0:
        frame_count_ds = frame_count
    else:
        frame_count_ds = sum([delay//min_duration for delay in delays])
    metadata = AnimatedImageMetadata({
        "name": filename, 
        "base_filename": base_fname,
        "width": width,
        "height": height,
        "format": fmt,
        "fsize": fsize,
        "absolute_url": abspath,
        "is_animated": True,
        "frame_count": frame_count,
        "delays": delays,
        "loop_count": loop_count
    })
    return metadata.format_info()
    # return image_info


def inspect_sequence(image_paths):
    """Returns information of a selected sequence of static images"""
    abs_image_paths = [os.path.abspath(ip) for ip in image_paths if os.path.exists(ip) and os.path.isfile(ip)]
    sequence_info = []
    perc_skip = 5
    shout_nums = shout_indices(len(abs_image_paths), perc_skip)
    for index, path in enumerate(abs_image_paths):
        if shout_nums.get(index):
            print(json.dumps({"msg": f'Loading images... ({shout_nums.get(index)})'}))
        info = inspect_general(path, filter_on="static", skip=True)
        if info:
            gen_info = info['general_info']
            sequence_info.append(gen_info)
    if not sequence_info:
        print(json.dumps({"error": "No images selected. Make sure the path to them are correct and they are not animated images!"}), file=sys.stderr)
        return
    static_img_paths = [si['absolute_url']['value'] for si in sequence_info]
    # print("imgs count", len(static_img_paths))
    first_img_name = os.path.splitext(os.path.basename(static_img_paths[0]))[0]
    # filename = first_img_name.split('_')[0] if '_' in first_img_name else first_img_name
    sequence_count = len(static_img_paths)
    sequence_filesize = read_filesize(sum( (si['fsize']['value'] for si in sequence_info) ))
    # im = Image.open(static_img_paths[0])
    # width, height = im.size
    # im.close()
    image_info = {
        "name": sequence_info[0]['base_filename']['value'],
        "total": sequence_count,
        "sequence": static_img_paths,
        "sequence_info": sequence_info,
        "total_size": sequence_filesize,
        "width": sequence_info[0]['width']['value'],
        "height": sequence_info[0]['height']['value'],
    }
    return image_info


def _inspect_smart(image_path):
    """ Receives a single image, then finds similar images with the same name and then returns the information of those sequence """
    if type(image_path) is list:
        image_path = image_path[0]
    imgdir = os.path.dirname(image_path)
    filename, ext = os.path.splitext(os.path.basename(image_path))
    base_fname = sequence_nameget(filename)
    print(json.dumps({"basefname": base_fname}))
    possible_sequence = [os.path.abspath(os.path.join(imgdir, f)) for f in os.listdir(imgdir) if base_fname in os.path.splitext(f)[0]]
    # paths_bufferio = io.StringIO(json.dumps(possible_sequence))
    return inspect_sequence(possible_sequence)

