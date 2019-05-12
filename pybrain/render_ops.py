import os
import string
from random import choices
from pprint import pprint
from urllib.parse import urlparse

from PIL import Image
from apng import APNG
from colorama import init, deinit
from hurry.filesize import size, alternative

from .config import IMG_EXTS, ANIMATED_IMG_EXTS, STATIC_IMG_EXTS


def _combine_image(dir_path: str, out_path: str, scale: float = 1.0, fps: int = 50, extension: str = "gif", reverse: bool=False, transparent: bool = True):
    upath = urlparse(dir_path)
    abspath = os.path.abspath(upath.path)
    init()
    # if not os.path.isdir(abspath):
    #     framesdir = str(os.path.basename(abspath))
    # workpath = os.path.dirname(abspath)
    if os.getcwd() != abspath:
        os.chdir(abspath)

    # If no name supplied, default name will be the framesdir folder name. Output will be in the same parent directory
    # as the framesdir
    if not out_path:
        raise Exception("No output folder selected, please select it first")

    imgs = [f for f in os.listdir('.') if '.' in f and str.lower(f.split('.')[-1]) in IMG_EXTS]
    filename = imgs[0].split('.')[0]

    duration = round(1000 / fps)
    # click.secho(f"{len(imgs)} frames @ {fps}fps", fg="cyan")

    if extension == 'gif':
        frames = [Image.open(i) for i in imgs]
        frames.sort(key=lambda i: i.filename, reverse=reverse)
        if scale != 1.0:
            # click.secho(f"Resizing image by {scale}...", fg="cyan")
            frames = [f.resize((round(f.width * scale), round(f.height * scale))) for f in frames]

        # pprint(frames[0].filename)

        disposal = 0
        if transparent:
            disposal = 2
        # click.secho("Generating GIF...", fg="cyan")
        frames[0].save(f"{filename}.gif", optimize=False,
                       save_all=True, append_images=frames[1:], duration=duration, loop=0, disposal=disposal)
        # click.secho(f"Created GIF {output_name}.gif", fg="cyan")

    elif extension == 'apng':
        # click.secho("Generating APNG...", fg="cyan")
        # click.secho(f"Created APNG {output_name}.png", fg="cyan")
        imgs.sort(reverse=reverse)
        APNG.from_files(imgs, delay=duration).save(f"{filename}.png")

    deinit()
    return True


def _split_image(image_path: str, out_path: str):
    if not image_path and not out_path:
        raise Exception("Please load a GIF or APNG and choose the output folder!")
    elif not image_path:
        raise Exception("Please load a GIF or APNG!")
    elif not out_path:
        raise Exception("Please choose an output folder!")

    upath = urlparse(image_path)
    abspath = os.path.abspath(upath.path)
    init()
    if not os.path.isfile(abspath):
        raise Exception(abspath, upath.path, "Oi skrubman the path here seems to be a bloody directory, should've been a file")
    filename = str(os.path.basename(abspath))
    workpath = os.path.dirname(abspath)
    # if verbose:
    #     click.secho(f"dir_path: {file_path}\nabspath: {abspath}\nworkpath: {workpath}\nfile: {filename}",
    #                 fg='bright_cyan')
    if os.getcwd() != workpath:
        os.chdir(workpath)

    # Custom output dirname and frame names if specified on the cli
    if '.' not in filename:
        raise Exception('Where the fuk is the extension mate?!')


    fname, ext = os.path.splitext(filename)
    if str.lower(ext) not in ANIMATED_IMG_EXTS:
        return
        # raise ClickException('Only supported extensions are gif and apng. Sry lad')

    # Create directory to contain all the frames if does not exist
    if not os.path.exists(out_path):
        os.mkdir(out_path)
        print(f"Creating directory {out_path}...")
    else:
        print(f"Directory {out_path} already exists, replacing the PNGs inside it...")

    # Image processing
    if ext == 'gif':
        try:
            gif: Image = Image.open(filename)
        except Exception:
            raise Exception(filename, "M8 I don't even think this file is even an image file in the first place")

        if gif.format != 'GIF' or not gif.is_animated:
            raise Exception(filename, "Sorry m9, the image you specified is not a valid animated GIF")

        # click.secho(f"{filename} ({gif.n_frames} frames). Splitting GIF...", fg='cyan')
        pad_count = max(len(str(gif.n_frames)), 3)
        frame_nums = list(range(0, gif.n_frames))

        # with click.progressbar(frame_nums, empty_char=" ", fill_char="█", show_percent=True, show_pos=True) as frames:
        for f in frame_nums:
            gif.seek(f)
            gif.save(os.path.join(out_path, f"{fname}_{str.zfill(str(f), pad_count)}.png"), 'PNG')

    elif ext == 'png':
        img: APNG = APNG.open(filename)
        iframes = img.frames
        pad_count = max(len(str(len(iframes))), 3)
        # click.secho(f"{filename} ({len(iframes)} frames). Splitting APNG...", fg='cyan')
        # print('frames', [(png, control.__dict__) for (png, control) in img.frames][0])
        # with click.progressbar(iframes, empty_char=" ", fill_char="█", show_percent=True, show_pos=True) as frames:
        for i, (png, control) in enumerate(iframes):
            png.save(os.path.join(out_path, f"{fname}_{str.zfill(str(i), pad_count)}.png"))

    # click.secho(f"Done!!1", fg='cyan')
    deinit()
    return True


# if __name__ == "__main__":
#     pprint(_inspect_sequence(""))
