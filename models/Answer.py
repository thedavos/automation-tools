""" Answer Model """


class Answer:
    def __init__(self, fraction, answer, feedback):
        self.table_name = 'mdl_question_answers'
        self.fraction = fraction
        self.answer = answer
        self.feedback = feedback
