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
from copy import deepcopy
from heapq import nsmallest

from PIL import Image, ImageChops
from PIL.GifImagePlugin import GifImageFile
from apng import APNG, PNG

from .bin_funcs.imager_api import apngdis_split
from .core_funcs.config import IMG_EXTS, ANIMATED_IMG_EXTS, STATIC_IMG_EXTS, ABS_CACHE_PATH, imager_exec_path
from .core_funcs.criterion import SplitCriteria
from .core_funcs.utility import _mk_temp_dir, _reduce_color, _unoptimize_gif, _log, shout_indices, generate_delay_file


def _get_aimg_delay_ratios(aimg_path: str, aimg_type: str, duration_sensitive: bool = False) -> List[Tuple[str, str]]:
    """ Returns a list of dual-valued tuples, first value being the frame numbers of the GIF, second being the ratio of the frame's delay to the lowest delay"""
    indexed_ratios = []
    if aimg_type == 'GIF':
        with Image.open(aimg_path) as gif:
            indices = list(range(0, gif.n_frames))
            delays = []
            for i in indices:
                gif.seek(i)
                delays.append(gif.info['duration'])
            min_delays = min(delays)
            if duration_sensitive:
                ratios = [d//min_delays for d in delays]
            else:
                ratios = [1 for d in delays]
            indexed_ratios.extend(list(zip(indices, ratios)))
    elif aimg_type == 'PNG':
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
            ratios = [d//min_delays for d in delays]
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


def _fragment_gif_frames(unop_gif_path: str, name: str, criteria: SplitCriteria) -> List[Image.Image]:
    fragment_dir = _mk_temp_dir(prefix_name="fragment_dir")
    """ Split GIF frames and return them as a list of PIL.Image.Images using Gifsicle based on the specified criteria"""
    frames = []
    indexed_ratios = _get_aimg_delay_ratios(unop_gif_path, "GIF", criteria.is_duration_sensitive)
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
    # shutil.rmtree(fragment_dir)
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
    save_name = criteria.new_name or name
    for index, fr in enumerate(frames):
        if shout_nums.get(index):
            yield {"msg": f'Saving frames... ({shout_nums.get(index)})'}
        save_path = os.path.join(out_dir, f'{save_name}_{str.zfill(str(index), criteria.pad_count)}.png')
        fr.save(save_path, "PNG")
        frame_paths.append(save_path)
    if criteria.will_generate_delay_info:
        yield {"msg": "Generating delay information file..."}
        generate_delay_file(gif_path, "GIF", out_dir)
    return frame_paths


def _fragment_apng_frames(apng_path: str, criteria: SplitCriteria) -> List[Image.Image]:
    """ Accepts the path of an APNG, and then returns a list of PIL.Image.Images for each of the frames. """
# def _fragment_apng_frames(apng: APNG, criteria: SplitCriteria) -> List[Image.Image]:
#     """ Accepts an APNG, and then returns a list of PIL.Image.Images for each of the frames. """
    frames = []
    indexed_ratios = _get_aimg_delay_ratios(apng_path, "PNG", duration_sensitive=criteria.is_duration_sensitive)
    yield {"INDEXED RATIOS": list(indexed_ratios)}
    if criteria.is_unoptimized:
        yield {"msg": "Unoptimizing and splitting APNG..."}
        fragment_paths = yield from apngdis_split(apng_path, criteria.new_name)
        for fp in fragment_paths:
            frames.append(Image.open(fp))
    else:
        apng = APNG.open(apng_path)
        iframes = apng.frames
        fcount = len(iframes)
        pad_count = max(len(str(fcount)), 3)
        shout_nums = shout_indices(fcount, 5)
        first_png = iframes[0][0]
        base_stack_image: Image.Image
        with io.BytesIO() as firstbox:
            first_png.save(firstbox)
            with Image.open(firstbox) as first_im:
                first_im = first_im.convert("RGBA")
                base_stack_image: Image = first_im.copy()
        # yield {"MODE FIRST": base_stack_image.mode}
        # yield {"msg": iframes[0][1].__dict__}
        separate_stack_image: Image.Image = Image.new("RGBA", base_stack_image.size)
        depose_blend_ops = []
        rerender = False
        width = iframes[0][0].width
        height = iframes[0][0].height
        base_alpha = Image.new("RGBA", (width, height))
        output_buffer = Image.new('RGBA', base_stack_image.size)
        for index, (png, control) in enumerate(iframes):
            if control:
                yield {"CONTROL": control.__dict__}
            if shout_nums.get(index):
                yield {"msg": f'Splitting APNG... ({shout_nums.get(index)})'}
            with io.BytesIO() as bytebox:
                png.save(bytebox)
                with Image.open(bytebox).convert("RGBA") as im:
                    # if criteria.is_unoptimized:
                    #     # if control.blend_op == 0:
                    #     #     output_buffer = base_alpha.copy()
                    #     if control.depose_op == 0:
                    #         output_buffer.alpha_composite(im, (control.x_offset, control.y_offset))
                    #         frames.append(output_buffer.copy())
                    #     elif control.depose_op == 1:
                    #         output_buffer.alpha_composite(im, (control.x_offset, control.y_offset))
                    #         frames.append(output_buffer.copy())
                    #         output_buffer = base_alpha.copy()
                    #     elif control.depose_op == 2:
                    #         separate_buffer = output_buffer.copy()
                    #         separate_buffer.alpha_composite(im, (control.x_offset, control.y_offset))
                    #         frames.append(separate_buffer.copy())
                        # OLD ALGORITHM 2
                        # if not control or (control and control.blend_op == 0 and control.depose_op != 1):
                        #     yield {"MSG": "control blend 0, full overwrite"}
                        #     if im.size != base_stack_image.size:
                        #         alpha_pad = Image.new("RGBA", base_stack_image.size)
                        #         alpha_pad.alpha_composite(im, (control.x_offset if control else 0, control.y_offset if control else 0))
                        #         frames.append(alpha_pad.copy())
                        #     else:
                        #         frames.append(im)
                        # if control and (control.blend_op == 1 or control.depose_op == 1):
                        #     yield {"MSG": "control blend 1, managing..."}
                        #     if control.depose_op in [0, 1]:
                        #         base_stack_image.paste(im, (control.x_offset if control else 0, control.y_offset if control else 0), im)
                        #         frames.append(base_stack_image.copy())
                        #     elif control.depose_op == 2:
                        #         temp_stack = base_stack_image.copy()
                        #         temp_stack.paste(im, (control.x_offset if control else 0, control.y_offset if control else 0), im)
                        #         frames.append(temp_stack.copy())

                        # OLD Algorithm
                        # # im = im.convert("RGBA")
                        # # yield {"CONTROL": control.depose_op}
                        # if rerender:
                        #     newplain = Image.new("RGBA", base_stack_image.size)
                        #     newplain.paste(im, (control.x_offset, control.y_offset), im)
                        #     frames.append(newplain.copy())
                        #     rerender = False
                        # else:
                        #     if control and (control.depose_op == 2 or control.depose_op == 1):
                        #         separate_stack = base_stack_image.copy()
                        #         separate_stack.paste(im, (control.x_offset, control.y_offset), im)
                        #         frames.append(separate_stack.copy())
                        #         if index == 0 and control.depose_op == 1:
                        #             rerender = True
                        #         # separate_stack.show()
                        #     # elif control.depose_op == 1:
                        #     #     frames.append(im.copy())
                        #     elif not control or control.depose_op == 0:
                        #         base_stack_image.paste(im, (control.x_offset if control else 0, control.y_offset if control else 0), im)
                        #         frames.append(base_stack_image.copy())
                        #     # base_stack_image.show()
                    # else:
                    frames.append(im)
                    # if control:
                    #     depose_blend_ops.append(f"blend: {control.blend_op}, depose: {control.depose_op}, x_off: {control.x_offset}, y_off: {control.y_offset}")
                    # else:
                    #     depose_blend_ops.append("NO CONTROL")
        # for fr in frames:
        #     fr.show()
        yield {"DEPOSE_BLEND_OPS": depose_blend_ops}
    if not all(ratio == 1 for index, ratio in indexed_ratios):
        yield {"msg": "REORDER RATIOS"}
        rationed_frames = []
        for index, ratio in indexed_ratios:
            for n in range(0, ratio):
                rationed_frames.append(frames[index])
        frames = deepcopy(rationed_frames)
        del rationed_frames
    return frames

# def generate_delay_file()

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
    frames = yield from _fragment_apng_frames(apng_path, criteria)
    pad_count = criteria.pad_count
    shout_nums = shout_indices(len(frames), 5)
    save_name = criteria.new_name or name
    for index, fr in enumerate(frames):
        if shout_nums.get(index):
            yield {"msg": f'Saving split frames... ({shout_nums.get(index)})'}
        save_path = os.path.join(out_dir, f"{save_name}_{str.zfill(str(index), pad_count)}.png")
        fr.save(save_path)
        frame_paths.append(save_path)
    if criteria.will_generate_delay_info:
        yield {"msg": "Generating delay information file..."}
        generate_delay_file(apng_path, "PNG", out_dir)
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
