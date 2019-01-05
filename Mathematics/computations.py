
from word2number import w2n


operators = ['plus', 'minus', 'over', 'divide', 'times']
operators_dict = {'plus': '+', 'minus': '-', 'times': '*', 'multiply': '*', 'over': '/', 'divide': '/'}


with open('/Users/setor/PycharmProjects/HomebotRemote/AssistingFiles/math_keywords') as f:
    content = f.readlines()
keep_words = [x.strip() for x in content]  # remove \n

with open('/Users/setor/PycharmProjects/HomebotRemote/AssistingFiles/number_words') as f:
    content = f.readlines()
math_words = [x.strip() for x in content]  # remove \n


def extract_operator(words: list):
    for operator in operators:
        if operator in words:
            return operators_dict.get(operator)


def extract_numbers(words: str):
    counter = []
    words = words.split()
    for word in words:
        if word in math_words:
            previous_word = counter[-1]
            counter.append(previous_word+1)
            counter[-2] = 0
        else:
            counter.append(0)

    # summed all number words the two longest are picked
    # la_size is the cum sum of consecutive number words
    print(counter)
    largest1_size = sorted(counter)[-1]
    largest2_size = sorted(counter)[-2]

    # finds the index of the longest consecutive values
    # the last word is the one with the largest size

    # returns all indices for the number
    indices = [i for i, x in enumerate(counter) if x == largest1_size]
    if len(indices) >= 2:
        largest1_pos = indices[-2]
        largest2_pos = indices[-1]
    elif len(indices) < 2:
        indices = sorted(indices + ([i for i, x in enumerate(counter) if x == largest2_size]))
        largest1_pos = indices[0]
        largest2_pos = indices[-1]

    # extract the text of the the two largest number strings
    largest1_txt = words[(largest1_pos - largest1_size+1):(largest1_pos+1)]
    largest2_txt = words[(largest2_pos - largest2_size+1):(largest2_pos+1)]

    # if largest1_pos < largest2_pos:
    #     number1 = w2n.word_to_num(' '.join(largest1_txt))
    #     number2 = w2n.word_to_num(' '.join(largest2_txt))
    #
    # elif largest1_pos > largest2_pos:
    #     number1 = w2n.word_to_num(' '.join(largest2_txt))
    #     number2 = w2n.word_to_num(' '.join(largest1_txt))

    number1 = w2n.word_to_num(' '.join(largest1_txt))
    number2 = w2n.word_to_num(' '.join(largest2_txt))

    # opti: if two second largest take the first
    # opti: correct length of number words for weak words e.g. million, point, etc...

    return number1, number2


def calculate(words):
    operator = extract_operator(words=words)
    num_1, num_2 = extract_numbers(words=words)
    equation = (str(num_1) + ' ' + str(operator) + ' ' + str(num_2))
    print(equation)

    result = round(eval(equation), 3)
    return result


if __name__ == '__main__':
    ergebnis = calculate('This is a four million five thousand dollar deal and i want to '
                         'divide six point three by five point six')
