import os
import io
import string
import shutil
import math
import time
import subprocess
import tempfile
from random import choices
from pprint import pprint
from urllib.parse import urlparse
from typing import List, Dict, Tuple
from datetime import datetime

from PIL import Image
from apng import APNG, PNG
from colorama import init, deinit
from hurry.filesize import size, alternative

from config import IMG_EXTS, ANIMATED_IMG_EXTS, STATIC_IMG_EXTS, CreationCriteria, SplitCriteria, SpritesheetBuildCriteria, SpritesheetSliceCriteria, ABS_CACHE_PATH


def _create_temp_gifs(image_paths: List, criteria: CreationCriteria) -> Tuple[str, List[str]]:
    frames = []
    disposal = 0
    if criteria.reverse:
        image_paths.reverse()
    timestamp_dirname = time.strftime("%Y%m%d_%H%M%S")
    gif_cache_dir = os.path.join(ABS_CACHE_PATH, timestamp_dirname)
    os.mkdir(gif_cache_dir)
    temp_gifs = []
    for index, ipath in enumerate(image_paths):
        im = Image.open(ipath)
        # orig_width, orig_height = im.size
        # must_resize = criteria.resize_width != orig_width or criteria.resize_height != orig_height
        # alpha = None
        # if criteria.flip_h:
        #     im = im.transpose(Image.FLIP_LEFT_RIGHT)
        # if criteria.flip_v:
        #     im = im.transpose(Image.FLIP_TOP_BOTTOM)
        # if must_resize:
        #     im = im.resize((round(criteria.resize_width) , round(criteria.resize_height)))
        save_path = f'{os.path.join(gif_cache_dir, os.path.splitext(os.path.basename(ipath))[0])}.gif'
        if im.mode == 'RGBA' and criteria.transparent:
            alpha = im.getchannel('A')
            # alpha.show(title='alpha')
            im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
            # im.show('im first convert')
            mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
            # mask.show('mask')
            im.paste(255, mask)
            # im.show('masked im')
            im.info['transparency'] = 255
            im.save(save_path)
        elif im.mode == 'RGB':
            im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE)
            im.save(save_path)
        elif im.mode == 'P':
            im.save(save_path, transparency=im.info['transparency'])
        temp_gifs.append(save_path)
    return gif_cache_dir, temp_gifs


def _build_gif(image_paths: List, out_full_path: str, criteria: CreationCriteria):
    frames = []
    disposal = 0
    if criteria.reverse:
        image_paths.reverse()
    for index, ipath in enumerate(image_paths):
        im = Image.open(ipath)
        orig_width, orig_height = im.size
        must_resize = criteria.resize_width != orig_width or criteria.resize_height != orig_height
        alpha = None
        if criteria.flip_h:
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        if criteria.flip_v:
            im = im.transpose(Image.FLIP_TOP_BOTTOM)
        if must_resize:
            im = im.resize((round(criteria.resize_width) , round(criteria.resize_height)))
        try: 
            alpha = im.getchannel('A')
        except Exception:
            alpha = False
        if criteria.transparent and alpha:
            disposal = 2
            # alpha.show(title='alpha')
            im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
            # im.show('im first convert')
            mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
            # mask.show('mask')
            im.paste(255, mask)
            # im.show('masked im')
            im.info['transparency'] = 255
        else:
            im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=256)
        yield f'Appending frames... ({index + 1}/{len(image_paths)})'
        frames.append(im)
    yield 'Saving GIF...'
    frames[0].save(out_full_path,
        save_all=True, append_images=frames[1:], duration=criteria.duration, loop=0, disposal=disposal)
    yield 'Finished!'


def _build_apng(image_paths, criteria: CreationCriteria) -> APNG:
    if criteria.reverse:
        image_paths.reverse()
    apng = APNG()
    first_width, first_height = Image.open(image_paths[0]).size
    first_must_resize = criteria.resize_width != first_width or criteria.resize_height != first_height
    if criteria.flip_h or criteria.flip_v or first_must_resize:
        for ipath in image_paths:
            # bytebox = io.BytesIO()
            with io.BytesIO() as bytebox:
                im = Image.open(ipath)
                orig_width, orig_height = im.size
                must_resize = criteria.resize_width != orig_width or criteria.resize_height != orig_height
                if must_resize:
                    im = im.resize((round(criteria.resize_width), round(criteria.resize_height)))
                if criteria.flip_h:
                    im = im.transpose(Image.FLIP_LEFT_RIGHT)
                if criteria.flip_v:
                    im = im.transpose(Image.FLIP_TOP_BOTTOM)
                im.save(bytebox, "PNG", optimize=True)
                apng.append(PNG.from_bytes(bytebox.getvalue()), delay=criteria.duration)
        return apng
    else:
        return APNG.from_files(image_paths, delay=criteria.duration)


