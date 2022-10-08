from operator import mod
import os
import io
import shutil
import math
from fractions import Fraction
from pathlib import Path
from typing import List

from PIL import Image
from apng import APNG, PNG, FrameControl
from typing import List, Tuple, Iterator, Optional, Generator
from pycore.imaging.gif import modify_animated_gif
from pycore.imaging.png import modify_animated_png


from pycore.models.criterion import (
    CriteriaBundle,
    CriteriaUtils,
    DelayHandling,
)
from pycore.models.image_formats import ImageFormat
from pycore.utility import filehandler, imageutils, vectorutils
from pycore.bin_funcs.imager_api import GifsicleAPI, ImageMagickAPI, APNGOptAPI, InternalImageAPI
from pycore.models.metadata import ImageMetadata, AnimatedImageMetadata
from pycore.models.criterion import CreationCriteria, SplitCriteria
from pycore.core_funcs import stdio
from pycore.inspect_ops import inspect_general
from pycore.create_ops import create_aimg
from pycore.split_ops import split_aimg


def rebuild_aimg(img_path: Path, out_path: Path, metadata: AnimatedImageMetadata, crbundle: CriteriaBundle):
    mod_criteria = crbundle.modify_aimg_criteria
    aopt_criteria = crbundle.apng_opt_criteria
    frames_dir = filehandler.mk_cache_dir(prefix_name="presplit_images")
    has_transparency = metadata.has_transparency
    # if mod_criteria.format == "PNG" and not aopt_criteria.convert_color_mode:
    #     aopt_criteria.convert_color_mode = True
    #     if has_transparency:
    #         aopt_criteria.new_color_mode = "RGBA"
    #     else:
    #         aopt_criteria.new_color_mode = "RGB"
    # is_unoptimized = mod_criteria.is_unoptimized or mod_criteria.apng_is_unoptimized or mod_criteria.change_format()
    split_criteria = SplitCriteria({
        "pad_count": 6,
        "color_space": "",
        "is_unoptimized": True,
        "new_name": "",
        "extract_delay_info": False,
        "convert_to_rgba": False,
    })
    frame_paths = split_aimg(img_path, frames_dir, split_criteria)
    stdio.debug({"presplit_fr_paths": frame_paths})
    # yield {"MOD split frames": frame_paths}
    # if mod_criteria.is_reversed:
    #     frames.reverse()
    # pq_args = pngquant_args(apngopt_criteria)
    # if mod_criteria.format == "PNG" and apngopt_criteria.is_lossy:
    #     logger.message("PNG QUANTIZATION SELECTED")
    #     frame_paths = pngquant_render(pq_args, frame_paths)
    # ds_fps = mod_criteria.orig_frame_count_ds / mod_criteria.orig_loop_duration
    # # ds_delay = 1 / ds_fps
    # ds_delay = mod_criteria.delay
    # ds_fps = mod_criteria.fps
    # yield {"NEW DELAY": ds_delay}
    delays = []
    if mod_criteria.delay_handling == DelayHandling.MULTIPLY_AVERAGE:
        delays = CriteriaUtils.calculate_new_delays(mod_criteria, metadata)
    elif mod_criteria.delay_handling == DelayHandling.EVEN_OUT:
        delays = [mod_criteria.delay] * len(frame_paths)
    # stdio.error(delays)
    create_criteria = CreationCriteria({
        # "name": mod_criteria.name,
        "fps": mod_criteria.fps,
        "delay": mod_criteria.delay,
        "delays_are_even": metadata.delays_are_even["value"],
        "delays_list": delays,
        "format": mod_criteria.format,
        "preserve_alpha": True,
        "flip_x": mod_criteria.flip_x,
        "flip_y": mod_criteria.flip_y,
        "width": mod_criteria.width,
        "height": mod_criteria.height,
        "loop_count": mod_criteria.loop_count,
        "start_frame": mod_criteria.start_frame,
        "is_reversed": mod_criteria.reverse,
        "rotation": mod_criteria.rotation,
        "resize_method": mod_criteria.resize_method,
        "frame_skip_count": mod_criteria.frame_skip_count,
        "frame_skip_gap": mod_criteria.frame_skip_gap,
        "frame_skip_offset": mod_criteria.frame_skip_offset,
        "frame_skip_maintain_delay": mod_criteria.frame_skip_maintain_delay,
    })
    creation_crbundle = CriteriaBundle({
        "create_aimg_criteria": create_criteria,
        "gif_opt_criteria": crbundle.gif_opt_criteria,
        "apng_opt_criteria": crbundle.apng_opt_criteria,
    })
    stdio.error("MOD CREATE")
    stdio.error(create_criteria)
    new_image_path = create_aimg(frame_paths, out_path, creation_crbundle)
    # stdio.error("MOD RETEMPO")
    if create_criteria.format == ImageFormat.GIF:
        frames_info = create_criteria.get_frames_info(len(frame_paths))
        GifsicleAPI.retempo_gif(new_image_path, create_criteria, frames_info)
    shutil.rmtree(frames_dir)
    return new_image_path



def modify_aimg(img_path: Path, out_path: Path, crbundle: CriteriaBundle) -> Path:
    orig_attribute = inspect_general(img_path, filter_on="animated")
    if orig_attribute is None:
        raise Exception("Error: cannot load image")
    criteria = crbundle.modify_aimg_criteria
    aopt_criteria = crbundle.apng_opt_criteria
    change_format = criteria.change_format(orig_attribute)

    if change_format or criteria.must_transform(orig_attribute) or criteria.start_frame > 1 \
        or criteria.frame_skip_count > 0 or (criteria.format == ImageFormat.PNG and aopt_criteria.quantization_enabled) :
        stdio.debug(f"Rebuilding {orig_attribute.format} image into {criteria.format}...")
        return rebuild_aimg(img_path, out_path, orig_attribute, crbundle)
    else:
        stdio.debug(f"Modifying {criteria.format} image...")
        if criteria.format == ImageFormat.GIF:
            return modify_animated_gif(img_path, out_path, orig_attribute, crbundle)
        elif criteria.format == ImageFormat.PNG:
            return modify_animated_png(img_path, out_path, orig_attribute, crbundle)
