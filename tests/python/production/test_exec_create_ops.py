import json
import pytest
import subprocess
import shlex
from typing import List
from itertools import chain
from pathlib import Path


def test_create_gif_prod(fx_prod_exec_path: Path, fx_sequence_dir_contents: List[Path], scaffold_spaced_dir: Path):
    fname = "good gif.gif"
    tmp_out_path = scaffold_spaced_dir.joinpath(fname)
    json_command = {
        "command": "combine_image",
        "args": [
            [str(sq) for sq in fx_sequence_dir_contents],
            str(tmp_out_path),
            {
                "criteria": {
                    "fps": "2",
                    "delay": 0.5,
                    "format": "GIF",
                    "is_reversed": False,
                    "preserve_alpha": True,
                    "flip_x": False,
                    "flip_y": False,
                    "width": 320,
                    "height": 320,
                    "resize_method": "BICUBIC",
                    "loop_count": "",
                    "start_frame": "3",
                    "rotation": 0,
                    "name": ""
                },
                "gif_opt_criteria": {
                    "is_optimized": True,
                    "optimization_level": "1",
                    "is_lossy": True,
                    "lossy_value": "200",
                    "is_reduced_color": True,
                    "color_space": "50",
                    "is_unoptimized": False,
                    "is_dither_alpha": True,
                    "dither_alpha_method": "SCREENDOOR",
                    "dither_alpha_threshold": 50
                },
                "apng_opt_criteria": {
                    "apng_is_optimized": False,
                    "apng_optimization_level": "1",
                    "apng_is_lossy": False,
                    "apng_lossy_value": "",
                    "apng_is_unoptimized": False,
                    "apng_preconvert_rgba": False,
                    "apng_convert_color_mode": False,
                    "apng_new_color_mode": "RGBA"
                }
            }
        ],
        "globalvar_overrides": {"debug": True}
    }
    str_cmd = json.dumps(json_command)
    p = subprocess.Popen([str(fx_prod_exec_path)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    output = p.communicate(str_cmd.encode('utf-8'))
    chunks = [o.decode('utf-8') for o in output]
    parsed_chunks = [json.loads(pc) for pc in chain.from_iterable([c.splitlines() for c in chunks])]
    preview = next(pc for pc in parsed_chunks if pc.get('preview_path') is not None)['preview_path']
    data = next(pc for pc in parsed_chunks if pc.get("data") is not None)['data']
    assert tmp_out_path.exists()
    assert Path(preview) == tmp_out_path
    assert Path(data) == tmp_out_path
