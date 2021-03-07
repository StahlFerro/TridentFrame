import os
import shutil
import time
import json
import subprocess
from collections import deque
from collections import OrderedDict
from pathlib import Path
from typing import Iterator, List, Dict

from PIL import Image
from apng import APNG

from .config import get_absolute_cache_path, imager_exec_path
from pycore.core_funcs import logger

SIZE_SUFFIXES = ["B", "KB", "MB", "GB", "TB", "PB"]


class FileSystemUtility:
    pass


class ImageFileUtility:
    pass


def _create_num_fragments():
    for i in range(0, 10):
        yield {"num": i}
    return 120


def _spit_numbers():
    yield "a"
    yield "b"
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


def shift_image_sequence(image_paths: List[Path], start_frame: int) -> List[Path]:
    """Shift an image sequence based on the indicated start frame.

    Args:
        image_paths (List[Path]): List of paths of each image in a sequence.
        start_frame (int): The frame number to start the sequence at.

    Returns:
        List[Path]: List of image sequence which ordering has been shifted.
    """
    shift_items = deque(image_paths)
    shift = -start_frame
    logger.message(f"SHIFT {shift}")
    shift_items.rotate(shift)
    image_paths = list(shift_items)
    return image_paths


def sequence_nameget(name: str) -> str:
    """Cuts of sequence number suffixes from a filename. Filenames only, extensions must be excluded from this check

    Args:
        name: Filename without extensions.

    Returns:
        str: Filename wuthout sequence number.

    """
    n_shards = name.split("_")
    if str.isnumeric(n_shards[-1]):
        return "_".join(n_shards[:-1])
    else:
        return name


# def filter_images(image_paths: List[Path], option: str = "static"):
#     """ Filter out image whether they are static images or animated images """
#     ipath_tuples = []
#     for path in image_paths:
#         # name = path.stem
#         # ext = path.suffix
#         im = Image.open(path)
#         if type(im) is GifImageFile and im.n_frames > 1:
#             continue
#         apng = APNG.open(path)
#         if len(apng.frames) > 1:
#             continue
#         ipath_tuples.append((im, path))
#     return ipath_tuples


# def _purge_cache():
#     get_absolute_cache_path = get_absolute_cache_path()
#     _purge_directory(get_absolute_cache_path)


# def _purge_temp():
#     get_absolute_temp_path = get_absolute_temp_path()
#     _purge_directory(get_absolute_temp_path)


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


def _mk_temp_dir(prefix_name: str = "") -> Path:
    """Creates a directory for temporary storage inside cache/, and then returns its absolute path

    Args:
        prefix_name (str, optional): Name of the temporary directory. Defaults to ''.

    Returns:
        Path: Absolute path of the created temporary directory
    """
    dirname = str(int(round(time.time() * 1000)))
    if prefix_name:
        dirname = f"{prefix_name}_{dirname}"
    temp_dir = get_absolute_cache_path().joinpath(dirname)
    # raise Exception(temp_dir, os.getcwd())
    Path.mkdir(temp_dir)
    return temp_dir


