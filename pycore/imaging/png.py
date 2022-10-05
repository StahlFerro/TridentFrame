import os
import io
import shutil
# import numpy as np
from typing import List, Tuple
from fractions import Fraction
from pathlib import Path
from unittest import skip

from PIL import Image
from apng import APNG, PNG, FrameControl

from pycore.core_funcs import stdio
from pycore.core_funcs.config import (
    STATIC_IMG_EXTS,
)
from pycore.models.criterion import (
    CreationCriteria,
    GIFOptimizationCriteria,
    CriteriaBundle,
    CriteriaUtils,
)
from pycore.models.metadata import (
    AnimatedImageMetadata,
    ImageMetadata,
)
from pycore.models.image_formats import ImageFormat
from pycore.utility import filehandler, imageutils, vectorutils
from pycore.bin_funcs.imager_api import GifsicleAPI, APNGOptAPI, PNGQuantAPI, InternalImageAPI


def create_animated_png(image_paths: List[Path], out_full_path: Path, crbundle: CriteriaBundle) -> Path:
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
    # delays_list = criteria.delays_list
    # logger.debug(crbundle.create_aimg_criteria.__dict__)
    # frame_skip_count_mult = criteria.frame_skip_count + 1
    frames_info = criteria.get_frames_info(len(image_paths))
    computed_delays_list = []
    for index, ipath in enumerate(image_paths):
        if frames_info[index]['is_skipped']:
            continue
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
        computed_delays_list.append(frames_info[index]['delay'])
            # apng.append(PNG.from_bytes(bytebox.getvalue()), delay=int(criteria.delay * 1000))
    stdio.message("Saving APNG....")
    stdio.debug(frames_info)
    stdio.debug(computed_delays_list)
    if criteria.start_frame:
        preprocessed_paths = imageutils.shift_image_sequence(preprocessed_paths, criteria.start_frame)
        # delays_list = vectorutils.shift_items(delays_list, criteria.start_frame)
        computed_delays_list = vectorutils.shift_items(computed_delays_list, criteria.start_frame)
        
    if criteria.delays_are_even:
        average_computed_delay = criteria._compute_average_delay(frames_info)
        delay_fraction = Fraction(round(average_computed_delay, 4)).limit_denominator()
        # delay_fraction = Fraction(round(1/criteria.fps * frame_skip_count_mult, 4)).limit_denominator()
        apng = APNG.from_files(preprocessed_paths, delay=delay_fraction.numerator, delay_den=delay_fraction.denominator)
    else:
        for index, preproc_path in enumerate(preprocessed_paths):
            frame_delay = computed_delays_list[index]
            delay_fraction = Fraction(round(frame_delay, 4)).limit_denominator()
            apng.append(PNG.open_any(preproc_path), delay=int(delay_fraction.numerator), delay_den=int(delay_fraction.denominator))
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
    # stdio.preview_path(out_full_path)
    # logger.control("CRT_FINISH")
    shutil.rmtree(out_dir)
    return out_full_path
  
  
def modify_animated_png(apng_path: Path, out_path: Path, metadata: AnimatedImageMetadata, crbundle: CriteriaBundle) -> Path:
    stdio.message("Modifying APNG...")
    mod_criteria = crbundle.modify_aimg_criteria
    aopt_criteria = crbundle.apng_opt_criteria
    apng_im: APNG = APNG.open(apng_path)
    stdio.debug({"crbundle": crbundle})
    # Reiterate through the frames if matching certain conditions, or per-frame lossy compression is required
    if mod_criteria.apng_must_reiterate(metadata) or aopt_criteria.is_reduced_color or aopt_criteria.is_unoptimized:
        stdio.debug(f"REITERATE APNG")
        new_apng: APNG = APNG()
        # orig_width, orig_height = metadata.width["value"], metadata.height["value"]
        unoptimized_apng_frames: List[Tuple[Image.Image, FrameControl]] = list(InternalImageAPI.get_apng_frames(apng_im, unoptimize=True))
        
        if mod_criteria.reverse:
            unoptimized_apng_frames = list(reversed(unoptimized_apng_frames))
            
        new_delays = CriteriaUtils.calculate_new_delays(mod_criteria, metadata)
        # orig_delays = [Fraction(f[1].delay, f[1].delay_den) if f[1] else 0 for f in unoptimized_apng_frames]
        # stdio.error({"orig_delays": orig_delays})
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
        # stdio.error({
        #     "new_delays": new_delays,
        #     "uaf": len(unoptimized_apng_frames)
        # })
        shout_nums = imageutils.shout_indices(len(unoptimized_apng_frames), 1)
        for index, (im, control) in enumerate(unoptimized_apng_frames):
            if shout_nums.get(index):
                stdio.message(f"Modifying APNG frames... ({shout_nums.get(index)})")
            # logger.debug(png.chunks)
            # delay_fraction = Fraction(1/mod_criteria.fps).limit_denominator()
            # delay = int(mod_criteria.delay * 1000)
            new_delay = round(new_delays[index], 4)
            control.delay = new_delay.numerator
            control.delay_den = new_delay.denominator
            # stdio.debug({
            #     "fr_control": control,
            #     "new_delay": new_delay,
            # })
            if mod_criteria.must_transform(metadata) or mod_criteria.reverse or aopt_criteria.is_reduced_color or aopt_criteria.convert_color_mode\
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