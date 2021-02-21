import os
import json
import shutil
import subprocess
import sys
import shlex
from pathlib import Path
from subprocess import PIPE
from typing import Generator, List, Tuple, Iterator

from PIL import Image
from apng import APNG

from ..core_funcs.utility import _mk_temp_dir, imager_exec_path, shout_indices, unbuffered_process
from ..core_funcs import logger
# from ..core_funcs.io_streaming import unbuffered_Popen


def gifsicle_render(sicle_args: List[Tuple[str, str]], target_path: str, out_full_path: str, total_ops: int) -> str:
    # yield {"sicle_args": sicle_args}
    gifsicle_path = imager_exec_path('gifsicle')
    for index, (arg, description) in enumerate(sicle_args, start=1):
        # yield {"msg": f"index {index}, arg {arg}, description: {description}"}
        cmdlist = [gifsicle_path, arg, f'"{target_path}"', "--output", f'"{out_full_path}"']
        cmd = ' '.join(cmdlist)
        # yield {"msg": f"[{index}/{total_ops}] {description}"}
        # yield {"cmd": cmd}
        subprocess.run(cmd, shell=True)
        if target_path != out_full_path:
            target_path = out_full_path
    return target_path


def imagemagick_render(magick_args: List[Tuple[str, str]], target_path: str, out_full_path: str, total_ops=0, shift_index=0) -> str:
    yield {"magick_args": magick_args}
    imagemagick_path = imager_exec_path('imagemagick')
    for index, (arg, description) in enumerate(magick_args, start=1):
        yield {"msg": f"index {index}, arg {arg}, description: {description}"}
        cmdlist = [imagemagick_path, arg, f'"{target_path}"', "--output", f'"{out_full_path}"']
        cmd = ' '.join(cmdlist)
        yield {"msg": f"[{shift_index + index}/{total_ops}] {description}"}
        yield {"cmd": cmd}
        subprocess.run(cmd, shell=True)
        if target_path != out_full_path:
            target_path = out_full_path
    return target_path


def apngopt_render(aopt_args, target_path: str, out_full_path: str, total_ops=0, shift_index=0):
    """ Use apngopt to optimize an APNG. Returns the output path """
    aopt_dir = _mk_temp_dir(prefix_name='apngopt_dir')
    opt_exec_path = imager_exec_path('apngopt')
    filename = os.path.basename(target_path)
    target_path = shutil.copyfile(target_path, os.path.join(aopt_dir, filename))
    cwd = os.getcwd()
    # common_path = os.path.commonpath([opt_exec_path, target_path])
    target_rel_path = os.path.relpath(target_path, cwd)
    for index, (arg, description) in enumerate(aopt_args, start=1):
        logger.message(f"index {index}, arg {arg}, description: {description}")
        cmdlist = [opt_exec_path, arg, f'"{target_rel_path}"', f'"{target_rel_path}"']
        # raise Exception(cmdlist, out_full_path)
        cmd = ' '.join(cmdlist)
        logger.message(f"[{shift_index + index}/{total_ops}] {description}")
        # result = subprocess.check_output(cmd, shell=True)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        index = 0
        while True:
            output = process.stdout.readline()
            if process.poll() is not None:
                break
            if output:
               logger.message(output.decode('utf-8'))
            index += 1
        # if target_path != out_full_path:
            # target_path = out_full_path
    x = shutil.move(target_path, out_full_path)
    # shutil.rmtree(aopt_dir)
    return out_full_path


class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)


def apngdis_split(target_path: Path, seq_rename: str="", out_dir: Path="") -> Iterator[Path]:
    """Split an APNG image into its individual frames

    Args:
        target_path (Path): Path of the APNG.
        seq_rename (str, optional): New prefix name of the sequence. Defaults to "".
        out_dir (Path, optional): Output directory. Defaults to "".

    Returns:
        Iterator[Path]: Iterator of paths to each split image frames of the APNG.
    """
    split_dir = _mk_temp_dir(prefix_name='apngdis_dir')
    dis_exec_path = imager_exec_path('apngdis')
    filename = target_path.name
    target_path = shutil.copyfile(target_path, split_dir.joinpath(filename))
    cwd = os.getcwd()
    # target_rel_path = os.path.relpath(target_path, cwd)
    args = [str(dis_exec_path), str(target_path)]
    if seq_rename:
        args.append(seq_rename)
    cmd = ' '.join(args)
    # logger.message(f"APNGDIS ARGS: {cmd}")
    fcount = len(APNG.open(target_path).frames)
    shout_nums = shout_indices(fcount, 5)
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
    # process = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stdout, bufsize=1, universal_newlines=True)
    # unbuffered_Popen(cmd)
    # for line in unbuffered_process(process):
    #     logger.message(line)
    index = 0
    while True:
        logger.message(index)
        output = process.stdout.readline()
        logger.message(output)
        err = process.stderr.readline()
        if process.poll() is not None:
            break
        if output and shout_nums.get(index):
            logger.message(f'Extracting frames... ({shout_nums.get(index)})')
        # if err:
        #     yield {"apngdis stderr": err.decode('utf-8')}
        index += 1
        
    # while True:
    #     # output = process.stdout.readline()
    #     # logger.message(output)
    #     # err = process.stderr.readline()
    #     if process.poll() is not None:
    #         break
    #     # if output and shout_nums.get(index):
    #     # logger.message(f'Extracting frames... ({shout_nums.get(index)})')
    #     # if err:
    #     #     yield {"apngdis stderr": err.decode('utf-8')}
    #     index += 1

    # for line in iter(process.stdout.readline(), b''):
    #     yield {"msg": line.decode('utf-8')}
    logger.message("Getting splitdir...")
    fragment_paths = (split_dir.joinpath(f) for f in split_dir.glob("*") if f != filename and f.suffixes[-1] == '.png')
    return fragment_paths
    # Remove generated text file and copied APNG file


def pngquant_render(pq_args: List, image_paths: List[str], optional_out_path="") -> List[Path]:
    quantized_frames = []
    logger.message(pq_args)
    pngquant_exec = imager_exec_path("pngquant")
    # quant_dir = _mk_temp_dir(prefix_name="quant_dir")
    shout_nums = shout_indices(len(image_paths), 5)
    for index, ipath in enumerate(image_paths):
        if optional_out_path:
            target_path = os.path.join(optional_out_path, os.path.basename(ipath))
        else:
            target_path = ipath
        if shout_nums.get(index):
            print(json.dumps({"msg": f'Quantizing PNG... ({shout_nums.get(index)})'}))

        args = [str(pngquant_exec), ' '.join([arg[0] for arg in pq_args]), f'"{ipath}"', "--force", "--output", f'"{target_path}"']
        cmd = ' '.join(args)
        # yield {"cmd": cmd}
        result = subprocess.check_output(cmd, shell=True)
        # Convert back to RGBA image
        with Image.open(target_path).convert("RGBA") as rgba_im:
            rgba_im.save(target_path)
        quantized_frames.append(target_path)
    # yield {"ssdsdsssdsd": quantized_frames}
    return quantized_frames
