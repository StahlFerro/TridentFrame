import os
import io
import math
import uuid
import shlex
import shutil
import subprocess
from pathlib import Path
from sys import platform, stderr
from enum import Enum, unique
from typing import List, Tuple, Iterator, Optional, Generator

from PIL import Image
from apng import APNG, FrameControl


from pycore.models.criterion import (
    CriteriaBundle,
    SplitCriteria,
    APNGOptimizationCriteria,
    ModificationCriteria,
    GIFOptimizationCriteria,
)
from pycore.models.metadata import ImageMetadata, AnimatedImageMetadata
from pycore.core_funcs import stdio
from pycore.core_funcs import config
from pycore.core_funcs.exception import MalformedCommandException, UnsupportedPlatformException, \
    UnsupportedImageModeException
from pycore.utility import filehandler, imageutils
from pycore.utility.sysinfo import os_platform, OS


@unique
class ALPHADITHER(Enum):
    """Options for different transparency dithering methods"""

    # Screen door transparency pattern inspired from
    # https://digitalrune.github.io/DigitalRune-Documentation/html/fa431d48-b457-4c70-a590-d44b0840ab1e.htm
    SCREENDOOR = 0
    DIFFUSION = 1  # Not implemented yet
    NOISE = 2  # Not implemented yet


class InternalImageAPI:

    @classmethod
    def dither_alpha(cls, im: Image, method: ALPHADITHER = ALPHADITHER.SCREENDOOR, threshold: int = 128,
                     w_mult: float = 2.0, w_factor: float = 1.6) -> Image:
        if im.mode != "RGBA":
            raise UnsupportedImageModeException(im.name, im.mode)
        if method == ALPHADITHER.SCREENDOOR:
            weights_matrix = [
                [1.0 / 16.0, 9.0 / 16.0, 3.0 / 16.0, 11.0 / 16.0],
                [13.0 / 16.0, 5.0 / 16.0, 15.0 / 16.0, 7.0 / 16.0],
                [4.0 / 16.0, 12.0 / 16.0, 2.0 / 16.0, 10.0 / 16.0],
                [16.0 / 16.0, 8.0 / 16.0, 14.0 / 16.0, 6.0 / 16.0],
            ]
            weights_matrix = [[math.pow(n * w_mult, w_factor + ((n - 0.5) * 3)) for n in mrow]
                              for mrow in weights_matrix]
            stdio.debug({"screendoor wmatrix": weights_matrix})
            width, height = im.size
            pixels = list(im.getdata())
            for y in range(int(height)):
                for x in range(int(width)):
                    index = y * width + x
                    pix = pixels[index]
                    orig_alpha = pix[3]
                    if orig_alpha == 0 or orig_alpha == 255:
                        continue
                    weight = weights_matrix[x % 4][y % 4]
                    display_alpha = orig_alpha * weight >= threshold
                    pixels[index] = (*pix[0:3], 255) if display_alpha else (*pix[0:3], 0)
            new_im = Image.new("RGBA", im.size)
            new_im.putdata(pixels)
            return new_im

    @classmethod
    def get_apng_frames(cls, apng: APNG, unoptimize: bool = False) -> \
            Generator[Tuple[Image.Image, FrameControl], None, None]:
        canvas: Image.Image
        for index, (png, control) in enumerate(apng.frames):
            final_im: Image.Image
            with io.BytesIO() as img_buf:
                png.save(img_buf)
                with Image.open(img_buf) as im:
                    stdio.debug({"index": index, "control": control, "mode": im.mode, "info": im.info})
                    if index == 0 or not unoptimize:
                        canvas = im.copy()
                        yield canvas.copy(), control
                    else:
                        prev_canvas = canvas.copy()
                        offsets = control.x_offset, control.y_offset
                        if control.blend_op == 0:
                            canvas.paste(im, box=offsets)
                        elif control.blend_op == 1:
                            canvas.alpha_composite(im, dest=offsets)
                        yield canvas.copy(), control
                        if control.depose_op == 1:
                            tp_mask: Image.Image
                            if im.mode == "P":
                                tp_mask = Image.new("P", size=im.size)
                                tp_mask.info["transparency"] = 0
                            elif im.mode == "RGB":
                                tp_color = im.info.get("transparency") if im.info.get("transparency") is not None else \
                                    [0, 0, 0]
                                stdio.debug({"tp_color": tp_color})
                                tp_mask = Image.new("RGB", size=im.size, color=tp_color)
                                tp_mask.info["transparency"] = tp_color
                                # tp_mask.show()
                            elif im.mode == "RGBA":
                                tp_mask = Image.new("RGBA", size=im.size)
                            canvas.paste(tp_mask, box=offsets)
                        elif control.depose_op == 2:
                            canvas = prev_canvas.copy()


