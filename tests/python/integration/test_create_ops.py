import json
import pytest
from typing import List, Dict
from pathlib import Path
from apng import APNG
from pycore.models.criterion import CriteriaBundle, CreationCriteria, GIFOptimizationCriteria, APNGOptimizationCriteria
from pycore.inspect_ops import inspect_general
from pycore.create_ops import create_aimg


def test_create_gif(scaffold_spaced_dir, fx_samples_crbundle_001_create_optimized_gif_json: Dict,
                    fx_samples_sequence_dir_contents: List[Path]):
    crpack = fx_samples_crbundle_001_create_optimized_gif_json
    crbundle = CriteriaBundle({
        "create_aimg_criteria": CreationCriteria(crpack["criteria"]),
        "gif_opt_criteria": GIFOptimizationCriteria(crpack["gif_opt_criteria"]),
        "apng_opt_criteria": APNGOptimizationCriteria(crpack["apng_opt_criteria"]),
    })
    tmp_out_path = scaffold_spaced_dir.joinpath("checker_rotating.gif")
    out_path = create_aimg(fx_samples_sequence_dir_contents, tmp_out_path, crbundle)
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


def test_create_apng(scaffold_spaced_dir: Path, fx_samples_crbundle_002_create_optimized_apng_json: Dict,
                     fx_samples_sequence_dir_contents: List[Path]):
    crpack = fx_samples_crbundle_002_create_optimized_apng_json
    crbundle = CriteriaBundle({
        "create_aimg_criteria": CreationCriteria(crpack["criteria"]),
        "gif_opt_criteria": GIFOptimizationCriteria(crpack["gif_opt_criteria"]),
        "apng_opt_criteria": APNGOptimizationCriteria(crpack["apng_opt_criteria"]),
    })
    tmp_out_path = scaffold_spaced_dir.joinpath("not_tetris.png")
    out_path = create_aimg(fx_samples_sequence_dir_contents, tmp_out_path, crbundle)
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
    assert metadata.hash_sha1['value'] == "657b0c1b7231fc150337bad43a0db2bcea11ea8d"
