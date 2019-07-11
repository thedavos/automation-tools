""" Question Model """
import csv
from db.connection import Database
from Config import Config
from utils.image_manager import *
from utils.text_manager import handle_text
from utils.os_manager import create_folder_if_not_exist
from models.Answer import AnswerModel


class QuestionModel(Database, AnswerModel):
    QUESTION_TABLE_NAME = 'mdl_question'
    CHAPTER_FILE = os.path.join(Config.FU_FILES, 'extraordinary_chapter_file.csv')
    CHAPTER_YEAR = Config.YEAR

    def __init__(self, question_id, name, statement, feedback):
        Database.__init__(self)
        self.id = question_id
        self.name = name
        self.statement = statement
        self.feedback = feedback
        self.feedback_image = has_text_an_image(self.feedback)
        AnswerModel.__init__(self, self.get_answers(), self.name)

    @staticmethod
    def get_questions(query):
        db = Database()
        result = db.get_all_data(query)

        return result

    def get_answers(self):
        query = """
                SELECT
                    a.fraction,
                    a.answer,
                    a.feedback
                FROM {} AS q
                JOIN {} AS a
                ON q.id = a.question
                WHERE q.id={}
            """.format(self.QUESTION_TABLE_NAME, AnswerModel.ANSWER_TABLE_NAME, self.id)

        result = self.get_all_data(query)

        return result

    def get_files(self):
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
            """.format(self.QUESTION_TABLE_NAME, 'mdl_files', self.id)

        result = self.get_all_data(query)

        return result

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
                    return int(row[1])

    def get_statement(self):
        return handle_text(self.statement)

    def get_statement_url(self):
        image = has_text_an_image(self.statement)

        create_folder_if_not_exist(self.OUTPUT_IMAGE_DIRNAME)
        create_folder_if_not_exist(self.OUTPUT_SQL_DIRNAME)

        images = []
        image_final_name = self.name + '-' + 'questiontext.png'

        if image is not None:
            matches = re.finditer(self.regex_to_extract, self.statement)
            for index, match in enumerate(matches, start=1):
                data, extension = get_data_image(match.group(), self.regex_to_replace)
                image_name = self.name + '-' + 'questiontext' + str(index) + '.' + extension
                write_image(self.OUTPUT_IMAGE_DIRNAME, image_name, data)

                images.append(os.path.join(self.OUTPUT_IMAGE_DIRNAME, image_name))

            if len(images) > 1:
                join_images(self.OUTPUT_IMAGE_DIRNAME, image_final_name, images)

                for filename in images:
                    remove_image(filename)

                return image_final_name

            else:
                return os.path.basename(images[0])
        else:
            return ''

    def get_hint_images(self, number):
        images = []

        if self.feedback_image is not None:
            matches = re.finditer(self.regex_to_extract, self.feedback)
            for index, match in enumerate(matches, start=1):
                data, extension = get_data_image(match.group(), self.regex_to_replace)
                image_name = self.name + '-' + 'generalfeedback' + str(index) + '.' + extension
                write_image(self.OUTPUT_IMAGE_DIRNAME, image_name, data)

                images.append(image_name)

            final_images = images + ([''] * (10 - len(images)))

            return final_images[number - 1]
        else:
            return ''

    def get_hint(self):
        return handle_text(self.feedback)

    def question_to_dict(self):
        """ returns an ordered dict with question data """
        chapter_id = self.get_chapter()
        statement = self.get_statement()
        statement_url = self.get_statement_url()

        return {
            'business_id': 2,
            'chapter_id': chapter_id,
            'video_id': None,
            'statement': statement,
            'statement_url': statement_url,
            'alternative_1': self.get_answer(1),
            'alternative_1_img': self.get_answer_image(1),
            'alternative_2': self.get_answer(2),
            'alternative_2_img': self.get_answer_image(2),
            'alternative_3': self.get_answer(3),
            'alternative_3_img': self.get_answer_image(3),
            'alternative_4': self.get_answer(4),
            'alternative_4_img': self.get_answer_image(4),
            'alternative_5': self.get_answer(5),
            'alternative_5_img': self.get_answer_image(5),
            'answer': self.get_correct_answer(),
            'hint_1': self.get_hint(),
            'hint_1_image': self.get_hint_images(1),
            'hint_2': '',
            'hint_2_image': self.get_hint_images(2),
            'hint_3': '',
            'hint_3_image': self.get_hint_images(3),
            'hint_4': '',
            'hint_4_image': self.get_hint_images(4),
            'hint_5': '',
            'hint_5_image': self.get_hint_images(5),
            'hint_6': '',
            'hint_6_image': self.get_hint_images(6),
            'hint_7': '',
            'hint_7_image': self.get_hint_images(7),
            'hint_8': '',
            'hint_8_image': self.get_hint_images(8),
            'hint_9': '',
            'hint_9_image': self.get_hint_images(9),
            'hint_10': '',
            'hint_10_image': self.get_hint_images(10)
        }

    def _extract_chapter_from_name(self):
        """ slice name of question to get a chapter """
        regex = r'(\w+-)'
        question_found = re.search(regex, self.name)

        chapter = question_found.group(0)[:-1]

        return chapter.upper()
