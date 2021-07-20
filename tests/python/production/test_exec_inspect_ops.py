import json
import pytest
import subprocess
import shlex
from itertools import chain
from pathlib import Path


def test_inspect_static_image_prod(fx_prod_exec_path: Path, fx_spaced_dir_static_image: Path):
    p = subprocess.Popen([str(fx_prod_exec_path)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    json_cmd = json.dumps({"command": "inspect_one", "args": [str(fx_spaced_dir_static_image)]})
    output = p.communicate(json_cmd.encode('utf-8'))
    chunks = [o.decode('utf-8') for o in output]
    parsed_chunks = [json.loads(pc) for pc in chain.from_iterable([c.splitlines() for c in chunks])]
    data = next(pc for pc in parsed_chunks if pc.get("data") is not None)['data']
    assert data is not None
    assert data.get('general_info') is not None
    info = data['general_info']
    assert Path(info['absolute_url']['value']) == fx_spaced_dir_static_image
    assert not info['is_animated']['value']
    assert info['width']['value'] == 4
    assert info['height']['value'] == 4
    assert info['name']['value'] == fx_spaced_dir_static_image.name
    assert info['fsize']['value'] == fx_spaced_dir_static_image.stat().st_size


def test_inspect_animated_image_prod(fx_prod_exec_path: Path, fx_spaced_dir_animated_image: Path):
    p = subprocess.Popen([str(fx_prod_exec_path)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    json_cmd = json.dumps({"command": "inspect_one", "args": [str(fx_spaced_dir_animated_image)]})
    output = p.communicate(json_cmd.encode('utf-8'))
    chunks = [o.decode('utf-8') for o in output]
    parsed_chunks = [json.loads(pc) for pc in chain.from_iterable([c.splitlines() for c in chunks])]
    data = next(pc for pc in parsed_chunks if pc.get("data") is not None)['data']
    assert data is not None
    assert data.get('general_info') is not None
    assert data.get('animation_info') is not None
    info = data['general_info']
    ainfo = data['animation_info']
    assert Path(info['absolute_url']['value']) == fx_spaced_dir_animated_image
    assert info['is_animated']['value']