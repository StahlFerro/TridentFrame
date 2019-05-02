import os
import string
from random import choices
from pprint import pprint
from urllib.parse import urlparse

from PIL import Image
from apng import APNG
from colorama import init, deinit
from hurry.filesize import size, alternative


img_exts = ['png', 'jpg', 'jpeg', 'gif', 'bmp']
static_img_exts = ['png', 'jpg']
animated_img_exts = ['gif', 'png']


def _inspect_image(image_path):
    filename = str(os.path.basename(image_path))
    abspath = os.path.abspath(image_path)
    workpath = os.path.dirname(abspath)
    ext = str.lower(os.path.splitext(filename)[1])

    if os.getcwd() != workpath:
        os.chdir(workpath)

    frame_count = 0
    fps = 0
    duration = 0
    fsize = size(os.stat(filename).st_size, system=alternative)
    # fsize = 0
    width = height = 0
    loop_duration = 0
    extension = ''

    if ext == '.gif':
        try:
            gif: Image = Image.open(filename)
        except Exception:
            return
        if gif.format != 'GIF' or not gif.is_animated:
            raise Exception(f"The chosen GIF ({filename}) is not an animated GIF!")
        width, height = gif.size
        frame_count = gif.n_frames
        # pprint(gif.info)
        durations = []
        for f in range(0, gif.n_frames):
            gif.seek(f)
            durations.append(gif.info['duration'])
        duration = sum(durations) / len(durations)
        fps = 1000.0 / duration
        loop_duration = frame_count / fps
        extension = 'GIF'
    
    elif ext == '.png':
        try:
            apng: APNG = APNG.open(filename)
        except Exception:
            pass
        frames = apng.frames
        frame_count = len(frames)
        if frame_count <= 1:
            raise Exception(f"The chosen PNG ({filename}) is not an APNG!")
        png_one, controller_one = frames[0]
        # pprint(png_one.__dict__)
        # pprint(controller_one.__dict__)
        extension = 'APNG'
        width = png_one.width
        height = png_one.height
        duration = controller_one.delay
        fps = 1000.0 / duration
        loop_duration = frame_count / fps
        

    image_info = {
        "name": filename,
        "fps": fps,
        "duration": duration,
        "fsize": fsize,
        "extension": extension,
        "frame_count": frame_count,
        "absolute_url": abspath,
        "width": width,
        "height": height,
        "loop_duration": loop_duration,
    }
    return image_info


def _combine_image(dir_path: str, out_path: str, scale: float = 1.0):
    upath = urlparse(dir_path)
    abspath = os.path.abspath(upath.path)
    init()
    if not os.path.isdir(abspath):
        framesdir = str(os.path.basename(abspath))
    workpath = os.path.dirname(abspath)
    if os.getcwd() != abspath:
        os.chdir(abspath)

    # If no name supplied, default name will be the framesdir folder name. Output will be in the same parent directory
    # as the framesdir
    if not output_name:
        output_name = framesdir
    output_name = os.path.join(workpath, output_name)

    imgs = [f for f in os.listdir('.') if '.' in f and str.lower(f.split('.')[-1]) in img_exts]

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
        frames[0].save(f"{output_name}.gif", optimize=False,
                       save_all=True, append_images=frames[1:], duration=duration, loop=0, disposal=disposal)
        # click.secho(f"Created GIF {output_name}.gif", fg="cyan")

    elif extension == 'apng':
        # click.secho("Generating APNG...", fg="cyan")
        # click.secho(f"Created APNG {output_name}.png", fg="cyan")
        imgs.sort(reverse=reverse)
        APNG.from_files(imgs, delay=duration).save(f"{output_name}.png")

    deinit()


def _split_image(image_path: str, out_path: str):
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

    if not out_path:
        raise Exception("No output folder selected, please select it first")

    ext = str.lower(filename.split('.')[-1])
    if ext not in animated_img_exts:
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
            gif.save(os.path.join(out_path, f"{filename}_{str.zfill(str(f), pad_count)}.png"), 'PNG')

    elif ext == 'png':
        img: APNG = APNG.open(filename)
        iframes = img.frames
        pad_count = max(len(str(len(iframes))), 3)
        # click.secho(f"{filename} ({len(iframes)} frames). Splitting APNG...", fg='cyan')
        # print('frames', [(png, control.__dict__) for (png, control) in img.frames][0])
        # with click.progressbar(iframes, empty_char=" ", fill_char="█", show_percent=True, show_pos=True) as frames:
        for i, (png, control) in enumerate(iframes):
            png.save(os.path.join(out_path, f"{filename}_{str.zfill(str(i), pad_count)}.png"))

    # click.secho(f"Done!!1", fg='cyan')
    deinit()
    return True
