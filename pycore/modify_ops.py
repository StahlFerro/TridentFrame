from operator import mod
import os
import io
import shutil
import math
from fractions import Fraction
from pathlib import Path
from typing import List

from PIL import Image
from apng import APNG, PNG

from pycore.models.criterion import (
    CriteriaBundle,
    DelayHandling,
)
from pycore.models.image_formats import ImageFormat
from pycore.utility import filehandler
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
    create_criteria = CreationCriteria({
        # "name": mod_criteria.name,
        "fps": mod_criteria.fps,
        "delay": mod_criteria.delay,
        "format": mod_criteria.format,
        "preserve_alpha": True,
        "flip_x": mod_criteria.flip_x,
        "flip_y": mod_criteria.flip_y,
        "width": mod_criteria.width,
        "height": mod_criteria.height,
        "loop_count": mod_criteria.loop_count,
        "start_frame": 1,
        "is_reversed": mod_criteria.reverse,
        "rotation": mod_criteria.rotation,
        "resize_method": mod_criteria.resize_method
    })
    creation_crbundle = CriteriaBundle({
        "create_aimg_criteria": create_criteria,
        "gif_opt_criteria": crbundle.gif_opt_criteria,
        "apng_opt_criteria": crbundle.apng_opt_criteria,
    })
    new_image_path = create_aimg(frame_paths, out_path, creation_crbundle)
    shutil.rmtree(frames_dir)
    return new_image_path


def _modify_gif(gif_path: Path, out_path: Path, metadata: AnimatedImageMetadata, crbundle: CriteriaBundle) -> Path:
    if crbundle.gif_opt_criteria.is_unoptimized:
        stdio.message("Unoptimizing GIF...")
        # ImageMagick is used to unoptimized rather than Gifsicle's unoptimizer because Gifsicle doesn't support
        # unoptimization of GIFs with local color table
        gif_path = ImageMagickAPI.unoptimize_gif(gif_path, out_path)
    final_path = GifsicleAPI.modify_gif_image(gif_path, out_path, metadata, crbundle)
    return final_path


def _modify_apng(apng_path: Path, out_path: Path, metadata: AnimatedImageMetadata, crbundle: CriteriaBundle) -> Path:
    stdio.message("Modifying APNG...")
    mod_criteria = crbundle.modify_aimg_criteria
    aopt_criteria = crbundle.apng_opt_criteria
    apng_im: APNG = APNG.open(apng_path)
    stdio.debug({"crbundle": crbundle})
    # Reiterate through the frames if matching certain conditions, or per-frame lossy compression is required
    if mod_criteria.apng_must_reiterate(metadata) or aopt_criteria.is_reduced_color or aopt_criteria.is_unoptimized:
        stdio.debug(f"REITERATE APNG")
        new_apng: APNG = APNG()
        orig_width, orig_height = metadata.width["value"], metadata.height["value"]
        alpha_base = Image.new("RGBA", size=(orig_width, orig_height))
        unoptimized_apng_frames = list(InternalImageAPI.get_apng_frames(apng_im, unoptimize=True))
        if mod_criteria.reverse:
            unoptimized_apng_frames = reversed(unoptimized_apng_frames)
            
        orig_delays = [Fraction(f[1].delay, f[1].delay_den) if f[1] else 0 for f in unoptimized_apng_frames]
        stdio.error({"orig_delays": orig_delays})
        new_delays = mod_criteria.calculate_new_delay(metadata)
        # if mod_criteria.delay_handling == DelayHandling.EVEN_OUT:
        #     new_delays = [Fraction(mod_criteria.delay).limit_denominator() for _ in orig_delays]
        # elif mod_criteria.delay_handling == DelayHandling.MULTIPLY_AVERAGE:
        #     orig_avg_delay = sum(orig_delays) / len(orig_delays)
        #     delay_ratio = Fraction(mod_criteria.delay).limit_denominator() / orig_avg_delay
        #     stdio.error(f"delay ratio {delay_ratio}, {mod_criteria.delay}, {Fraction(mod_criteria.delay).limit_denominator()}, {orig_avg_delay}")
        #     new_delays = [delay_ratio * od for od in orig_delays]
        # elif mod_criteria.delay_handling == DelayHandling.DO_NOTHING:
        #     new_delays = orig_delays
        # else:
        #     raise Exception(f"Unknown delay handling method: {mod_criteria.delay_handling}")
        stdio.error({
            "new_delays": new_delays,
            "uaf": len(unoptimized_apng_frames)
        })
        for index, (im, control) in enumerate(unoptimized_apng_frames):
            # logger.debug(png.chunks)
            # delay_fraction = Fraction(1/mod_criteria.fps).limit_denominator()
            # delay = int(mod_criteria.delay * 1000)
            new_delay = new_delays[index]
            control.delay = new_delay.numerator
            control.delay_den = new_delay.denominator
            stdio.debug({
                "fr_control": control,
                "new_delay": new_delay,
            })
            if mod_criteria.must_transform(metadata) or aopt_criteria.is_reduced_color or aopt_criteria.convert_color_mode\
                    or aopt_criteria.is_unoptimized:
                # with io.BytesIO() as img_buf:
                #     png.save(img_buf)
                #     with Image.open(img_buf) as im:
                #         im.show()
                stdio.debug({"fr_orig_size": im.size})
                has_transparency = im.info.get("transparency") is not None or im.mode == "RGBA"
                im = im.resize(mod_criteria.size, resample=getattr(Image, mod_criteria.resize_method))
                im = im.transpose(Image.FLIP_LEFT_RIGHT) if mod_criteria.flip_x else im
                im = im.transpose(Image.FLIP_TOP_BOTTOM) if mod_criteria.flip_y else im
                if im.mode == "P":
                    if has_transparency:
                        im = im.convert("RGBA")
                    else:
                        im = im.convert("RGB")
                quant_method = Image.FASTOCTREE if has_transparency else Image.MEDIANCUT
                if aopt_criteria.is_reduced_color:
                    im = im.quantize(
                        aopt_criteria.color_count, method=quant_method, dither=1).convert("RGBA")
                if aopt_criteria.convert_color_mode:
                    im = im.convert(aopt_criteria.new_color_mode)
                with io.BytesIO() as new_buf:
                    im.save(new_buf, "PNG")
                    new_apng.append(PNG.from_bytes(new_buf.getvalue()), delay=new_delay.numerator,
                                    delay_den=new_delay.denominator)
        stdio.debug(f"NEW FRAMES COUNT: {len(new_apng.frames)}")
        if len(new_apng.frames) > 0:
            apng_im = new_apng
    apng_im.num_plays = mod_criteria.loop_count
    apng_im.save(out_path)
    if aopt_criteria.is_optimized:
        stdio.message(f"Optimizing APNG...")
        APNGOptAPI.optimize_apng(out_path, out_path, aopt_criteria)
    return out_path


