import click
import kolore.palette as palette


@click.command()
@click.argument('filename')
@click.option('--output', help='path of the generated file', default='./palette.png')
@click.option('--from', 'from_', help='format of the input file', hidden=True)
@click.option('--to', help='format of output file', hidden=True)
@click.option('--width', default=400, type=int, help="image width size in pixels")
@click.option('--height', default=200, type=int, help="image height size in pixels")
def parse(filename: str, output: str, from_: str, to: str, width: int, height: int):
    palette.create(width, height, filename, output)
