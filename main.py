from puzzle import State as pst
from random import shuffle
import os
import time

EXIT = "x"


# noinspection PyProtectedMember,PyBroadException
def play_game(initial_values, pc_moves, pc_time):
    key = ""
    puzzle = pst.State(initial_values)
    attempts = 0
    solved = puzzle.is_solved()
    start = time.time()
    while key != EXIT and not solved:
        print()
        print("New state: ")
        print(puzzle)
        print("Current errors: %d" % puzzle.errors_count())
        if attempts > 0:
            print("Current movements: %d" % attempts)
        print()
        key = input("Next move? (w,a,s,d,x) --> ").lower()
        # print("You pressed:", key)
        if key == EXIT:
            break
            """
            try:
                print("Exiting!")
                os._exit(0)
            except Exception:
                pass
            """
        else:
            moved, new_state = puzzle.move(key)
            if new_state is None:
                print("The key you pressed [" + key + "] is not valid")
            elif moved:
                attempts += 1
                solved = new_state.is_solved()
                puzzle = new_state

    if solved:
        print()
        if pc_moves < 0:
            print("Awesome! The computer was not even able to solve it :O")
        else:
            if pc_moves == attempts:
                print("It's a tie!")
            elif pc_moves < attempts:
                print("Too bad, the PC was faster than you :/ !")
            else:
                print("Wow! You solved it faster than the PC, what's your IQ?")
    else:
        print()
        print("So you gave up?")

    print()
    print("======================")
    print("====== RESULTS =======")
    print("======================")
    print("PC movements: %d" % pc_moves)
    print("PC time: %.5f seconds" % pc_time)
    print("======================")
    print("Human movements: %d" % attempts)
    print("Human time: %.5f seconds" % float(time.time() - start))
    print("======================")
    print()


def main():
    # initial_values = [4, 1, 3, 0, 5, 7, 6, 2, 8]
    # initial_values = list(range(9))
    initial_values = [4, 1, 3, 0, 5, 7, 6, 2, 8]
    # shuffle(initial_values)
    initial_state = pst.State(initial_values)
    print()
    moves, time, path, steps = initial_state.solve(print_states=True)
    print(path)
    print("Let's play the game!")
    # play_game(initial_values, moves, time)


if __name__ == '__main__':
    main()
