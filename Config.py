""" Configuration of project """
import os
from utils.os_manager import create_folder_if_not_exist


class Config:
    ROOT = os.getcwd()
    FU_FILES = os.path.join(ROOT, 'fu_files')
    CHAPTER_FILE = 'extraordinary_chapter_file.csv'
    OUTPUT_DIRNAME = '/home/davos/FractalUp/questions/'
    OUTPUT_IMAGE_DIRNAME = os.path.join(OUTPUT_DIRNAME, 'images/')
    OUTPUT_SQL_DIRNAME = os.path.join(OUTPUT_DIRNAME, 'sql/')
    YEAR = '2018'
    FU_QUESTION_TABLE_NAME = 'svn_classroom_questions'
    SQL_FILENAME = 'EXTRAORDINARIO-FALTANTES-{year}.sql'.format(year=YEAR)

    # regex patterns
    regex_to_extract = r'data:image.+\"'
    regex_to_replace = r'\"\W.*'
    regex_to_sanitize_text = r'(<!--.+?-->)'

    def __init__(self):
        create_folder_if_not_exist(self.OUTPUT_IMAGE_DIRNAME)
        create_folder_if_not_exist(self.OUTPUT_SQL_DIRNAME)
