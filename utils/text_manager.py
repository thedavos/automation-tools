""" Text Module: do actions to texts """
import re
from utils.image_manager import remove_image_tag_from_html


def sanitize_text(regex, text):
    sanitized_text = re.sub(regex, '', text)
    return remove_duplicate_whitespaces(sanitized_text)


def backslash_apostrophe_to_letter(letter):
    if letter == "'":
        return '{apostrophe}{letter}'.format(apostrophe='\\', letter=letter)
    else:
        return letter


def backslash_apostrophe_to_text(text):
    text_without_apostrophe = [backslash_apostrophe_to_letter(letter) for letter in text]

    return "".join(text_without_apostrophe)


def remove_linebreaks_from_text(text):
    text_list = text.split('\n')
    return ''.join(text_list)


def remove_duplicate_whitespaces(text):
    text_without_duplicate_whitespaces = ' '.join(text.split())
    return text_without_duplicate_whitespaces


def handle_text(text):
    html = remove_image_tag_from_html(text)

    html_with_apostrophe_backslashed = backslash_apostrophe_to_text(html)
    text_without_linebreaks = remove_linebreaks_from_text(html_with_apostrophe_backslashed)
    text_without_duplicate_whitespaces = remove_duplicate_whitespaces(text_without_linebreaks)
    return text_without_duplicate_whitespaces.strip()
