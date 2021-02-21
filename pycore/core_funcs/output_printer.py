import json
import sys


def out_message(message: str):
    data = {"msg": message}
    print(json.dumps(data))


def out_error(message: str):
    data = {"error": message}
    print(json.dumps(data), file=sys.stderr)


def out_control(message: str):
    data = {"CONTROL": message}
    print(json.dumps(data))
