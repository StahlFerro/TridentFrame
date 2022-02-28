import sys
import os
import json
import time
import ctypes
from pathlib import Path


IS_FROZEN = getattr(sys, "frozen", False)
if IS_FROZEN:
    frozen_dir = Path(sys.executable).resolve().parents[0]
    # print(json.dumps({"msg": f"Detected frozen dir: {frozen_dir}"}))
    os.chdir(frozen_dir)


from pycore.core_funcs import stdio, exception
from pycore.core_funcs.wrappers import enable_diagnostics
from pycore.utility import filehandler
from typing import Dict, List
from pycore.inspect_ops import inspect_sequence, inspect_general, inspect_sequence_autodetect
from pycore.create_ops import create_aimg
from pycore.split_ops import split_aimg
from pycore.sprite_ops import _build_spritesheet, _slice_spritesheet
from pycore.modify_ops import modify_aimg
from pycore.models.criterion import (
    CriteriaBundle,
    CreationCriteria,
    SplitCriteria,
    ModificationCriteria,
    SpritesheetBuildCriteria,
    SpritesheetSliceCriteria,
    GIFOptimizationCriteria,
    APNGOptimizationCriteria,
)
# from pycore.core_funcs.c_interface import c_ping


class TridentFrameImager:
    def __init__(self):
        self.start_time = time.time()

    def echo(self, msg):
        stdio.debug(f"{msg}")

    def ping_c_interface(self):
        pass
        msg = c_ping()
        stdio.message(msg)

    def info(self):
        stdio.debug({
            "name": "TridentFrame",
            "version": "0.1.0-beta.10",
        })

    def purge_previews_dir(self, excluded_images: List[str]):
        filehandler.empty_previews_dir(excluded_images)

    def purge_temp_dir(self, excluded_images: List[str]):
        filehandler.empty_temp_dir(excluded_images)

    def inspect_one(self, image_path: str, filter: str = ""):
        """Inspect a single image and then return its information"""
        image_path = Path(image_path).resolve()
        if not image_path.exists():
            raise FileNotFoundError(f"{image_path} not found")
        info = inspect_general(image_path, filter)
        if info:
            # print(info.__dict__)
            stdio.data(info.format_info())

    def inspect_many(self, image_paths: List[str]):
        """Inspect a sequence of images and then return their information.
        Intermediary buffer file is used to avoid char limit of command lines
        """
        resolved_paths = []
        for ipath in image_paths:
            cpath = Path(ipath).resolve()
            if cpath.exists():
                resolved_paths.append(cpath)
        info = inspect_sequence(resolved_paths)
        if info:
            stdio.data(info)

    def inspect_smart(self, image_path: str):
        """Inspect a sequence of images and then return their information"""
        if not image_path:
            raise Exception("Please load an image!")
        elif type(image_path) is list:
            image_path = image_path[0]
        image_path = Path(image_path).resolve()
        if not image_path.exists():
            raise FileNotFoundError(image_path.name)
        info = inspect_sequence_autodetect(image_path)
        if info:
            stdio.data(info)

    @enable_diagnostics
    # def combine_image(self, image_paths: List[str], out_dir: str, criteria_pack: Dict):
    def combine_image(self, image_paths: List[str], out_path: str, criteria_pack: Dict):
        """Combine a sequence of images into a GIF/APNG"""
        # raise Exception(image_paths, out_dir, filename, fps, extension, fps, reverse, transparent)
        if not image_paths and not out_path:
            raise Exception("Please load the images and choose the output file!")
        elif not image_paths:
            raise Exception("Please load the images!")
        elif not out_path:
            raise Exception("Please choose the output file!")
        resolved_paths = []
        for ipath in image_paths:
            resolved_path = Path(ipath).resolve()
            if resolved_path.exists():
                resolved_paths.append(resolved_path)
        missing_paths = set(image_paths) - set((str(rp) for rp in resolved_paths))
        out_path = Path(out_path).resolve()
        # out_dir = Path(out_dir).resolve()
        if len(missing_paths) == len(image_paths):
            raise FileNotFoundError("All of the image sequences are missing! Check if they are not moved/deleted")
        if not out_path.parent.exists():
            raise FileNotFoundError(f"The directory {str(out_path.parent)} is not found!")
        crbundle = CriteriaBundle({
            "create_aimg_criteria": CreationCriteria(criteria_pack["criteria"]),
            "gif_opt_criteria": GIFOptimizationCriteria(criteria_pack["gif_opt_criteria"]),
            "apng_opt_criteria": APNGOptimizationCriteria(criteria_pack["apng_opt_criteria"]),
        })
        out_path = create_aimg(resolved_paths, out_path, crbundle)
        stdio.preview_path(out_path)
        if out_path:
            stdio.data(str(out_path))
        if len(missing_paths) > 0:
            stdio.warn(str(missing_paths))
        return

    def split_image(self, image_path: str, out_dir: str, criteria_vals: Dict):
        """Split all the frames of a GIF/APNG into a sequence of images"""
        if not image_path and not out_dir:
            raise Exception("Please load a GIF or APNG and choose the output folder!")
        elif not image_path:
            raise Exception("Please load a GIF or APNG!")
        elif not out_dir:
            raise Exception("Please choose an output folder!")
        image_path = Path(image_path).resolve()
        out_dir = Path(out_dir).resolve()
        if not image_path.exists():
            raise FileNotFoundError(image_path.name)
        if not out_dir.exists():
            raise FileNotFoundError(f"The directory {out_dir} is not found!")
        criteria = SplitCriteria(criteria_vals)
        split_aimg(image_path, out_dir, criteria)
        return

    def modify_image(self, image_path: str, out_path: str, criteria_pack: Dict):
        """Modify the criteria and behavior of a GIF/APNG"""
        if not image_path and not out_path:
            raise Exception("Please load a GIF or APNG and choose the output folder!")
        elif not image_path:
            raise Exception("Please load a GIF or APNG!")
        elif not out_path:
            raise Exception("Please choose an output folder!")
        image_path = Path(image_path).resolve()
        out_path = Path(out_path).resolve()
        if not out_path.parent.exists():
            raise FileNotFoundError(f"The directory {str(out_path.parent)} is not found!")
        if not image_path.exists():
            raise FileNotFoundError(image_path.name)
        crbundle = CriteriaBundle({
            "modify_aimg_criteria": ModificationCriteria(criteria_pack["criteria"]),
            "gif_opt_criteria": GIFOptimizationCriteria(criteria_pack["gif_opt_criteria"]),
            "apng_opt_criteria": APNGOptimizationCriteria(criteria_pack["apng_opt_criteria"]),
        })
        out_path = modify_aimg(image_path, out_path, crbundle)
        if out_path:
            stdio.preview_path(out_path)
            stdio.control("MOD_FINISH")
        return

    def build_spritesheet(self, image_paths, out_dir, filename, vals: dict):
        """Build a spritesheet using the specified sequence of images"""
        if not image_paths and not out_dir:
            raise Exception("Please load the images and choose the output folder!")
        elif not image_paths:
            raise Exception("Please load the images!")
        elif not out_dir:
            raise Exception("Please choose the output folder!")
        criteria = SpritesheetBuildCriteria(vals)
        # raise Exception(criteria.__dict__)
        # yield {"msg": "yo"}
        return _build_spritesheet(image_paths, out_dir, filename, criteria)

    def slice_spritesheet(self, image_path, out_dir, filename, vals: dict):
        """Slice a spritesheet into individual sections"""
        if not image_path and not out_dir:
            raise Exception("Please load the spritesheet and choose the output folder!")
        elif not image_path:
            raise Exception("Please load the spritesheet!")
        elif not out_dir:
            raise Exception("Please choos the output folder")
        criteria = SpritesheetSliceCriteria(vals)
        return _slice_spritesheet(image_path, out_dir, filename, criteria)


