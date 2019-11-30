import os
import shutil
import time
import subprocess
from typing import List, Tuple, Dict

from PIL import Image
from PIL.GifImagePlugin import GifImageFile
from apng import APNG

from .config import ABS_CACHE_PATH, ABS_TEMP_PATH, imager_exec_path
from .criterion import CreationCriteria, SplitCriteria, ModificationCriteria
# from .create_ops import create_aimg
# from .split_ops import split_aimg


size_suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


def _filter_images(image_paths, option="static"):
    """ Filter out image whether they are static images or animated images """
    ipath_tuples = []
    for path in image_paths:
        name, ext = os.path.splitext(os.path.basename(path))
        im = Image.open(path)
        if type(im) is GifImageFile and im.n_frames > 1:
            continue
        apng = APNG.open(path)
        if len(apng.frames) > 1:
            continue
        ipath_tuples.append((im, path))
    return ipath_tuples


# def _purge_cache():
#     abs_cache_path = ABS_CACHE_PATH()
#     _purge_directory(abs_cache_path)


# def _purge_temp():
#     abs_temp_path = ABS_TEMP_PATH()
#     _purge_directory(abs_temp_path)


def _purge_directory(target_folder):
    for stuff in os.listdir(target_folder):
        stuff_path = os.path.join(target_folder, stuff)
        try:
            name, ext = os.path.splitext(stuff_path)
            if os.path.isfile(stuff_path) and ext:
                os.unlink(stuff_path)
            elif os.path.isdir(stuff_path):
                shutil.rmtree(stuff_path)
        except Exception as e:
            raise Exception(e)


def _mk_temp_dir(prefix_name: str = ''):
    """ Creates a temporary directory for AIMG manipulation purposes. Returns the absolute path """
    dirname = time.strftime("%Y%m%d_%H%M%S")
    if prefix_name:
        dirname = f"{prefix_name}_{dirname}"
    temp_dir = os.path.join(ABS_CACHE_PATH(), dirname)
    # raise Exception(temp_dir, os.getcwd())
    os.mkdir(temp_dir)
    return temp_dir


def _unoptimize_gif(gif_path, out_dir, decoder: str) -> str:
    """ Perform GIF unoptimization using Gifsicle/ImageMagick, in order to obtain the true singular frames for Splitting purposes. Returns the path of the unoptimized GIF """
    # raise Exception(gif_path, out_dir)
    unop_gif_save_path = os.path.join(out_dir, os.path.basename(gif_path))
    imager_path = imager_exec_path(decoder)
    if decoder == 'imagemagick':
        args = [imager_path, "-coalesce", f'"{gif_path}"', f'"{unop_gif_save_path}"']
    elif decoder == 'gifsicle':
        args = [imager_path, "-b", "--unoptimize", f'"{gif_path}"', "--output", f'"{unop_gif_save_path}"']
    cmd = ' '.join(args)
    # print(cmd)
    subprocess.run(cmd, shell=True)
    return unop_gif_save_path


def _reduce_color(gif_path, out_dir, color: int = 256) -> str:
    " Reduce the color of a gif. Returns the reduxed GIF path"
    print("Performing color reduction...")
    gifsicle_path = imager_exec_path('gifsicle')
    redux_gif_path = os.path.join(out_dir, os.path.basename(gif_path))
    args = [gifsicle_path, f"--colors={color}", gif_path, "--output", redux_gif_path]
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
    

def read_filesize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(size_suffixes)-1:
        nbytes /= 1024.
        i += 1
    size = str(round(nbytes, 3)).rstrip('0').rstrip('.')
    return f"{size} {size_suffixes[i]}"


def shout_indices(frame_count: int, percentage_skip: int) -> Dict[int, str]:
    """ Returns a dictionary of indices for message yielding, with the specified percentage skip. Examples:\n
        shout_incides(24, 50) -> {0: "0%", 12: "50%"}\n
        shout_indices(40, 25) -> {0: "0%", 10: "25%", 20: "50%", 30: "75%"}
    """
    mults = 100 // percentage_skip
    return {round(frame_count / mults * mult): f"{mult * percentage_skip}%" for mult in range(0, mults)}

        

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
