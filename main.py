import sys
import os
import json
from pathlib import Path


IS_FROZEN = getattr(sys, "frozen", False)
if IS_FROZEN:
    frozen_dir = Path(sys.executable).resolve().parents[0]
    # print(json.dumps({"msg": f"Detected frozen dir: {frozen_dir}"}))
    os.chdir(frozen_dir)


from pycore.core_funcs import logger
from pycore.core_funcs import exception
from typing import Dict, List
from pycore.inspect_ops import inspect_sequence, inspect_general, _inspect_smart
from pycore.create_ops import create_aimg
from pycore.split_ops import split_aimg
from pycore.sprite_ops import _build_spritesheet, _slice_spritesheet
from pycore.modify_ops import modify_aimg
from pycore.core_funcs.criterion import (
    CriteriaBundle,
    CreationCriteria,
    SplitCriteria,
    ModificationCriteria,
    SpritesheetBuildCriteria,
    SpritesheetSliceCriteria,
    GIFOptimizationCriteria,
    APNGOptimizationCriteria,
)
from pycore.core_funcs.config import get_absolute_cache_path, get_absolute_temp_path


class TridentFrameImager:
    def echo(self, msg):
        print(msg)
        return f"{msg} echoed"

    def echostream(self, stdin_data):
        print(type(stdin_data))
        if type(stdin_data) != str:
            print(stdin_data.read())
        else:
            print(stdin_data)

    def inspect_one(self, image_path: str, filter: str = ""):
        """Inspect a single image and then return its information"""
        image_path = Path(image_path).resolve()
        if not image_path.exists():
            raise FileNotFoundError(f"{image_path} not found")
        info = inspect_general(image_path, filter)
        if info:
            logger.data(info)

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
            logger.data(info)

    def inspect_smart(self, image_path: str):
        """Inspect a sequence of images and then return their information"""
        if not image_path:
            raise Exception("Please load an image!")
        elif type(image_path) is list:
            image_path = image_path[0]
        image_path = Path(image_path).resolve()
        if not image_path.exists():
            raise FileNotFoundError(image_path.name)
        info = _inspect_smart(image_path)
        if info:
            logger.data(info)

    def combine_image(self, image_paths: List[str], out_dir: str, criteria_pack: Dict):
        """Combine multiple static images into a single animated image file"""
        """Combine a sequence of images into a GIF/APNG"""
        # raise Exception(image_paths, out_dir, filename, fps, extension, fps, reverse, transparent)
        if not image_paths and not out_dir:
            raise Exception("Please load the images and choose the output folder!")
        elif not image_paths:
            raise Exception("Please load the images!")
        elif not out_dir:
            raise Exception("Please choose the output folder!")
        resolved_paths = []
        for ipath in image_paths:
            resolved_path = Path(ipath).resolve()
            if resolved_path.exists():
                resolved_paths.append(resolved_path)
        missing_paths = set(image_paths) - set((str(rp) for rp in resolved_paths))
        out_dir = Path(out_dir).resolve()
        if len(missing_paths) == len(image_paths):
            raise FileNotFoundError("All of the image sequences are missing! Check if they are not moved/deleted")
        if not out_dir.exists():
            raise FileNotFoundError(out_dir)
        crbundle = CriteriaBundle(
            {
                "create_aimg_criteria": CreationCriteria(criteria_pack["criteria"]),
                "gif_opt_criteria": GIFOptimizationCriteria(criteria_pack["gif_opt_criteria"]),
                "apng_opt_criteria": APNGOptimizationCriteria(criteria_pack["apng_opt_criteria"]),
            }
        )
        out_path = create_aimg(resolved_paths, out_dir, criteria_pack["criteria"]["name"], crbundle)
        if out_path:
            logger.data(str(out_path))
        if len(missing_paths) > 0:
            logger.warn(str(missing_paths))
        return

    def split_image(self, image_path: str, out_dir: str, criteria_vals: SplitCriteria):
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
            raise FileNotFoundError(out_dir)
        criteria = SplitCriteria(criteria_vals)
        split_aimg(image_path, out_dir, criteria)
        return

    def modify_image(self, image_path, out_dir, criteria_pack):
        """Modify the criteria and behavior of a GIF/APNG"""
        if not image_path and not out_dir:
            raise Exception("Please load a GIF or APNG and choose the output folder!")
        elif not image_path:
            raise Exception("Please load a GIF or APNG!")
        elif not out_dir:
            raise Exception("Please choose an output folder!")
        crbundle = CriteriaBundle(
            {
                "modify_aimg": ModificationCriteria(criteria_pack["criteria"]),
                "gif_opt": GIFOptimizationCriteria(criteria_pack["gif_opt"]),
                "apng_opt": APNGOptimizationCriteria(criteria_pack["apng_opt"]),
            }
        )
        return modify_aimg(image_path, out_dir, crbundle)

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
            logger.message(str(e))
        if not data:
            raise Exception("No data received from stdin!")
        pyimager = TridentFrameImager()
        try:
            method = getattr(pyimager, data["command"])
        except AttributeError:
            errmsg = f"Method {data['command']} not implemented"
            raise NotImplementedError(errmsg)
        globalvar_overrides = data.get("globalvar_overrides", None)
        if globalvar_overrides:
            debug = globalvar_overrides.get("debug", None)
            if debug is not None:
                exception.set_exception_handler(debug)
        args = data["args"]
        method(*args)


if __name__ == "__main__":
    main()
