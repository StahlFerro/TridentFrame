import json
from pathlib import Path
from pycore.models.criterion import TransformativeCriteria, CreationCriteria, SplitCriteria, CriteriaBundle,\
    GIFOptimizationCriteria, APNGOptimizationCriteria
from pycore.models.image_formats import ImageFormat


def test_transformative_criteria():
    trans_criteria = TransformativeCriteria({
        "width": 200.4,
        "height": 301.11,
        "resize_method": "hamming",
        "flip_x": True,
        "flip_y": False,
        "rotation": ""
    })
    assert trans_criteria.width == 200
    assert trans_criteria.height == 301
    assert trans_criteria.size == (trans_criteria.width, trans_criteria.height)
    assert trans_criteria.must_resize(width=400, height=400)
    assert trans_criteria.size == (200, 301)
    assert trans_criteria.resize_method == "HAMMING"
    assert trans_criteria.rotation == 0
    assert trans_criteria.flip_x
    assert not trans_criteria.flip_y
    assert trans_criteria.must_flip()


def test_creation_criteria():
    creation_criteria = CreationCriteria({
        "fps": "4",
        "delay": 0.25,
        "format": "GIF",
        "is_reversed": False,
        "preserve_alpha": False,
        "flip_x": False,
        "flip_y": False,
        "width": 320,
        "height": 320,
        "resize_method": "",
        "loop_count": "",
        "start_frame": "1",
        "rotation": 0
    })

    assert creation_criteria.size == (320, 320)
    assert not creation_criteria.must_resize(width=320, height=320)
    assert not creation_criteria.flip_x
    assert not creation_criteria.flip_y
    assert not creation_criteria.must_flip()
    assert creation_criteria.fps == 4
    assert creation_criteria.delay == 0.25
    assert creation_criteria.fps == 1/creation_criteria.delay
    assert creation_criteria.format == ImageFormat.GIF
    assert creation_criteria.resize_method == "BICUBIC"
    assert creation_criteria.loop_count == 0
    assert creation_criteria.start_frame == 0
    assert creation_criteria.rotation == 0


def test_split_criteria():
    split_criteria = SplitCriteria({
        "new_name": "Navigation",
        "pad_count": "3",
        "color_space": "",
        "is_duration_sensitive": False,
        "is_unoptimized": True,
        "convert_to_rgba": True,
        "extract_delay_info": True
    })

    assert split_criteria.is_unoptimized
    assert split_criteria.convert_to_rgba
    assert split_criteria.extract_delay_info
    assert split_criteria.new_name == "Navigation"
    assert split_criteria.pad_count == 3


def test_criteria_bundle(fx_samples_json_dir):
    with open(fx_samples_json_dir.joinpath("crbundle_002_create_optimized_apng.json"), "r") as f:
        crpack = json.loads(f.read())
    crbundle = CriteriaBundle({
        "create_aimg_criteria": CreationCriteria(crpack["criteria"]),
        "gif_opt_criteria": GIFOptimizationCriteria(crpack["gif_opt_criteria"]),
        "apng_opt_criteria": APNGOptimizationCriteria(crpack["apng_opt_criteria"]),
    })
    assert crbundle.create_aimg_criteria
    assert crbundle.apng_opt_criteria
