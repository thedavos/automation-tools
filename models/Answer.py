""" Answer Model """
from utils.text_manager import handle_text, sanitize_text
from utils.image_manager import has_text_an_image, get_data_image, write_image
from Config import Config


class AnswerModel(Config):
    ANSWER_TABLE_NAME = 'mdl_question_answers'

    def __init__(self, answers, name):
        super().__init__()
        self.answers = answers
        self.name = name

    def get_answer(self, number):
        """
        :param number: number of answer
        :return: answer text
        """
        number -= 1
        answer_html = self.answers[number][1]

        text = handle_text(answer_html)
        return sanitize_text(self.regex_to_sanitize_text, text)

    def get_answer_image(self, number):
        """
        :param number: number of answer
        :return: image name if exist
        """
        if number == 0:
            raise ValueError

        answer_html = self.answers[number - 1][1]
        image = has_text_an_image(answer_html)

        if image is not None:
            data, extension = get_data_image(image.group(), self.regex_to_replace)
            image_name = self.name + '-' + 'answer' + str(number) + '.' + extension
            write_image(self.OUTPUT_IMAGE_DIRNAME, image_name, data)
            return image_name
        else:
            return ''

    def get_correct_answer(self):
        """
        :return: index of correct answer
        """
        for index, answer in enumerate(self.answers, start=1):
            if 1.0000000 in answer:
                return index
