import os
from pycore.core_funcs.output_printer import out_message
import shutil
import time
import subprocess
import json
import contextlib
import subprocess
from pathlib import Path
from typing import Iterator, List, Tuple, Dict

from PIL import Image
from PIL.GifImagePlugin import GifImageFile
from apng import APNG

from .config import ABS_CACHE_PATH, ABS_TEMP_PATH, imager_exec_path
from .criterion import CreationCriteria, SplitCriteria, ModificationCriteria
# from .create_ops import create_aimg
# from .split_ops import split_aimg


size_suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


def _create_num_fragments():
    for i in range(0, 10):
        yield {"num": i}
    return 120


def _spit_numbers():
    yield 'a'
    yield 'b'
    x = yield from _create_num_fragments()
    print(f"x is {x}")
    yield {"x": x}
    # return x


def util_generator():
    yield from _spit_numbers()


def util_generator_shallow():
    x = yield from _create_num_fragments()
    print(f"x is {x}")
    return x


def sequence_nameget(name: str):
    """ Cuts of sequence number suffixes from a filename. Filenames only, extensions must be excluded from this check. """
    n_shards = name.split("_")
    if str.isnumeric(n_shards[-1]):
        return "_".join(n_shards[:-1])
    else:
        return name


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


def _mk_temp_dir(prefix_name: str = '') -> Path:
    """Creates a directory for temporary storage inside cache/, and then returns its absolute path

    Args:
        prefix_name (str, optional): Name of the temporary directory. Defaults to ''.

    Returns:
        Path: Absolute path of the created temporary directory
    """
    dirname = str(int(round(time.time() * 1000)))
    if prefix_name:
        dirname = f"{prefix_name}_{dirname}"
    temp_dir = ABS_CACHE_PATH().joinpath(dirname)
    # raise Exception(temp_dir, os.getcwd())
    Path.mkdir(temp_dir)
    return temp_dir


def _unoptimize_gif(gif_path: Path, out_dir: Path, decoder: str) -> Path:
    """Perform GIF unoptimization using Gifsicle/ImageMagick, in order to obtain the true singular frames for Splitting purposes. Returns the path of the unoptimized GIF

    Args:
        gif_path (Path): Path to GIF image
        out_dir (Path): Output directory of unoptimized GIF
        decoder (str): 'imagemagick' or 'gifsicle', to be used to unoptimize the GIF

    Returns:
        Path: Path of unoptimized GIF
    """
    # raise Exception(gif_path, out_dir)
    unop_gif_save_path = out_dir.joinpath(gif_path.name)
    imager_path = imager_exec_path(decoder)
    if decoder == 'imagemagick':
        args = [str(imager_path), "-coalesce", f'"{gif_path}"', f'"{unop_gif_save_path}"']
    elif decoder == 'gifsicle':
        args = [str(imager_path), "-b", "--unoptimize", f'"{gif_path}"', "--output", f'"{unop_gif_save_path}"']
    cmd = ' '.join(args)
    # print(cmd)
    subprocess.run(cmd, shell=True)
    return unop_gif_save_path


def _reduce_color(gif_path: Path, out_dir: Path, color: int = 256) -> Path:
    """Reduce the color of a gif.

    Args:
        gif_path (Path): Path to the GIF.
        out_dir (Path): Output directory to save the color-reduced GIF to.
        color (int, optional): Amount of color to reduce to. Defaults to 256.

    Returns:
        Path: Absolute path of the color-reduced GIF.
    """
    out_message("Performing color reduction...")
    gifsicle_path = imager_exec_path('gifsicle')
    redux_gif_path = out_dir.joinpath(gif_path.name)
    args = [str(gifsicle_path), f"--colors={color}", str(gif_path), "--output", str(redux_gif_path)]
    cmd = ' '.join(args)
    subprocess.run(cmd, shell=True)
    return redux_gif_path


def _convert_to_rgba(image_paths: List[str]):
    pass


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


def get_image_delays(image_path: str, extension: str) -> Iterator[float]:
    """Get the delays of each frame from an animated image

    Args:
        image_path (str): Path to the animated image
        extension (str): The animated image format

    Yields:
        Iterator[float]: Image delays
    """
    if extension == 'GIF':
        with Image.open(image_path) as gif:
            for i in range(0, gif.n_frames):
                gif.seek(i)
                yield gif.info['duration']
    elif extension == 'PNG':
        apng = APNG.open(image_path)
        for png, control in apng.frames:
            if control:
                yield control.delay
            else:
                yield ""


def generate_delay_file(image_path: str, extension: str, out_folder: str):
    """Create a file containing the frame delays of an animated image

    Args:
        image_path (str): Path to animated image
        extension (str): Format of the animated image
        out_folder (str): Output directory of the delay file
    """
    delays = get_image_delays(image_path, extension)
    delay_info = {
        "delays": {index: d for index, d in enumerate(delays)}
    }
    filename = "_delays.json"
    save_path = os.path.join(out_folder, filename)
    with open(save_path, "w") as outfile:
        json.dump(delay_info, outfile, indent=4, sort_keys=True)


# def _restore_disposed_frames(frame_paths: List[str]):
#     """ Pastes the target_frame over the first_frame (applied when restoring GIF frames). Overrides every single frames on disk """
#     im = Image.open(frame_paths[0])
#     # im.transparency = 0
#     im = im.convert("RGBA")
#     fm = []
#     for index, f in enumerate(frame_paths):
#         frame = Image.open(f)
#         # frame.transparency = 0
#         frame = frame.convert("RGBA")
#         # frame.show()
#         fm.append((frame.mode, im.info))
#         # im.paste(frame)
#         frame.save(f, "PNG")
#         yield f"Coalescing frames... ({index + 1}/{len(frame_paths)})"
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

def unbuffered_process(proc, stream='stdout'):
    newlines = ['\n', '\r\n', '\r']
    stream = getattr(proc, stream)
    with contextlib.closing(stream):
        while True:
            out = []
            last = stream.read(1)
            # Don't loop forever
            if last == '' and proc.poll() is not None:
                break
            while last not in newlines:
                # Don't loop forever
                if last == '' and proc.poll() is not None:
                    break
                out.append(last)
                last = stream.read(1)
            out = ''.join(out)
            yield out