class GifsicleAPI:
    """Class wrapper around gifsicle's functionalities"""

    gifsicle_path = config.imager_exec_path("gifsicle")

    @classmethod
    def _combine_cmd_builder(cls, out_full_path: Path, crbundle: CriteriaBundle, quotes=False) -> List[str]:
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
        args = [
            shlex.quote(str(cls.gifsicle_path)) if quotes else str(cls.gifsicle_path),
            opti_mode,
        ]
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
                args.append(opti_mode)
            if gif_opt_criteria.is_lossy and gif_opt_criteria.lossy_value:
                lossy_arg = f"--lossy={gif_opt_criteria.lossy_value}"
                args.append(lossy_arg)
            if gif_opt_criteria.is_reduced_color and gif_opt_criteria.color_space:
                colorspace_arg = f"--colors={gif_opt_criteria.color_space}"
                args.append(colorspace_arg)

        args.extend([
            f"--delay={delay}",
            f"--disposal={disposal}",
            loop_arg,
            globstar_path,
            "--output",
            shlex.quote(str(out_full_path)) if quotes else str(out_full_path),
        ])
        if ";" in " ".join(args):
            raise MalformedCommandException("gifsicle")
        return args

    @classmethod
    def _mod_options_builder(
            cls, metadata: AnimatedImageMetadata, criteria: ModificationCriteria, gif_criteria: GIFOptimizationCriteria
    ) -> List[Tuple[str, str]]:
        """Get a list of gifsicle arguments from either ModificationCriteria, or GIFOptimizationCriteria

        Args:
            criteria (ModificationCriteria): Image modification criteria
            gif_criteria (GIFOptimizationCriteria): GIF Optimization criteria

        Returns:
            List[Tuple[str, str]]: List of two valued tuples containing imagemagick argument on the first value, and
            a status string to echo out on the second value
        """
        options = []
        if criteria.must_resize(metadata):
            options.append((f"--resize={criteria.width}x{criteria.height}", "Resizing image..."))
        if criteria.must_redelay(metadata):
            options.append((f"--delay={int(criteria.delay * 100)}", f"Setting per-frame delay to {criteria.delay}"))
        if gif_criteria.is_optimized and gif_criteria.optimization_level:
            options.append((f"--optimize={gif_criteria.optimization_level}",
                            f"Optimizing image with level {gif_criteria.optimization_level}..."))
        if gif_criteria.is_lossy and gif_criteria.lossy_value:
            options.append((f"--lossy={gif_criteria.lossy_value}",
                            f"Lossy compressing with value: {gif_criteria.lossy_value}..."))
        if gif_criteria.is_reduced_color and gif_criteria.color_space:
            options.append((f"--colors={gif_criteria.color_space}",
                            f"Reducing colors to: {gif_criteria.color_space}..."))
        # if criteria.flip_x:
        #     args.append(("--flip-horizontal", "Flipping image horizontally..."))
        # if criteria.flip_y:
        #     args.append((f"--flip-vertical", "Flipping image vertically..."))
        if criteria.must_reloop(metadata):
            loop_count = criteria.loop_count
            loop_arg = "--loopcount"
            if not loop_count or loop_count == 0:
                loop_arg = "--loopcount"
            elif loop_count == 1:
                loop_arg = "--no-loopcount"
            elif loop_count > 1:
                loop_arg = f"--loopcount={loop_count - 1}"
            options.append((loop_arg, f"Changing loop count to {loop_count or 'Infinite'}..."))
        if ";" in " ".join(opt[0] for opt in options):
            raise MalformedCommandException("gifsicle")
        return options

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
        ROOT_PATH = str(os.getcwd())
        if os.getcwd() != gifragment_dir:
            stdio.message(f"Changing directory from {os.getcwd()} to {gifragment_dir}")
            os.chdir(gifragment_dir)
        stdio.message("Combining frames...")
        supressed_error_txts = ["warning: too many colors, using local colormaps",
                                "You may want to try", "input images have conflicting background colors",
                                "This means some animation frames may appear incorrect."]

        # result = subprocess.run(cmd, shell=True, capture_output=True)
        # stdout_res = result.stdout.decode("utf-8")
        # stderr_res = result.stderr.decode("utf-8")
        # logger.message(stdout_res)
        # if "gifsicle.exe: warning: too many colors, using local colormaps" not in stderr_res:
        #     logger.error(stderr_res)

        if os_platform() == OS.WINDOWS:
            args = cls._combine_cmd_builder(out_full_path, crbundle, quotes=False)
            stdio.debug(args)
            result = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif os_platform() == OS.LINUX:
            args = cls._combine_cmd_builder(out_full_path, crbundle, quotes=True)
            cmd = " ".join(args)
            stdio.debug(f"linux cmd -> {cmd}")
            result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        else:
            raise UnsupportedPlatformException(platform)
        while result.poll() is None:
            if result.stdout:
                stdout_res = result.stdout.readline().decode("utf-8")
                if stdout_res and not any(s in stdout_res for s in supressed_error_txts):
                    stdio.message(stdout_res)
            if result.stderr:
                stderr_res = result.stderr.readline().decode("utf-8")
                if stderr_res and not any(s in stderr_res for s in supressed_error_txts):
                    stdio.error(stderr_res)

        os.chdir(ROOT_PATH)
        return out_full_path

    @classmethod
    def modify_gif_image(cls, target_path: Path, out_full_path: Path, original_metadata: AnimatedImageMetadata,
                         crbundle: CriteriaBundle) -> Path:
        """Use gifsicle to perform an array of modifications on an existing GIF image, by looping through the supplied
        arguments.

        Args:
            target_path (Path): Target path of the existing GIF image.
            out_full_path (Path): Output full path to save the GIF to.
            original_metadata (AnimatedImageMetadata): Original GIF metadata
            crbundle (CriteriaBundle): Criteria bundle object

        Returns:
            Path: Resulting path of the new modified GIF image.
        """
        gifsicle_options = cls._mod_options_builder(original_metadata, crbundle.modify_aimg_criteria,
                                                    crbundle.gif_opt_criteria)
        supressed_error_txts = ["warning: too many colors, using local colormaps",
                                "You may want to try"]
        # yield {"sicle_args": sicle_args}
        if os_platform() not in (OS.WINDOWS, OS.LINUX):
            raise UnsupportedPlatformException(platform)
        for index, (option, description) in enumerate(gifsicle_options, start=1):
            # yield {"msg": f"index {index}, arg {arg}, description: {description}"}
            stdio.message(description)
            args = [
                shlex.quote(str(cls.gifsicle_path)) if os_platform() == OS.LINUX else str(cls.gifsicle_path),
                option,
                shlex.quote(str(target_path)) if os_platform() == OS.LINUX else str(target_path),
                "--output",
                shlex.quote(str(out_full_path)) if os_platform() == OS.LINUX else str(out_full_path)
            ]
            # cmd = " ".join(cmdlist)
            # yield {"msg": f"[{index}/{total_ops}] {description}"}
            # yield {"cmd": cmd}
            cmd = " ".join(args)
            if ";" in cmd:
                raise MalformedCommandException("gifsicle")
            stdio.debug(f"modify_gif_image cmd -> {cmd}")
            result = subprocess.Popen(args if os_platform() == OS.WINDOWS else cmd,
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                      shell=os_platform() == OS.LINUX)
            while result.poll() is None:
                if result.stdout:
                    stdout_res = result.stdout.readline().decode("utf-8")
                    if stdout_res and not any(s in stdout_res for s in supressed_error_txts):
                        stdio.message(stdout_res)
                if result.stderr:
                    stderr_res = result.stderr.readline().decode("utf-8")
                    if stderr_res and not any(s in stderr_res for s in supressed_error_txts):
                        stdio.error(stderr_res)
            if target_path != out_full_path:
                target_path = out_full_path
        return target_path

    @classmethod
    def extract_gif_frames(cls, gif_path: Path, name: str, criteria: SplitCriteria,
                           out_dir: Path) -> List[Path]:
        """Extract all frames of a GIF image and return a list of paths of each frame

        Args:
            gif_path (Path): Path to gif.
            name (str): Filename of sequence, before appending sequence numbers (zero-padded).
            criteria (SplitCriteria): Criteria to follow.
            out_dir (Optional[Path]): Optional output directory of the split frames, else use default fragment_dir

        Returns:
            List[Path]: List of paths of each extracted gif frame.
        """
        fr_paths = []
        # indexed_ratios = _get_aimg_delay_ratios(unop_gif_path, "GIF", criteria.is_duration_sensitive)
        with Image.open(gif_path) as gif:
            total_frames = gif.n_frames
        gifsicle_path = cls.gifsicle_path
        shout_nums = imageutils.shout_indices(total_frames, 1)
        for n in range(0, total_frames):
            if shout_nums.get(n):
                stdio.message(f"Extracting frames ({n}/{total_frames})")
            split_gif_path: Path = out_dir.joinpath(f"{name}_{str.zfill(str(n), criteria.pad_count)}.gif")
            args = [
                str(gifsicle_path),
                str(gif_path),
                f'#{n}',
                "--output",
                str(split_gif_path)
            ]
            cmd = " ".join(args)
            # logger.debug(cmd)
            process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            index = 0
            while process.poll() is None:
                output = process.stdout.readline()
                # if process.poll() is not None:
                # break
                # if output:
                #     output = output.decode("utf-8")
                #     logger.message(output.capitalize())
            fr_paths.append(split_gif_path)
        return fr_paths

    @classmethod
    def reduce_gif_color(cls, gif_path: Path, out_path: Path, color: int = 256) -> Path:
        """Reduce the color of a GIF image.

        Args:
            gif_path (Path): Path to the GIF.
            out_path (Path): Output path to save the color-reduced GIF as.
            color (int, optional): Amount of color to reduce to. Defaults to 256.

        Returns:
            Path: Absolute path of the color-reduced GIF.
        """
        stdio.message("Performing color reduction...")
        # redux_gif_path = out_dir.joinpath(gif_path.name)
        args = [
            str(cls.gifsicle_path),
            f"--colors={color}",
            str(gif_path),
            "--output",
            str(out_path),
        ]
        cmd = " ".join(args)
        subprocess.run(args)
        return out_path

    @classmethod
    def unoptimize_gif(cls, gif_path: Path, out_dir: Path) -> Path:
        """Perform GIF unoptimization using Gifsicle/ImageMagick, in order to obtain the true singular frames for
        Splitting purposes. Returns the path of the unoptimized GIF.

        Args:
            gif_path (Path): Path to GIF image
            out_dir (Path): Output directory of unoptimized GIF

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
        subprocess.run(cmd, shell=False)
        return unop_gif_save_path


class ImageMagickAPI:
    imagemagick_path = config.imager_exec_path("imagemagick")

    @classmethod
    def _mod_args_builder(cls, gifopt_criteria: GIFOptimizationCriteria) -> List[Tuple[str, str]]:
        """Get a list of imagemagick arguments from a GIFOptimizationCriteria

        Args:
            gifopt_criteria (GIFOptimizationCriteria): GIF Optimization Criteria

        Returns:
            List[Tuple[str, str]]: List of two valued tuples containing imagemagick argument on the first value, and a
            status string to echo out on the second value
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
            target_path (Path): Target path of the animated image.
            out_full_path (Path): Output full path to save the animated image to.

        Returns:
            Path: Path of the new modified animated image.
        """
        magick_args = cls._mod_args_builder(crbundle.gif_opt_criteria)
        # yield {"magick_args": magick_args}
        for index, (arg, description) in enumerate(magick_args, start=1):
            stdio.message(f"index {index}, arg {arg}, description: {description}")
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
    def unoptimize_gif(cls, gif_path: Path, out_path: Path) -> Path:
        """Perform GIF unoptimization using Gifsicle/ImageMagick, in order to obtain the true singular frames for
        Splitting purposes. Returns the path of the unoptimized GIF.

        Args:
            gif_path (Path): Path to GIF image
            out_path (Path): Output path of unoptimized GIF

        Returns:
            Path: Path of unoptimized GIF
        """
        # raise Exception(gif_path, out_dir)
        supressed_error_txts = ["binary operator expected"]
        args = [
            str(cls.imagemagick_path),
            "convert",
            "-coalesce",
            str(gif_path),
            str(out_path)
        ]
        cmd = " ".join(args)
        stdio.debug(cmd)
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while process.poll() is None:
            if process.stdout:
                stdout_res = process.stdout.readline().decode("utf-8")
                if stdout_res:
                    stdio.message(stdout_res)
            if process.stderr:
                stderr_res = process.stderr.readline().decode("utf-8")
                if stderr_res and not any(s in stderr_res for s in supressed_error_txts):
                    stdio.error(stderr_res)
        return out_path


    @classmethod
    def extract_unoptimized_gif_frames(cls, gif_path: Path, name: str, criteria: SplitCriteria,
                                       out_dir: Path) -> List[Path]:
        """Unoptimize and extract all frames of a GIF image and return a list of paths of each frame

        Args:
            gif_path (Path): Path to gif.
            name (str): Filename of sequence, before appending sequence numbers (zero-padded).
            criteria (SplitCriteria): Criteria to follow.
            out_dir (Optional[Path]): Optional output directory of the split frames, else use default fragment_dir

        Returns:
            List[Path]: List of paths of each extracted gif frame.
        """
        fr_count = Image.open(gif_path).n_frames
        pad_format = str(criteria.pad_count).zfill(4)
        output_format_path = out_dir.joinpath(f"{name}_%{pad_format}d.png")
        args = [
            str(cls.imagemagick_path),
            "-coalesce",
            "-verbose",
            str(gif_path),
            str(output_format_path)
        ]
        # Linux executable need to specify as 'magick convert', while windows already has the executable as 'convert.exe'
        if os_platform() == OS.LINUX:
            args.insert(1, "convert")
        cmd = " ".join(args)
        stdio.debug(f"extract_unoptimized_gif_frames cmd -> {cmd}")
        stdio.debug(args)
        process = subprocess.run(args, capture_output=True)
        print(process.stdout)
        print(process.stderr)
        # process.check_returncode()
        all_frnames = [f"{name}_{str(n).zfill(criteria.pad_count)}.png" for n in range(0, fr_count)]
        fr_paths = [p for p in out_dir.iterdir() if p.name in all_frnames]
        fr_paths.sort()
        return fr_paths


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
        # logger.message(f"COPY FROM {target_path} TO {aopt_temp_path}")
        target_path = shutil.copy(target_path, aopt_temp_path, follow_symlinks=False)
        cwd = os.getcwd()
        # common_path = os.path.commonpath([opt_exec_path, target_path])
        target_rel_path = Path(os.path.relpath(target_path, cwd))
        # out_rel_path = Path(os.path.relpath(out_full_path, cwd))
        newline_check = ["\r\n", "\n"]
        for index, (arg, description) in enumerate(aopt_args, start=1):
            stdio.message(f"index {index}, arg {arg}, description: {description}")
            cmdlist = [
                str(cls.opt_exec_path),
                arg,
                str(target_rel_path),
                str(target_rel_path),
            ]
            # raise Exception(cmdlist, out_full_path)
            cmd = " ".join(cmdlist)
            # result = subprocess.check_output(cmd, shell=True)
            stdio.message("Performing optimization...")
            stdio.debug(cmd)
            stdio.debug(cmdlist)
            process = subprocess.Popen(cmdlist, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            index = 0
            while process.poll() is None:
                # if process.poll() is not None:
                # break
                if process.stdout:
                    stdout_res = process.stdout.readline().decode("utf-8")
                    stdio.debug(stdout_res.capitalize())
                    if stdout_res and stdout_res not in newline_check and "saving" in stdout_res:
                        out_words = " ".join(
                            stdout_res.translate({ord("\r"): None, ord("\n"): None}).capitalize().split(" ")[3:]
                        )[:-1]
                        out_msg = f"Optimizing frame {out_words}..."
                        stdio.message(out_msg)
                        index += 1
                if process.stderr:
                    stderr_res = process.stderr.readline().decode("utf-8")
                    # if stderr_res and not any(s in stderr_res for s in supressed_error_txts):
                    if stderr_res:
                        stdio.error(stderr_res)
            # if target_path != out_full_path:
            # target_path = out_full_path
        out_full_path = shutil.move(target_path, out_full_path)
        shutil.rmtree(aopt_dir)
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
        uuid_name = f"{uuid.uuid4()}_"
        stdio.debug(f"UUID: {uuid_name}")
        args = [str(cls.dis_exec_path), str(target_path), uuid_name]
        if seq_rename:
            args.append(seq_rename)
        cmd = " ".join(args)
        # logger.message(f"APNGDIS ARGS: {cmd}")
        fcount = len(APNG.open(target_path).frames)
        stdio.debug(f"fcount: {fcount}")
        shout_nums = imageutils.shout_indices(fcount, 5)
        stdio.debug(f"split_apng cmd -> {cmd}")
        stdio.debug(args)
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
            stdio.message(index)
            output = process.stdout.readline()
            stdio.message(output)
            err = process.stderr.readline()
            if process.poll() is not None:
                break
            if output and shout_nums.get(index):
                stdio.message(f"Extracting frames... ({shout_nums.get(index)})")
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
        stdio.message("Getting splitdir...")
        fragment_paths = (split_dir.joinpath(f) for f in split_dir.glob("*") if
                          f != filename and f.name.startswith(uuid_name) and f.suffixes[-1] == ".png")
        return fragment_paths
        # Remove generated text file and copied APNG file

# class PNGQuantAPI:

#     pngquant_path = config.imager_exec_path("pngquant")

#     @classmethod
#     def _pngquant_args_builder(cls, apngopt_criteria: APNGOptimizationCriteria) -> List[str]:
#         """Get a list of pngquant arguments from an APNGOptimizationCriteria