def _unoptimize_gif(gif_path: Path, out_dir: Path, decoder: str) -> Path:
    """Perform GIF unoptimization using Gifsicle/ImageMagick, in order to obtain the true singular frames for
    Splitting purposes. Returns the path of the unoptimized GIF.

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
    args = []
    if decoder == "imagemagick":
        args = [
            str(imager_path),
            "-coalesce",
            f'"{gif_path}"',
            f'"{unop_gif_save_path}"',
        ]
    elif decoder == "gifsicle":
        args = [
            str(imager_path),
            "-b",
            "--unoptimize",
            f'"{gif_path}"',
            "--output",
            f'"{unop_gif_save_path}"',
        ]
    cmd = " ".join(args)
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
    logger.message("Performing color reduction...")
    gifsicle_path = imager_exec_path("gifsicle")
    redux_gif_path = out_dir.joinpath(gif_path.name)
    args = [
        str(gifsicle_path),
        f"--colors={color}",
        str(gif_path),
        "--output",
        str(redux_gif_path),
    ]
    cmd = " ".join(args)
    subprocess.run(cmd, shell=True)
    return redux_gif_path


def _delete_temp_images():
    # raise Exception(os.getcwd())
    temp_dir = os.path.abspath("temp")
    # raise Exception(os.getcwd(), temp_dir)
    # raise Exception(image_name, path)
    # os.remove(path)
    temp_aimgs = [os.path.join(temp_dir, i) for i in os.listdir(temp_dir)]
    for ta in temp_aimgs:
        os.remove(ta)
    return True


def get_image_delays(image_path: Path, extension: str) -> Iterator[float]:
    """Get the delays of each frame from an animated image

    Args:
        image_path (Path): Path to the animated image
        extension (str): The animated image format

    Yields:
        Iterator[float]: Image delays
    """
    if extension == "GIF":
        with Image.open(image_path) as gif:
            for i in range(0, gif.n_frames):
                gif.seek(i)
                yield gif.info["duration"]
    elif extension == "PNG":
        apng = APNG.open(image_path)
        for png, control in apng.frames:
            if control:
                yield control.delay
            else:
                yield ""


def generate_delay_file(image_path: Path, extension: str, out_folder: Path):
    """Create a file containing the frame delays of an animated image

    Args:
        image_path (Path): Path to animated image
        extension (str): Format of the animated image
        out_folder (Path): Output directory of the delay file
    """
    delays = get_image_delays(image_path, extension)

    # delay_info = OrderedDict({
    #     "filename": str(image_path),
    #     "delays": {index: d for index, d in enumerate(delays)}
    # })
    delay_info = OrderedDict()
    delay_info["image_path"] = str(image_path)
    delay_info["delays"] = {index: d for index, d in enumerate(delays)}
    filename = "_delays.json"
    save_path = out_folder.joinpath(filename)
    with open(save_path, "w") as outfile:
        json.dump(delay_info, outfile, indent=4, sort_keys=True)


# def _restore_disposed_frames(frame_paths: List[str]):
#     """ Pastes the target_frame over the first_frame (applied when restoring GIF frames). Overrides every single
#     frames on disk """
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


def read_filesize(nbytes: int) -> str:
    """Convert bytes into a human-readable file size notation using the biggest unit suffix in which the numerical
    value is equal or greater than 1

    Args:
        nbytes (int): Amount of bytes

    Returns:
        str: Human-readable file size
    """
    i = 0
    while nbytes >= 1024 and i < len(SIZE_SUFFIXES) - 1:
        nbytes /= 1024.0
        i += 1
    size = str(round(nbytes, 3)).rstrip("0").rstrip(".")
    return f"{size} {SIZE_SUFFIXES[i]}"


def shout_indices(frame_count: int, percentage_mult: int) -> Dict[int, str]:
    """Returns a dictionary of indices for message logging, with the specified percentage skip.

    Args:
        frame_count (int): Number of image frames.
        percentage_mult (int): Percentage multiples.

    Returns:
        Dict[int, str]: Examples:
        shout_incides(24, 50) -> {0: "0%", 12: "50%"}
        shout_indices(40, 25) -> {0: "0%", 10: "25%", 20: "50%", 30: "75%"}
    """
    mults = 100 // percentage_mult
    return {round(frame_count / mults * mult): f"{mult * percentage_mult}%" for mult in range(0, mults)}


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

# def unbuffered_process(proc, stream='stdout'):
#     newlines = ['\n', '\r\n', '\r']
#     stream = getattr(proc, stream)
#     with contextlib.closing(stream):
#         while True:
#             out = []
#             last = stream.read(1)
#             # Don't loop forever
#             if last == '' and proc.poll() is not None:
#                 break
#             while last not in newlines:
#                 # Don't loop forever
#                 if last == '' and proc.poll() is not None:
#                     break
#                 out.append(last)
#                 last = stream.read(1)
#             out = ''.join(out)
#             yield out
