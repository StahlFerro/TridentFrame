import os
import platform
import io
import string
import shutil
import shlex
import math
import time
import subprocess
import tempfile
from collections import deque
from random import choices
from pprint import pprint
from typing import List, Dict, Tuple
from datetime import datetime

from PIL import Image
from apng import APNG, PNG

from .core_funcs.config import IMG_EXTS, ANIMATED_IMG_EXTS, STATIC_IMG_EXTS, ABS_CACHE_PATH, imager_exec_path
from .core_funcs.criterion import CreationCriteria, GIFOptimizationCriteria, APNGOptimizationCriteria, CriteriaBundle
from .core_funcs.utility import _mk_temp_dir, shout_indices
from .bin_funcs.arg_builder import apngopt_args, pngquant_args
from .bin_funcs.imager_api import apngopt_render, pngquant_render


def _create_gifragments(image_paths: List, out_path: str, criteria: CreationCriteria) -> Tuple[str, List[str]]:
    """ Generate a sequence of GIFs created from the input sequence with the specified criteria, before compiling them into a single animated GIF"""
    # disposal = 0
    # if criteria.reverse:
    #     image_paths.reverse()
    # temp_gifs = []
    fcount = len(image_paths)
    if criteria.start_frame:
        shift_items = deque(image_paths)
        shift_items.rotate(-criteria.start_frame)
        image_paths = list(shift_items)
    perc_skip = 5
    shout_nums = shout_indices(fcount, perc_skip)
    for index, ipath in enumerate(image_paths):
        if shout_nums.get(index):
            yield {"msg": f'Processing frames... ({shout_nums.get(index)})'}
        with Image.open(ipath) as im:
            im: Image.Image
            transparency = im.info.get("transparency", False)
            orig_width, orig_height = im.size
            must_resize = criteria.resize_width != orig_width or criteria.resize_height != orig_height
            # raise Exception(criteria.resize_width, criteria.resize_height, im.size, must_resize)
            alpha = None
            if criteria.flip_h:
                im = im.transpose(Image.FLIP_LEFT_RIGHT)
            if criteria.flip_v:
                im = im.transpose(Image.FLIP_TOP_BOTTOM)
            if must_resize:
                resize_method_enum = getattr(Image, criteria.resize_method)
                # yield {"resize_method_enum": resize_method_enum}
                im = im.resize((round(criteria.resize_width) , round(criteria.resize_height)), resample=resize_method_enum)
            if criteria.rotation:
                im = im.rotate(criteria.rotation, expand=True)
            fragment_name = os.path.splitext(f"{str.zfill(str(index), 6)}_{os.path.basename(ipath)}")[0]
            if criteria.reverse:
                reverse_index = len(image_paths) - (index + 1)
                fragment_name = f"rev_{str.zfill(str(reverse_index), 3)}_{fragment_name}"
            save_path = f'{os.path.join(out_path, fragment_name)}.gif'
            if im.mode == 'RGBA':
                if criteria.transparent:
                    alpha = im.getchannel('A')
                    im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
                    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
                    im.paste(255, mask)
                    im.info['transparency'] = 255
                else:
                    black_bg = Image.new("RGBA", size=im.size)
                    black_bg.alpha_composite(im)
                    # im.show()
                    im = black_bg
                    # black_bg.show()
                    im = im.convert('P', palette=Image.ADAPTIVE)
                im.save(save_path)
            elif im.mode == 'RGB':
                im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE)
                im.save(save_path)
            elif im.mode == 'P':
                if transparency:
                    if type(transparency) is int:
                        im.save(save_path, transparency=transparency)
                    else:
                        im = im.convert('RGBA')
                        alpha = im.getchannel('A')
                        im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
                        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
                        im.paste(255, mask)
                        im.info['transparency'] = 255
                        im.save(save_path)
                else:
                    im.save(save_path)
            # yield {"msg": f"Save path: {save_path}"}
            # if absolute_paths:
                # temp_gifs.append(save_path)
            # else:
                # temp_gifs.append(os.path.relpath(save_path, os.getcwd()))


def _build_gif(image_paths: List, out_full_path: str, crbundle: CriteriaBundle):
    gifragment_dir = _mk_temp_dir(prefix_name="tmp_gifrags")
    criteria = crbundle.create_aimg
    gif_criteria = crbundle.gif_opt
    yield from _create_gifragments(image_paths, gifragment_dir, criteria)
    executable = str(imager_exec_path('gifsicle'))
    delay = int(criteria.delay * 100)
    disposal = "background"
    loop_arg = "--loopcount"
    opti_mode = "--unoptimize"
    colorspace_arg = ""
    lossy_arg = ""
    if (not criteria.loop_count or criteria.loop_count == 0):
        loop_arg = "--loopcount"
    elif (criteria.loop_count == 1):
        loop_arg = '--no-loopcount'
    elif (criteria.loop_count > 1):
        loop_arg = f'--loopcount={criteria.loop_count - 1}'
    globstar_path = "*.gif"

    if gif_criteria:
        if gif_criteria.is_optimized and gif_criteria.optimization_level:
            opti_mode = f"--optimize={gif_criteria.optimization_level}"
        if gif_criteria.is_lossy and gif_criteria.lossy_value:
            lossy_arg = f"--lossy={gif_criteria.lossy_value}"
        if gif_criteria.is_reduced_color and gif_criteria.color_space:
            colorspace_arg = f"--colors={gif_criteria.color_space}"

    ROOT_PATH = str(os.getcwd())
    if os.getcwd() != gifragment_dir:
        yield {"msg": f"Changing directory from {os.getcwd()} to {gifragment_dir}"}
        os.chdir(gifragment_dir)
    yield {"msg": f"Obtained gifsicle exec path: {executable}"}
    args = [executable, opti_mode, lossy_arg, colorspace_arg, f"--delay={delay}", f"--disposal={disposal}", loop_arg, globstar_path, "--output", f'"{out_full_path}"']
    cmd = ' '.join(args)
    yield {"cmd": cmd}
    # yield {"shlexed cmd": cmd}
    yield {"msg": "Combining frames..."}
    result = subprocess.run(cmd, shell=True, capture_output=True)
    yield {"gifsicle STDOUT": result.stdout.decode('utf-8')}
    yield {"gifsicle STDERR": result.stderr.decode('utf-8')}
    # if result.stderr:
    #     raise Exception(result.stderr)
    os.chdir(ROOT_PATH)
    # shutil.rmtree(gifragment_dir)
    yield {"preview_path": out_full_path}
    yield {"CONTROL": "CRT_FINISH"}
    return out_full_path