def create_aimg(image_paths: List[str], out_dir: str, filename: str, criteria: CreationCriteria):
    abs_image_paths = [os.path.abspath(ip) for ip in image_paths if os.path.exists(ip)]
    img_paths = [f for f in abs_image_paths if str.lower(os.path.splitext(f)[1][1:]) in STATIC_IMG_EXTS]
    # workpath = os.path.dirname(img_paths[0])
    init()
    # Test if inputted filename has extension, then remove it from the filename
    fname, ext = os.path.splitext(filename)
    if ext:
        filename = fname
    if not out_dir:
        raise Exception("No output folder selected, please select it first")
    out_dir = os.path.abspath(out_dir)
    if not os.path.exists(out_dir):
        raise Exception("The specified absolute out_dir does not exist!")

    if criteria.extension == 'gif':
        out_full_path = os.path.join(out_dir, f"{filename}.gif")
        filename = f"{filename}.gif"
        return _build_gif(image_paths, out_full_path, criteria)
        
    elif criteria.extension == 'apng':
        out_full_path = os.path.join(out_dir, f"{filename}.png")
        apng = _build_apng(img_paths, criteria)
        apng.save(out_full_path)

    deinit()
    return out_full_path


def split_aimg(image_path: str, out_dir: str, criteria: SplitCriteria):
    abspath = os.path.abspath(image_path)
    init()
    if not os.path.isfile(image_path):
        raise Exception("Oi skrubman the path here seems to be a bloody directory, should've been a file")
    filename = str(os.path.basename(abspath))
    workpath = os.path.dirname(abspath)

    if os.getcwd() != workpath:
        os.chdir(workpath)

    # Custom output dirname and frame names if specified on the cli
    if '.' not in filename:
        raise Exception('Where the fuk is the extension mate?!')

    fname, ext = os.path.splitext(filename)
    ext = str.lower(ext[1:])
    # raise Exception(fname, ext)
    if ext not in ANIMATED_IMG_EXTS:
        raise Exception('Only supported extensions are gif and apng. Sry lad')

    # Create directory to contain all the frames if does not exist
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
        # yield f"Creating directory {out_dir}..."
    # else:
        # yield f"Directory {out_dir} already exists, replacing the PNGs inside it..."

    # Image processing
    if ext == 'gif':

        with WImage(filename=image_path) as gif:
            yield 'ok'
            sequence = list(gif.sequence)
            yield 'converted to list', sequence
            pad_count = criteria.pad_count or  max(len(str(len(sequence))), 3)
            for index in range(0, len(sequence)):
                yield f'Splitting GIF... ({index + 1}/{len(sequence)})'
                frame = sequence[index]
                frame_name = os.path.join(out_dir, f"{fname}_{str.zfill(str(index), pad_count)}.png")
                frame.container.save(filename=frame_name)
        # TODO: Delete below in case Wand successfully split GIF frames without any transparency/color issues like Pillow
        # try:
        #     gif: Image = Image.open(filename)
        # except Exception:
        #     raise Exception(filename, "M8 I don't even think this file is even an image file in the first place")

        # if gif.format != 'GIF' or not gif.is_animated:
        #     raise Exception(filename, "Sorry m9, the image you specified is not a valid animated GIF")

        # # click.secho(f"{filename} ({gif.n_frames} frames). Splitting GIF...", fg='cyan')

        # # with click.progressbar(frame_nums, empty_char=" ", fill_char="█", show_percent=True, show_pos=True) as frames:
        # pad_count: int = 3 if (not criteria.pad_count or criteria.pad_count <= 0) else criteria.pad_count
        # durations = []
        # for f in frame_nums:
        #     gif.seek(f)
        #     durations.append(gif.info['duration'])
        # min_duration = min(durations)
        # if criteria.is_duration_sensitive:
        #     multipliers = [dur//min_duration for dur in durations]
        # else:
        #     multipliers = [1 for dur in durations]
        # frame_multipliers = list(zip(frame_nums, multipliers))
        # seq_no = 0
        
        # gif_analysis = analyse_gif(gif)
        # mode = gif_analysis['mode']
        # p = gif.getpalette()
        # last_frame = gif.convert('RGBA')
        
        # for index, multiplier in frame_multipliers:
        #     gif.seek(index)

        #     '''
        #     If the GIF uses local colour tables, each frame will have its own palette.
        #     If not, we need to apply the global palette to the new frame.
        #     '''
        #     if not gif.getpalette():
        #         yield('No palettes')
        #         gif.putpalette(p)
        #     new_frame = Image.new('RGBA', gif.size)

        #     '''
        #     Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
        #     If so, we need to construct the new frame by pasting it on top of the preceding frames.
        #     '''
        #     if mode == 'partial':
        #         new_frame.paste(last_frame)

        #     new_frame.paste(gif, (0,0), gif.convert('RGBA'))
        #     # yield new_frame

        #     last_frame = new_frame

        #     for n in range(0, multiplier):
        #         yield f'Splitting GIF... ({seq_no + 1}/{sum(multipliers)})'
        #         new_frame.save(os.path.join(out_dir, f"{fname}_{str.zfill(str(seq_no), pad_count)}.png"), 'PNG', optimize=False)
        #         seq_no += 1

    elif ext == 'png':
        img: APNG = APNG.open(filename)
        iframes = img.frames
        pad_count = max(len(str(len(iframes))), 3)
        # print('frames', [(png, control.__dict__) for (png, control) in img.frames][0])
        # with click.progressbar(iframes, empty_char=" ", fill_char="█", show_percent=True, show_pos=True) as frames:
        for index, (png, control) in enumerate(iframes):
            yield f'Splitting APNG... ({index + 1}/{len(iframes)})'
            png.save(os.path.join(out_dir, f"{fname}_{str.zfill(str(index), pad_count)}.png"))

    deinit()
    yield 'Finished!'