#         Args:
#             apngopt_criteria (APNGOptimizationCriteria): APNG Optimization criteria

#         Returns:
#             List[Tuple[str, str]]: List of two valued tuples containing pngquant argument on the first value, and a status string to echo out on the second value
#         """
#         args = []
#         if apngopt_criteria.is_lossy:
#             lossyval = apngopt_criteria.lossy_value
#             speedval = apngopt_criteria.speed_value
#             if lossyval:
#                 args.append(f"--quality={lossyval}")
#             if speedval:
#                 args.append(f"--speed={speedval}")
#         logger.debug(f"aopt_criteria ------> {apngopt_criteria}")
#         logger.debug(f"internal args ------> {args}")
#         # if criteria.apng_is_lossy:
#         # args.append(())
#         return args

#     @classmethod
#     def quantize_png_image(
#         cls,
#         apngopt_criteria: APNGOptimizationCriteria,
#         image_path: Path,
#         out_dir: Path = "",
#     ) -> Path:
#         """Use pngquant to perform an array of modifications on a sequence of PNG images.

#         Args:
#             pq_args (List): pngquant arguments.
#             image_paths (List[Path]): Path to each image
#             optional_out_path (Path, optional): Optional path to save the quantized PNGs to. Defaults to "".

#         Returns:
#             List[Path]: [description]
#         """
#         # if not out_dir:
#         #     out_dir = filehandler.mk_cache_dir(prefix_name="quant_temp")
#         pq_args = cls._pngquant_args_builder(apngopt_criteria)
#         quantized_frames = []
#         # quantization_args = " ".join([arg[0] for arg in pq_args])
#         # descriptions = " ".join([arg[1] for arg in pq_args])
#         # quant_dir = mk_cache_dir(prefix_name="quant_dir")
#         # target_path = out_dir.joinpath(image_path.name)
#         args = [
#             str(cls.pngquant_path),
#             *pq_args,
#             str(image_path),
#             "--force",
#             "--output",
#             str(image_path),
#         ]
#         cmd = " ".join(args)
#         logger.debug(f"PNQUANT ARGSdddddddddddd ---------> {cmd}")
#         result = subprocess.check_output(args)
#         # Convert back to RGBA image
#         with Image.open(image_path).convert("RGBA") as rgba_im:
#             rgba_im.save(image_path)
#         # yield {"ssdsdsssdsd": quantized_frames}
#         return image_path