def modify_aimg(img_path: Path, out_path: Path, crbundle: CriteriaBundle) -> Path:
    orig_attribute = inspect_general(img_path, filter_on="animated")
    if orig_attribute is None:
        raise Exception("Error: cannot load image")
    criteria = crbundle.modify_aimg_criteria
    change_format = criteria.change_format(orig_attribute)

    if change_format or criteria.must_transform(orig_attribute):
        stdio.debug(f"Rebuilding {orig_attribute.format} image into {criteria.format}...")
        return rebuild_aimg(img_path, out_path, orig_attribute, crbundle)
    else:
        stdio.debug(f"Modifying {criteria.format} image...")
        if criteria.format == ImageFormat.GIF:
            return _modify_gif(img_path, out_path, orig_attribute, crbundle)
        elif criteria.format == ImageFormat.PNG:
            return _modify_apng(img_path, out_path, orig_attribute, crbundle)

    # sicle_args = gifsicle_mod_args(criteria, gifopt_criteria)
    # magick_args = imagemagick_args(gifopt_criteria)
    # pq_args = pngquant_args(apngopt_criteria)
    # # yield sicle_args
    # target_path = str(img_path)
    # total_ops = 0
    # logger.message(criteria.change_format)
    # if criteria.change_format():
    #     if criteria.format == "PNG":
    #         # if
    #         :
    #         #     target_path = yield from _gifsicle_modify(sicle_args, target_path, orig_out_full_path, total_ops)
    #         # if magick_args:
    #         #     target_path = yield from _imagemagick_modify(magick_args, target_path, orig_out_full_path, total_ops, len(sicle_args))
    #         # yield {"preview_path": target_path}
    #         yield {"msg": f"Changing format ({criteria.orig_format} -> {criteria.format})"}
    #         target_path = yield from rebuild_aimg(target_path, out_dir, crbundle)
    #         if aopt_args:
    #             target_path = yield from APNGOptAPI.optimize_apng(
    #                 aopt_args,
    #                 target_path,
    #                 out_full_path,
    #                 total_ops,
    #                 len(sicle_args) + len(magick_args),
    #             )
    #     elif criteria.format == "GIF":
    #         yield {"msg": f"Changing format ({criteria.orig_format} -> {criteria.format})"}
    #         target_path = yield from rebuild_aimg(target_path, out_dir, crbundle)
    #         out_full_path = str(target_path)
    #         if sicle_args:
    #             target_path = yield from gifsicle_render(sicle_args, target_path, out_full_path, total_ops)
    #         if magick_args:
    #             target_path = yield from imagemagick_render(
    #                 magick_args, target_path, out_full_path, total_ops, len(sicle_args)
    #             )
    #         # yield {"preview_path": target_path}
    # else:
    #     if criteria.orig_format == "GIF":
    #         if criteria.gif_mustsplit_alteration():
    #             target_path = yield from rebuild_aimg(target_path, out_dir, crbundle)
    #         if sicle_args or criteria.renamed():
    #             target_path = yield from gifsicle_render(sicle_args, target_path, orig_out_full_path, total_ops)
    #         if magick_args:
    #             target_path = yield from imagemagick_render(
    #                 magick_args,
    #                 target_path,
    #                 orig_out_full_path,
    #                 total_ops,
    #                 len(sicle_args),
    #             )
    #         # yield {"preview_path": target_path}
    #     elif criteria.orig_format == "PNG":
    #         if criteria.apng_mustsplit_alteration() or pq_args or apngopt_criteria.is_unoptimized:
    #             target_path = yield from rebuild_aimg(target_path, out_dir, crbundle)
    #         if aopt_args:
    #             yield {"MSGGGGGGGGGGGGG": "AOPT ARGS"}
    #             target_path = yield from APNGOptAPI.optimize_apng(
    #                 aopt_args,
    #                 target_path,
    #                 out_full_path,
    #                 total_ops,
    #                 len(sicle_args) + len(magick_args),
    #             )
    #             # elif criteria.renamed():
    #             #     yield {"MSGGGGGGGGGGGGG": "RENAME"}
    #             if target_path != out_full_path:
    #                 shutil.copy(target_path, out_full_path)
    # logger.preview_path(target_path)
    # logger.control("MOD_FINISH")
