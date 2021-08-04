import json
import pytest
from typing import List
from pathlib import Path
from apng import APNG
from pycore.models.criterion import CriteriaBundle, CreationCriteria, GIFOptimizationCriteria, APNGOptimizationCriteria
from pycore.inspect_ops import inspect_general
from pycore.create_ops import _build_gif, _build_apng


def test_build_gif(scaffold_temp_dir, fx_crbundle_001_create_optimized_gif: Path, fx_sequence_dir_contents: List[Path]):
    with open(fx_crbundle_001_create_optimized_gif, "r") as f:
        crpack = json.loads(f.read())
    crbundle = CriteriaBundle({
        "create_aimg_criteria": CreationCriteria(crpack["criteria"]),
        "gif_opt_criteria": GIFOptimizationCriteria(crpack["gif_opt_criteria"]),
        "apng_opt_criteria": APNGOptimizationCriteria(crpack["apng_opt_criteria"]),
    })
    tmp_out_path = scaffold_temp_dir.joinpath("checker_rotating.gif")
    out_path = _build_gif(fx_sequence_dir_contents, tmp_out_path, crbundle)
    assert out_path == tmp_out_path

    metadata = inspect_general(out_path)
    assert metadata.name['value'] == "checker_rotating.gif"
    assert metadata.base_filename['value'] == "checker_rotating"
    assert metadata.width['value'] == 71
    assert metadata.height['value'] == 71
    assert metadata.loop_count['value'] == 4
    assert metadata.fps['value'] == 10
    assert metadata.average_delay['value'] == 100
    assert metadata.frame_count['value'] == 4
    assert not metadata.has_transparency['value']
    assert metadata.hash_sha1['value'] == "17912c45bf386ca5ca86c50c6dad2edc11220ed1"


def test_build_apng(scaffold_temp_dir, fx_crbundle_002_create_optimized_apng: Path, fx_sequence_dir_contents):
    with open(fx_crbundle_002_create_optimized_apng, "r") as f:
        crpack = json.loads(f.read())
    crbundle = CriteriaBundle({
        "create_aimg_criteria": CreationCriteria(crpack["criteria"]),
        "gif_opt_criteria": GIFOptimizationCriteria(crpack["gif_opt_criteria"]),
        "apng_opt_criteria": APNGOptimizationCriteria(crpack["apng_opt_criteria"]),
    })
    tmp_out_path = scaffold_temp_dir.joinpath("not_tetris.png")
    out_path = _build_apng(fx_sequence_dir_contents, tmp_out_path, crbundle)
    assert out_path == tmp_out_path

    metadata = inspect_general(out_path)
    assert metadata.name['value'] == "not_tetris.png"
    assert metadata.base_filename['value'] == "not_tetris"
    assert metadata.width['value'] == 128
    assert metadata.height['value'] == 128
    assert metadata.loop_count['value'] == 0
    assert metadata.fps['value'] == 5
    assert metadata.average_delay['value'] == 200
    assert metadata.frame_count['value'] == 4
    assert metadata.has_transparency['value']
    assert metadata.hash_sha1['value'] == "cef0c9f6938a9d8d36a10e4bc13debeba5cb43e4"
