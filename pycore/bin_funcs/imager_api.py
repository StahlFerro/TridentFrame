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

from pycore.core_funcs.criterion import (
    CriteriaBundle,
    SplitCriteria,
    APNGOptimizationCriteria,
    ModificationCriteria,
    GIFOptimizationCriteria,
)
from pycore.core_funcs import logger
from pycore.core_funcs import config
from pycore.core_funcs.exception import MalformedCommandException
from pycore.utility import filehandler, imageutils


class GifsicleAPI:
    """Class wrapper around gifsicle's functionalities"""

    gifsicle_path = config.imager_exec_path("gifsicle")

    @classmethod
    def _combine_cmd_builder(cls, out_full_path: Path, crbundle: CriteriaBundle) -> List[str]:
        """Generate a list containing gifsicle command and its arguments.

        Args:
            out_full_path (Path): Output path of the final created GIF.
            crbundle (CriteriaBundle): Bundle of image creation criterias to build the arguments around.

        Returns:
            List[str]: List with the first element being the gifsicle executable path, with the following elements
            being its needed arguments.
        """
        criteria = crbundle.create_aimg_criteria
        gif_opt_criteria = crbundle.gif_opt_criteria
        delay = int(criteria.delay * 100)
        disposal = "background"
        loop_arg = "--loopcount"
        opti_mode = "--unoptimize"
        colorspace_arg = ""
        lossy_arg = ""
        if not criteria.loop_count or criteria.loop_count == 0:
            loop_arg = "--loopcount"
        elif criteria.loop_count == 1:
            loop_arg = "--no-loopcount"
        elif criteria.loop_count > 1:
            loop_arg = f"--loopcount={criteria.loop_count - 1}"
        globstar_path = "*.gif"
        if gif_opt_criteria:
            if gif_opt_criteria.is_optimized and gif_opt_criteria.optimization_level:
                opti_mode = f"--optimize={gif_opt_criteria.optimization_level}"
            if gif_opt_criteria.is_lossy and gif_opt_criteria.lossy_value:
                lossy_arg = f"--lossy={gif_opt_criteria.lossy_value}"
            if gif_opt_criteria.is_reduced_color and gif_opt_criteria.color_space:
                colorspace_arg = f"--colors={gif_opt_criteria.color_space}"

        args = [
            str(cls.gifsicle_path),
            opti_mode,
            lossy_arg,
            colorspace_arg,
            f"--delay={delay}",
            f"--disposal={disposal}",
            loop_arg,
            globstar_path,
            "--output",
            f'"{out_full_path}"',
        ]
        if ";" in " ".join(args):
            raise MalformedCommandException("gifsicle")
        return args

    @classmethod
    def _mod_args_builder(
        cls, criteria: ModificationCriteria, gif_criteria: GIFOptimizationCriteria
    ) -> List[Tuple[str, str]]:
        """Get a list of gifsicle arguments from either ModificationCriteria, or GIFOptimizationCriteria

        Args:
            criteria (ModificationCriteria): Image modification criteria
            gif_criteria (GIFOptimizationCriteria): GIF Optimization criteria

        Returns:
            List[Tuple[str, str]]: List of two valued tuples containing imagemagick argument on the first value, and
            a status string to echo out on the second value
        """
        args = []
        if criteria.must_resize():
            args.append((f"--resize={criteria.width}x{criteria.height}", "Resizing image..."))
        if criteria.orig_delay != criteria.delay:
            args.append(
                (
                    f"--delay={int(criteria.delay * 100)}",
                    f"Setting per-frame delay to {criteria.delay}",
                )
            )
        if gif_criteria.is_optimized and gif_criteria.optimization_level:
            args.append(
                (
                    f"--optimize={gif_criteria.optimization_level}",
                    f"Optimizing image with level {gif_criteria.optimization_level}...",
                )
            )
        if gif_criteria.is_lossy and gif_criteria.lossy_value:
            args.append(
                (
                    f"--lossy={gif_criteria.lossy_value}",
                    f"Lossy compressing with value: {gif_criteria.lossy_value}...",
                )
            )
        if gif_criteria.is_reduced_color and gif_criteria.color_space:
            args.append(
                (
                    f"--colors={gif_criteria.color_space}",
                    f"Reducing colors to: {gif_criteria.color_space}...",
                )
            )
        # if criteria.flip_x:
        #     args.append(("--flip-horizontal", "Flipping image horizontally..."))
        # if criteria.flip_y:
        #     args.append((f"--flip-vertical", "Flipping image vertically..."))
        if criteria.orig_loop_count != criteria.loop_count:
            loop_count = criteria.loop_count
            loop_arg = "--loopcount"
            if not loop_count or loop_count == 0:
                loop_arg = "--loopcount"
            elif loop_count == 1:
                loop_arg = "--no-loopcount"
            elif loop_count > 1:
                loop_arg = f"--loopcount={loop_count - 1}"
            args.append((loop_arg, f"Changing loop count to {loop_count or 'Infinite'}..."))
        return args

    @classmethod
    def combine_gif_images(cls, gifragment_dir: Path, out_full_path: Path, crbundle: CriteriaBundle) -> Path:
        """Combine a list of static GIF images in a directory into one animated GIF image.

        Args:
            gifragment_dir (List[Path]): Path to the directory containing static GIF images.
            out_full_path (Path): Full path including the name of the new animated GIF image.
            crbundle (CriteriaBundle): Bundle of image creation criteria to adhere to.

        Returns:
            Path: Path of the created GIF.
        """
        args = cls._combine_cmd_builder(out_full_path, crbundle)
        ROOT_PATH = str(os.getcwd())
        if os.getcwd() != gifragment_dir:
            logger.message(f"Changing directory from {os.getcwd()} to {gifragment_dir}")
            os.chdir(gifragment_dir)
        cmd = " ".join(args)
        logger.message("Combining frames...")
        result = subprocess.run(cmd, shell=True, capture_output=True)
        stdout_res = result.stdout.decode("utf-8")
        stderr_res = result.stderr.decode("utf-8")
        logger.message(stdout_res)
        logger.error(stderr_res)
        os.chdir(ROOT_PATH)
        return out_full_path

    @classmethod
    def modify_gif_image(cls, target_path: Path, out_full_path: Path, crbundle: CriteriaBundle) -> Path:
        """Use gifsicle to perform an array of modifications on an existing GIF image, by looping through the supplied
        arguments.

        Args:
            sicle_args (List[Tuple[str, str]]): gifsicle arguments.
            target_path (Path): Target path of the existing GIF image.
            out_full_path (Path): Output full path to save the GIF to.
            total_ops (int): UNUSED

        Returns:
            Path: Resulting path of the new modified GIF image.
        """
        sicle_args = cls._mod_args_builder(crbundle.modify_aimg_criteria, crbundle.gif_opt_criteria)
        # yield {"sicle_args": sicle_args}
        for index, (arg, description) in enumerate(sicle_args, start=1):
            # yield {"msg": f"index {index}, arg {arg}, description: {description}"}
            cmdlist = [
                str(cls.gifsicle_path),
                arg,
                f'"{target_path}"',
                "--output",
                f'"{out_full_path}"',
            ]
            cmd = " ".join(cmdlist)
            # yield {"msg": f"[{index}/{total_ops}] {description}"}
            # yield {"cmd": cmd}
            subprocess.run(cmd)
            if target_path != out_full_path:
                target_path = out_full_path
        return target_path

    @classmethod
    def extract_gif_frames(cls, unop_gif_path: Path, name: str, criteria: SplitCriteria) -> List[Path]:
        fragment_dir = filehandler.mk_cache_dir(prefix_name="fragment_dir")
        frames = []
        # indexed_ratios = _get_aimg_delay_ratios(unop_gif_path, "GIF", criteria.is_duration_sensitive)
        with Image.open(unop_gif_path) as gif:
            total_frames = gif.n_frames
        gifsicle_path = cls.gifsicle_path
        shout_nums = imageutils.shout_indices(total_frames, 1)
        for n in range(0, total_frames):
            if shout_nums.get(n):
                logger.message(f"Extracting frames ({n}/{total_frames})")
            split_gif_path: Path = fragment_dir.joinpath(f"{name}_{str.zfill(str(n), criteria.pad_count)}.png")
            args = [
                str(gifsicle_path),
                str(unop_gif_path),
                f'#{n}',
                "--output",
                str(split_gif_path)
            ]
            cmd = " ".join(args)
            logger.debug(cmd)
            process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            index = 0
            while process.poll() is None:
                output = process.stdout.readline()
                # if process.poll() is not None:
                # break
                # if output:
                #     output = output.decode("utf-8")
                #     logger.message(output.capitalize())
            frames.append(split_gif_path)
        return frames

    @classmethod
    def reduce_gif_color(cls, gif_path: Path, out_dir: Path, color: int = 256) -> Path:
        """Reduce the color of a GIF image.

        Args:
            gif_path (Path): Path to the GIF.
            out_dir (Path): Output directory to save the color-reduced GIF to.
            color (int, optional): Amount of color to reduce to. Defaults to 256.

        Returns:
            Path: Absolute path of the color-reduced GIF.
        """
        logger.message("Performing color reduction...")
        redux_gif_path = out_dir.joinpath(gif_path.name)
        args = [
            str(cls.gifsicle_path),
            f"--colors={color}",
            str(gif_path),
            "--output",
            str(redux_gif_path),
        ]
        cmd = " ".join(args)
        subprocess.run(cmd, shell=True)
        return redux_gif_path

    @classmethod
    def unoptimize_gif(cls, gif_path: Path, out_dir: Path) -> Path:
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
        args = [
            str(cls.gifsicle_path),
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


class ImageMagickAPI:

    imagemagick_path = config.imager_exec_path("imagemagick")

    @classmethod
    def _mod_args_builder(cls, gifopt_criteria: GIFOptimizationCriteria) -> List[Tuple[str, str]]:
        """Get a list of imagemagick arguments from a GIFOptimizationCriteria

        Args:
            gifopt_criteria (GIFOptimizationCriteria): GIF Optimization Criteria

        Returns:
            List[Tuple[str, str]]: List of two valued tuples containing imagemagick argument on the first value, and a status string to echo out on the second value
        """
        args = []
        if gifopt_criteria.is_unoptimized:
            args.append(("-coalesce", "Unoptimizing GIF..."))
        # if criteria.rotation and criteria.rotation != 0:
        #     args.append((f"-rotate {criteria.rotation}", f"Rotating image {criteria.rotation} degrees..."))
        return args

    @classmethod
    def imagemagick_render(cls, target_path: Path, out_full_path: Path, crbundle: CriteriaBundle) -> Path:
        """Use imagemagick to perform an array of modifications to an existing animated image.

        Args:
            magick_args (List[Tuple[str, str]]): Arguments to supply to imagemagick.
            target_path (Path): Target path of the animated image.
            out_full_path (Path): Output full path to save the animated image to.
            total_ops (int, optional): UNUSED. Defaults to 0.
            shift_index (int, optional): UNUSED. Defaults to 0.

        Returns:
            Path: Path of the new modified animated image.
        """
        magick_args = cls._mod_args_builder(crbundle.gif_opt_criteria)
        # yield {"magick_args": magick_args}
        for index, (arg, description) in enumerate(magick_args, start=1):
            logger.message(f"index {index}, arg {arg}, description: {description}")
            cmdlist = [
                str(cls.imagemagick_path),
                arg,
                f'"{target_path}"',
                "--output",
                f'"{out_full_path}"',
            ]
            cmd = " ".join(cmdlist)
            # logger.message(f"[{shift_index + index}/{total_ops}] {description}")
            # yield {"cmd": cmd}
            subprocess.run(cmd)
            if target_path != out_full_path:
                target_path = out_full_path
        return target_path

    @classmethod
    def unoptimize_gif(cls, gif_path: Path, out_dir: Path) -> Path:
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
        args = [
            str(cls.imagemagick_path),
            "-coalesce",
            str(gif_path),
            str(unop_gif_save_path)
        ]
        cmd = " ".join(args)
        logger.debug(cmd)
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        index = 0
        while process.poll() is None:
            output = process.stdout.readline()
            # if process.poll() is not None:
            # break
            if output:
                output = output.decode("utf-8")
                logger.message(output.capitalize())
        return unop_gif_save_path


class APNGOptAPI:

    opt_exec_path = config.imager_exec_path("apngopt")

    @classmethod
    def _opt_args_builder(cls, apngopt_criteria: APNGOptimizationCriteria) -> List[Tuple[str, str]]:
        """Get a list apngopt arguments from an APNGOptimizationCriteria

        Args:
            apngopt_criteria (APNGOptimizationCriteria): APNG Optimization criteria

        Returns:
            List[Tuple[str, str]]: List of two valued tuples containing apngopt argument on the first value, and a status string to echo out on the second value
        """
        args = []
        if apngopt_criteria.is_optimized:
            args.append(
                (
                    f"-z{apngopt_criteria.optimization_level - 1}",
                    f"Optimizing APNG with level {apngopt_criteria.optimization_level} compression...",
                )
            )
        return args

    @classmethod
    def optimize_apng(
        cls,
        target_path: Path,
        out_full_path: Path,
        apngopt_criteria: APNGOptimizationCriteria,
    ) -> Path:
        """Use apngopt to optimize an APNG. Returns the output path

        Args:
            aopt_args (List[Tuple[str, str]]): apngopt arguments
            target_path (Path): Target path of the animated image to be optimized
            out_full_path (Path): Destination output path to save the optimized image to
            total_ops (int, optional): UNUSED. Defaults to 0.
            shift_index (int, optional): UNUSED. Defaults to 0.

        Returns:
            Path: [description]
        """
        aopt_args = cls._opt_args_builder(apngopt_criteria)
        aopt_dir = filehandler.mk_cache_dir(prefix_name="apngopt_dir")
        filename = target_path.name
        aopt_temp_path = aopt_dir.joinpath(filename)
        logger.message(f"COPY FROM {target_path} TO {aopt_temp_path}")
        target_path = shutil.copy(target_path, aopt_temp_path, follow_symlinks=False)
        cwd = os.getcwd()
        # common_path = os.path.commonpath([opt_exec_path, target_path])
        target_rel_path = Path(os.path.relpath(target_path, cwd))
        for index, (arg, description) in enumerate(aopt_args, start=1):
            logger.message(f"index {index}, arg {arg}, description: {description}")
            cmdlist = [
                str(cls.opt_exec_path),
                arg,
                str(target_rel_path),
                str(target_rel_path),
            ]
            # raise Exception(cmdlist, out_full_path)
            cmd = " ".join(cmdlist)
            # result = subprocess.check_output(cmd, shell=True)
            logger.message("Starting optimization...")
            process = subprocess.Popen(cmdlist, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            index = 0
            while process.poll() is None:
                output = process.stdout.readline()
                # if process.poll() is not None:
                # break
                if output:
                    output = output.decode("utf-8")
                    logger.message(output.capitalize())
                    if "saving" in output:
                        out_words = " ".join(
                            output.translate({ord("\r"): None, ord("\n"): None}).capitalize().split(" ")[3:]
                        )[:-1]
                        out_msg = f"Optimizing frame {out_words}..."
                        logger.message(out_msg)
                        index += 1
            # if target_path != out_full_path:
            # target_path = out_full_path
        out_full_path = shutil.move(target_path, out_full_path)
        # shutil.rmtree(aopt_dir)
        return out_full_path


class APNGDisAPI:

    dis_exec_path = config.imager_exec_path("apngdis")

    @classmethod
    def _dis_args_builder(cls, criteria: ModificationCriteria) -> List[Tuple[str, str]]:
        args = []
        return args
    @classmethod
    def split_apng(cls, target_path: Path, seq_rename: str = "", out_dir: Path = "") -> Iterator[Path]:
        """Split an APNG image into its individual frames using apngdis

        Args:
            target_path (Path): Path of the APNG.
            seq_rename (str, optional): New prefix name of the sequence. Defaults to "".
            out_dir (Path, optional): Output directory. Defaults to "".

        Returns:
            Iterator[Path]: Iterator of paths to each split image frames of the APNG.
        """
        split_dir = filehandler.mk_cache_dir(prefix_name="apngdis_dir")
        filename = target_path.name
        target_path = shutil.copyfile(target_path, split_dir.joinpath(filename))
        cwd = os.getcwd()
        # target_rel_path = os.path.relpath(target_path, cwd)
        args = [str(cls.dis_exec_path), str(target_path)]
        if seq_rename:
            args.append(seq_rename)
        cmd = " ".join(args)
        # logger.message(f"APNGDIS ARGS: {cmd}")
        fcount = len(APNG.open(target_path).frames)
        shout_nums = imageutils.shout_indices(fcount, 5)
        process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
        )
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
                logger.message(f"Extracting frames... ({shout_nums.get(index)})")
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
        fragment_paths = (split_dir.joinpath(f) for f in split_dir.glob("*") if
                          f != filename and f.suffixes[-1] == ".png")
        return fragment_paths
        # Remove generated text file and copied APNG file


class PNGQuantAPI:

    pngquant_path = config.imager_exec_path("pngquant")

    @classmethod
    def _pngquant_args_builder(cls, apngopt_criteria: APNGOptimizationCriteria) -> List[Tuple[str, str]]:
        """Get a list of pngquant arguments from an APNGOptimizationCriteria

        Args:
            apngopt_criteria (APNGOptimizationCriteria): APNG Optimization criteria

        Returns:
            List[Tuple[str, str]]: List of two valued tuples containing pngquant argument on the first value, and a status string to echo out on the second value
        """
        args = []
        if apngopt_criteria.is_lossy and apngopt_criteria.lossy_value:
            args.append(
                (
                    f"--quality={apngopt_criteria.lossy_value}",
                    f"Quantizing PNG with quality value: {apngopt_criteria.lossy_value}",
                )
            )
        # if criteria.apng_is_lossy:
        # args.append(())
        return args

    @classmethod
    def quantize_png_images(
        cls,
        apngopt_criteria: APNGOptimizationCriteria,
        image_paths: List[Path],
        out_dir: Path = "",
    ) -> List[Path]:
        """Use pngquant to perform an array of modifications on a sequence of PNG images.

        Args:
            pq_args (List): pngquant arguments.
            image_paths (List[Path]): Path to each image
            optional_out_path (Path, optional): Optional path to save the quantized PNGs to. Defaults to "".

        Returns:
            List[Path]: [description]
        """
        if not out_dir:
            out_dir = filehandler.mk_cache_dir(prefix_name="quant_temp")
        pq_args = cls._pngquant_args_builder(apngopt_criteria)
        quantized_frames = []
        logger.message(pq_args)
        # quant_dir = mk_cache_dir(prefix_name="quant_dir")
        shout_nums = imageutils.shout_indices(len(image_paths), 1)
        for index, ipath in enumerate(image_paths):
            target_path = out_dir.joinpath(ipath.name)
            if shout_nums.get(index):
                logger.message(f"Quantizing PNG... ({shout_nums.get(index)})")
            args = [
                str(cls.pngquant_path),
                " ".join([arg[0] for arg in pq_args]),
                str(ipath),
                "--force",
                "--output",
                str(target_path),
            ]
            cmd = " ".join(args)
            result = subprocess.check_output(args)
            # Convert back to RGBA image
            with Image.open(target_path).convert("RGBA") as rgba_im:
                rgba_im.save(target_path)
            quantized_frames.append(target_path)
        # yield {"ssdsdsssdsd": quantized_frames}
        return quantized_frames


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
