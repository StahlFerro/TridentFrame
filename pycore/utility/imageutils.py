from fileinput import filename
import json
import re
from collections import deque
from collections import OrderedDict
from pathlib import Path
from tracemalloc import start
from typing import Iterator, List, Dict, Union, Any, Tuple

from PIL import Image
from apng import APNG

from pycore.core_funcs import stdio
from pycore.models.image_formats import ImageFormat
from pycore.utility import vectorutils


PNG_BLOCK_SIZE = 64
ACTL_CHUNK = b"\x61\x63\x54\x4C"
FILENAME_GROUPING_REGEX = re.compile('^(?P<filestem>.*?)(?P<sequence>\d*)?(?P<extension>\..{1,4})?$', flags=re.M|re.S)
ALPHANUMERIC_RSTRIP_REGEX = re.compile('(?P<filtered_name>.*[A-Za-z0-9])')


# def reshape_palette(palette_array) -> np.array:
#     """Reshape im.getpalette() one-dimensional array to
#
#     Args:
#         palette_array ([type]): One-dimensional array (im.getpalette()) [r, g, b, r, g, b, ...]
#
#     Returns:
#         np.array: 2 dimensional numpy array of (R, G, B) value per item [[r, g, b], [r, g, b], ...]
#     """
#     return np.array(palette_array, dtype=np.uint8).reshape(256, 3)
#
#
# def get_palette_image(im) -> Image:
#     palette = np.array(im.getpalette(), dtype=np.uint8).reshape(16, 16, 3)
#     return Image.fromarray(palette, "RGB").resize((256, 256), resample=Image.NEAREST)


def get_image_delays(image_path: Path, extension: str) -> Iterator[float]:
    """Get the delays of each frame from an animated image

    Args:
        image_path (Path): Path to the animated image
        extension (str): The animated image format

    Yields:
        Iterator[float]: Image delays
    """
    iformat = ImageFormat[extension.upper()]
    if iformat == ImageFormat.GIF:
        with Image.open(image_path) as gif:
            for i in range(0, gif.n_frames):
                gif.seek(i)
                yield gif.info["duration"]
    elif iformat == ImageFormat.PNG:
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


def shift_image_sequence(image_paths: List[Path], start_frame: int) -> List[Path]:
    """Shift an image sequence based on the indicated start frame.

    Args:
        image_paths (List[Path]): List of paths of each image in a sequence.
        start_frame (int): The frame number to start the sequence at.

    Returns:
        List[Path]: List of image sequence which ordering has been shifted.
    """
    image_paths = vectorutils.shift_items(image_paths, start_frame)
    # shift_items = deque(image_paths)
    # shift = -start_frame
    # stdio.message(f"SHIFT {shift}")
    # shift_items.rotate(shift)
    # image_paths = list(shift_items)
    return image_paths


def get_filename_components(f: Union[Path, str]):
    """Get the stem filename without sequence numbers
    Example: sequence_nameget('dogs_0024.png') = 'dogs'
    
    Args:
        f: File path or filename.

    Returns:
        Any: Tuple of all matched regex groups

    """
    if isinstance(f, Path):
        f = f.name
    # elif type(f) is str:
        # f = f.split(".")[0]
    # sqre = re.compile(FILENAME_GROUPING_REGEX)
    root_fname = FILENAME_GROUPING_REGEX.match(f)
    # root_fname = sqre.match(f)
    return root_fname
    

def sequence_nameget(f: Union[Path, str]) -> str:
    """Get the stem filename without sequence numbers
    Example: sequence_nameget('dogs_0024.png') = 'dogs'
    
    However, file names containing only sequence of numbers will be returned
    Example: sequence_nameget('04185.png') = '04185'
    
    Args:
        f: File path or filename.

    Returns:
        str: Filename without sequence number and extension.

    """
    fname_parts = get_filename_components(f)
    file_stem = fname_parts.group('filestem')
    file_sequence = fname_parts.group('sequence')
    if fname_parts and file_stem:
        return file_stem
    elif fname_parts and file_sequence:
        return file_stem + file_sequence
    else:
        return ''


def rstrip_trailing_symbols(text: str) -> str:
    """Right-strip trailing non-alphanumeric characters from a string

    Args:
        name (str): Input string

    Returns:
        str: The resulting string with no trailing non-alphanumeric characters
    """
    match = ALPHANUMERIC_RSTRIP_REGEX.match(text)
    return match.group('filtered_name')


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


def png_is_animated(png_path: Path) -> bool:
    img_hex = b""
    with open(png_path, "rb") as png_file:
        buf = png_file.read(PNG_BLOCK_SIZE)
        img_hex = buf
    # print(img_hex)
    return ACTL_CHUNK in img_hex


# def validate_image_name(filename: str, extension: str) -> str:
#     name_path = Path(filename)
#     if name_path.suffixes:
#         last_suffix = name_path.suffixes[-1]
#         extension_re = re.compile(extension.upper(), re.IGNORECASE)
#         if extension_re.match(filename):
#             filename = 
