import os
import io
from pathlib import Path
from typing import List, Dict, Optional, Union

from PIL import Image, ImageCms, ExifTags, UnidentifiedImageError
from apng import APNG
from pycore.core_funcs import stdio
from pycore.core_funcs.exception import (
    ImageNotStaticException,
    ImageNotAnimatedException,
    UnidentifiedImageException,
)
from pycore.utility import filehandler, imageutils
from pycore.models.metadata import ImageMetadata, AnimatedImageMetadata


Image.MAX_IMAGE_PIXELS = None

COLOR_MODE_BIT_DEPTH = {
    "1": 1,
    "L": 8,
    "P": 8,
    "RGB": 24,
    "RGBA": 32,
    "CMYK": 32,
    "YCbCr": 24,
    "LAB": 24,
    "HSV": 24,
    "I": 32,
    "F": 32,
    "I;16": 16,
    "I;16B": 16,
    "I;16L": 16,
    "I;16S": 16,
    "I;16BS": 16,
    "I;16LS": 16,
    "I;32": 32,
    "I;32B": 32,
    "I;32L": 32,
    "I;32S": 32,
    "I;32BS": 32,
    "I;32LS": 32
}

COLOR_MODE_FULL_NAME = {
    "RGBA": "RGBA",
    "RGB": "RGB",
    "P": "Palette/Indexed",
    "PA": "Palette/Indexed + Alpha",
    "L": "Grayscale",
    "LA": "Greyscale + Alpha",
    "La": "Greyscale + Premultiplied Alpha",
    "1": "Bitmap",
    "I": "Integer Pixels",
    "F": "Floating-point Pixels",
}


def inspect_general(image_path: Path, filter_on: str = "", skip: bool = False) -> \
        Optional[Union[ImageMetadata, AnimatedImageMetadata]]:
    """Main single image inspection handler function.

    Args:
        image_path (Path): Input path
        filter_on (str, optional): "static" = Throws error on detecting an animated image; "animated": Throws error
        on detecting a static image. Defaults to ""
        skip: (bool): If true, returns an empty Dict, if False, throws an Exception if inspected image does not
        match filter_on argument. Defaults to False.

    Raises:
        UnidentifiedImageException: If file is not a valid image file.
        ImageNotStaticException: If filter_on="static", skip=False but the file is an animated image.
        ImageNotAnimatedException: [If filter_on="animated", skip=False but the file is a static image.

    Returns:
        Optional[ImageMetadata]: ImageMetadata or AnimatedImageMetadata depending on the image.
    """
    abspath = image_path
    filename = image_path.name
    # logger.message(str(image_path))
    ext = image_path.suffixes[-1]
    ext = ext.lower()
    if ext == ".gif":
        try:
            gif: Image = Image.open(abspath)
        except UnidentifiedImageError:
            raise UnidentifiedImageException(abspath)
        if gif.format == "GIF":
            if gif.is_animated:
                if filter_on == "static":
                    if skip:
                        return None
                    else:
                        raise ImageNotStaticException(filename, "GIF")
                else:
                    return inspect_animated_gif(image_path, gif)
            else:
                if filter_on == "animated":
                    if skip:
                        return None
                    else:
                        raise ImageNotAnimatedException(filename, "GIF")
                else:
                    return inspect_static_image(image_path)
    elif ext == ".png":
        try:
            apng: APNG = APNG.open(abspath)
        except UnidentifiedImageError:
            raise UnidentifiedImageException(abspath)
        frames = apng.frames
        # n_frames = Image.open(abspath).n_frames
        # stdio.debug({"fr": len(frames), "nfr": n_frames})
        frame_count = len(frames)
        if frame_count > 1:
            if filter_on == "static":
                if skip:
                    return None
                else:
                    raise ImageNotStaticException(filename, "PNG")
            else:
                return inspect_animated_png(image_path, apng)
        else:
            if filter_on == "animated":
                if skip:
                    return None
                else:
                    raise ImageNotAnimatedException(filename, "PNG")
            else:
                return inspect_static_image(image_path)
    else:
        return inspect_static_image(image_path)


