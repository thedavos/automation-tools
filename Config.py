""" Configuration of project """
import os


class Config:
    ROOT = os.getcwd()
    FU_FILES = os.path.join(ROOT, 'fu_files')
    OUTPUT_DIRNAME = '/home/davos/FractalUp/questions/'
    OUTPUT_IMAGE_DIRNAME = os.path.join(OUTPUT_DIRNAME, 'images/')
    OUTPUT_SQL_DIRNAME = os.path.join(OUTPUT_DIRNAME, 'sql/')
    YEAR = '2017'
    FU_QUESTION_TABLE_NAME = 'svn_classroom_questions'
    SQL_FILENAME = 'EXTRAORDINARIO-FALTANTES-{year}.sql'.format(year=YEAR)
    regex_to_extract = r'data:image.+\"'
    regex_to_replace = r'\"\W.*'
