#!venv/bin/python

import json

package_json = {}

with open("../package.json", "r") as jsonfile:
    package_json = json.load(jsonfile)

build_info = package_json['build']