# def inspect_static_image(path: Path):
#     return _inspect_static_image(Image.open(path))
#
#
# def inspect_static_image(image: Image.Image):
#     return _inspect_static_image(image)


def inspect_static_image(image_path: Path) -> ImageMetadata:
    """Returns all information regarding a single static image

    Args:
        image_path (Path): Path to the image file

    Returns:
        Dict: Information of the static image file
    """
    # image_info = {}
    # im: Image = None
    try:
        # if image_path.__class__.__bases__[0] is ImageFile.ImageFile:
        #     im = image_path
        # else:
        #     im = Image.open(image)
        im = Image.open(image_path)
    except Exception as e:
        stdio.error(str(e).replace("\\\\", "/"))
        return
    fmt = im.format
    exif = ""
    if fmt.upper() != "GIF":
        exif_raw = im._getexif()
        if exif_raw:
            exif = {ExifTags.TAGS[k]: v for k, v in exif_raw.items() if k in ExifTags.TAGS}
    width, height = im.size
    filename = image_path.name
    base_fname = image_path.stem
    ext = image_path.suffix
    base_fname = imageutils.sequence_nameget(base_fname)
    fsize = image_path.stat().st_size
    # fsize_hr = read_filesize(fsize)
    color_mode = COLOR_MODE_FULL_NAME.get(im.mode) or im.mode
    has_transparency = im.info.get("transparency") is not None or im.mode == "RGBA"
    # alpha = im.getchannel('A')
    comment = im.info.get("comment", "")
    icc = im.info.get("icc_profile")
    color_profile = ""
    if icc:
        f = io.BytesIO(icc)
        color_profile = ImageCms.getOpenProfile(f).profile
        # print(color_profile.profile_description)
        stdio.debug({"copyright": color_profile.copyright, "technology": color_profile.technology,
                     "manufacturer": color_profile.manufacturer, "creation_date": '',
                     "header_manufacturer": color_profile.header_manufacturer, "header_model": color_profile.header_model,
                     "icc_version": color_profile.icc_version, "target": color_profile.target})
        color_profile = color_profile.profile_description
    # if palette:
    #     logger.debug(imageutils.reshape_palette(palette))
    #     color_counts = np.array(im.getcolors())
    #     logger.debug(color_counts)
    #     logger.debug(color_counts.sum(axis=0)[0])
        # imageutils.get_palette_image(im).show()
    creation_dt = filehandler.get_creation_time(image_path)
    modification_dt = filehandler.get_modification_time(image_path)
    checksum = filehandler.hash_sha1(image_path)
    # logger.debug({"im.info": im.info, "icc": icc, "palette": imageutils.reshape_palette(palette) if palette else None})
    stdio.debug(im.info)
    if im.mode == "P":
        stdio.debug(im.getpalette())
    im.close()
    metadata = ImageMetadata({
        "name": filename,
        "base_filename": base_fname,
        "width": width,
        "height": height,
        "format": fmt,
        "fsize": fsize,
        "creation_datetime": creation_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "modification_datetime": modification_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "hash_sha1": checksum,
        "absolute_url": str(image_path),
        "comments": str(comment),
        "color_mode": str(color_mode),
        "color_profile": color_profile,
        "bit_depth": COLOR_MODE_BIT_DEPTH.get(im.mode),
        "has_transparency": has_transparency,
        "is_animated": False,
        "exif": str(exif),
    })
    return metadata


