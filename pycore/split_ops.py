import io
import shutil
from pathlib import Path
from copy import deepcopy
from heapq import nsmallest
from typing import List, Tuple, Iterator

from PIL import Image
from apng import APNG

from .bin_funcs.imager_api import GifsicleAPI, ImageMagickAPI, APNGDisAPI, InternalImageAPI
from .core_funcs.config import (
    ANIMATED_IMG_EXTS,
)
from pycore.models.criterion import SplitCriteria
from .utility import filehandler, imageutils
from .core_funcs import logger


def _get_aimg_delay_ratios(aimg_path: Path, aimg_type: str, duration_sensitive: bool = False) -> List[Tuple[str, str]]:
    """Returns a list of dual-valued tuples, first value being the frame numbers of the GIF, second being the ratio
    of the frame's delay to the lowest delay
    Args:
        aimg_path: Path to the animated image.
        aimg_type: Animated image type.
        duration_sensitive:

    Returns:

    """
    indexed_ratios = []
    if aimg_type == "GIF":
        with Image.open(aimg_path) as gif:
            indices = list(range(0, gif.n_frames))
            delays = []
            for i in indices:
                gif.seek(i)
                delays.append(gif.info["duration"])
            min_delays = min(delays)
            if duration_sensitive:
                ratios = [d // min_delays for d in delays]
            else:
                ratios = [1 for d in delays]
            indexed_ratios.extend(list(zip(indices, ratios)))
    elif aimg_type == "PNG":
        frames = APNG.open(aimg_path).frames
        indices = list(range(0, len(frames)))
        # Get the delay of every frames. Set zero if frame control chunk f[1] is None (this may occur in some APNGs)
        delays = [f[1].delay if f[1] else 0 for f in frames]
        # raise Exception(list(delays))
        # Delays fix for frames with no control chunks
        if 0 in delays:
            actual_min = nsmallest(2, set(delays))[-1]
            # Replace those zeroes in the delays generator
            delays = [actual_min if d == 0 else d for d in delays]
            # raise Exception(actual_min, list(delays))
        min_delays = min(delays)
        if duration_sensitive:
            ratios = [d // min_delays for d in delays]
        else:
            ratios = [1 for d in delays]
        indexed_ratios.extend(list(zip(indices, ratios)))
    return indexed_ratios


# def _pillow_fragment_gif_frames(unop_gif_path: str, out_dir: str, criteria: SplitCriteria):
#     """ Currently UNUSED. Missing pixels """
#     gif = Image.open(unop_gif_path)
#     orig_name = os.path.splitext(os.path.basename(unop_gif_path))[0]
#     indexed_ratios = _get_gif_delay_ratios(unop_gif_path, criteria.is_duration_sensitive)
#     total_ratio = sum([ir[1] for ir in indexed_ratios])
#     sequence = 0
#     gifragment_paths = []
#     for index, ratio in indexed_ratios:
#         selector = f'"#{index}"'
#         gif.seek(index)
#         for n in range(0, ratio):
#             yield f"Splitting GIF... ({sequence + 1}/{total_ratio})"
#             save_path = os.path.join(out_dir, f'{orig_name}_{str.zfill(str(sequence), criteria.pad_count)}.png')
#             gif.save(save_path, "PNG")
#             sequence += 1


# def _fragment_gif_frames(unop_gif_path: Path, name: str, criteria: SplitCriteria) -> List[Image.Image]:
#     """
#     Split GIF frames and return them as a list of PIL.Image.Images using Gifsicle based on the specified criteria

#     Args:
#         unop_gif_path (Path): Path to unoptimized GIF
#         name (str): New name of the sequence
#         criteria (SplitCriteria): Criteria

#     Returns:
#         List[Image.Image]: List of the split images as Pillow Image
#     """
#     fragment_dir = filehandler.mk_cache_dir(prefix_name="fragment_dir")
#     frames = []
#     indexed_ratios = _get_aimg_delay_ratios(unop_gif_path, "GIF", criteria.is_duration_sensitive)
#     total_frames = sum([ir[1] for ir in indexed_ratios])
#     cumulative_index = 0
#     gifsicle_path = imager_exec_path("gifsicle")
#     shout_nums = imageutils.shout_indices(total_frames, 5)
#     for index, ratio in indexed_ratios:
#         if shout_nums.get(cumulative_index):
#             logger.message(f"Splitting frames... ({shout_nums.get(index)})")
#         selector = f'#{index}'
#         for n in range(0, ratio):
#             logger.message(f"Splitting GIF... ({cumulative_index + 1}/{total_frames})")
#             dir_path = fragment_dir.joinpath(f"{name}_{str.zfill(str(cumulative_index), criteria.pad_count)}.png")
#             args = [
#                 str(gifsicle_path),
#                 str(unop_gif_path),
#                 selector,
#                 "--output",
#                 str(dir_path)
#             ]
#             cmd = " ".join(args)
#             logger.message(cmd)
#             subprocess.run(args)
#             # process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#             # while process.poll() is None:
#             #     output = process.stdout.readline()
#             #     # if process.poll() is not None:
#             #     # break
#             #     if output:
#             #         output = output.decode("utf-8")
#             #         logger.message(output.capitalize())
#             cumulative_index += 1
#             with Image.open(dir_path).convert("RGBA") as im:
#                 # if gif.info.get('transparency'):
#                 #     yield {"msg": "Palette has transparency"}
#                 #     gif = gif.convert('RGBA')
#                 # else:
#                 #     yield {"msg": "Palette has no transparency"}
#                 #     gif = gif.convert('RGB')
#                 frames.append(im)
#     # shutil.rmtree(fragment_dir)
#     return frames


def _split_gif(gif_path: Path, out_dir: Path, criteria: SplitCriteria) -> List[Path]:
    """Unoptimizes GIF, and then splits the frames into separate images

    Args:
        gif_path (Path): Path to the GIF image
        out_dir (Path): Output directory of the image sequence
        criteria (SplitCriteria): Image splitting criteria

    Raises:
        Exception: [description]

    Returns:
        List[Path]: Paths to each split images
    """
    frame_paths = []
    name = criteria.new_name or gif_path.stem
    # unop_dir = filehandler.mk_cache_dir(prefix_name="unop_gif")
    # unop_gif_path = unop_dir.joinpath(gif_path.name)
    # color_space = criteria.color_space
    target_path = Path(gif_path)
    logger.message(str(target_path))
    # if color_space:
    #     if color_space < 2 or color_space > 256:
    #         raise Exception("Color space must be between 2 and 256!")
    #     else:
    #         logger.message(f"Reducing colors to {color_space}...")
    #         target_path = GifsicleAPI.reduce_gif_color(gif_path, unop_gif_path, color=color_space)

    # ===== Start test splitting code =====
    # gif: GifImageFile = GifImageFile(gif_path)
    # for index in range(0, gif.n_frames):
    #     gif.seek(index)
    #     gif.show()
    #     new = gif.convert("RGBA")
    #     new.show()

    # with io.BytesIO() as bytebox:
    #     gif.save(bytebox, "GIF")
    #     yield {"bytebox": bytebox.getvalue()}
    # yield {"GIFINFO": [f"{d} {getattr(gif, d, '')}" for d in gif.__dir__()]}
    # ===== End test splitting code =====

    if criteria.is_unoptimized:
        logger.message("Unoptimizing and splitting GIF...")
        # ImageMagick is used to unoptimized rather than Gifsicle's unoptimizer because Gifsicle doesn't support
        # unoptimization of GIFs with local color table
        # target_path = ImageMagickAPI.unoptimize_gif(gif_path, unop_gif_path)
        frame_paths = ImageMagickAPI.extract_unoptimized_gif_frames(gif_path, name, criteria, out_dir)
    else:
        logger.message("Splitting GIF...")
        # frames = _fragment_gif_frames(target_path, name, criteria)
        frame_paths = GifsicleAPI.extract_gif_frames(target_path, name, criteria, out_dir)
    # gif = Image.open(gif_path)

    if criteria.convert_to_rgba:
        shout_nums = imageutils.shout_indices(len(frame_paths), 5)
        for index, fpath in enumerate(frame_paths):
            # gif.seek(index)
            if shout_nums.get(index):
                logger.message(f"Converting frames into RGBA color mode... ({shout_nums.get(index)})")
            # save_path = out_dir.joinpath(f"{save_name}_{str.zfill(str(index), criteria.pad_count)}.png")
            with Image.open(fpath).convert("RGBA") as im:
                # alpha = im.getchannel("A")
                # im = im.convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=255)
                # mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
                # im.paste(255, mask)
                # im.info["transparency"] = 255
                im.save(fpath, "PNG")
            # else:
            #     with Image.open(fpath, formats=["GIF"]) as im:
            #         if index in range(0, 4):
            #             im.show()
            #         logger.debug(im.info)
            #         im.save(fpath, "GIF")
    if criteria.extract_delay_info:
        logger.message("Generating delay information file...")
        imageutils.generate_delay_file(gif_path, "GIF", out_dir)
    # shutil.rmtree(unop_dir)
    logger.debug({"frame_paths": frame_paths})
    return frame_paths


# def _fragment_apng_frames(apng_path: Path, criteria: SplitCriteria) -> Iterator[Image.Image]:
#     apng_im = APNG.open(apng_path)
#     canvas: Image.Image
#     for index, (png, control) in enumerate(apng_im.frames):
#         final_im: Image.Image
#         with io.BytesIO() as img_buf:
#             png.save(img_buf)
#             with Image.open(img_buf) as im:
#                 logger.debug({"index": index, "control": control, "mode": im.mode, "info": im.info})
#                 if index == 0 or not criteria.is_unoptimized:
#                     canvas = im.copy()
#                     yield canvas.copy()
#                 else:
#                     prev_canvas = canvas.copy()
#                     offsets = control.x_offset, control.y_offset
#                     if control.blend_op == 0:
#                         canvas.paste(im, box=offsets)
#                     elif control.blend_op == 1:
#                         canvas.alpha_composite(im, dest=offsets)
#                     yield canvas.copy()
#                     if control.depose_op == 1:
#                         tp_mask: Image.Image
#                         if im.mode == "P":
#                             tp_mask = Image.new("P", size=im.size)
#                             tp_mask.info["transparency"] = 0
#                         elif im.mode == "RGB":
#                             tp_color = im.info.get("transparency") if im.info.get("transparency") is not None else \
#                                 [0, 0, 0]
#                             logger.debug({"tp_color": tp_color})
#                             tp_mask = Image.new("RGB", size=im.size, color=tp_color)
#                             tp_mask.info["transparency"] = tp_color
#                             # tp_mask.show()
#                         elif im.mode == "RGBA":
#                             tp_mask = Image.new("RGBA", size=im.size)
#                         canvas.paste(tp_mask, box=offsets)
#                     elif control.depose_op == 2:
#                         canvas = prev_canvas.copy()


# def _fragment_apng_frames_old(apng_path: Path, criteria: SplitCriteria) -> List[Image.Image]:
#     """Extracts all frames of an APNG and returns them as Pillow Images
#
#     Args:
#         apng_path (Path): Path to the APNG
#         criteria (SplitCriteria): Splitting criteria to follow
#
#     Returns:
#         List[Image.Image]: List of APNG's image frames, each as a Pillow Image
#     """
#     # def _fragment_apng_frames(apng: APNG, criteria: SplitCriteria) -> List[Image.Image]:
#     #     """ Accepts an APNG, and then returns a list of PIL.Image.Images for each of the frames. """
#     frames = []
#     # indexed_ratios = _get_aimg_delay_ratios(apng_path, "PNG", duration_sensitive=criteria.is_duration_sensitive)
#     # logger.message(list(indexed_ratios))
#     if criteria.is_unoptimized:
#         logger.message("Unoptimizing and splitting APNG...")
#         fragment_paths = APNGDisAPI.split_apng(apng_path, criteria.new_name)
#         # fragment_paths = sorted(list(fragment_paths), key=lambda fragment: str(fragment))
#         # for fp in fragment_paths:
#         #     logger.message(str(fp))
#         #     frames.append(Image.open(fp))
#         # frames = list(TridentFrameImagingAPI.get_apng_true_frames(APNG.open(apng_path)))
#     else:
#         logger.message("Splitting APNG...")
#         apng = APNG.open(apng_path)
#         iframes = apng.frames
#         fcount = len(iframes)
#         pad_count = max(len(str(fcount)), 3)
#         shout_nums = imageutils.shout_indices(fcount, 5)
#         first_png = iframes[0][0]
#         base_stack_image: Image.Image
#         with io.BytesIO() as firstbox:
#             first_png.save(firstbox)
#             with Image.open(firstbox) as first_im:
#                 first_im = first_im.convert("RGBA")
#                 base_stack_image: Image = first_im.copy()
#         # yield {"MODE FIRST": base_stack_image.mode}
#         # yield {"msg": iframes[0][1].__dict__}
#         # separate_stack_image: Image.Image = Image.new("RGBA", base_stack_image.size)
#         depose_blend_ops = []
#         rerender = False
#         width = iframes[0][0].width
#         height = iframes[0][0].height
#         base_alpha = Image.new("RGBA", (width, height))
#         output_buffer = Image.new("RGBA", base_stack_image.size)
#         for index, (png, control) in enumerate(iframes):
#             # if control:
#             #     out_control(control.__dict__)
#             if shout_nums.get(index):
#                 logger.message(f"Splitting APNG... ({shout_nums.get(index)})")
#             with io.BytesIO() as bytebox:
#                 png.save(bytebox)
#                 with Image.open(bytebox).convert("RGBA") as im:
#                     # if criteria.is_unoptimized:
#                     #     # if control.blend_op == 0:
#                     #     #     output_buffer = base_alpha.copy()
#                     #     if control.depose_op == 0:
#                     #         output_buffer.alpha_composite(im, (control.x_offset, control.y_offset))
#                     #         frames.append(output_buffer.copy())
#                     #     elif control.depose_op == 1:
#                     #         output_buffer.alpha_composite(im, (control.x_offset, control.y_offset))
#                     #         frames.append(output_buffer.copy())
#                     #         output_buffer = base_alpha.copy()
#                     #     elif control.depose_op == 2:
#                     #         separate_buffer = output_buffer.copy()
#                     #         separate_buffer.alpha_composite(im, (control.x_offset, control.y_offset))
#                     #         frames.append(separate_buffer.copy())
#                     # OLD ALGORITHM 2
#                     # if not control or (control and control.blend_op == 0 and control.depose_op != 1):
#                     #     yield {"MSG": "control blend 0, full overwrite"}
#                     #     if im.size != base_stack_image.size:
#                     #         alpha_pad = Image.new("RGBA", base_stack_image.size)
#                     #         alpha_pad.alpha_composite(im, (control.x_offset if control else 0, control.y_offset
#                     #         if control else 0))
#                     #         frames.append(alpha_pad.copy())
#                     #     else:
#                     #         frames.append(im)
#                     # if control and (control.blend_op == 1 or control.depose_op == 1):
#                     #     yield {"MSG": "control blend 1, managing..."}
#                     #     if control.depose_op in [0, 1]:
#                     #         base_stack_image.paste(im, (control.x_offset if control else 0, control.y_offset
#                     #         if control else 0), im)
#                     #         frames.append(base_stack_image.copy())
#                     #     elif control.depose_op == 2:
#                     #         temp_stack = base_stack_image.copy()
#                     #         temp_stack.paste(im, (control.x_offset if control else 0, control.y_offset if control
#                     #         else 0), im)
#                     #         frames.append(temp_stack.copy())
#
#                     # OLD Algorithm
#                     # # im = im.convert("RGBA")
#                     # # yield {"CONTROL": control.depose_op}
#                     # if rerender:
#                     #     newplain = Image.new("RGBA", base_stack_image.size)
#                     #     newplain.paste(im, (control.x_offset, control.y_offset), im)
#                     #     frames.append(newplain.copy())
#                     #     rerender = False
#                     # else:
#                     #     if control and (control.depose_op == 2 or control.depose_op == 1):
#                     #         separate_stack = base_stack_image.copy()
#                     #         separate_stack.paste(im, (control.x_offset, control.y_offset), im)
#                     #         frames.append(separate_stack.copy())
#                     #         if index == 0 and control.depose_op == 1:
#                     #             rerender = True
#                     #         # separate_stack.show()
#                     #     # elif control.depose_op == 1:
#                     #     #     frames.append(im.copy())
#                     #     elif not control or control.depose_op == 0:
#                     #         base_stack_image.paste(im, (control.x_offset if control else 0, control.y_offset if
#                     #         control else 0), im)
#                     #         frames.append(base_stack_image.copy())
#                     #     # base_stack_image.show()
#                     # else:
#                     frames.append(im)
#                     # if control:
#                     #     depose_blend_ops.append(f"blend: {control.blend_op}, depose: {control.depose_op}, x_off:
#                     #     {control.x_offset}, y_off: {control.y_offset}")
#                     # else:
#                     #     depose_blend_ops.append("NO CONTROL")
#         # for fr in frames:
#         #     fr.show()
#         # logger.message(str(depose_blend_ops))
#     # if not all(ratio == 1 for index, ratio in indexed_ratios):
#     #     logger.message("REORDER RATIOS")
#     #     rationed_frames = []
#     #     for index, ratio in indexed_ratios:
#     #         for n in range(0, ratio):
#     #             rationed_frames.append(frames[index])
#     #     frames = deepcopy(rationed_frames)
#     #     del rationed_frames
#     return frames


# def imageutils.generate_delay_file()

# def _fragment_apng_frames(apng: APNG, criteria: SplitCriteria) -> List[Image.Image]:
#     """ Accepts an APNG, and then returns a list of PIL.Image.Images for each of the frames. """
#     frames = []
#     iframes = apng.frames
#     fcount = len(iframes)
#     pad_count = max(len(str(fcount)), 3)
#     shout_nums = imageutils.shout_indices(fcount, 5)
#     first_png = iframes[0][0]
#     base_stack_image: Image.Image
#     with io.BytesIO() as firstbox:
#         first_png.save(firstbox)
#         with Image.open(firstbox) as im:
#             im = im.convert("RGBA")
#             base_stack_image: Image = im.copy()
#     # yield {"MODE FIRST": base_stack_image.mode}
#     depose_blend_ops = [{}]
#     # rerender = False
#     for index, (png, control) in enumerate(iframes):
#         if shout_nums.get(index):
#             yield {"msg": f'Splitting APNG... ({shout_nums.get(index)})'}
#         with io.BytesIO() as bytebox:
#             png.save(bytebox)
#             with Image.open(bytebox).convert("RGBA") as im:
#                 # yield {"MSG": control.__dict__}
#                 if criteria.is_unoptimized:
#                     # im = im.convert("RGBA")
#                     # yield {"CONTROL": control.depose_op}
#                     # if rerender:
#                     # else:
#                     if control.depose_op == 2:
#                         separate_stack = base_stack_image.copy()
#                         separate_stack.paste(im, (control.x_offset, control.y_offset), im)
#                         frames.append(separate_stack.copy())
#                         # if index == 0 and control.depose_op == 1:
#                             # rerender = True
#                         # separate_stack.show()
#                     elif control.depose_op == 1 or control.blend_op == 0:
#                         newplain = Image.new("RGBA", base_stack_image.size)
#                         newplain.paste(im, (control.x_offset, control.y_offset), im)
#                         frames.append(newplain.copy())
#                         # rerender = False
#                     elif control.depose_op == 0:
#                         base_stack_image.paste(im, (control.x_offset, control.y_offset), im)
#                         frames.append(base_stack_image.copy())
#                     # base_stack_image.show()
#                 else:
#                     frames.append(im)
#                 depose_blend_ops.append((control.depose_op, control.blend_op))
#     # for fr in frames:
#     #     fr.show()
#     yield {"DEPOSE_BLEND_OPS": depose_blend_ops}
#     return frames


def _split_apng(apng_path: Path, out_dir: Path, name: str, criteria: SplitCriteria) -> List[Path]:
    """Extracts all of the frames of an animated PNG into a folder

    Args:
        apng_path (Path): Path to the APNG.
        out_dir (Path): Path to the output directory.
        name (str): New prefix name of the sequence.
        criteria (SplitCriteria): Splitting criteria to follow.

    Returns:
        List[Path]: List of paths for every split image.
    """
    frame_paths = []
    apng = APNG.open(apng_path)
    apng_frames = InternalImageAPI.get_apng_frames(apng, criteria.is_unoptimized)
    # frames = _fragment_apng_frames(apng_path, criteria)
    pad_count = criteria.pad_count
    shout_nums = imageutils.shout_indices(len(apng.frames), 5)
    save_name = criteria.new_name or name
    for index, (fr, control) in enumerate(apng_frames):
        if shout_nums.get(index):
            logger.message(f"Saving split frames... ({shout_nums.get(index)})")
        save_path = out_dir.joinpath(f"{save_name}_{str.zfill(str(index), pad_count)}.png")
        fr.save(save_path, format="PNG")
        frame_paths.append(save_path)
    if criteria.extract_delay_info:
        logger.message("Generating delay information file...")
        imageutils.generate_delay_file(apng_path, "PNG", out_dir)
    return frame_paths


def split_aimg(image_path: Path, out_dir: Path, criteria: SplitCriteria) -> List[Path]:
    """Umbrella function for splitting animated images into individual frames

    Args:
        image_path (Path): Path to animated image
        out_dir (Path): Path to output directory
        criteria (SplitCriteria): Criteria to follow for splitting the animated image

    Raises:
        Exception: [description]
        Exception: [description]
        Exception: [description]

    Returns:
        List[Path]: List of paths for each split images
    """
    # print(error)
    frame_paths = []
    name = image_path.stem
    try:
        ext = image_path.suffixes[-1]
    except Exception:
        raise Exception("Image needs to have an extension!")
    ext = str.lower(ext[1:])
    # raise Exception(fname, ext)
    if ext not in ANIMATED_IMG_EXTS:
        raise Exception("Only supported extensions are .gif and .png (for APNG)")
    if ext == "gif":
        frame_paths = _split_gif(image_path, out_dir, criteria)
    elif ext == "png":
        frame_paths = _split_apng(image_path, out_dir, name, criteria)
    logger.control("SPL_FINISH")
    return frame_paths


# if __name__ == "__main__":
#     pprint(inspect_sequence(""))

# gs_split("./test/blobsekiro.gif", "./test/sequence/")
# test()
# _unoptimize_gif("./test/blobkiro.gif")
