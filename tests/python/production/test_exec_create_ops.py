import json
import pytest
import subprocess
import shlex
from typing import List
from itertools import chain
from pathlib import Path
from typing import Dict


def test_create_gif_prod(fx_prod_exec_path: Path, fx_samples_checkers_01_sequence: List[Path], fx_samples_crbundle_001_create_optimized_gif_json: Dict,
                         scaffold_spaced_dir: Path):
    fname = "good gif.gif"
    tmp_out_path = scaffold_spaced_dir.joinpath(fname)
    crpack = fx_samples_crbundle_001_create_optimized_gif_json
    crbundle = {
        "criteria": crpack["criteria"],
        "gif_opt_criteria": crpack["gif_opt_criteria"],
        "apng_opt_criteria": crpack["apng_opt_criteria"],
    }
    print(json.dumps(crbundle))
    json_command = {
        "command": "combine_image",
        "args": [
            [str(sq) for sq in fx_samples_checkers_01_sequence],
            str(tmp_out_path),
            crbundle
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


def test_create_apng_prod(fx_prod_exec_path: Path, fx_samples_checkers_01_sequence: List[Path], fx_samples_crbundle_002_create_optimized_apng_json: Dict,
                          scaffold_spaced_dir: Path):
    fname = "$ome #apng.gif"
    tmp_out_path = scaffold_spaced_dir.joinpath(fname)
    crpack = fx_samples_crbundle_002_create_optimized_apng_json
    crbundle = {
        "criteria": crpack["criteria"],
        "gif_opt_criteria": crpack["gif_opt_criteria"],
        "apng_opt_criteria": crpack["apng_opt_criteria"],
    }
    json_command = {
        "command": "combine_image",
        "args": [
            [str(sq) for sq in fx_samples_checkers_01_sequence],
            str(tmp_out_path),
            crbundle,
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
