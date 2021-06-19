import os
import io
import shutil
from pathlib import Path

from PIL import Image
from apng import APNG, PNG

from pycore.models.criterion import (
    CriteriaBundle,
)
from pycore.utility import filehandler
from pycore.bin_funcs.imager_api import GifsicleAPI, ImageMagickAPI, APNGOptAPI
from pycore.models.metadata import ImageMetadata, AnimatedImageMetadata
from pycore.models.criterion import CreationCriteria, SplitCriteria
from pycore.core_funcs import logger
from pycore.inspect_ops import inspect_general
from pycore.create_ops import create_aimg
from pycore.split_ops import split_aimg


def rebuild_aimg(img_path: Path, out_path: Path, metadata: AnimatedImageMetadata, crbundle: CriteriaBundle):
    mod_criteria = crbundle.modify_aimg_criteria
    aopt_criteria = crbundle.apng_opt_criteria
    frames_dir = filehandler.mk_cache_dir(prefix_name="presplit_images")
    has_transparency = metadata.transparency is not None
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
    return new_image_path


def _modify_gif(gif_path: Path, out_path: Path, metadata: AnimatedImageMetadata, crbundle: CriteriaBundle) -> Path:
    if crbundle.gif_opt_criteria.is_unoptimized:
        logger.message("Unoptimizing GIF...")
        # ImageMagick is used to unoptimized rather than Gifsicle's unoptimizer because Gifsicle doesn't support
        # unoptimization of GIFs with local color table
        gif_path = ImageMagickAPI.unoptimize_gif(gif_path, out_path)
    final_path = GifsicleAPI.modify_gif_image(gif_path, out_path, metadata, crbundle)
    return final_path


def _modify_apng(apng_path: Path, out_path: Path, metadata: AnimatedImageMetadata, crbundle: CriteriaBundle) -> Path:
    logger.message("Modifying APNG...")
    mod_criteria = crbundle.modify_aimg_criteria
    aopt_criteria = crbundle.apng_opt_criteria
    apng_im: APNG = APNG.open(apng_path)
    # Reiterate through the frames if matching certain conditions, or per-frame lossy compression is required
    if mod_criteria.apng_must_reiterate(metadata) or aopt_criteria.is_lossy:
        logger.debug(f"REITERATE APNG")
        new_apng: APNG = APNG()
        for index, (png, control) in enumerate(apng_im.frames):
            # logger.debug(png.chunks)
            delay = int(mod_criteria.delay * 1000)
            control.delay = delay
            if mod_criteria.must_transform(metadata) or aopt_criteria.is_lossy or aopt_criteria.convert_color_mode:
                with io.BytesIO() as img_buf:
                    png.save(img_buf)
                    with Image.open(img_buf) as im:
                        im = im.resize((mod_criteria.width, mod_criteria.height),
                                       resample=getattr(Image, mod_criteria.resize_method))
                        if im.mode == "P":
                            im = im.convert("RGBA")
                        if aopt_criteria.is_lossy:
                            im = im.quantize(
                                aopt_criteria.lossy_value, method=Image.FASTOCTREE, dither=1).convert("RGBA")
                        if aopt_criteria.convert_color_mode:
                            im = im.convert(aopt_criteria.new_color_mode)
                        with io.BytesIO() as new_buf:
                            im.save(new_buf, "PNG")
                            new_apng.append(PNG.from_bytes(new_buf.getvalue()), delay=delay)
        logger.debug(f"NEW FRAMES COUNT: {len(new_apng.frames)}")
        if len(new_apng.frames) > 0:
            apng_im = new_apng
    apng_im.num_plays = mod_criteria.loop_count
    apng_im.save(out_path)
    logger.message(f"Optimizing APNG...")
    if aopt_criteria.is_optimized:
        APNGOptAPI.optimize_apng(out_path, out_path, aopt_criteria)
    logger.error(Image.open(out_path).mode)
    return out_path


def modify_aimg(img_path: Path, out_path: Path, crbundle: CriteriaBundle) -> Path:
    orig_attribute = inspect_general(img_path, filter_on="animated")
    if orig_attribute is None:
        raise Exception("Error: cannot load image")
    criteria = crbundle.modify_aimg_criteria
    change_format = criteria.change_format(orig_attribute)

    if change_format or criteria.gif_must_rebuild():
        logger.message("Rebuilding im...")
        return rebuild_aimg(img_path, out_path, orig_attribute, crbundle)
    else:
        logger.message("Modifying im...")
        if criteria.format == "GIF":
            return _modify_gif(img_path, out_path, orig_attribute, crbundle)
        elif criteria.format == "PNG":
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
