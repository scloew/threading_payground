import threading

import db_test
import classes.puzzle_factory as factory


def solve_puzzle(thread_num, puzzle__, lock, out_file):
    original_puz = puzzle__.to_string()
    print(f'running on sub-thread {thread_num}')
    print(f'original puzzle:\n{puzzle__.to_string()}\n')
    puzzle__.solve_puzzle()
    print(f'solved puzzle:\n{puzzle__.to_string()}\n')

    with open(out_file, 'a') as out:
        out.write(f'running on sub-thread {thread_num}\n')
        out.write(f'original puzzle:\n\n{original_puz}\n\n')
        out.write(f'solved puzzle:\n\n{puzzle__.to_string()}\n\n')
        out.write(f'********\n********\n')


def thread_func(thread_num, puzzles_, lock, out_file):
    print(f'running on thread {thread_num}')
    while lock.locked():
        continue

    lock.acquire()
    for num, p in enumerate(puzzles_):
        puzzle = factory.build_puzzle_str(p[0])
        sub_thread = threading.Thread(target=solve_puzzle, args=((thread_num+num/10), puzzle, lock, out_file))
        sub_thread.start()
    lock.release()


if __name__ == '__main__':
    puzzles = puzzles = [
        (''.join([str(int(p.solution[i])*int(p.mask[i])) for i in range(81)]), p)
        for p in db_test.get_puzzles()
    ]

    lock = threading.Lock()

    for i in range(0, len(puzzles), 5):
        thread = threading.Thread(target=thread_func, args=(int(i/5), puzzles[i:i+5], lock, 'test.txt'))
        thread.start()
