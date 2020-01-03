#!venv/bin/python

import json
import os
import platform
import hashlib
from pprint import pprint


SCRIBE_PATH = os.path.realpath(__file__)
SCRIBE_DIR = os.path.dirname(SCRIBE_PATH)
MD_DIR = os.path.join(SCRIBE_DIR, "markdown")
PROJECT_DIR = os.path.abspath(os.path.join(SCRIBE_DIR, ".."))
RELEASES_DIR = os.path.join(PROJECT_DIR, "release/tridentframe/")
PACKAGEJSON_PATH = os.path.join(PROJECT_DIR, "package.json")

package_json = {}
targets = []
scribe_texts = []
os_name = ""
with open(PACKAGEJSON_PATH, "r") as jsonfile:
    package_json = json.load(jsonfile)

build_info = package_json['build']
VERSION = package_json['version']
print("VERSION", VERSION)

os_name = platform.system()
if os_name == 'Windows':
    targets = build_info['win']['target']
elif os_name == 'Linux':
    targets = build_info['linux']['target']

releases_content = (os.path.join(RELEASES_DIR, diritem) for diritem in os.listdir(RELEASES_DIR))
release_files = [r for r in releases_content if os.path.isfile(r)]
for target in targets:
    print(target)
    relfile = next((r for r in release_files if target == os.path.splitext(os.path.basename(r))[1][1:]), None)
    print(relfile)
    sha256_hash = hashlib.sha256()
    hashstring = ""
    if relfile:
        with open(relfile, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
            hashstring = sha256_hash
    scribe_texts.append(f"- **{target}** {os.path.basename(relfile)}")
    scribe_texts.append(f"  SHA256: `{hashstring.hexdigest()}`")

with open(os.path.join(MD_DIR, "version.md"), "w") as mdfile:
    mdfile.write("\n".join(scribe_texts))
