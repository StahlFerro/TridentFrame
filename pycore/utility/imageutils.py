import json
from collections import deque
from collections import OrderedDict
from pathlib import Path
from typing import Iterator, List, Dict

from PIL import Image
from apng import APNG

from pycore.core_funcs import logger


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
