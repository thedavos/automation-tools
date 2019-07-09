""" Text Module: do actions to texts """


def backslash_apostrophe_to_letter(letter):
    if letter == "'":
        return '{apostrophe}{letter}'.format(apostrophe='\\', letter=letter)
    else:
        return letter


def backslash_apostrophe_to_text(text):
    text_without_apostrophe = [backslash_apostrophe_to_letter(letter) for letter in text]

    return "".join(text_without_apostrophe)
