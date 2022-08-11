import os
import io
import shutil
# import numpy as np
from typing import List
from fractions import Fraction
from pathlib import Path

from PIL import Image
from apng import APNG, PNG

from pycore.core_funcs import stdio
from pycore.core_funcs.config import (
    STATIC_IMG_EXTS,
)
from pycore.models.criterion import (
    CreationCriteria,
    GIFOptimizationCriteria,
    CriteriaBundle,
)
from pycore.models.image_formats import ImageFormat
from pycore.utility import filehandler, imageutils
from pycore.bin_funcs.imager_api import GifsicleAPI, APNGOptAPI, PNGQuantAPI, InternalImageAPI
from pycore.imaging.gif import create_animated_gif


def _create_gifragments(image_paths: List[Path], criteria: CreationCriteria, gif_opt_criteria: GIFOptimizationCriteria):
    """Generate a sequence of static GIF images created from the input sequence with the specified criteria.

    Args:
        image_paths (List[Path]): List of image paths to be converted into GIF images.
        criteria (CreationCriteria): Creation criteria.
    """
    # disposal = 0
    # if criteria.reverse:
    #     image_paths.reverse()
    # temp_gifs = []
    out_dir = filehandler.mk_cache_dir(prefix_name="tmp_gifrags")
    fcount = len(image_paths)
    if criteria.start_frame:
        image_paths = imageutils.shift_image_sequence(image_paths, criteria.start_frame)
    shout_nums = imageutils.shout_indices(fcount, 1)
    black_bg = Image.new("RGBA", size=criteria.size)
    for index, ipath in enumerate(image_paths):
        if shout_nums.get(index):
            stdio.message(f"Processing frames... ({shout_nums.get(index)})")
        with Image.open(ipath) as im:
            im: Image.Image
            transparency = im.info.get("transparency", False)
            orig_width, orig_height = im.size
            alpha = None
            # if im.mode == "RGBA" and criteria.preserve_alpha:
            #     pass
            #     im = InternalImageAPI.dither_alpha(im)
            if criteria.flip_x:
                im = im.transpose(Image.FLIP_LEFT_RIGHT)
            if criteria.flip_y:
                im = im.transpose(Image.FLIP_TOP_BOTTOM)
            if criteria.must_resize(width=orig_width, height=orig_height):
                resize_method_enum = getattr(Image, criteria.resize_method)
                # yield {"resize_method_enum": resize_method_enum}
                im = im.resize(
                    (round(criteria.width), round(criteria.height)),
                    resample=resize_method_enum,
                )
            # if criteria.must_rotate():
            #     im = im.rotate(criteria.rotation, expand=True)
            fragment_name = str(ipath.name)
            if criteria.reverse:
                reverse_index = len(image_paths) - (index + 1)
                fragment_name = f"rev_{str.zfill(str(reverse_index), 6)}_{fragment_name}"
            else:
                fragment_name = f"{str.zfill(str(index), 6)}_{fragment_name}"
            save_path = out_dir.joinpath(f"{fragment_name}.gif")
            if im.mode == "RGBA":
                if gif_opt_criteria.is_dither_alpha:
                    stdio.debug(gif_opt_criteria.dither_alpha_threshold_value)
                    stdio.debug(gif_opt_criteria.dither_alpha_method_enum)
                    im = InternalImageAPI.dither_alpha(im, method=gif_opt_criteria.dither_alpha_method_enum,
                                                       threshold=gif_opt_criteria.dither_alpha_threshold_value)
                if criteria.preserve_alpha:
                    alpha = im.getchannel("A")
                    im = im.convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=255)
                    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
                    im.paste(255, mask)
                    im.info["transparency"] = 255
                else:
                    bg_image = black_bg.copy()
                    bg_image.alpha_composite(im)
                    # im.show()
                    im = bg_image
                    # black_bg.show()
                    im = im.convert("P", palette=Image.ADAPTIVE)
                im.save(save_path)
            elif im.mode == "RGB":
                im = im.convert("RGB").convert("P", palette=Image.ADAPTIVE)
                im.save(save_path)
            elif im.mode == "P":
                if transparency:
                    if type(transparency) is int:
                        im.save(save_path, transparency=transparency)
                    else:
                        im = im.convert("RGBA")
                        alpha = im.getchannel("A")
                        im = im.convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=255)
                        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
                        im.paste(255, mask)
                        im.info["transparency"] = 255
                        im.save(save_path)
                else:
                    im.save(save_path)
            # yield {"msg": f"Save path: {save_path}"}
            # if absolute_paths:
            # temp_gifs.append(save_path)
            # else:
            # temp_gifs.append(os.path.relpath(save_path, os.getcwd()))
    return out_dir