def _build_apng(image_paths, out_full_path, crbundle: CriteriaBundle) -> APNG:
    criteria = crbundle.create_aimg
    aopt_criteria = crbundle.apng_opt
    temp_dirs = []
    aopt_args = apngopt_args(aopt_criteria) if aopt_criteria else []
    pq_args = pngquant_args(aopt_criteria) if aopt_criteria else []

    if pq_args:
        qtemp_dir = _mk_temp_dir(prefix_name="quant_temp")
        temp_dirs.append(qtemp_dir)
        image_paths = yield from pngquant_render(pq_args, image_paths, optional_out_path=qtemp_dir)

    if criteria.reverse:
        image_paths.reverse()
    
    apng = APNG()
    first_width, first_height = Image.open(image_paths[0]).size
    first_must_resize = criteria.resize_width != first_width or criteria.resize_height != first_height
    shout_nums = shout_indices(len(image_paths), 5)
    yield criteria.__dict__
    if criteria.flip_h or criteria.flip_v or first_must_resize or criteria.rotation:
        for index, ipath in enumerate(image_paths):
            if shout_nums.get(index):
                yield {"msg": f'Processing frames... ({shout_nums.get(index)})'}
            with io.BytesIO() as bytebox:
                with Image.open(ipath) as im:
                    # im = Image.open(ipath)
                    im: Image.Image
                    orig_width, orig_height = im.size
                    must_resize = criteria.resize_width != orig_width or criteria.resize_height != orig_height
                    if must_resize:
                        resize_method_enum = getattr(Image, criteria.resize_method)
                        # yield {"resize_method_enum": resize_method_enum}
                        im = im.resize((round(criteria.resize_width), round(criteria.resize_height)), resize_method_enum)
                    if criteria.flip_h:
                        im = im.transpose(Image.FLIP_LEFT_RIGHT)
                    if criteria.flip_v:
                        im = im.transpose(Image.FLIP_TOP_BOTTOM)
                    if criteria.rotation:
                        im = im.rotate(criteria.rotation, expand=True)
                    im.save(bytebox, "PNG")
                apng.append(PNG.from_bytes(bytebox.getvalue()), delay=int(criteria.delay * 1000))
        yield {"msg": "Saving APNG...."}
        apng.num_plays = criteria.loop_count
        apng.save(out_full_path)
    else:
        yield {"msg": "Saving APNG..."}
        apng = APNG.from_files(image_paths, delay=int(criteria.delay * 1000))
        apng.num_plays = criteria.loop_count
        apng.save(out_full_path)
    
    if aopt_args:
        out_full_path = yield from apngopt_render(aopt_args, out_full_path, out_full_path)

    # for td in temp_dirs:
    #     shutil.rmtree(td)
    yield {"preview_path": out_full_path}
    yield {"CONTROL": "CRT_FINISH"}

    return out_full_path


def create_aimg(image_paths: List[str], out_dir: str, filename: str, crbundle: CriteriaBundle) -> bool:
    """ Umbrella generator for creating animated images from a sequence of images """
    abs_image_paths = [os.path.abspath(ip) for ip in image_paths if os.path.exists(ip)]
    img_paths = [f for f in abs_image_paths if str.lower(os.path.splitext(f)[1][1:]) in STATIC_IMG_EXTS]
    # workpath = os.path.dirname(img_paths[0])
    # Test if inputted filename has extension, then remove it from the filename
    img_format = crbundle.create_aimg.extension
    if len(img_paths) < 2:
        raise Exception(f"At least 2 images is needed for an animated {img_format}!")
    fname, ext = os.path.splitext(filename)
    if ext:
        filename = fname
    if not out_dir:
        raise Exception("No output folder selected, please select it first")
    out_dir = os.path.abspath(out_dir)
    if not os.path.exists(out_dir):
        raise Exception(f"The specified absolute out_dir does not exist!\n{out_dir}")
    if img_format == 'GIF':
        out_full_path = os.path.join(out_dir, f"{filename}.gif")
        filename = f"{filename}.gif"
        return _build_gif(image_paths, out_full_path, crbundle)
    
    elif img_format == 'PNG':
        out_full_path = os.path.join(out_dir, f"{filename}.png")
        return _build_apng(img_paths, out_full_path, crbundle)
