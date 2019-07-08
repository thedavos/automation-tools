""" Module that makes actions to one or several images """
import os
import re
from base64 import b64decode as decode
from PIL import Image


def get_data_image(image_html, regex):
    """
    decode a html with image data
    and returns base64 data
    """
    image_text = re.sub(regex, '', image_html).strip()
    image_without_headers = image_text.split(',')[1].strip()
    data = decode(image_without_headers)

    return data


def write_image(dirname, basename, data):
    image_path = os.path.join(dirname, basename)
    with open(image_path, 'wb') as image:
        image.write(data)


def join_images(dirname, basename, *args):
    """
    Take an array of images and
    join them horizontly, then save it
    """
    images = map(Image.open, args)
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_image = Image.new('RGB', (total_width, max_height))

    x_offset = 0

    for image in images:
        new_image.paste(image, (x_offset, 0))
        x_offset += image.size[0]

    new_image.save(os.path.join(dirname, basename))
