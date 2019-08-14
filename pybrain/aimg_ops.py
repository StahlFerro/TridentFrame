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
from hurry.filesize import size, alternative

from config import IMG_EXTS, ANIMATED_IMG_EXTS, STATIC_IMG_EXTS, CreationCriteria, SplitCriteria, SpritesheetBuildCriteria, SpritesheetSliceCriteria, ABS_CACHE_PATH, gifsicle_exec


def _purge_cache():
    for stuff in os.listdir(ABS_CACHE_PATH):
        stuff_path = os.path.join(ABS_CACHE_PATH, stuff)
        try:
            if os.path.isfile(stuff_path):
                os.unlink(stuff_path)
            elif os.path.isdir(stuff_path):
                shutil.rmtree(stuff_path)
        except Exception as e:
            print("e")


def _mk_temp_dir(prefix_name: str = ''):
    dirname = time.strftime("%Y%m%d_%H%M%S")
    if prefix_name:
        dirname = f"{prefix_name}_{dirname}"
    temp_dir = os.path.join(ABS_CACHE_PATH, dirname)
    os.mkdir(temp_dir)
    return temp_dir


def _create_gifragments(image_paths: List, criteria: CreationCriteria, absolute_paths=True) -> Tuple[str, List[str]]:
    """ Generate a sequence of GIFs created from the input sequence with the specified criteria, before compiling them into a single animated GIF"""
    print("Generating GIF fragments...")
    frames = []
    disposal = 0
    if criteria.reverse:
        image_paths.reverse()
    temp_dir = _mk_temp_dir(prefix_name="temp_gifragments")
    temp_gifs = []
    for index, ipath in enumerate(image_paths):
        print(f"Processing GIF ({index}/{len(image_paths)})")
        with Image.open(ipath) as im:
            # orig_width, orig_height = im.size
            # must_resize = criteria.resize_width != orig_width or criteria.resize_height != orig_height
            # alpha = None
            # if criteria.flip_h:
            #     im = im.transpose(Image.FLIP_LEFT_RIGHT)
            # if criteria.flip_v:
            #     im = im.transpose(Image.FLIP_TOP_BOTTOM)
            # if must_resize:
            #     im = im.resize((round(criteria.resize_width) , round(criteria.resize_height)))
            fragment_name = os.path.splitext(os.path.basename(ipath))[0]
            save_path = f'{os.path.join(temp_dir, fragment_name)}.gif'
            print('save path', save_path)
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
            elif im.mode == 'RGB' or not criteria.transparent:
                im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE)
                im.save(save_path)
            elif im.mode == 'P':
                im.save(save_path, transparency=im.info['transparency'])
            if absolute_paths:
                temp_gifs.append(save_path)
            else:
                temp_gifs.append(os.path.relpath(save_path, os.getcwd()))
    return temp_dir, temp_gifs


# def _build_sharded_gifs(cluster_gifs: List, out_full_path: str, criteria: CreationCriteria):
    


def _build_gif(image_paths: List, out_full_path: str, criteria: CreationCriteria):
    temp_dir, temp_gifs = _create_gifragments(image_paths, criteria, absolute_paths=False)
    print(temp_dir)
    executable = gifsicle_exec()
    colors = 256
    delay = 2
    optimization = "--unoptimize"
    disposal = "background"
    loopcount = "--loopcount"
    globstar_path = os.path.join(temp_dir, "*.gif")
    args = [executable, f"--colors={colors}", optimization, f"--delay={delay}", f"--disposal={disposal}", loopcount, globstar_path, "--output", out_full_path]
    # pprint(args)
    cmd = ' '.join(args)
    # print(cmd) 
    subprocess.run(cmd, shell=True)
    shutil.rmtree(temp_dir)


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
        _build_gif(image_paths, out_full_path, criteria)
    
    elif criteria.extension == 'apng':
        out_full_path = os.path.join(out_dir, f"{filename}.png")
        apng = _build_apng(img_paths, criteria)
        apng.save(out_full_path)

    # return out_full_path


def _reduce_color(gif_path, color: int = 256) -> str:
    print("Performing color reduction...")
    executable = gifsicle_exec()
    args = [executable, f"--colors={color}", gif_path]


def _unoptimize_gif(gif_path) -> str:
    """ Perform GIF unoptimization using Gifsicle, in order to obtain the true singular frames for Splitting purposes. Returns the path of the unoptimized GIF """
    print("Performing unoptimization...")
    executable = gifsicle_exec()
    temp_dir = _mk_temp_dir(prefix_name="unoptimized_gif")
    pure_gif_path = os.path.join(temp_dir, os.path.basename(gif_path))
    args = [executable, "-b", "--unoptimize", gif_path, "--output", pure_gif_path]
    cmd = ' '.join(args)
    print(cmd)
    subprocess.run(cmd, shell=True)
    return pure_gif_path


