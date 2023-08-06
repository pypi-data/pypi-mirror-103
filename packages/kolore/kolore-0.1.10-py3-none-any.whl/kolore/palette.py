from zipfile import ZipFile
import os
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw
import tempfile


def create(width: int, height: int, path: str, output: str):
    colors = get_colors(path)
    save(width, height, colors, output)

def get_colors(path: str) -> [str]:
    with tempfile.TemporaryDirectory() as tmp_dir:
        with ZipFile(path, 'r') as zipObj:
            zipObj.extractall(tmp_dir)

            tree = ET.parse(f'{tmp_dir}/colorset.xml')
            root = tree.getroot()
            colors = []
            for child in root:
                rgb = child[0].attrib
                r = int(float(rgb['r']) * 255)
                g = int(float(rgb['g']) * 255)
                b = int(float(rgb['b']) * 255)
                colors.append(f'#{r:02x}{g:02x}{b:02x}')

    return colors

def save(width: int, height: int, colors: [str], output: str):
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    num_colors = len(colors)
    color_width = width / num_colors
    for i, color in enumerate(colors):
        draw.rectangle([(color_width * i, 0), (color_width * (i + 1), height)], fill=color)
    
    img.save(output)
