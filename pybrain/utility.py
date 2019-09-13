import os
import shutil
import time
import subprocess
from typing import List, Tuple

from PIL import Image
from PIL.GifImagePlugin import GifImageFile
from apng import APNG

from .config import gifsicle_exec, imagemagick_exec, ABS_CACHE_PATH
from .criterion import CreationCriteria, SplitCriteria, ModificationCriteria
# from .create_ops import create_aimg
# from .split_ops import split_aimg


def _filter_images(image_paths, option="static"):
    for i in image_paths:
        name, ext = os.path.splitext(os.path.basename(i))
        im = Image.open(i)
        if type(im) is GifImageFile and im.n_frames > 1:
            continue
        apng = APNG.open(i)
        if len(apng.frames) > 1:
            continue
        yield i


def _purge_cache():
    for stuff in os.listdir(ABS_CACHE_PATH):
        stuff_path = os.path.join(ABS_CACHE_PATH, stuff)
        try:
            if os.path.isfile(stuff_path):
                os.unlink(stuff_path)
            elif os.path.isdir(stuff_path):
                shutil.rmtree(stuff_path)
        except Exception as e:
            raise Exception(e)


def _mk_temp_dir(prefix_name: str = ''):
    dirname = time.strftime("%Y%m%d_%H%M%S")
    if prefix_name:
        dirname = f"{prefix_name}_{dirname}"
    temp_dir = os.path.join(ABS_CACHE_PATH, dirname)
    os.mkdir(temp_dir)
    return temp_dir


def _unoptimize_gif(gif_path, out_dir, decoder: str) -> str:
    """ Perform GIF unoptimization using Gifsicle/ImageMagick, in order to obtain the true singular frames for Splitting purposes. Returns the path of the unoptimized GIF """
    unop_gif_save_path = os.path.join(out_dir, os.path.basename(gif_path))
    if decoder == 'imagemagick':
        args = [imagemagick_exec(), "-coalesce", gif_path, unop_gif_save_path]
    elif decoder == 'gifsicle':
        args = [gifsicle_exec(), "-b", "--unoptimize", gif_path, "--output", unop_gif_save_path]
    cmd = ' '.join(args)
    print(cmd)
    subprocess.run(cmd, shell=True)
    return unop_gif_save_path


def _reduce_color(gif_path, out_dir, color: int = 256) -> str:
    " Reduce the color of a gif. Overwrites the GIF "
    print("Performing color reduction...")
    executable = gifsicle_exec()
    redux_gif_path = os.path.join(out_dir, os.path.basename(gif_path))
    args = [executable, f"--colors={color}", gif_path, "--output", redux_gif_path]
    cmd = ' '.join(args)
    subprocess.run(cmd, shell=True)
    return redux_gif_path


def _delete_temp_images():
    # raise Exception(os.getcwd())
    temp_dir = os.path.abspath('temp')
    # raise Exception(os.getcwd(), temp_dir)
    # raise Exception(image_name, path)
    # os.remove(path)
    temp_aimgs = [os.path.join(temp_dir, i) for i in os.listdir(temp_dir)]
    for ta in temp_aimgs:
        os.remove(ta)
    return True


def _restore_disposed_frames(frame_paths: List[str]):
    """ Pastes the target_frame over the first_frame (applied when restoring GIF frames). Overrides every single frames on disk """
    im = Image.open(frame_paths[0])
    # im.transparency = 0
    im = im.convert("RGBA")
    fm = []
    for index, f in enumerate(frame_paths):
        frame = Image.open(f)
        # frame.transparency = 0
        frame = frame.convert("RGBA")
        # frame.show()
        fm.append((frame.mode, im.info))
        # im.paste(frame)
        frame.save(f, "PNG")
        yield f"Coalescing frames... ({index + 1}/{len(frame_paths)})"
    # yield '\n'.join(fm)
    

def _log(message):
    return {"log": message}


def generate_gifsicle_args(criteria: ModificationCriteria):
    args = []
    if criteria.must_resize():
        args.append(f"--resize={criteria.width}x{criteria.height}")
    if criteria.is_optimized:
        args.append(f"--optimize={criteria.optimization_level}")
    if criteria.is_lossy:
        args.append(f"--lossy={criteria.lossy_value}")
    if criteria.is_reduced_color:
        args.append(f"--colors={criteria.color_space}")
    if criteria.flip_x:
        args.append("--flip-horizontal")
    if criteria.flip_y:
        args.append("--flip-vertical")
    return args


def generate_imagemagick_args(criteria: ModificationCriteria):
    args = []
    if not criteria.rotation:
        args.append(f"-rotation {criteria.rotation}")
    return args

# def gs_build():
#     gifsicle_exec = os.path.abspath("./bin/gifsicle-1.92-win64/gifsicle.exe")
#     orig_path = os.path.abspath('./test/orig2/')
#     images = [os.path.abspath(os.path.join(orig_path, f)) for f in os.listdir(orig_path)]
#     out_dir = os.path.abspath('./test/')
#     criteria = CreationCriteria(fps=50, extension='gif', transparent=True, reverse=False)
#     create_aimg(images, out_dir, "sicle_test", criteria)
    

# def gs_split(gif_path: str, out_dir: str):
#     criteria = SplitCriteria(pad_count=3, is_duration_sensitive=False)
#     # pprint(criteria.__dict__)
#     split_aimg(gif_path, out_dir, criteria)


# if __name__ == "__main__":
#     gs_build()
