import threading
import time
from random import randint

import db_test
import classes.puzzle_factory as factory


def solve_puzzle(thread_num, puzzle):
    print(f'running on sub-thread {thread_num}')
    print(f'original puzzle:\n{puzzle.to_string()}\n')
    puzzle.solve_puzzle()
    print(f'solved puzzle:\n{puzzle.to_string()}\n')


def thread_func(thread_num, puzzles):
    print(f'running on thread {thread_num}')
    for num, puzzle_str in enumerate(puzzles):
        puzzle = factory.build_puzzle_str(puzzle_str)
        thread = threading.Thread(target=solve_puzzle, args=((thread_num+num/10), puzzle))
        thread.start()

if __name__ == '__main__':
    puzzles = puzzles = [
        ''.join([str(int(p.solution[i])*int(p.mask[i])) for i in range(81)])
        for p in db_test.get_puzzles()
    ]

    for i in range(0, len(puzzles), 5):
        thread = threading.Thread(target=thread_func, args=(int(i/5), puzzles[i:i+5]))
        thread.start()
    # x = threading.Thread(target=thread_func, args=(1, puzzles[0]))
    # y = threading.Thread(target=thread_func, args=(2, puzzles[1]))
    # x.start()
    # y.start()