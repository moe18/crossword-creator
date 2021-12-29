
import pandas as pd
import numpy as np


from util import read_puz_format, np_to_puz, create_puz_puzzle
# from word_list_theme import get_theme_words
from src.crossword_gen.blank_cross_gen import xword_matrix_gen


def get_h_word_length(puzzle, v, h):
    """
    find the length of a word, by seeing how many ones are in front,
    and in back

    :param horizontal_pos:
    :param vertical_pos:
    :return: horizontal word length
    """
    word_length = 0

    for i in range(5):
        if puzzle[v][h + i] != '0':
            word_length += 1
        else:
            break

    for i in range(5):
        if puzzle[v][h - i] != '0':
            word_length += 1
        else:
            break

    return word_length - 1


def get_v_word_length(puzzle, v, h):
    """
    find the length of a word, by seeing how many ones are in front,
    and in back

    :param horizontal_pos:
    :param vertical_pos:
    :return: horizontal word length
    """
    word_length = 0

    for i in range(17):
        if puzzle[v + i][h] != '0':
            word_length += 1
        else:
            break

    for i in range(17):
        if puzzle[v - i][h] != '0':
            word_length += 1
        else:
            break

    return word_length - 1


def get_h_frag(puzzle, v, h, h_word_len):
    word = []
    for i in range(h_word_len):
        if puzzle[v][h - i] == '0':
            break
        else:
            word.append(puzzle[v][h - i])

    word_frag = ''

    for m in word:
        if m != '0' and m != '1':
            word_frag += m
    h_word_frag = word_frag[::-1]
    return h_word_frag


def get_v_frag(puzzle, v, h, v_word_len):
    word = []
    for i in range(v_word_len):
        if puzzle[v - i][h] == '0':
            break
        else:
            word.append(puzzle[v - i][h])
    word_frag = ''
    for m in word:
        if m != '0' and m != '1':
            word_frag += m

    v_word_frag = word_frag[::-1]
    return v_word_frag


def get_possible_h_letters(h_word_frag, h_word_length, word_list):
    possible_letter_h = []
    for word in word_list:
        try:
            if word.startswith(str(h_word_frag)) and len(word) == h_word_length:
                possible_letter_h.append(word[len(h_word_frag)])
        except AttributeError:
            pass

    return possible_letter_h


def get_possible_v_letters(v_word_frag, v_word_length, word_list):
    possible_letter_v = []
    for word in word_list:
        try:
            if word.startswith(str(v_word_frag)) and len(word) == v_word_length:
                possible_letter_v.append(word[len(v_word_frag)])
        except AttributeError:
            pass

    return possible_letter_v


def prob_of_letter(possible_letter_h, possible_letter_v, puzzle):
    possible_letters = (pd.Series(possible_letter_h).value_counts() / len(possible_letter_h) * pd.Series(
        possible_letter_v).value_counts() / len(possible_letter_v)).dropna()

    if len(np.argwhere(puzzle == '1')) < 130:
        if np.random.uniform(0, 1) < .2:
            return possible_letters
        else:
            return possible_letters.sort_values(ascending=False)[:2]
    else:
        return possible_letters


def create(puzzle, word_list, h_past, v_past):
    print(puzzle, '\n')
    try:
        value = np.argwhere(puzzle == '1')[0]
    except IndexError:
        return True

    print(len(np.argwhere(puzzle == '1')))
    if len(np.argwhere(puzzle == '1')) < 1:
        return True
    else:
        row = value[0]
        column = value[1]

        h_word_length = get_h_word_length(puzzle, row, column)
        v_word_length = get_v_word_length(puzzle, row, column)

        h_frag = get_h_frag(puzzle, row, column, h_word_length)
        v_frag = get_v_frag(puzzle, row, column, v_word_length)

        if h_frag + str(h_word_length) in list(h_past.keys()):
            pos_h = h_past[h_frag + str(h_word_length)]
        else:
            pos_h = get_possible_h_letters(h_frag, h_word_length, word_list)
            h_past[h_frag + str(h_word_length)] = pos_h

        if v_frag + str(v_word_length) in list(v_past.keys()):
            pos_v = v_past[v_frag + str(v_word_length)]
        else:
            pos_v = get_possible_v_letters(v_frag, v_word_length, word_list)
            v_past[v_frag + str(v_word_length)] = pos_v

        possible_letters = prob_of_letter(pos_h, pos_v, puzzle)

        try:
            p_letters = np.random.choice(possible_letters.index, len(possible_letters.index), replace=False,
                                         p=possible_letters / sum(possible_letters))
        except ValueError:
            p_letters = []

        p_letters = p_letters[:2]
        print(p_letters)
        for letter in p_letters:
            print(letter)
            puzzle[row][column] = letter

            create(puzzle, word_list,h_past,v_past)

            if len(np.argwhere(puzzle == '1')) < 1:
                return puzzle

            print('\n back \n')
            puzzle[row][column] = '1'


        return False

def pad_with(vector, pad_width, iaxis, kwargs):
    pad_value = kwargs.get('padder', 10)
    vector[:pad_width[0]] = pad_value
    vector[-pad_width[1]:] = pad_value


def pad_puzzle(puzzle):
    """
    adds a layer of zeros around the puzzle

    :return: 17 by 17 matrix with padding
    """
    return np.pad(puzzle, 1, pad_with, padder=0)


def get_h_words(p):
    words_h = []
    for row in p:
        current_word = ''
        for letter in row:
            if letter != '0':
                current_word += letter
            else:
                if len(current_word) > 0:
                    words_h.append(current_word)
                current_word = ''
    return words_h


def get_v_words(p):
    words_v = []
    for row in p.T:
        current_word = ''
        for letter in row:
            if letter != '0':
                current_word += letter
            else:
                if len(current_word) > 0:
                    words_v.append(current_word)
                current_word = ''
    return words_v


def get_questions(word_list, data):
    questions = []
    for word in word_list:
        questions.append(np.random.choice(data[data['answers'] == word.upper()]['question'].values, 1)[0][:-2])

    return questions




nyt_data = pd.read_csv('/Users/mordechaichabot/Projects/crossword-creator/Data/processed_data/NYT_crossword.csv')
p_format_file = '/Users/mordechaichabot/Projects/crossword-creator/Data/raw_data/other_crosswords/jz140107.puz'

word_list = np.array(nyt_data['answers'].str.lower())


p = pad_puzzle(xword_matrix_gen(size=5))
puzzle_str = p.astype('str')

import time

start = time.time()



h_past = {}
v_past = {}

print(puzzle_str)

data = create(puzzle_str, word_list, h_past, v_past)
np.save('solved_puzzle2.txt', data)

h_words = get_h_words(data)
v_words = get_v_words(data)

h_questions = get_questions(h_words, nyt_data)
v_questions = get_questions(v_words, nyt_data)

np_to_puz(data, p_format_file, 'output_file.puz')
print(h_questions)
print(v_questions)
create_puz_puzzle('output_file.puz', h_questions, v_questions)


end = time.time()
print(end-start)
np.save('solved_puzzle2.txt', data)