def print_cwd():
    """Dev method for displaying python cwd"""
    msg = {
        "os.getcwd()": os.getcwd(),
        "sys.executable": sys.executable,
        "__file__": __file__,
        "IS_FROZEN": IS_FROZEN,
    }
    return msg


def handle_execpath():
    pass


def main():
    # print(json.dumps({"msg": "Main called"}))
    # handle_execpath()
    # print(json.dumps(print_cwd()))
    # print(json.dumps(f"{len(sys.argv) == 1}, {sys.stdin.isatty()}"))
    exception.set_exception_handler(True)
    if len(sys.argv) == 1 and not sys.stdin.isatty():
        data = {}
        try:
            data = json.loads(sys.stdin.read())
        except Exception as e:
            raise Exception(e)
        if not data:
            raise Exception("No data received from stdin!")
        pyimager = TridentFrameImager()
        try:
            # print(dir(pyimager))
            method = getattr(pyimager, data["command"])
            if method is None:
                raise AttributeError
        except AttributeError:
            errmsg = f"Method {data['command']} not implemented"
            raise NotImplementedError(errmsg)
        globalvar_overrides = data.get("globalvar_overrides", None)
        if globalvar_overrides:
            debug = globalvar_overrides.get("debug", None)
            if debug:
                exception.set_exception_handler(debug)
        args = data["args"]
        method(*args)


if __name__ == "__main__":
    # TRIDENT_CLIB = ctypes.CDLL("ccore/release/libtridentframe_cf.so")
    # val = ctypes.c_char_p(TRIDENT_CLIB.ping()).value
    # print(val)
    main()