def inspect_animated_gif(abspath: Path, gif: Image) -> AnimatedImageMetadata:
    """Inspect an animated GIF and return its metadata

    Args:
        abspath (Path): Path to the animated GIF
        gif (Image): Pillow image instance of the animated GIF

    Returns:
        Dict: Metadata of the animated GIF
    """
    filename = abspath.name
    base_fname = imageutils.sequence_nameget(abspath.stem)
    width, height = gif.size
    frame_count = gif.n_frames
    fsize = os.stat(abspath).st_size
    # fsize_hr = read_filesize(fsize)
    loop_info = gif.info.get("loop")
    if loop_info is None:
        loop_count = 1
    elif loop_info == 0:
        loop_count = 0
    else:
        loop_count = loop_info + 1
    delays = []
    comments = []
    for f in range(0, gif.n_frames):
        gif.seek(f)
        stdio.debug(gif.info)
        # if f in range(0, 3):
        #     logger.debug(f"Frame #{f}\nDisposal: {gif.disposal_method}\nBackground: {gif.info.get('background', '')}\n"
        #         f"Transparency: {gif.info.get('transparency', '')}")
            # gif.show()
            # palette = np.array(gif.getpalette(), dtype=np.uint8).reshape(16, 16, 3)
            # if f == 0:
                # Image.fromarray(palette, "RGB").resize((256, 256), resample=Image.NEAREST).show()
            # logger.debug(gif.getpalette())
        delays.append(gif.info["duration"])
        frame_comment = gif.info.get("comment", "")
        try:
            frame_comment = frame_comment.decode('utf-8')
        except (UnicodeDecodeError, AttributeError):
            pass
        comments.append(frame_comment)
    if len(set(comments)) == 1:
        comments = comments[0]
    elif len(comments) == 0:
        comments = ""
    fmt = "GIF"
    full_format = str(gif.info.get("version") or "")
    has_transparency = gif.info.get("transparency") is not None
    creation_dt = filehandler.get_creation_time(abspath)
    modification_dt = filehandler.get_modification_time(abspath)
    checksum = filehandler.hash_sha1(abspath)
    palette = gif.getpalette()
    # if palette:
    #     logger.debug(f"Palette: {imageutils.reshape_palette(palette)}")
    #     color_counts = np.array(gif.getcolors())
    #     logger.debug(f"Color counts: {color_counts}")
    #     logger.debug(f"Total colors: {color_counts.shape[1]}")
        # imageutils.get_palette_image(gif).show()
    color_mode = COLOR_MODE_FULL_NAME.get(gif.mode) or gif.mode
    # logger.debug({"gif.info": gif.info, "palette": imageutils.reshape_palette(palette) if palette else None})
    gif.close()
    metadata = AnimatedImageMetadata({
        "name": filename,
        "base_filename": base_fname,
        "width": width,
        "height": height,
        "format": fmt,
        "format_version": full_format,
        "fsize": fsize,
        "creation_datetime": creation_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "modification_datetime": modification_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "hash_sha1": checksum,
        "absolute_url": str(abspath),
        "comments": comments,
        "color_mode": color_mode,
        "bit_depth": COLOR_MODE_BIT_DEPTH.get(gif.mode),
        "has_transparency": has_transparency,
        "is_animated": True,
        "frame_count": frame_count,
        "delays": delays,
        "loop_count": loop_count,
    })
    return metadata


