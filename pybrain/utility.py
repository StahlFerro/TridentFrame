import os
import shutil
import time

from .config import gifsicle_exec, ABS_CACHE_PATH, CreationCriteria, SplitCriteria
from .create_ops import create_aimg
from .split_ops import split_aimg


def _purge_cache():
    for stuff in os.listdir(ABS_CACHE_PATH):
        stuff_path = os.path.join(ABS_CACHE_PATH, stuff)
        try:
            if os.path.isfile(stuff_path):
                os.unlink(stuff_path)
            elif os.path.isdir(stuff_path):
                shutil.rmtree(stuff_path)
        except Exception as e:
            print("e")


def _mk_temp_dir(prefix_name: str = ''):
    dirname = time.strftime("%Y%m%d_%H%M%S")
    if prefix_name:
        dirname = f"{prefix_name}_{dirname}"
    temp_dir = os.path.join(ABS_CACHE_PATH, dirname)
    os.mkdir(temp_dir)
    return temp_dir


def _reduce_color(gif_path, color: int = 256) -> str:
    print("Performing color reduction...")
    executable = gifsicle_exec()
    args = [executable, f"--colors={color}", gif_path]


def _delete_temp_images():
    # raise Exception(os.getcwd())
    temp_dir = os.path.abspath('temp')
    # raise Exception(os.getcwd(), temp_dir)
    # raise Exception(image_name, path)
    # os.remove(path)
    temp_aimgs = [os.path.join(temp_dir, i) for i in os.listdir(temp_dir)]
    for ta in temp_aimgs:
        os.remove(ta)
    return True


def gs_build():
    gifsicle_exec = os.path.abspath("./bin/gifsicle-1.92-win64/gifsicle.exe")
    orig_path = os.path.abspath('./test/orig2/')
    images = [os.path.abspath(os.path.join(orig_path, f)) for f in os.listdir(orig_path)]
    out_dir = os.path.abspath('./test/')
    criteria = CreationCriteria(fps=50, extension='gif', transparent=True, reverse=False)
    create_aimg(images, out_dir, "sicle_test", criteria)
    

def gs_split(gif_path: str, out_dir: str):
    criteria = SplitCriteria(pad_count=3, is_duration_sensitive=False)
    # pprint(criteria.__dict__)
    split_aimg(gif_path, out_dir, criteria)


if __name__ == "__main__":
    gs_build()