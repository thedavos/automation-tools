""" Question Model """
from db.connection import Database
from Config import Config
from utils.image_manager import get_data_image
import csv
import os
import re


class QuestionModel(Database):
    TABLE_NAME = 'mdl_question'
    CHAPTER_FILE = os.path.join(Config.FU_FILES, 'extraordinary_chapter_file.csv')
    CHAPTER_YEAR = '2017'

    def __init__(self, question_id, name, statement, feedback):
        super().__init__()
        self.id = question_id
        self.name = name
        self.statement = statement
        self.feedback = feedback

    @staticmethod
    def get_questions(query):
        db = Database()
        result = db.get_all_data(query)

        return result

    def get_answers(self, answer):
        """
        :param answer Answer
        """
        connection = self.get_connection()
        query = """
                SELECT
                    a.fraction,
                    a.answer,
                    a.feedback
                FROM {} AS q
                JOIN {} AS a
                ON q.id = a.question
                WHERE q.id={}
            """.format(self.TABLE_NAME, answer.table_name, self.id)

        result = self.get_all_data(connection, query)

        return result

    def get_files(self):
        connection = self.get_connection()

        query = """
                SELECT
                    f.filename,
                    f.filearea,
                    f.contenthash
                FROM {} AS q
                JOIN {} AS f
                ON q.id = f.itemid
                WHERE q.id={}
                AND f.filearea in (
                'generalfeedback',
                'answer',
                'answerfeedback',
                'questiontext'
                )
                AND f.filesize > 0
            """.format(self.TABLE_NAME, 'mdl_files', self.id)

        result = self.get_all_data(connection, query)

        return result

    def _extract_chapter_from_name(self):
        """ slice name of question to get a chapter """
        regex = r'(\w+-)'
        question_found = re.search(regex, self.name)

        chapter = question_found.group(0)[:-1]

        return chapter.upper()

    def get_chapter(self):
        """
        Looks and compare question_name
        with a given csv file and
        returns a chapter
        """
        chapter = self._extract_chapter_from_name()

        with open(self.CHAPTER_FILE) as file:
            rows = csv.reader(file, delimiter=',')
            for row in rows:
                if row[4] == chapter and self.CHAPTER_YEAR in row[2]:
                    print(int(row[1]))
                    return int(row[1])

    def get_statement(self):
        regex_to_replace = '\"\W.*'
        regex_to_extract = 'data:image.+\"'

        image = re.search(regex_to_extract, self.statement)
        if image is not None:
            matches = re.finditer(regex_to_extract, self.statement)
            for index, match in enumerate(matches, start=1):
                data = get_data_image(match.group(), regex_to_replace)
                return ''

    def question_to_dict(self):
        """ returns an ordered dict with question data """
        chapter_id = self.get_chapter()
        statement = self.get_statement()

        return {
            'business_id': 2,
            'chapter_id': chapter_id,
            'video_id': None,
            'statement': '',
            'statement_url': '',
            'alternative_1': '',
            'alternative_1_img': '',
            'alternative_2': '',
            'alternative_2_img': '',
            'alternative_3': '',
            'alternative_3_img': '',
            'alternative_4': '',
            'alternative_4_img': '',
            'alternative_5': '',
            'alternative_5_img': '',
            'answer': 0,
            'hint_1': '',
            'hint_1_image': '',
            'hint_2': '',
            'hint_2_image': '',
            'hint_3': '',
            'hint_3_image': '',
            'hint_4': '',
            'hint_4_image': '',
            'hint_5': '',
            'hint_5_image': '',
            'hint_6': '',
            'hint_6_image': '',
            'hint_7': '',
            'hint_7_image': '',
            'hint_8': '',
            'hint_8_image': '',
            'hint_9': '',
            'hint_9_image': '',
            'hint_10': '',
            'hint_10_image': ''
        }