def inspect_animated_png(abspath: Path, apng: APNG) -> AnimatedImageMetadata:
    """Inspect an animated PNG and return its metadata

    Args:
        abspath (Path): Path to the animated PNG
        apng (Image): APNG.APNG instance of the animated PNG

    Returns:
        Dict: Metadata of the animated PNG
    """
    filename = abspath.name
    base_fname = imageutils.sequence_nameget(abspath.stem)
    frames = apng.frames
    frame_count = len(frames)
    loop_count = apng.num_plays
    png_one, controller_one = frames[0]
    fmt = "PNG"
    fsize = os.stat(abspath).st_size
    # fsize_hr = read_filesize(fsize)
    width = png_one.width
    height = png_one.height
    # raise Exception(frames)
    delays = [f[1].delay / f[1].delay_den * 1000 if f[1] else 0 for f in frames]
    stdio.debug([(f[1].delay, f[1].delay_den) if f[1] else 0 for f in frames])
    im = Image.open(abspath)
    stdio.debug(im.default_image)
    # for index in range(0, im.n_frames):
        # logger.debug(im.info)
        # logger.debug(im.mode)
        # im.seek(index)
    color_mode = COLOR_MODE_FULL_NAME.get(im.mode) or im.mode
    has_transparency = im.info.get("transparency") is not None or im.mode == "RGBA"
    # min_duration = min(delays)
    # if min_duration == 0:
    #     frame_count_ds = frame_count
    # else:
    #     frame_count_ds = sum([delay//min_duration for delay in delays])
    creation_dt = filehandler.get_creation_time(abspath)
    modification_dt = filehandler.get_modification_time(abspath)
    checksum = filehandler.hash_sha1(abspath)
    # for index, (png, control) in enumerate(apng.frames):
    #     with io.BytesIO() as img_buf:
    #         png.save(img_buf)
    #         with Image.open(img_buf) as im:
    #             logger.debug({"control": control, "mode": im.mode, "info": im.info})

    # for index, im in enumerate(TridentFrameImagingAPI.get_apng_true_frames(apng)):
    #     if index < 4:
    #         im.show()

    metadata = AnimatedImageMetadata({
        "name": filename,
        "base_filename": base_fname,
        "width": width,
        "height": height,
        "format": fmt,
        "fsize": fsize,
        "creation_datetime": creation_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "modification_datetime": modification_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "hash_sha1": checksum,
        "absolute_url": str(abspath),
        "is_animated": True,
        "frame_count": frame_count,
        "delays": delays,
        "loop_count": loop_count,
        "color_mode": color_mode,
        "bit_depth": COLOR_MODE_BIT_DEPTH.get(im.mode),
        "has_transparency": has_transparency,
    })
    return metadata
    # return image_info


def inspect_sequence(image_paths: List[Path]) -> Dict:
    """Gets information of a selected sequence of static images

    Args:
        image_paths (List[Path]): List of resolved image sequence paths

    Returns:
        Dict: Information of the image sequence as a whole
    """
    abs_image_paths = image_paths
    sequence_info = []
    shout_nums = imageutils.shout_indices(len(abs_image_paths), 1)
    for index, path in enumerate(abs_image_paths):
        if shout_nums.get(index):
            stdio.message(f"Loading images... ({shout_nums.get(index)})")
        info = inspect_general(path, filter_on="static", skip=True)
        if info:
            gen_info = info.format_info()["general_info"]
            sequence_info.append(gen_info)
    # logger.message(sequence_info)
    if not sequence_info:
        stdio.error("No images selected. Make sure the path to them are correct and they are not animated images!")
        return {}
    static_img_paths = [si["absolute_url"]["value"] for si in sequence_info]
    # print("imgs count", len(static_img_paths))
    # first_img_name = os.path.splitext(os.path.basename(static_img_paths[0]))[0]
    # filename = first_img_name.split('_')[0] if '_' in first_img_name else first_img_name
    sequence_count = len(static_img_paths)
    sequence_filesize = filehandler.read_filesize(sum((si["fsize"]["value"] for si in sequence_info)))
    # im = Image.open(static_img_paths[0])
    # width, height = im.size
    # im.close()
    image_info = {
        "name": sequence_info[0]["base_filename"]["value"],
        "total": sequence_count,
        "sequence": static_img_paths,
        "sequence_info": sequence_info,
        "total_size": sequence_filesize,
        "width": sequence_info[0]["width"]["value"],
        "height": sequence_info[0]["height"]["value"],
    }
    return image_info


def inspect_sequence_autodetect(image_path: Path) -> Dict:
    """Receives a single image, then finds similar images with the same name and then returns the information of those
    sequence"""
    images_dir = image_path.parents[0]
    filename = imageutils.sequence_nameget(image_path.stem)
    # logger.message(f"filename {filename}")
    possible_sequence = [f for f in sorted(images_dir.glob("*")) if filename in f.stem and f.is_file()]
    # raise Exception(str(possible_sequence))
    # raise Exception(possible_sequence)
    # paths_bufferio = io.StringIO(json.dumps(possible_sequence))
    return inspect_sequence(possible_sequence)