#     @classmethod
#     def quantize_png_images(
#         cls,
#         apngopt_criteria: APNGOptimizationCriteria,
#         image_paths: List[Path],
#         out_dir: Path = "",
#     ) -> List[Path]:
#         """Use pngquant to perform an array of modifications on a sequence of PNG images.

#         Args:
#             pq_args (List): pngquant arguments.
#             image_paths (List[Path]): Path to each image
#             optional_out_path (Path, optional): Optional path to save the quantized PNGs to. Defaults to "".

#         Returns:
#             List[Path]: [description]
#         """
#         if not out_dir:
#             out_dir = filehandler.mk_cache_dir(prefix_name="quant_temp")
#         pq_args = cls._pngquant_args_builder(apngopt_criteria)
#         quantized_frames = []
#         logger.debug("WILL QUANTIZE")
#         # quantization_args = " ".join([arg[0] for arg in pq_args])
#         # descriptions = " ".join([arg[1] for arg in pq_args])
#         # quant_dir = mk_cache_dir(prefix_name="quant_dir")
#         shout_nums = imageutils.shout_indices(len(image_paths), 1)
#         for index, ipath in enumerate(image_paths):
#             target_path = out_dir.joinpath(ipath.name)
#             if shout_nums.get(index):
#                 logger.message(f"Quantizing PNGs... ({shout_nums.get(index)})")
#             args = [
#                 str(cls.pngquant_path),
#                 *pq_args,
#                 str(ipath),
#                 "--force",
#                 "--output",
#                 str(target_path),
#             ]
#             cmd = " ".join(args)
#             logger.debug(f"PNQUANT ARGS ---------> {cmd}")
#             result = subprocess.check_output(args)
#             # Convert back to RGBA image
#             with Image.open(target_path).convert("RGBA") as rgba_im:
#                 rgba_im.save(target_path)
#             quantized_frames.append(target_path)
#         # yield {"ssdsdsssdsd": quantized_frames}
#         return quantized_frames
