from pathlib import Path
import subprocess
import json


def test_echo(fx_prod_exec_path: Path):
    p = subprocess.Popen([str(fx_prod_exec_path)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = p.communicate('{"command": "echo", "args": ["Hello TridentFrame"]}'.encode('utf-8'))
    output = output[0]
    outstr = output.decode('utf-8')
    outjson = json.loads(outstr)
    assert outjson.get("debug")
    assert outjson["debug"] == 'Hello TridentFrame echoed'
