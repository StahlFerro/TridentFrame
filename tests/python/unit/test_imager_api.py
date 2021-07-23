import io
import json
import pytest
from pathlib import Path
from pycore.utility.sysinfo import os_platform, shell_type, OS, SHELL
from pycore.bin_funcs.imager_api import GifsicleAPI
from pycore.core_funcs.exception import MalformedCommandException
from pycore.utility.sysinfo import shell_type
from pycore.models.criterion import CriteriaBundle, CreationCriteria, GIFOptimizationCriteria, APNGOptimizationCriteria


def test_malformed_combine_cmd_builder(fx_spaced_dir_animated_image: Path, fx_crbundle_002_create_optimized_apng: Path):
    with open(fx_crbundle_002_create_optimized_apng, "r") as f:
        crpack = json.loads(f.read())
    crbundle = CriteriaBundle({
        "create_aimg_criteria": CreationCriteria(crpack["criteria"]),
        "gif_opt_criteria": GIFOptimizationCriteria(crpack["gif_opt_criteria"]),
        "apng_opt_criteria": APNGOptimizationCriteria(crpack["apng_opt_criteria"]),
    })
    must_quote = os_platform() == OS.LINUX
    malicious_path = Path(str(fx_spaced_dir_animated_image) + "; echo 'rm -rf';").resolve()
    with pytest.raises(MalformedCommandException) as excinfo:
        cmd_list = GifsicleAPI._combine_cmd_builder(malicious_path, crbundle, must_quote)
    assert 'is malformed' in str(excinfo.value)


def test_current_shell_type():
    assert shell_type() != SHELL.OTHER

