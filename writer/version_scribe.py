#!venv/bin/python

import json
import os
import platform
from pprint import pprint


SCRIBE_PATH = os.path.realpath(__file__)
SCRIBE_DIR = os.path.dirname(SCRIBE_PATH)
PROJECT_DIR = os.path.abspath(os.path.join(SCRIBE_DIR, ".."))
RELEASES_DIR = os.path.join(PROJECT_DIR, "release/tridentframe/")
PACKAGEJSON_PATH = os.path.join(PROJECT_DIR, "package.json")

package_json = {}
with open(PACKAGEJSON_PATH, "r") as jsonfile:
    package_json = json.load(jsonfile)

build_info = package_json['build']

if platform.system() == 'Windows':
    targets = build_info['win']['target']
elif platform.system() == 'Linux':
    targets = build_info['linux']['target']

releases_content = (os.path.join(RELEASES_DIR, diritem) for diritem in os.listdir(RELEASES_DIR))
release_files = [r for r in releases_content if os.path.isfile(r)]
for target in targets:
    print(target)
    relfile = next((r for r in release_files if target == os.path.splitext(os.path.basename(r))[1][1:]), "None")
    print(relfile)
    
