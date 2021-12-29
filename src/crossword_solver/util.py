import puz
import numpy as np


def read_puz_format(puzzle):
    p = puz.read(puzzle)

    puzzle_raw_format = []
    for row in range(p.height):
        cell = row * p.width
        puzzle_raw_format.append(' '.join(p.fill[cell:cell + p.width]))

    puzzle_format = []
    for i in puzzle_raw_format:
        puzzle_format.append(i.replace('-', '1').replace('.', '0'))

    puz2 = []
    for i in puzzle_format:
        puz2.append(i.split())

    return np.array(puz2)


def np_to_puz(p, input_file, output_file):
    puzzle_file = puz.read(input_file)
    puzzle = p[1:-1, 1:-1]
    words = ''
    for row in puzzle:
        for letter in row:
            if letter != '0':
                words += letter
            else:
                words += '.'
    print(words)
    puzzle_file.fill = words
    puzzle_file.save(output_file)


def create_puz_puzzle(input_file, h_questions, v_questions):
    puzzle = puz.read(input_file)
    numbering = puzzle.clue_numbering()

    for i, j in zip(numbering.across, h_questions):
        i['clue'] = j

    for i, j in zip(numbering.down, v_questions):
        i['clue'] = j

    full_list = []
    full_list.extend(numbering.across)
    full_list.extend(numbering.down)

    newlist = sorted(full_list, key=lambda k: k['num'])

    new_clues = []
    for i in newlist:
        new_clues.append(i['clue'])

    puzzle.clues = new_clues

    print(puzzle.clues)
    puzzle.save(input_file)
