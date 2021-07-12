import json
import pytest
from pathlib import Path
from pycore.models.criterion import CriteriaBundle, CreationCriteria, GIFOptimizationCriteria, APNGOptimizationCriteria
from pycore.create_ops import _build_apng


TEST_JSON_DIR = Path(__file__).resolve().parents[1].joinpath("_fixtures/json/")
TEST_SEQUENCE_PATH = [p for p in Path(__file__).resolve().parents[1].joinpath("_fixtures/sequence/").iterdir()
                 if p.stem.startswith("checker_4x4_")]


def test_build_apng(scaffold_temp_dir):
    with open(TEST_JSON_DIR.joinpath("createpanel_criteria_pack_001.json"), "r") as f:
        crpack = json.loads(f.read())
    crbundle = CriteriaBundle({
        "create_aimg_criteria": CreationCriteria(crpack["criteria"]),
        "gif_opt_criteria": GIFOptimizationCriteria(crpack["gif_opt_criteria"]),
        "apng_opt_criteria": APNGOptimizationCriteria(crpack["apng_opt_criteria"]),
    })
    tmp_out_path = scaffold_temp_dir.joinpath("not_tetris.png")
    out_path = _build_apng(TEST_SEQUENCE_PATH, tmp_out_path, crbundle)
    assert out_path == tmp_out_path
