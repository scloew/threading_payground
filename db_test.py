import pyodbc
from collections import namedtuple
from classes.puzzle_factory import build_puzzle_str, build_puzzle_file

def get_puzzles():
    conn = pyodbc.connect(
        "Driver={SQL Server};"
        "Server=LAPTOP-B3HSU0AK\LOEWSQL;"
        "Database=SodukuPuzzles;"
        "Trusted_Connection=yes"
    )

    Puzzle = namedtuple('Puzzle', ['index_', 'difficulty', 'solution', 'mask'])

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Puzzles')
    # for row in cursor:
    #     print('test', row[3])
    #     # print([i for i in row])
    #     # print(type(row))
    #     # break
    return (Puzzle(i[0], i[1], i[2], i[3]) for i in cursor)

if __name__ == '__main__':
    puzzles = [(''.join([str(int(p.solution[i])*int(p.mask[i])) for i in range(81)]), p) for p in get_puzzles()]
    sanity = set()
    for p, solution in puzzles:
        puzzle = build_puzzle_str(p)
        puzzle.solve_puzzle()
        test = puzzle.to_string()
        p_solution = test.replace('\n', '').replace(' ', '').replace('-', '').replace('|', '')
        sanity.add(solution.solution == p_solution)
        print(solution.solution == p_solution)
    print(sanity)