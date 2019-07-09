""" OS MODULE """
import os


def create_folder_if_not_exist(path):
    if os.path.exists(path) is False:
        os.makedirs(path)
