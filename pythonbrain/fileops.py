import os
import string
from random import choices
from pprint import pprint

from PIL import Image
from apng import APNG
from colorama import init, deinit
from hurry.filesize import size, alternative


img_exts = ['png', 'jpg', 'jpeg', 'gif', 'bmp']
static_img_exts = ['png', 'jpg']
animated_img_exts = ['gif', 'png']


def _inspect_image(image_path):
    file = str(os.path.basename(image_path))
    abspath = os.path.abspath(image_path)
    workpath = os.path.dirname(abspath)
    ext = str.lower(os.path.splitext(file)[1])

    if os.getcwd() != workpath:
        os.chdir(workpath)

    frame_count = 0
    fps = 0
    duration = 0
    fsize = size(os.stat(file).st_size, system=alternative)
    # fsize = 0
    width = height = 0
    loop_duration = 0
    extension = ''

    if ext == '.gif':
        try:
            gif: Image = Image.open(file)
        except Exception:
            return
        width, height = gif.size
        #     raise FileError(file, "M8 I don't even think this file is even an image file in the first place")
        #
        # if gif.format != 'GIF' or not gif.is_animated:
        #     raise FileError(file, "Sorry m9, the image you specified is not a valid animated GIF")
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
            apng: APNG = APNG.open(file)
        except Exception:
            return
        frames = apng.frames
        frame_count = len(frames)
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
        "name": file,
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


def _split_image(image_path: str, out_path: str):
    fslash = 'file://'
    if fslash in image_path:
        image_path = image_path.replace(fslash, '')
    init()
    if not os.path.isfile(image_path):
        raise Exception(image_path, "Oi skrubman the path here seems to be a bloody directory, should've been a file")
    filename = str(os.path.basename(image_path))
    abspath = os.path.abspath(image_path)
    workpath = os.path.dirname(abspath)
    # if verbose:
    #     click.secho(f"dir_path: {file_path}\nabspath: {abspath}\nworkpath: {workpath}\nfile: {filename}",
    #                 fg='bright_cyan')
    if os.getcwd() != workpath:
        os.chdir(workpath)

    # Custom output dirname and frame names if specified on the cli
    if '.' not in filename:
        raise Exception('Where the fuk is the extension mate?!')

    # if not out_path:
    #     out_path = '_'.join(filename.split('.')[:-1])

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
            gif.save(os.path.join(out_path, f"{image_path}_{str.zfill(str(f), pad_count)}.png"), 'PNG')

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


if __name__ == "__main__":
    info = _inspect_image('/home/andreas/Pictures/fortfade_80px_download.png')
    pprint(info)