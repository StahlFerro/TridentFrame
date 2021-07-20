import json
import pytest
import subprocess
import shlex
from pathlib import Path


@pytest.mark.parametrize("input_data, output_text", [
    ("Hello TridentFrame", "Hello TridentFrame"),
    ("Where's your motivation?", "Where's your motivation?"),
    (-420.69, "-420.69"),
    (True, "True"),
    (False, "False"),
    ("Goodbye TridentFrame", "Goodbye TridentFrame"),
])
def test_echo_prod(input_data, output_text, fx_prod_exec_path: Path):
    p = subprocess.Popen([str(fx_prod_exec_path)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    json_cmd = json.dumps({"command": "echo", "args": [input_data]})
    output = p.communicate(json_cmd.encode('utf-8'))
    output = output[0]
    outstr = output.decode('utf-8')
    outjson = json.loads(outstr)
    assert outjson.get("debug")
    assert outjson["debug"] == output_text
