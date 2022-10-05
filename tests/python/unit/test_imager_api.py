import io
import json
import pytest
from typing import List, Dict
from pathlib import Path
from pycore.utility.sysinfo import os_platform, parent_process_name, shell_type, OS, SHELL
from pycore.bin_funcs.imager_api import GifsicleAPI
from pycore.core_funcs.exception import MalformedCommandException
from pycore.utility.sysinfo import shell_type
from pycore.models.criterion import CriteriaBundle, CreationCriteria, GIFOptimizationCriteria, APNGOptimizationCriteria


def test_malformed_combine_cmd_builder(fx_samples_checkers_02_sequence: List[Path],
                                       fx_samples_crbundle_002_create_optimized_apng_json: Path,
                                       scaffold_spaced_dir: Path):
    crpack = fx_samples_crbundle_002_create_optimized_apng_json
    crbundle = CriteriaBundle({
        "create_aimg_criteria": CreationCriteria(crpack["criteria"]),
        "gif_opt_criteria": GIFOptimizationCriteria(crpack["gif_opt_criteria"]),
        "apng_opt_criteria": APNGOptimizationCriteria(crpack["apng_opt_criteria"]),
    })
    frames_info = crbundle.create_aimg_criteria.get_frames_info(len(fx_samples_checkers_02_sequence))
    must_quote = os_platform() == OS.LINUX
    malicious_path = Path(str(scaffold_spaced_dir) + "animated_image.png; echo 'rm -rf';").resolve()
    with pytest.raises(MalformedCommandException) as excinfo:
        cmd_list = GifsicleAPI._combine_cmd_builder(malicious_path, crbundle, frames_info, must_quote)
    assert 'is malformed' in str(excinfo.value)


def test_parent_process_name():
    assert parent_process_name() is not None


def test_current_shell_type():
    assert shell_type() is not None
