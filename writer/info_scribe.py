import json
import platform
import hashlib
from pathlib import Path


SCRIBE_PATH = Path(__file__).resolve()
SCRIBE_DIR = Path(SCRIBE_PATH).parents[0]
MD_DIR = SCRIBE_DIR.joinpath("markdown")
PROJECT_DIR = SCRIBE_DIR.parents[0]
RELEASES_DIR = PROJECT_DIR.joinpath("release/tridentframe/")
PACKAGEJSON_FILE = PROJECT_DIR.joinpath("package.json")

package_json = {}
targets = []
scribe_texts = []
hash_info = []
os_name = ""
with open(PACKAGEJSON_FILE, "r") as jsonfile:
    package_json = json.load(jsonfile)
build_info = package_json['build']
VERSION = package_json['version']

os_name = platform.system()
if os_name == 'Windows':
    targets = build_info['win']['target']
    scribe_texts.append(f"- Windows 7 SP1, 10 (64bit)")
elif os_name == 'Linux':
    targets = build_info['linux']['target']
    scribe_texts.append(f"- Ubuntu 18.04 LTS (64bit)")
release_files = [RELEASES_DIR.joinpath(diritem) for diritem in RELEASES_DIR.glob("*") if Path.is_file(diritem)]
for target in targets:
    release_file = next((r for r in release_files if target == r.suffix[1:]), None)
    sha256_hash = hashlib.sha256()
    hash_obj = ''
    if release_file:
        with open(release_file, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
            hash_obj = sha256_hash
        checksum = hash_obj.hexdigest()
        scribe_texts.append(f"  - **{target}** {release_file.name}")
        scribe_texts.append(f"    SHA256: `{checksum}`")
        hash_info.append(f"{checksum} - {Path.resolve(release_file).name}")
scribe_texts.append("")
hash_info.append("")

with open(MD_DIR.joinpath("version.md"), "w") as mdfile:
    mdfile.write("\n".join(scribe_texts))

with open(RELEASES_DIR.joinpath("SHA256SUMS.txt"), "w") as sumsfile:
    sumsfile.write("\n".join(hash_info))
