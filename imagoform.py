import os
import string
from random import choices

import click
from click import FileError
from PIL import Image
from colorama import init, deinit


@click.group()
def cli():
    pass


img_exts = ['png', 'jpg', 'jpeg', 'gif', 'bmp']


@cli.command()
@click.option('-n', '--name', help='Custom filename')
@click.argument('directory',  type=click.Path(exists=True))
def renamer(name, directory):
    init()
    if not os.path.isfile(directory):
        raise FileError(directory, "Oi skrubman the path here seems to be a bloody file, should've been a directory")
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


@cli.command('split')
@click.argument('file_path', type=click.Path(exists=True))
@click.option('-o', '--output_name', help='Name of the split gif images')
def gifsplitter(file_path, output_name):
    init()
    if not os.path.isfile(file_path):
        raise FileError(file_path, "Oi skrubman the path here seems to be a bloody directory, should've been a file")
    file = os.path.basename(file_path)
    abspath = os.path.abspath(file_path)
    workdir = os.path.dirname(abspath)
    if os.getcwd() != workdir:
        os.chdir(workdir)

    # Custom output dirname and frame names if specified on the cli
    if not output_name:
        output_name = '_'.join(file.split('.')[:-1])
        if not output_name:
            raise FileError(file, "Can't find the bloody file mate. Maybe forgot to include dem extension?")

    # Directory handling
    dirname = output_name
    # Create directory to contain all the frames if does not exist
    if not os.path.exists(dirname):
        os.mkdir(dirname)
        click.secho(f"Creating directory {dirname}...", fg='cyan')
    else:
        click.secho(f"Directory {dirname} already exists, replacing the PNGs inside it...", fg='cyan')

    # Image processing
    try:
        gif: Image = Image.open(file)
    except Exception:
        raise FileError(file, "M8 I don't even think this file is even an image file in the first place")

    if gif.format != 'GIF' or not gif.is_animated:
        raise FileError(file, "Sorry m9, the image you specified is not a valid animated GIF")

    click.secho(f"{file} ({gif.n_frames} frames). Splitting...", fg='cyan')
    pad_count = max(len(str(gif.n_frames)), 3)
    frame_nums = list(range(0, gif.n_frames))

    with click.progressbar(frame_nums, empty_char=" ", fill_char="█", show_percent=True, show_pos=True) as frames:
        for f in frames:
            gif.seek(f)
            gif.save(os.path.join(dirname, f"{output_name}_{str.zfill(str(f), pad_count)}.png"), 'PNG')

    click.secho(f"Done!!1", fg='cyan')
    deinit()


@cli.command('compose')
@click.argument('dir_path', type=click.Path(exists=True))
@click.option('-f', '--fps', default=60)
@click.option('-o', '--output_name', help='Name of the split gif images')
@click.option('--transparent', is_flag=True, help='Use this for images with transparent background')
@click.option('--reverse', is_flag=True, help='Reverse the frames')
def gifcomposer(dir_path, fps, output_name, transparent, reverse):
    init()
    if not os.path.isdir(dir_path):
        raise FileError(dir_path, "Oi skrubman the path here seems to be a bloody file, should've been a directory")
    framesdir = os.path.abspath(dir_path)
    outdir = os.path.dirname(framesdir)
    basename = os.path.basename(framesdir)
    # print('argument', dir_path)
    # print('framesdir absolute', framesdir)
    # print('framesdir dirname', outdir)
    # print('basename', basename)
    if os.getcwd() != framesdir:
        os.chdir(framesdir)

    click.secho(f"Directory: {framesdir}", fg="cyan")
    # print('now cd', os.getcwd())
    if not output_name:
        output_name = basename
    output_name = f"{outdir}/{output_name}"

    frames = [Image.open(f) for f in os.listdir('.') if '.' in f and str.lower(f.split('.')[-1]) != 'gif']
    frames.sort(key=lambda i: i.filename, reverse=reverse)

    if fps > 50:
        fps = 50  # GIFs are actually limited to 50fps max. RIP 60fps dreams
    elif fps < 1:
        fps = 1  #

    click.secho(f"{len(frames)} frames @ {fps}fps", fg="cyan")
    duration = 1000 / fps

    disposal = 0
    if transparent:
        disposal = 2
    click.secho("Generating GIF...", fg="cyan")
    frames[0].save(f"{output_name}.gif",
                   save_all=True, append_images=frames[1:], duration=duration, loop=0, disposal=disposal)
    click.secho(f"Created GIF {output_name}.gif", fg="cyan")
    deinit()


if __name__ == '__main__':
    cli()
