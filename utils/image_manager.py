""" Module that makes actions to one or several images """
import os
import re
import numpy as np
from base64 import b64decode as decode
from PIL import Image


def has_text_an_image(text):
    regex_to_extract = r'data:image.+\"'

    return re.search(regex_to_extract, text)


def remove_image_tag_from_html(html):
    pattern = r'<img.+?>'
    html_without_image = re.sub(pattern, '', html)

    return html_without_image


def get_extension_from_data(data):
    headers = data.split(',')[0]

    if 'png' in headers:
        return 'png'
    elif 'jpg' in headers:
        return 'jpg'
    else:
        return 'jpeg'


def get_data_image(image_html, regex):
    """
    decode a html with image data
    and returns base64 data and extension
    """
    image_text = re.sub(regex, '', image_html).strip()
    image_without_headers = image_text.split(',')[1].strip()

    extension = get_extension_from_data(image_text)
    data = decode(image_without_headers)

    return data, extension


def write_image(dirname, basename, data):
    image_path = os.path.join(dirname, basename)
    with open(image_path, 'wb') as image:
        image.write(data)


def remove_image(filename):
    os.remove(filename)

    if os.path.exists(filename) is False:
        return True
    else:
        return False


def join_images(dirname, basename, images_list):
    """
    Take an array of images and
    join them horizontly, then save it
    """
    images = [Image.open(i) for i in images_list]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    images_data = np.vstack(list((np.asarray(i.resize((total_width, max_height))) for i in images)))
    images_combined = Image.fromarray(images_data)
    images_combined.save(os.path.join(dirname, basename))
