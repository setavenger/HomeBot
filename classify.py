
# This file uses the text input to find the nature of the command e.g. math question or a remind me note etc.


class Classifier:

    def __init__(self):
        with open('/home/pi/HomeBotRemote/AssistingFiles/math_keywords') as f:
            content = f.readlines()
        self.keep_words = [x.strip() for x in content]  # remove \n

        with open('/home/pi/HomeBotRemote/AssistingFiles/number_words') as f:
            content = f.readlines()
        self.number_words = [x.strip() for x in content]  # remove \n

        self.operators_dict = {'plus': '+', 'minus': '-', 'times': '*', 'over': '/', 'divided': '/', 'divide': '/',
                               'sum': '+'}
        self.operators = list(self.operators_dict.keys())

        self.math_key_identifiers = self.operators + ['calculate']
        self.remind_me_key_identifiers = ['remind me', 'remind', 'remember']

        self.math_weight = 0
        self.remind_me_weight = 0

        self.math_keys = 0
        self.remind_me_keys = 0

    def reset(self):
        self.math_weight = 0
        self.remind_me_weight = 0

        self.math_keys = 0
        self.remind_me_keys = 0

    def find_keys(self, words):
        words = str(words).split()
        for word in words:
            if word in self.math_key_identifiers:
                self.math_keys += 1
            elif word in self.remind_me_key_identifiers:
                self.remind_me_keys += 1

    def choice_easy(self, words):
        self.find_keys(words=words)
        if self.math_keys < 1 and self.remind_me_keys > 0:
            return 'remind me'
        elif self.math_keys > 0 and self.remind_me_keys < 1:
            return 'mathematics'
        elif self.math_keys == 0 and self.remind_me_keys == 1:
            return None
        self.reset()

    # opti
    #  function below not needed yet
    #   if there are more functions and more keys needed conditional weighting makes sense
    #   at the moment and easy prioritising will be sufficient

    # def math_component(self, words):
    #
    #     # weights can be adjusted and more conditions implemented
    #     words = str(words).split()
    #     for word in words:
    #         if word in self.operators:
    #             self.math_weight += 50
    #
    #         # if there is no other remind me key the
    #         elif word in self.number_words and not self.remind_me_keys:
    #             self.math_weight += 15
