
from word2number import w2n


class Computation:

    def __init__(self):
        with open('/home/pi/HomeBotRemote/AssistingFiles/math_keywords') as f:
            content = f.readlines()
        self.keep_words = [x.strip() for x in content]  # remove \n

        with open('/home/pi/HomeBotRemote/AssistingFiles/number_words') as f:
            content = f.readlines()
        self.math_words = [x.strip() for x in content]  # remove \n

        self.operators_dict = {'plus': '+', 'minus': '-', 'times': '*', 'over': '/', 'divided': '/', 'divide': '/',
                               'sum': '+'}

        self.operators = list(self.operators_dict.keys())

        # check whether the current word string is still full featured
        # if one check fails e.g. no operator found or any other errors the sentence is not valid
        # hence the state will change to 0
        self.valid = 1

    def extract_operator(self, words):
        found_operators = []
        for operator in self.operators:
            if operator in words:
                found_operators.append(operator)
        if len(found_operators) > 0:
            operator = found_operators[-1]
            return self.operators_dict.get(operator)
        elif len(found_operators) == 0:
            return None

    def extract_numbers(self, words):
        counter = [0]
        words = words.split()
        for word in words:
            if word in self.math_words:
                previous_word = counter[-1]
                counter.append(previous_word + 1)
                counter[-2] = 0
            else:
                counter.append(0)

        del counter[0]

        # summed all number words the two longest are picked
        # largest_size is the cumulative sum of consecutive number words
        largest1_size = sorted(counter)[-1]
        largest2_size = sorted(counter)[-2]

        if largest2_size < 1:
            self.valid = 0
            return None, None
        # finds the index of the longest consecutive values
        # the last word is the one with the largest size

        # returns all indices for the number
        indices = [i for i, x in enumerate(counter) if x == largest1_size]
        if len(indices) >= 2:
            largest1_pos = indices[-2]
            largest2_pos = indices[-1]
        else:
            indices = sorted(indices + ([i for i, x in enumerate(counter) if x == largest2_size]))
            largest1_pos = indices[0]
            largest2_pos = indices[-1]

        # extract the text of the the two largest number strings
        largest1_txt = words[(largest1_pos - largest1_size + 1):(largest1_pos + 1)]
        largest2_txt = words[(largest2_pos - largest2_size + 1):(largest2_pos + 1)]

        number1 = w2n.word_to_num(' '.join(largest1_txt))
        number2 = w2n.word_to_num(' '.join(largest2_txt))

        # opti:
        #  if two second largest take the last in the text
        # opti:
        #  correct length of number words for weak words e.g. million, point, etc...

        return number1, number2

    def calculate(self, words):
        words = str(words)
        if len(words.split()) < 3:
            return 'Incomplete sentence \n' \
                   'At least three words needed: 2 numbers and an operator'
        operator = self.extract_operator(words=words)
        if operator is None:
            return 'No operator was found.'

        num_1, num_2 = self.extract_numbers(words=words)

        if num_1 is None or num_2 is None:
            return 'Not enough numbers in the sentence'

        equation = (str(num_1) + ' ' + str(operator) + ' ' + str(num_2))
        print('equation:', equation)

        result = round(eval(equation), 3)
        return result


if __name__ == '__main__':
    Nums = Computation()
    res1 = Nums.calculate('thirteen times fourteen point six')
    print(res1)