def _get_gif_delay_ratios(gif_path: str, duration_sensitive: bool = False) -> List[Tuple[str, str]]:
    """ Returns a list of dual-valued tuples, first value being the frame numbers of the GIF, second being the ratiko of the frame's delay to the lowest delay"""
    with Image.open(gif_path) as gif:
        indices = list(range(0, gif.n_frames))
        durations = []
        for i in indices:
            gif.seek(i)
            durations.append(gif.info['duration'])
        min_duration = min(durations)
        if duration_sensitive:
            ratios = [dur//min_duration for dur in durations]
        else:
            ratios = [1 for dur in durations]
        indexed_ratios = list(zip(indices, ratios))
    return indexed_ratios


def _split_gif(gif_path: str, out_dir: str, criteria: SplitCriteria) -> List[str]:
    """ Split GIF. Returns a list of absolute path of each split'd frames """
    unop_gif_path = _unoptimize_gif(gif_path)
    print('unop gif path', unop_gif_path)
    executable = gifsicle_exec()
    orig_name = os.path.splitext(os.path.basename(unop_gif_path))[0]
    indexed_ratios = _get_gif_delay_ratios(unop_gif_path, criteria.is_duration_sensitive)
    sequence = 0
    for index, ratio in indexed_ratios:
        selector = f'"#{index}"'
        for n in range(0, ratio):
            save_path = os.path.join(out_dir, f'{orig_name}_{str.zfill(str(sequence), 3)}.png')
            args = [executable, unop_gif_path, selector, "--output", save_path]
            cmd = ' '.join(args)
            subprocess.run(cmd, shell=True)
            sequence += 1


def split_aimg(image_path: str, out_dir: str, criteria: SplitCriteria) -> bool:
    """ Resolves paths, and decide whether to split a GIF or APNG """
    # print(error)
    abspath = os.path.abspath(image_path)
    print(abspath)
    if not os.path.isfile(image_path):
        raise Exception("Oi skrubman the path here seems to be a bloody directory, should've been a file")
    filename = str(os.path.basename(abspath))

    # Custom output dirname and frame names if specified on the cli
    if '.' not in filename:
        raise Exception('Where the fuk is the extension mate?!')

    fname, ext = os.path.splitext(filename)
    ext = str.lower(ext[1:])
    # raise Exception(fname, ext)
    if ext not in ANIMATED_IMG_EXTS:
        raise Exception('Only supported extensions are gif and apng. Sry lad')

    out_dir = os.path.abspath(out_dir)
    print(out_dir)
    # Image processing
    if ext == 'gif':
        print(image_path, out_dir, criteria)
        _split_gif(image_path, out_dir, criteria)
        # with WImage(filename=image_path) as gif:
        #     yield 'ok'
        #     sequence = list(gif.sequence)
        #     yield 'converted to list', sequence
        #     pad_count = criteria.pad_count or  max(len(str(len(sequence))), 3)
        #     for index in range(0, len(sequence)):
        #         yield f'Splitting GIF... ({index + 1}/{len(sequence)})'
        #         frame = sequence[index]
        #         frame_name = os.path.join(out_dir, f"{fname}_{str.zfill(str(index), pad_count)}.png")
        #         frame.container.save(filename=frame_name)
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
            # yield f'Splitting APNG... ({index + 1}/{len(iframes)})'
            png.save(os.path.join(out_dir, f"{fname}_{str.zfill(str(index), pad_count)}.png"))
    return True



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


def gs_build():
    gifsicle_exec = os.path.abspath("./bin/gifsicle-1.92-win64/gifsicle.exe")
    orig_path = os.path.abspath('./test/orig2/')
    images = [os.path.abspath(os.path.join(orig_path, f)) for f in os.listdir(orig_path)]
    out_dir = os.path.abspath('./test/')
    criteria = CreationCriteria(fps=50, extension='gif', transparent=True, reverse=False)
    create_aimg(images, out_dir, "sicle_test", criteria)
    

def gs_split(gif_path: str, out_dir: str):
    criteria = SplitCriteria(pad_count=3, is_duration_sensitive=False)
    # pprint(criteria.__dict__)
    split_aimg(gif_path, out_dir, criteria)

def test():
    temp_dir = tempfile.TemporaryDirectory()
    print(temp_dir)


if __name__ == "__main__":
    gs_build()
    # gs_split("./test/blobsekiro.gif", "./test/sequence/")
    # test()
    # _unoptimize_gif("./test/blobkiro.gif")
