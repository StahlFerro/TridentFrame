import os
import io
import string
import shutil
import math
import time
import subprocess
import tempfile
from random import choices
from pprint import pprint
from urllib.parse import urlparse
from typing import List, Dict, Tuple
from datetime import datetime

from PIL import Image, ImageChops
from PIL.GifImagePlugin import GifImageFile
from apng import APNG, PNG
from hurry.filesize import size, alternative

from .core_funcs.config import IMG_EXTS, ANIMATED_IMG_EXTS, STATIC_IMG_EXTS, ABS_CACHE_PATH, imager_exec_path
from .core_funcs.criterion import SplitCriteria
from .core_funcs.utility import _mk_temp_dir, _reduce_color, _unoptimize_gif, _log, shout_indices


def _get_gif_delay_ratios(gif_path: str, duration_sensitive: bool = False) -> List[Tuple[str, str]]:
    """ Returns a list of dual-valued tuples, first value being the frame numbers of the GIF, second being the ratio of the frame's delay to the lowest delay"""
    with Image.open(gif_path) as gif:
        indices = list(range(0, gif.n_frames))
        durations = []
        for i in indices:
            gif.seek(i)
            durations.append(gif.info['duration'])
        min_duration = min(durations)
        if duration_sensitive:
            ratios = [dur//min_duration for dur in durations]
        else:
            ratios = [1 for dur in durations]
        indexed_ratios = list(zip(indices, ratios))
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


def _fragment_gif_frames(unop_gif_path: str, name: str, criteria: SplitCriteria) -> List[Image.Image]:
    fragment_dir = _mk_temp_dir(prefix_name="fragment_dir")
    """ Split GIF frames and return them as a list of PIL.Image.Images using Gifsicle based on the specified criteria"""
    frames = []
    indexed_ratios = _get_gif_delay_ratios(unop_gif_path, criteria.is_duration_sensitive)
    total_frames = sum([ir[1] for ir in indexed_ratios])
    cumulative_index = 0
    gifsicle_path = imager_exec_path('gifsicle')
    shout_nums = shout_indices(total_frames, 5)
    for index, ratio in indexed_ratios:
        if shout_nums.get(cumulative_index):
            yield {"msg": f'Splitting frames... ({shout_nums.get(index)})'}
        selector = f'"#{index}"'
        for n in range(0, ratio):
            # yield {"msg": f"Splitting GIF... ({cumulative_index + 1}/{total_frames})"}
            dir_path = os.path.join(fragment_dir, f'{name}_{str.zfill(str(cumulative_index), criteria.pad_count)}.png')
            args = [gifsicle_path, f'"{unop_gif_path}"', selector, "--output", f'"{dir_path}"']
            cmd = ' '.join(args)
            subprocess.run(cmd, shell=True)
            cumulative_index += 1
            with Image.open(dir_path).convert("RGBA") as im:
            # if gif.info.get('transparency'):
            #     yield {"msg": "Palette has transparency"}
            #     gif = gif.convert('RGBA')
            # else:
            #     yield {"msg": "Palette has no transparency"}
            #     gif = gif.convert('RGB')
                frames.append(im)
    shutil.rmtree(fragment_dir)
    return frames


def _split_gif(gif_path: str, out_dir: str, criteria: SplitCriteria):
    """ Unoptimizes GIF, and then splits the frames into separate images """
    frame_paths = []
    name = os.path.splitext(os.path.basename(gif_path))[0]
    unop_dir = _mk_temp_dir(prefix_name="unop_gif")
    color_space = criteria.color_space
    target_path = gif_path
    if color_space:
        if color_space < 2 or color_space > 256:
            raise Exception("Color space must be between 2 and 256!")
        else:
            yield {"msg": f"Reducing colors to {color_space}..."}
            target_path = _reduce_color(gif_path, unop_dir, color=color_space)

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
        yield {"msg": f"Unoptimizing GIF..."}
        target_path = _unoptimize_gif(gif_path, unop_dir, "imagemagick")
    frames = yield from _fragment_gif_frames(target_path, name, criteria)
    shout_nums = shout_indices(len(frames), 5)
    for index, fr in enumerate(frames):
        if shout_nums.get(index):
            yield {"msg": f'Saving frames... ({shout_nums.get(index)})'}
        save_path = os.path.join(out_dir, f'{name}_{str.zfill(str(index), criteria.pad_count)}.png')
        fr.save(save_path, "PNG")
        frame_paths.append(save_path)
    return frame_paths


def _fragment_apng_frames(apng: APNG, criteria: SplitCriteria) -> List[Image.Image]:
    """ Accepts an APNG, and then returns a list of PIL.Image.Images for each of the frames. """
    frames = []
    iframes = apng.frames
    fcount = len(iframes)
    pad_count = max(len(str(fcount)), 3)
    shout_nums = shout_indices(fcount, 5)
    first_png = iframes[0][0]
    base_stack_image: Image.Image
    with io.BytesIO() as firstbox:
        first_png.save(firstbox)
        with Image.open(firstbox) as im:
            im = im.convert("RGBA")
            base_stack_image: Image = im.copy()
    # yield {"MODE FIRST": base_stack_image.mode}
    depose_blend_ops = []
    rerender = False
    for index, (png, control) in enumerate(iframes):
        if shout_nums.get(index):
            yield {"msg": f'Splitting APNG... ({shout_nums.get(index)})'}
        with io.BytesIO() as bytebox:
            png.save(bytebox)
            with Image.open(bytebox).convert("RGBA") as im:
                # yield {"MSG": control.__dict__}
                if criteria.is_unoptimized:
                    # im = im.convert("RGBA")
                    # yield {"CONTROL": control.depose_op}
                    if rerender:
                        newplain = Image.new("RGBA", base_stack_image.size)
                        newplain.paste(im, (control.x_offset, control.y_offset), im)
                        frames.append(newplain.copy())
                        rerender = False
                    else:
                        if control and (control.depose_op == 2 or control.depose_op == 1):
                            separate_stack = base_stack_image.copy()
                            separate_stack.paste(im, (control.x_offset, control.y_offset), im)
                            frames.append(separate_stack.copy())
                            if index == 0 and control.depose_op == 1:
                                rerender = True
                            # separate_stack.show()
                        # elif control.depose_op == 1:
                        #     frames.append(im.copy())
                        elif not control or control.depose_op == 0:
                            base_stack_image.paste(im, (control.x_offset if control else 0, control.y_offset if control else 0), im)
                            frames.append(base_stack_image.copy())
                        # base_stack_image.show()
                else:
                    frames.append(im)
                if control:
                    depose_blend_ops.append((control.depose_op, control.blend_op))
                else:
                    depose_blend_ops.append(("", ""))
    # for fr in frames:
    #     fr.show()
    yield {"DEPOSE_BLEND_OPS": depose_blend_ops}
    return frames


# def _fragment_apng_frames(apng: APNG, criteria: SplitCriteria) -> List[Image.Image]:
#     """ Accepts an APNG, and then returns a list of PIL.Image.Images for each of the frames. """
#     frames = []
#     iframes = apng.frames
#     fcount = len(iframes)
#     pad_count = max(len(str(fcount)), 3)
#     shout_nums = shout_indices(fcount, 5)
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




def _split_apng(apng_path: str, out_dir: str, name: str, criteria: SplitCriteria):
    """ Extracts all of the frames of an animated PNG into a folder and return a list of each of the frames' absolute paths """
    frame_paths = []
    apng: APNG = APNG.open(apng_path)
    frames = yield from _fragment_apng_frames(apng, criteria)
    pad_count = criteria.pad_count
    shout_nums = shout_indices(len(frames), 5)
    for index, fr in enumerate(frames):
        if shout_nums.get(index):
            yield {"msg": f'Saving split frames... ({shout_nums.get(index)})'}
        save_path = os.path.join(out_dir, f"{name}_{str.zfill(str(index), pad_count)}.png")
        fr.save(save_path)
        frame_paths.append(save_path)
    return frame_paths


def split_aimg(image_path: str, out_dir: str, criteria: SplitCriteria):
    """ Umbrella function for splitting animated images into individual frames """
    # print(error)
    frame_paths = []
    image_path = os.path.abspath(image_path)
    if not os.path.isfile(image_path):
        raise Exception("Oi skrubman the path here seems to be a bloody directory, should've been a file", image_path)
    filename = str(os.path.basename(image_path))

    # Custom output dirname and frame names if specified on the cli
    if '.' not in filename:
        raise Exception('Where the fuk is the extension mate?!')

    name, ext = os.path.splitext(filename)
    ext = str.lower(ext[1:])
    # raise Exception(fname, ext)
    if ext not in ANIMATED_IMG_EXTS:
        raise Exception('Only supported extensions are gif and apng. Sry lad')

    out_dir = os.path.abspath(out_dir)
    if ext == 'gif':
        frame_paths = yield from _split_gif(image_path, out_dir, criteria)

    elif ext == 'png':
        frame_paths = yield from _split_apng(image_path, out_dir, name, criteria)
    yield {"CONTROL": "SPL_FINISH"}
    return frame_paths

# if __name__ == "__main__":
#     pprint(inspect_sequence(""))

    # gs_split("./test/blobsekiro.gif", "./test/sequence/")
    # test()
    # _unoptimize_gif("./test/blobkiro.gif")
