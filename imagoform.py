import os
import string
from random import choices

import click
from click import FileError
from PIL import Image
from apng import APNG
from colorama import init, deinit


@click.group()
def cli():
    pass


img_exts = ['png', 'jpg', 'jpeg', 'gif', 'bmp']
static_img_exts = ['png', 'jpg']
animated_img_exts = ['gif', 'png']


@cli.command('rename')
@click.option('-n', '--name', help='Custom filename')
@click.argument('directory',  type=click.Path(exists=True))
def rename(name, directory):
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
@click.option('-v', '--verbose', is_flag=True, help='Outputs more detailed information')
def split(file_path, output_name, verbose):
    init()
    if not os.path.isfile(file_path):
        raise FileError(file_path, "Oi skrubman the path here seems to be a bloody directory, should've been a file")
    file = str(os.path.basename(file_path))
    abspath = os.path.abspath(file_path)
    workpath = os.path.dirname(abspath)
    if verbose:
        click.secho(f"dir_path: {file_path}\nabspath: {abspath}\nworkpath: {workpath}\nfile: {file}",
                    fg='bright_cyan')
    if os.getcwd() != workpath:
        os.chdir(workpath)

    # Custom output dirname and frame names if specified on the cli
    if '.' not in file:
        raise click.ClickException('Where the fuk is the extension mate?!')

    if not output_name:
        output_name = '_'.join(file.split('.')[:-1])

    ext = str.lower(file.split('.')[-1])
    if ext not in animated_img_exts:
        raise click.ClickException('Only supported extensions are gif and apng. Sry lad')

    # Output directory handling
    dirname = output_name
    # Create directory to contain all the frames if does not exist
    if not os.path.exists(dirname):
        os.mkdir(dirname)
        click.secho(f"Creating directory {dirname}...", fg='cyan')
    else:
        click.secho(f"Directory {dirname} already exists, replacing the PNGs inside it...", fg='cyan')

    # Image processing
    if ext == 'gif':
        try:
            gif: Image = Image.open(file)
        except Exception:
            raise FileError(file, "M8 I don't even think this file is even an image file in the first place")

        if gif.format != 'GIF' or not gif.is_animated:
            raise FileError(file, "Sorry m9, the image you specified is not a valid animated GIF")

        click.secho(f"{file} ({gif.n_frames} frames). Splitting GIF...", fg='cyan')
        pad_count = max(len(str(gif.n_frames)), 3)
        frame_nums = list(range(0, gif.n_frames))

        with click.progressbar(frame_nums, empty_char=" ", fill_char="█", show_percent=True, show_pos=True) as frames:
            for f in frames:
                gif.seek(f)
                gif.save(os.path.join(dirname, f"{output_name}_{str.zfill(str(f), pad_count)}.png"), 'PNG')

    elif ext == 'png':
        img: APNG = APNG.open(file)
        iframes = img.frames
        pad_count = max(len(str(len(iframes))), 3)
        click.secho(f"{file} ({len(iframes)} frames). Splitting APNG...", fg='cyan')
        # print('frames', [(png, control.__dict__) for (png, control) in img.frames][0])
        with click.progressbar(iframes, empty_char=" ", fill_char="█", show_percent=True, show_pos=True) as frames:
            for i, (png, control) in enumerate(frames):
                png.save(os.path.join(dirname, f"{output_name}_{str.zfill(str(i), pad_count)}.png"))

    click.secho(f"Done!!1", fg='cyan')
    deinit()


@cli.command('compose')
@click.argument('dir_path', type=click.Path(exists=True))
@click.option('-x', '--extension', type=click.Choice(['gif', 'apng']), default='gif',
              help='Output format extension (gif or apng). Defaults to gif')
@click.option('-f', '--fps', type=click.IntRange(1, 50), default=50, help='Frame rate of the output (1 to 50)')
@click.option('-o', '--output_name', help='Name of the resulting animated image')
@click.option('-t', '--transparent', is_flag=True, help='Use this for images with transparent background')
@click.option('-r', '--reverse', is_flag=True, help='Reverse the frames')
@click.option('-v', '--verbose', is_flag=True, help='Outputs more detailed information')
def compose(dir_path, extension, fps, output_name, transparent, reverse, verbose):
    init()
    if not os.path.isdir(dir_path):
        raise FileError(dir_path, "Oi skrubman the path here seems to be a bloody file, should've been a directory")
    framesdir = str(os.path.basename(dir_path))
    abspath = os.path.abspath(dir_path)
    workpath = os.path.dirname(abspath)
    if verbose:
        click.secho(f"dir_path: {dir_path}\nabspath: {abspath}\nworkpath: {workpath}\nframesdir: {framesdir}",
                    fg='bright_cyan')
    # print('argument', dir_path)
    # print('framesdir absolute', framesdir)
    # print('framesdir dirname', outdir)
    # print('basename', basename)
    if os.getcwd() != abspath:
        os.chdir(abspath)

    # If no name supplied, default name will be the framesdir folder name. Output will be in the same parent directory
    # as the framesdir
    if not output_name:
        output_name = framesdir
    output_name = os.path.join(workpath, output_name)

    imgs = [f for f in os.listdir('.') if '.' in f and str.lower(f.split('.')[-1]) in img_exts]
    # First check to make sure every file name have extensions
    # if not all('.' in i for i in imgs):
    #     raise click.ClickException('Not all the file names have extensions')

    # Second checks to make sure extensions are PNG and JPG, and are all uniform
    # extensions = [str.lower(i.split('.')[-1]) for i in imgs]
    # if any(x not in static_img_exts for x in extensions):
    #     raise click.ClickException('Only accepted extensions are PNG and JPG')
    # if len(set(extensions)) > 1:
    #     raise click.ClickException('Images contain inconsistent file extensions')

    duration = round(1000 / fps)
    click.secho(f"{len(imgs)} frames @ {fps}fps", fg="cyan")

    if extension == 'gif':
        frames = [Image.open(i) for i in imgs]
        frames.sort(key=lambda i: i.filename, reverse=reverse)

        disposal = 0
        if transparent:
            disposal = 2
        click.secho("Generating GIF...", fg="cyan")
        frames[0].save(f"{output_name}.gif",
                       save_all=True, append_images=frames[1:], duration=duration, loop=0, disposal=disposal)
        click.secho(f"Created GIF {output_name}.gif", fg="cyan")

    elif extension == 'apng':
        click.secho("Generating APNG...", fg="cyan")
        click.secho(f"Created APNG {output_name}.png", fg="cyan")
        APNG.from_files(imgs, delay=duration).save(f"{output_name}.png")

    deinit()


if __name__ == '__main__':
    cli()
