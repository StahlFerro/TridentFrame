import shutil

import PIL.Image
from PIL import Image
from pathlib import Path
from typing import List, Tuple
import hitherdither
from pycore.core_funcs import stdio
from pycore.models.criterion import CriteriaBundle, GIFOptimizationCriteria
from pycore.models.metadata import ImageMetadata, AnimatedImageMetadata
from pycore.bin_funcs.imager_api import InternalImageAPI, GifsicleAPI, ImageMagickAPI
from pycore.imaging.generic import transform_image
from pycore.utility import filehandler, imageutils


def create_animated_gif(image_paths: List, out_full_path: Path, crbundle: CriteriaBundle) -> Path:
    """Generate an animated GIF image by first applying transformations and lossy compression on them (if specified)
        and then converting them into singular static GIF images to a temporary directory, before compiled by Gifsicle.

    Args:
        image_paths (List): List of path to each image in a sequence
        crbundle (CriteriaBundle): Bundle of animated image creation criteria to adhere to.
        out_full_path (Path): Complete output path with the target name of the GIF.

    Returns:
        Path: Path of the created GIF.
    """
    criteria = crbundle.create_aimg_criteria
    stdio.debug({"_build_gif crbundle": crbundle})
    black_bg_rgba = Image.new("RGBA", size=criteria.size, color=(0, 0, 0, 255))
    target_dir = filehandler.mk_cache_dir(prefix_name="tmp_gifrags")
    fcount = len(image_paths)
    if criteria.start_frame:
        image_paths = imageutils.shift_image_sequence(image_paths, criteria.start_frame)
    skip_frame_mult = criteria.skip_frame + 1
    shout_nums = imageutils.shout_indices(fcount, 1)
    for index, ipath in enumerate(image_paths):
        if skip_frame_mult > 1:
            im_number = index + 1
            if im_number % skip_frame_mult == 0:
                continue
        if shout_nums.get(index):
            stdio.message(f"Processing frames... ({shout_nums.get(index)})")
        with Image.open(ipath) as im:
            im = transform_image(im, crbundle.create_aimg_criteria)
            im = gif_encode(im, crbundle, black_bg_rgba)

            fragment_name = str(ipath.name)
            if criteria.reverse:
                reverse_index = len(image_paths) - (index + 1)
                fragment_name = f"rev_{str.zfill(str(reverse_index), 6)}_{fragment_name}"
            else:
                fragment_name = f"{str.zfill(str(index), 6)}_{fragment_name}"
            save_path = target_dir.joinpath(f"{fragment_name}.gif")

            im.save(save_path)

    out_full_path = GifsicleAPI.combine_gif_images(target_dir, out_full_path, crbundle)
    shutil.rmtree(target_dir)
    # logger.control("CRT_FINISH")
    return out_full_path


def modify_animated_gif(gif_path: Path, out_path: Path, metadata: AnimatedImageMetadata, crbundle: CriteriaBundle) -> Path:
    if crbundle.gif_opt_criteria.is_unoptimized:
        stdio.message("Unoptimizing GIF...")
        # ImageMagick is used to unoptimized rather than Gifsicle's unoptimizer because Gifsicle doesn't support
        # unoptimization of GIFs with local color table
        gif_path = ImageMagickAPI.unoptimize_gif(gif_path, out_path)
    final_path = GifsicleAPI.modify_gif_image(gif_path, out_path, metadata, crbundle)
    return final_path


def palletize_image(im: PIL.Image.Image, dither_method: str, palletization_method: str) -> PIL.Image.Image:
    pil_pal_enum = 1
    if palletization_method == "ADAPTIVE":
        pil_pal_enum = Image.ADAPTIVE
    elif palletization_method == "WEB":
        pil_pal_enum = Image.WEB
    
    if dither_method == "FLOYD_STEINBERG":
        im = im.convert("RGB").convert("P", palette=pil_pal_enum, colors=255, dither=Image.FLOYDSTEINBERG)
    elif dither_method == "BAYER":
        im = im.convert("RGB")
        palette = hitherdither.palette.Palette.create_by_median_cut(im)
        im = hitherdither.ordered.bayer.bayer_dithering(im, palette, [256/4, 256/4, 256/4], order=8)
    elif dither_method == "YLILUOMA_1":
        palette = hitherdither.palette.Palette(
            [0x080000, 0x201A0B, 0x432817, 0x492910,
            0x234309, 0x5D4F1E, 0x9C6B20, 0xA9220F,
            0x2B347C, 0x2B7409, 0xD0CA40, 0xE8A077,
            0x6A94AB, 0xD5C4B3, 0xFCE76E, 0xFCFAE2]
        )
        im = hitherdither.ordered.yliluoma.yliluomas_1_ordered_dithering(im, palette, order=8)
    elif dither_method == "NONE":
        im = im.convert("RGB").convert("P", palette=pil_pal_enum, colors=255, dither=Image.NONE)
    return im


def has_rgba_use(im: PIL.Image.Image) -> bool:
    """Checks whether or not a RGBA PNG image's alpha channel is used (has transparent/translucent pixels)

    Args:
        im (PIL.Image.Image): RGBA PNG image's alpha

    Returns:
        bool: True if the image has transparent/translucent pixels
    """
    for pixel in im.getdata():
        # stdio.warn(pixel)
        if pixel != 255:
            return True
    return False


