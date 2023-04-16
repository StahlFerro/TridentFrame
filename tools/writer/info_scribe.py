import json
import platform
import hashlib
from pathlib import Path
from typing import List


SCRIBE_PATH = Path(__file__).resolve()
SCRIBE_DIR = Path(SCRIBE_PATH).parents[0]

MD_DIR = SCRIBE_DIR.joinpath("markdown")
PROJECT_DIR = SCRIBE_PATH.parents[2]
RELEASES_DIR = PROJECT_DIR.joinpath("release/tridentframe/")
PACKAGEJSON_FILE = PROJECT_DIR.joinpath("package.json")
ELECTRON_BUILDER_CONF_FILE = ""

package_json = {}
build_config = {}
targets: List[str] = []
scribe_texts = []
hash_info = []
os_name = ""
with open(PACKAGEJSON_FILE, "r") as jsonfile:
    package_json = json.load(jsonfile)
VERSION = package_json["version"]

os_name = platform.system()
if os_name == "Windows":
    ELECTRON_BUILDER_CONF_FILE = PROJECT_DIR.joinpath("shipping-configs/electron-builder-win.json")
    with open(ELECTRON_BUILDER_CONF_FILE, "r") as jsonfile:
        build_config = json.load(jsonfile)
    targets = build_config["win"]["target"]
    scribe_texts.append(f"- Windows 10+ (64bit)")
elif os_name == "Linux":
    ELECTRON_BUILDER_CONF_FILE = PROJECT_DIR.joinpath("shipping-configs/electron-builder-linux.json")
    with open(ELECTRON_BUILDER_CONF_FILE, "r") as jsonfile:
        build_config = json.load(jsonfile)
    targets = build_config["linux"]["target"]
    scribe_texts.append(f"- Linux")
release_files = [RELEASES_DIR.joinpath(diritem) for diritem in RELEASES_DIR.glob("*") if Path.is_file(diritem)]
for target in targets:
    release_file = next((r for r in release_files if target == r.suffix[1:] or target in r.name), None)
    sha512_hash = hashlib.sha512()
    hash_obj = ""
    if release_file:
        with open(release_file, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha512_hash.update(byte_block)
            hash_obj = sha512_hash
        checksum = hash_obj.hexdigest()
        scribe_texts.append(f"  - **{target}** {release_file.name}")
        scribe_texts.append(f"    SHA512: `{checksum}`")
        hash_info.append(f"{checksum} - {Path.resolve(release_file).name}")
scribe_texts.append("")
hash_info.append("")


MD_DIR.mkdir(parents=True, exist_ok=True)
MD_FILE = MD_DIR.joinpath("version.md")
MD_FILE.touch(exist_ok=True)

CHKSUM_FILE = RELEASES_DIR.joinpath("SHA512SUMS.txt")
CHKSUM_FILE.touch(exist_ok=True)


with open(MD_FILE, "w") as md_file:
    md_file.write("\n".join(scribe_texts))

with open(CHKSUM_FILE, "w") as chksums_file:
    chksums_file.write("\n".join(hash_info))
