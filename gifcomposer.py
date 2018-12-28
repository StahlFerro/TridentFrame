import os

import click
from click import FileError
from PIL import Image
import moviepy.editor as mpe


@click.command()
@click.argument('dir_path', type=click.Path(exists=True))
@click.option('-f', '--fps', default=60)
@click.option('-o', '--output_name', help='Name of the split gif images')
def gifcomposer(dir_path, fps, output_name):
    if not os.path.isdir(dir_path):
        raise FileError(dir_path, "Oi skrubman the path here seems to be a bloody file, should've been a directory")
    dirname = os.path.dirname(dir_path)
    framesdir = os.path.abspath(dir_path)
    if os.getcwd() != framesdir:
        os.chdir(framesdir)

    click.secho(f"Directory: {dirname}", fg="cyan")

    if not output_name:
        output_name = dirname

    frames = os.listdir('.')
    frames.sort()
    click.secho(f"Frame count: {len(frames)}", fg="cyan")
    click.secho(f"FPS: {fps}", fg="cyan")
    clip = mpe.ImageSequenceClip(frames, fps=fps)
    clip.write_gif(f"{output_name}.gif", fps=fps)


if __name__ == '__main__':
    gifcomposer()