def _build_gif(image_paths: List, out_full_path: Path, crbundle: CriteriaBundle) -> Path:
    """Generate an animated GIF iamge by first applying transformations and lossy compression on them (if specified) and then converting them
    into singular static GIF images, before compiled by Gifsicle.

    Args:
        image_paths (List): List of path to each image in a sequence
        out_full_path (Path): Complete output path with the target name of the GIF.
        crbundle (CriteriaBundle): Bundle of animated image creation criteria to adhere to.

    Returns:
        Path: Path of the created GIF.
    """
    stdio.debug({"_build_gif crbundle": crbundle})
    gifragment_dir = _create_gifragments(image_paths, crbundle.create_aimg_criteria, crbundle.gif_opt_criteria)
    out_full_path = GifsicleAPI.combine_gif_images(gifragment_dir, out_full_path, crbundle)
    shutil.rmtree(gifragment_dir)
    stdio.preview_path(out_full_path)
    # logger.control("CRT_FINISH")
    return out_full_path


def _build_apng(image_paths: List[Path], out_full_path: Path, crbundle: CriteriaBundle) -> Path:
    criteria = crbundle.create_aimg_criteria
    aopt_criteria = crbundle.apng_opt_criteria
    # temp_dirs = []

    # if aopt_criteria.is_lossy:
        # qtemp_dir = mk_cache_dir(prefix_name="quant_temp")
        # temp_dirs.append(qtemp_dir)
        # image_paths = PNGQuantAPI.quantize_png_images(aopt_criteria, image_paths)
        # qsequence_info = {}
        # for index, ip in enumerate(image_paths):
        #     with Image.open(ip) as im:
        #         palette = im.getpalette()
        #         if palette:
        #             qimg_info = {
        #                 'colors': np.array(im.getcolors()),
        #                 'palette': imageutils.reshape_palette(palette),
        #                 'transparency': im.info.get('transparency')
        #             }
        #             qsequence_info[index] = qimg_info
        #             logger.debug(qimg_info)
                # im.resize((256, 256), Image.NEAREST).show()

    if criteria.reverse:
        image_paths.reverse()

    apng = APNG()
    img_sizes = set(Image.open(i).size for i in image_paths)
    stdio.message(str([f"({i[0]}, {i[1]})" for i in img_sizes]))
    uneven_sizes = len(img_sizes) > 1 or (criteria.width, criteria.height) not in img_sizes

    shout_nums = imageutils.shout_indices(len(image_paths), 1)
    # if criteria.flip_x or criteria.flip_y or uneven_sizes or aopt_criteria.is_lossy\
    #         or aopt_criteria.convert_color_mode:
    out_dir = filehandler.mk_cache_dir(prefix_name="tmp_apngfrags")
    preprocessed_paths = []
    # logger.debug(crbundle.create_aimg_criteria.__dict__)
    for index, ipath in enumerate(image_paths):
        fragment_name = str(ipath.name)
        if criteria.reverse:
            reverse_index = len(image_paths) - (index + 1)
            fragment_name = f"rev_{str.zfill(str(reverse_index), 6)}_{fragment_name}"
        else:
            fragment_name = f"{str.zfill(str(index), 6)}_{fragment_name}"
        save_path = out_dir.joinpath(f"{fragment_name}.png")
        if shout_nums.get(index):
            stdio.message(f"Processing frames... ({shout_nums.get(index)})")
        # with io.BytesIO() as bytebox:
        with Image.open(ipath) as im:
            im: Image.Image
            orig_width, orig_height = im.size
            has_transparency = im.info.get("transparency") is not None or im.mode == "RGBA"
            stdio.debug(f"Color mode im: {im.mode}")
            if criteria.must_resize(width=orig_width, height=orig_height):
                resize_method_enum = getattr(Image, criteria.resize_method)
                # yield {"resize_method_enum": resize_method_enum}
                im = im.resize(
                    (round(criteria.width), round(criteria.height)),
                    resize_method_enum,
                )
            im = im.transpose(Image.FLIP_LEFT_RIGHT) if criteria.flip_x else im
            im = im.transpose(Image.FLIP_TOP_BOTTOM) if criteria.flip_y else im
            if im.mode == "P":
                if has_transparency:
                    im = im.convert("RGBA")
                else:
                    im = im.convert("RGB")
            # if criteria.rotation:
            #     im = im.rotate(criteria.rotation, expand=True)
            # logger.debug(f"Modes comparison: {im.mode}, {aopt_criteria.new_color_mode}")
            quant_method = Image.FASTOCTREE if has_transparency else Image.MEDIANCUT
            if aopt_criteria.is_reduced_color:
                stdio.debug(f"Frame #{index}, has transparency: {has_transparency}, transparency: "
                             f"{im.info.get('transparency')}, quantization method: {quant_method}")
                im = im.quantize(aopt_criteria.color_count, method=quant_method).convert("RGBA")
            if aopt_criteria.convert_color_mode:
                im = im.convert(aopt_criteria.new_color_mode)
            # logger.debug(f"SAVE PATH IS: {save_path}")
            im.save(save_path, "PNG")
            if aopt_criteria.quantization_enabled:
                save_path = PNGQuantAPI.quantize_png_image(aopt_criteria, save_path)
            preprocessed_paths.append(save_path)
            # apng.append(PNG.from_bytes(bytebox.getvalue()), delay=int(criteria.delay * 1000))
    stdio.message("Saving APNG....")
    if criteria.start_frame:
        preprocessed_paths = imageutils.shift_image_sequence(preprocessed_paths, criteria.start_frame)
    delay_fraction = Fraction(1/criteria.fps).limit_denominator()
    apng = APNG.from_files(preprocessed_paths, delay=delay_fraction.numerator, delay_den=delay_fraction.denominator)
    apng.num_plays = criteria.loop_count
    apng.save(out_full_path)
    # else:
    #     logger.message("Saving APNG....")
    #     apng = APNG.from_files(image_paths, delay=int(criteria.delay * 1000))
    #     apng.num_plays = criteria.loop_count
    #     apng.save(out_full_path)

    if aopt_criteria.is_optimized:
        out_full_path = APNGOptAPI.optimize_apng(out_full_path, out_full_path, aopt_criteria)

    # for td in temp_dirs:
    #     shutil.rmtree(td)
    stdio.preview_path(out_full_path)
    # logger.control("CRT_FINISH")
    shutil.rmtree(out_dir)
    return out_full_path


