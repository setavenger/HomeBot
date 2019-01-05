
#
# example program for kaldi live nnet3 chain online decoding
#
# configured for embedded systems (e.g. an rpi3) with models
# installed in /opt/kaldi/model/
#

import sys

import traceback
import logging
import datetime

from time import time
from nltools import misc
from nltools.pulserecorder import PulseRecorder
from nltools.vad import VAD, BUFFER_DURATION
from nltools.asr import ASR, ASR_ENGINE_NNET3
from optparse import OptionParser

from word2number import w2n


sys.path.append('/home/pi/HomeBot/')

PROC_TITLE = 'kaldi_live_demo'

DEFAULT_VOLUME = 150
DEFAULT_AGGRESSIVENESS = 2

# DEFAULT_MODEL_DIR                = '/opt/kaldi/model/kaldi-generic-de-tdnn_250'
DEFAULT_MODEL_DIR = '/opt/kaldi/model/kaldi-generic-en-tdnn_250'
DEFAULT_ACOUSTIC_SCALE = 1.0
DEFAULT_BEAM = 7.0
DEFAULT_FRAME_SUBSAMPLING_FACTOR = 3

STREAM_ID = 'mic'

#
# init
#

misc.init_app(PROC_TITLE)

print("Kaldi live demo V0.2")

#
# cmdline, logging
#

parser = OptionParser("usage: %prog [options]")

parser.add_option("-a", "--aggressiveness", dest="aggressiveness", type="int", default=DEFAULT_AGGRESSIVENESS,
                   help="VAD aggressiveness, default: %d" % DEFAULT_AGGRESSIVENESS)

parser.add_option("-m", "--model-dir", dest="model_dir", type="string", default=DEFAULT_MODEL_DIR,
                   help="kaldi model directory, default: %s" % DEFAULT_MODEL_DIR)

parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                   help="verbose output")

parser.add_option("-s", "--source", dest="source", type="string", default=None,
                   help="pulseaudio source, default: auto-detect mic")

parser.add_option("-V", "--volume", dest="volume", type="int", default=DEFAULT_VOLUME,
                   help="broker port, default: %d" % DEFAULT_VOLUME)

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

source = options.source
volume = options.volume
aggressiveness = options.aggressiveness
model_dir = options.model_dir

#
# pulseaudio recorder
#

rec = PulseRecorder(source_name=source, volume=volume)

#
# VAD
#

vad = VAD(aggressiveness=aggressiveness)

#
# ASR
#

print("Loading model from %s ..." % model_dir)

asr = ASR(engine=ASR_ENGINE_NNET3, model_dir=model_dir,
          kaldi_beam=DEFAULT_BEAM, kaldi_acoustic_scale=DEFAULT_ACOUSTIC_SCALE,
          kaldi_frame_subsampling_factor=DEFAULT_FRAME_SUBSAMPLING_FACTOR)


operators = ['plus', 'minus', 'over', 'divide', 'times']
operators_dict = {'plus': '+', 'minus': '-', 'times': '*', 'multiply': '*', 'over': '/', 'divide': '/'}


with open('/home/pi/HomeBot/AssistingFiles/math_keywords') as f:
    content = f.readlines()
keep_words = [x.strip() for x in content]  # remove \n

with open('/home/pi/HomeBot/AssistingFiles/number_words') as f:
    content = f.readlines()
math_words = [x.strip() for x in content]  # remove \n


def extract_operator(words):
    for operator in operators:
        if operator in words:
            return operators_dict.get(operator)


def extract_numbers(words):
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

    largest1_txt = ' '.join(largest1_txt)
    largest2_txt = ' '.join(largest2_txt)

    print(largest1_txt, largest2_txt)

    number1 = w2n.word_to_num(largest1_txt)
    number2 = w2n.word_to_num(largest2_txt)

    # opti: if two second largest take the first
    # opti: correct length of number words for weak words e.g. million, point, etc...

    return number1, number2


def extract_number(words):
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
    words = str(words)
    operator = extract_operator(words=words)
    num_1, num_2 = extract_number(words=words)
    equation = (str(num_1) + ' ' + str(operator) + ' ' + str(num_2))
    print(equation)

    result = round(eval(equation), 3)
    return result


def findmathkeywords(words):
    words = str(words).split()
    intensity = []
    operatorss = []
    for word in words:
        if word in math_words:
            intensity.append(1)
        if word in operators:
            operatorss.append(1)
        else:
            intensity.append(0)
    print(sum(intensity))
    print(intensity)
    if sum(operatorss) > 0:

        if sum(intensity) > 1:
            return True
        else:
            return False
    else:
        return False
#
# main
#


rec.start_recording()

print("Please speak.")

while True:

    samples = rec.get_samples()

    audio, finalize = vad.process_audio(samples)

    if not audio:
        continue

    logging.debug('decoding audio len=%d finalize=%s audio=%s' % (len(audio), repr(finalize), audio[0].__class__))

    user_utt, confidence = asr.decode(audio, finalize, stream_id=STREAM_ID)

#    print("\r%s                     " % user_utt)

    if finalize:
        print("\r%s                     " % user_utt)
        if findmathkeywords(user_utt):
            print(calculate(user_utt))
        if 'stop listening' in user_utt:
            break
