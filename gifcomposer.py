import os

import click
from click import FileError
from PIL import Image
from colorama import init, deinit


@click.command()
@click.argument('dir_path', type=click.Path(exists=True))
@click.option('-f', '--fps', default=60)
@click.option('-o', '--output_name', help='Name of the split gif images')
@click.option('--transparent', is_flag=True, help='Use this for images with transparent background')
def gifcomposer(dir_path, fps, output_name, transparent):
    init()
    if not os.path.isdir(dir_path):
        raise FileError(dir_path, "Oi skrubman the path here seems to be a bloody file, should've been a directory")
    framesdir = os.path.abspath(dir_path)
    dirname = os.path.basename(framesdir)
    # print('argument', dir_path)
    # print('framesdir absolute', framesdir)
    # print('dirname', dirname)
    if os.getcwd() != framesdir:
        os.chdir(framesdir)

    click.secho(f"Directory: {framesdir}", fg="cyan")
    # print('now cd', os.getcwd())
    if not output_name:
        output_name = dirname

    frames = [f for f in os.listdir('.') if '.' in f and str.lower(f.split('.')[-1]) != 'gif']
    frames.sort()
    frames = [Image.open(f) for f in frames]

    if fps > 50:
        fps = 50  # GIFs are actually limited to 50fps max. RIP 60fps dreams

    click.secho(f"{len(frames)} frames @ {fps}fps", fg="cyan")
    duration = 1000 / fps

    disposal = 0
    if transparent:
        disposal = 2
    click.secho("Generating GIF...", fg="cyan")
    frames[0].save(f"{output_name}.gif",
                   save_all=True, append_images=frames[1:], duration=duration, loop=0, disposal=disposal)
    click.secho(f"Created GIF {output_name}.gif in the directory!!1", fg="cyan")


if __name__ == '__main__':
    gifcomposer()
