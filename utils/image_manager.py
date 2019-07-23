""" Module that makes actions to one or several images """
import os
import re
from base64 import b64decode as decode
from PIL import Image


def has_text_an_image(text):
    """
    :param text: String with base64 data
    :return: true if text has base64 data otherwise false
    """
    regex_to_extract = r'data:image.+\"'

    return re.search(regex_to_extract, text)


def remove_image_tag_from_html(html):
    """
    :param html: a html sentence with image tag inside
    :return: html sentence without image tag
    """
    pattern = r'<img.+?>'
    html_without_image = re.sub(pattern, '', html)

    return html_without_image


def get_extension_from_data(data):
    """
    given data as base64,
    returns extension from data headers
    """
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
    """ Create an image in a given pathname from a base64 data """
    image_path = os.path.join(dirname, basename)
    with open(image_path, 'wb') as image:
        image.write(data)


def join_images(dirname, basename, images_list):
    """
    Take an array of images and
    join them horizontly, then save it
    """
    images = [Image.open(i) for i in images_list]
    widths, heights = zip(*(i.size for i in images))
    images_length = len(images_list)

    max_width = max(widths)
    max_height = max(heights)

    result = Image.new("RGBA", (max_width, max_height))

    y = 0
    for index, path in enumerate(images_list):
        img = Image.open(path)
        total_height = max_height // images_length
        img.thumbnail((max_width, total_height), Image.ANTIALIAS)
        width, height = img.size

        offset_x = (max_width - width) // 2
        offset_y = (total_height - height) // 2

        result.paste(img, (offset_x, y, width + offset_x, y + height))
        y += (offset_y + height)

    result.save(os.path.join(dirname, basename))
