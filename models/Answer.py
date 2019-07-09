""" Answer Model """
from utils.text_manager import backslash_apostrophe_to_text
from utils.image_manager import remove_image_tag_from_html


class AnswerModel:
    TABLE_NAME = 'mdl_question_answers'

    def __init__(self, answers):
        self.answers = answers

    def get_answer(self, number):
        """
        :param number: number of answer
        :return : answer text
        """
        number -= 1
        answer_html = self.answers[number][1]
        return backslash_apostrophe_to_text(remove_image_tag_from_html(answer_html))

    def get_answer_image(self, number):
        """
        :param number: number of answer
        :return: image name if exist
        """
        number -= 1
        return self.answers[number][2]

    def get_correct_answer(self):
        """
        :return: index of correct answer
        """
        for index, answer in enumerate(self.answers, start=1):
            if 1.0000000 in answer:
                return index