def create_aimg(image_paths: List[Path], out_path: Path, crbundle: CriteriaBundle) -> Path:
    """ Umbrella generator for creating animated images from a sequence of images """
    # abs_image_paths = [os.path.abspath(ip) for ip in image_paths if os.path.exists(ip)]
    img_paths = [f for f in image_paths if str.lower(f.suffix[1:]) in STATIC_IMG_EXTS]
    # workpath = os.path.dirname(img_paths[0])
    # Test if inputted filename has extension, then remove it from the filename
    img_format = crbundle.create_aimg_criteria.format
    if len(img_paths) < 2:
        raise Exception(f"At least 2 images is needed for an animated {img_format}!")
    # if not out_dir:
    #     raise Exception("No output folder selected, please select it first")
    # out_dir = os.path.abspath(out_dir)
    # if not os.path.exists(out_dir):
    #     raise Exception(f"The specified absolute out_dir does not exist!\n{out_dir}")

    if img_format == ImageFormat.GIF:
        # out_full_path = out_dir.joinpath(f"{filename}.gif")
        # filename = f"{filename}.gif"
        out_full_path = create_animated_gif(img_paths, out_path, crbundle)
        return out_full_path
        # return _build_gif(img_paths, out_path, crbundle)

    elif img_format == ImageFormat.PNG:
        # out_full_path = out_dir.joinpath(f"{filename}.png")
        return _build_apng(img_paths, out_path, crbundle)
        # return _build_apng(img_paths, out_full_path, crbundle)
    else:
        stdio.error(f"The image format {img_format} is not supported")