# if __name__ == "__main__":
#     pprint(_inspect_sequence(""))

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


def analyse_gif(im):
    '''
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode
    before processing all frames.
    '''
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    im.seek(0)
    return results


def extract_gif_frames(gif: Image):
    '''
    Iterate the GIF, extracting each frame.
    '''
    gif_analysis = analyse_gif(gif)
    mode = gif_analysis['mode']
    p = gif.getpalette()
    last_frame = gif.convert('RGBA')

    try:
        while True:
            '''
            If the GIF uses local colour tables, each frame will have its own palette.
            If not, we need to apply the global palette to the new frame.
            '''
            if not gif.getpalette():
                gif.putpalette(p)

            new_frame = Image.new('RGBA', gif.size)

            '''
            Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
            If so, we need to construct the new frame by pasting it on top of the preceding frames.
            '''
            if mode == 'partial':
                new_frame.paste(last_frame)

            new_frame.paste(gif, (0,0), gif.convert('RGBA'))
            yield new_frame

            last_frame = new_frame
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    

def gs_build():
    gifsicle_exec = os.path.abspath("./bin/gifsicle-1.92-win64/gifsicle.exe")
    orig_path = os.path.abspath('./test/orig/')
    gifcache_path = os.path.abspath('./test/gifcache')
    print('gifcache_path', gifcache_path)
    raydns = [os.path.abspath(os.path.join(orig_path, f)) for f in os.listdir(orig_path)]
    # pprint(raydns)
    gif_cache_dir, gifraydns = _create_temp_gifs(raydns, CreationCriteria(fps=50, extension='gif', reverse=True, transparent=True))
    pprint(gifraydns)
    out_dir = os.path.abspath('./test/')
    print('orig_path', orig_path)
    colors = 256
    delay = 2
    optimization = "--unoptimize"
    disposal = "background"
    loopcount = ""
    out_dir = os.path.join(out_dir, "xdr.gif")
    print(out_dir)
    args = [gifsicle_exec, f"--colors={colors}", optimization, f"--delay={delay}", f"--disposal={disposal}", "--loopcount", " ".join(gifraydns), "--output", out_dir]
    
    cmd = ' '.join(args)
    print(cmd)
    subprocess.run(cmd)
    shutil.rmtree(gif_cache_dir)
    

        
def gs_split(gif_path: str, out_dir: str):
    gifsicle_exec = os.path.abspath("./bin/gifsicle-1.92-win64/gifsicle.exe")
    gif_path = os.path.abspath(gif_path)
    out_dir = os.path.abspath(out_dir)
    frame_count = Image.open(gif_path).n_frames
    for index in range(0, frame_count):
        padnum = str.zfill(str(index), 3)
        filename = f'argento_{padnum}.png'
        out_file_path = os.path.join(out_dir, filename)
        args = [gifsicle_exec, gif_path, f'"#{index}"', "--output", out_file_path, "-Okeep-empty"]
        cmd = ' '.join(args)
        print(cmd)
        subprocess.run(cmd)

def test():
    temp_dir = tempfile.TemporaryDirectory()
    print(temp_dir)
    

if __name__ == "__main__":
    gs_build()
    # gs_split("./test/xdr.gif", "./test/sequence")
    # test()