def gif_encode(im: PIL.Image.Image, crbundle: CriteriaBundle, bg_im: PIL.Image.Image) -> PIL.Image.Image:
    """
    Encodes any Pillow image into a GIF image
    Args:
        im (Image): Pillow image
        crbundle: Criteria bundle
        bg_im: Fallback background image if the image will be saved without transparency

    Returns:
        Image: GIF-encoded image
    """
    criteria = crbundle.create_aimg_criteria
    gif_opt_criteria = crbundle.gif_opt_criteria
    transparency = im.info.get("transparency", False)
    
    if im.mode == "RGBA":
        if gif_opt_criteria.is_dither_alpha:
            # stdio.debug(gif_opt_criteria.dither_alpha_threshold_value)
            # stdio.debug(gif_opt_criteria.dither_alpha_method_enum)
            im = InternalImageAPI.dither_alpha(im, method=gif_opt_criteria.dither_alpha_method_enum,
                                               threshold=gif_opt_criteria.dither_alpha_threshold_value)
        if criteria.preserve_alpha:
            alpha = im.getchannel("A")
            
            try:
                im = palletize_image(im, gif_opt_criteria.dither_method, gif_opt_criteria.palletization_method)
            except Exception:
                stdio.warn(f"Fail to palletize image using method: {gif_opt_criteria.dither_method}, falling back to FLOYD_STEINBERG...")
                im = palletize_image(im, "FLOYD_STEINBERG", gif_opt_criteria.palletization_method)
            
            mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
            im.paste(255, mask)
            im.info["transparency"] = 255
        else:  # If alpha is not preserved, composite over black image regardless whether or not the RGBA image has any actual transparent/translucent pixels
            alpha = im.getchannel("A")
            # If all the pixels are opaque, the alpha channel of the image is unused
            if has_rgba_use(alpha):
                # stdio.warn("Warning: This RGBA PNG image doesn't use its alpha channel on any pixels!")

                # stdio.warn("Has alpha, compositing black...")
                bg_image = bg_im.copy()
                bg_image.alpha_composite(im)
                im = bg_image
                # im.show()
                # black_bg.show()
                
                try:
                    im = palletize_image(im, gif_opt_criteria.dither_method, gif_opt_criteria.palletization_method)
                except Exception:
                    stdio.warn(f"Fail to palletize image using method: {gif_opt_criteria.dither_method}, falling back to FLOYD_STEINBERG...")
                    im = palletize_image(im, "FLOYD_STEINBERG", gif_opt_criteria.palletization_method)

            else:
                # stdio.warn("Warning: This RGBA PNG image doesn't use its alpha channel on any pixels!")
                
                try:
                    im = palletize_image(im, gif_opt_criteria.dither_method, gif_opt_criteria.palletization_method)
                except Exception:
                    stdio.warn(f"Fail to palletize image using method: {gif_opt_criteria.dither_method}, falling back to FLOYD_STEINBERG...")
                    im = palletize_image(im, "FLOYD_STEINBERG", gif_opt_criteria.palletization_method)
            # im = im.convert("RGB")
            # palette = hitherdither.palette.Palette.create_by_median_cut(im)
            # im = hitherdither.ordered.bayer.bayer_dithering(
            #     im, palette, [256/4, 256/4, 256/4], order=8)
            # im = hitherdither.ordered.cluster.cluster_dot_dithering(im, palette, [256/4, 256/4, 256/4], order=8)

            # im = im.convert("RGB")
            # im.show()
            # im = im.convert("P", palette=Image.WEB, dither=Image.FLOYDSTEINBERG)
            # im.show()
            # im.show()
        # im.save(save_path)
    elif im.mode == "RGB":
        
        # im = im.convert("RGB")
        try:
            im = palletize_image(im, gif_opt_criteria.dither_method, gif_opt_criteria.palletization_method)
        except Exception:
            stdio.warn(f"Fail to palletize image using method: {gif_opt_criteria.dither_method}, falling back to FLOYD_STEINBERG...")
            im = palletize_image(im, "FLOYD_STEINBERG", gif_opt_criteria.palletization_method)
            
        # im = hitherdither.ordered.bayer.bayer_dithering(
        #     im, palette, [256/4, 256/4, 256/4], order=8)
        # im = hitherdither.ordered.bayer.bayer_dithering(im, palette, [256/4, 256/4, 256/4], order=8)
        
        # im = im.convert("RGB").convert("P", palette=Image.ADAPTIVE)
        # im.save(save_path)
    elif im.mode == "P":
        if transparency:
            if type(transparency) is int:
                pass
                # im.save(save_path, transparency=transparency)
            else:
                im = im.convert("RGBA")
                alpha = im.getchannel("A")
                im = palletize_image(im, gif_opt_criteria.dither_method, gif_opt_criteria.palletization_method)
                # im = im.convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=255)
                mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
                im.paste(255, mask)
                im.info["transparency"] = 255
                # im.save(save_path)
        else:
            pass
            # im.save(save_path)
            
    return im
