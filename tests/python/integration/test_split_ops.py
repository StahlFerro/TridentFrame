import json
import pytest
from typing import List, Dict
from pathlib import Path
from apng import APNG
from pycore.models.criterion import CriteriaBundle, CreationCriteria, GIFOptimizationCriteria, APNGOptimizationCriteria
from pycore.inspect_ops import inspect_general
from pycore.models.criterion import SplitCriteria
from pycore.split_ops import split_aimg


def test_split_gif(tmpdir: Path, fx_samples_spaced_dir_agif_checker: Path,
                   fx_samples_splitcriteria_001_split_gif_json: Dict):
    temp_dir = Path(tmpdir).joinpath("Split gif")
    temp_dir.mkdir()
    split_criteria = SplitCriteria(fx_samples_splitcriteria_001_split_gif_json)
    split_images = split_aimg(fx_samples_spaced_dir_agif_checker, temp_dir, split_criteria)
    out_dirs = set(s.parents[0] for s in split_images)
    assert len(out_dirs) == 1
    out_dir = next(iter(out_dirs))
    out_dir_contents = list(o for o in out_dir.iterdir())
    assert out_dir == temp_dir
    assert len(out_dir_contents) == 4
    assert len(split_images) == 4
    assert len(split_images) == len(out_dir_contents)


def test_split_gif_with_delay_file(tmpdir: Path, fx_samples_spaced_dir_agif_checker: Path,
                   fx_samples_splitcriteria_002_split_gif_json: Dict):
    temp_dir = Path(tmpdir).joinpath("Split gif with delay files")
    temp_dir.mkdir()
    split_criteria = SplitCriteria(fx_samples_splitcriteria_002_split_gif_json)
    split_images = split_aimg(fx_samples_spaced_dir_agif_checker, temp_dir, split_criteria)
    out_dirs = set(s.parents[0] for s in split_images)
    assert len(out_dirs) == 1
    out_dir = next(iter(out_dirs))
    out_dir_contents = list(o for o in out_dir.iterdir())
    assert out_dir == temp_dir
    assert len(out_dir_contents) == 5
    assert len(split_images) == 4
    assert len(split_images) != len(out_dir_contents)

    delay_file = set(out_dir_contents).difference(set(split_images))
    assert len(delay_file) == 1
    delay_file = next(iter(delay_file))
    assert delay_file.exists()

