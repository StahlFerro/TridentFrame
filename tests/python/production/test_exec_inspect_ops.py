import json
import pytest
import subprocess
import shlex
from itertools import chain
from pathlib import Path

from pycore.models.image_formats import ImageFormat


def test_inspect_static_image_prod(fx_prod_exec_path: Path, fx_samples_spaced_dir_static_image: Path):
    p = subprocess.Popen([str(fx_prod_exec_path)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    str_cmd = json.dumps({"command": "inspect_one", "args": [str(fx_samples_spaced_dir_static_image)]})
    output = p.communicate(str_cmd.encode('utf-8'))
    chunks = [o.decode('utf-8') for o in output]
    parsed_chunks = [json.loads(pc) for pc in chain.from_iterable([c.splitlines() for c in chunks])]
    data = next(pc for pc in parsed_chunks if pc.get("data") is not None)['data']
    assert data is not None
    assert data.get('general_info') is not None
    info = data['general_info']
    assert Path(info['absolute_url']['value']) == fx_samples_spaced_dir_static_image
    assert not info['is_animated']['value']
    assert info['width']['value'] == 4
    assert info['height']['value'] == 4
    assert info['name']['value'] == fx_samples_spaced_dir_static_image.name
    assert info['fsize']['value'] == fx_samples_spaced_dir_static_image.stat().st_size


def test_inspect_agif_prod(fx_prod_exec_path: Path, fx_samples_spaced_dir_agif_checker: Path):
    p = subprocess.Popen([str(fx_prod_exec_path)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    str_cmd = json.dumps({"command": "inspect_one", "args": [str(fx_samples_spaced_dir_agif_checker)]})
    output = p.communicate(str_cmd.encode('utf-8'))
    chunks = [o.decode('utf-8') for o in output]
    parsed_chunks = [json.loads(pc) for pc in chain.from_iterable([c.splitlines() for c in chunks])]
    data = next(pc for pc in parsed_chunks if pc.get("data") is not None)['data']
    assert data is not None
    assert data.get('general_info') is not None
    assert data.get('animation_info') is not None
    info = data['general_info']
    ainfo = data['animation_info']
    assert Path(info['absolute_url']['value']) == fx_samples_spaced_dir_agif_checker
    assert info['is_animated']['value']
    assert info['format']['value'] == "GIF"
    assert ImageFormat[info['format']['value']] == ImageFormat.GIF
    assert ainfo['frame_count']['value'] == 4
    assert ainfo['loop_count']['value'] == 0


def test_inspect_apng_prod(fx_prod_exec_path: Path, fx_samples_spaced_dir_apng_checker: Path):
    p = subprocess.Popen([str(fx_prod_exec_path)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    str_cmd = json.dumps({"command": "inspect_one", "args": [str(fx_samples_spaced_dir_apng_checker)]})
    output = p.communicate(str_cmd.encode('utf-8'))
    chunks = [o.decode('utf-8') for o in output]
    parsed_chunks = [json.loads(pc) for pc in chain.from_iterable([c.splitlines() for c in chunks])]
    data = next(pc for pc in parsed_chunks if pc.get("data") is not None)['data']
    assert data is not None
    assert data.get('general_info') is not None
    assert data.get('animation_info') is not None
    info = data['general_info']
    ainfo = data['animation_info']
    assert Path(info['absolute_url']['value']) == fx_samples_spaced_dir_apng_checker
    assert info['is_animated']['value']
    assert info['format']['value'] == "PNG"
    assert ainfo['frame_count']['value'] == 4
    assert ainfo['loop_count']['value'] == 0
