import State as pst
import socket
from flask import Flask, render_template, request, jsonify

app = Flask("Sliding Puzzle")
SOLUTION_FILE = 'solutions.jff'


# noinspection PyBroadException
def get_all_solutions_in_file():
    try:
        file = open(SOLUTION_FILE, 'r')
    except IOError:
        file = open(SOLUTION_FILE, 'w')

    dictio = {}
    try:
        file = open(SOLUTION_FILE, 'r')
        for line in file:
            (key, val) = line.replace('\n', '').replace('\r', '').split('=')
            dictio[key] = val
        file.close()
    except Exception:
        pass
    return dictio


# noinspection PyBroadException
def get_solution_from_file(expected):
    solution = []
    try:
        solutions = get_all_solutions_in_file()
        if expected in solutions:
            print('Solution found')
            solution = [char for char in solutions[expected]]
            print(solution)
    except Exception:
        solution = []
        pass
    return solution


# noinspection PyBroadException
def save_solution_in_file(state, path):
    try:
        file = open(SOLUTION_FILE, 'r')
    except IOError:
        file = open(SOLUTION_FILE, 'w')

    try:
        solution = ''.join(str(n) for n in path)
        solutions = get_all_solutions_in_file()

        solutions[state] = solution

        file = open(SOLUTION_FILE, 'w')
        for (st, sol) in solutions.items():
            file.write(st + "=" + sol + "\n")
        file.close()
        return True
    except Exception:
        return False


@app.route("/")
def main():
    return render_template('index.html')


# noinspection PyBroadException
@app.route('/solve', methods=['GET'])
def solve():
    try:
        state_string = str(request.args.get('initial_state')) \
            .replace('[', '').replace(']', '').replace("'", '')

        state_array = []
        for char in state_string:
            state_array.append(int(char))

        solution = get_solution_from_file(state_string)

        if solution is None or len(solution) <= 0:
            initial_state = pst.State(state_array)
            moves, time, path, steps = initial_state.solve(print_states=True)
            save_solution_in_file(state_string, steps)
        else:
            moves = len(solution)
            time = 250
            path = []
            steps = solution

        return jsonify(moves=moves, time=time, path=path, steps=steps)
    except Exception:
        return jsonify(moves=-1, time=-1, path=[], steps=[])


# noinspection PyBroadException
@app.route('/save', methods=['POST'])
def save():
    try:
        state_string = str(request.args.get('initial_state')) \
            .replace('[', '').replace(']', '').replace("'", '')

        steps_arg = str(request.args.get('steps')) \
            .replace('[', '').replace(']', '').replace("'", '')
        steps = []
        for char in steps_arg:
            steps.append(str(char))

        solution = get_solution_from_file(state_string)

        saved = False
        if solution is None or len(solution) <= 0 or len(steps) < len(solution):
            saved = save_solution_in_file(state_string, steps)

        return jsonify(success=saved)
    except Exception:
        return jsonify(success=False)


if __name__ == "__main__":
    # hoster = socket.gethostbyname(socket.gethostname())
    # app.run(host=hoster)
    app.run()
