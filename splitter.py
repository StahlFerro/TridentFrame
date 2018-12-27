import os

import click
from click import FileError
from PIL import Image


@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('-o', '--output_name', help='Name of the split gif images')
def splitter(file_path, output_name):
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
        click.secho(f"Directory {dirname} already exists, replacing the gifs inside it...", fg='cyan')

    # Image processing
    try:
        gif: Image = Image.open(file)
    except Exception:
        raise FileError(file, "M8 I don't even think this file is even an image file in the first place")

    if gif.format != 'GIF' or not gif.is_animated:
        raise FileError(file, "Sorry m9, the image you specified is not a valid animated GIF")

    click.secho(f"Obtained GIF: {file}. Frame count: {gif.n_frames}. Splitting...", fg='cyan')
    pad_count = max(len(str(gif.n_frames)), 3)
    for fcount in range(0, gif.n_frames):
        gif.seek(fcount)
        gif.save(os.path.join(dirname, f"{output_name}_{str.zfill(str(fcount), pad_count)}.png"), 'PNG')
    click.secho(f"Done!!1", fg='cyan')


if __name__ == '__main__':
    splitter()
