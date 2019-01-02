import os
from random import choices
import string

import click
from colorama import init, deinit


img_exts = ['png', 'jpg', 'jpeg', 'gif', 'bmp']


@click.command()
@click.option('-n', '--name', help='Custom filename')
@click.option('-d', '--directory', help='Target a specific directory of images')
def renamer(name, directory):
    init()
    if directory:
        os.chdir(directory)
    images = [(f, str.lower(f.split('.')[-1])) for f in os.listdir('.')
              if not os.path.isdir(f) and '.' in f and str.lower(f.split('.')[-1]) in img_exts]
    if not name:
        name = ''.join(choices(string.ascii_letters, k=10))
    pad_count = max(len(str(len(images))), 3)
    click.secho(f"Renaming {len(images)} images...", fg='blue')
    for index, (img, ext) in enumerate(images):
        new_name = f"{name}_{str.zfill(str(index), pad_count)}.{ext}"
        os.rename(img, new_name)
        click.secho(f"{index + 1}. {img} -> {new_name}", fg='cyan')
    click.secho(f"Done!!1", fg='blue')
    deinit()


if __name__ == '__main__':
    renamer()
