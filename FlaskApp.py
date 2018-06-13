import State as pst
from flask import Flask, render_template, request, jsonify

# import socket

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

        old_solution = None
        if state in solutions:
            old_solution = solutions[state]

        if old_solution is None or len(old_solution) <= 0 or len(solution) <= len(old_solution):
            if len(solution) > 0:
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

        force = 'true' in str(request.args.get('force'))

        state_array = []
        for char in state_string:
            state_array.append(int(char))

        solution = get_solution_from_file(state_string)

        if force or solution is None or len(solution) <= 0:
            initial_state = pst.State(state_array)
            path, time = initial_state.optimal_solution()
            if path is None or len(path) <= 0:
                path = []
                time = 0
            else:
                save_solution_in_file(state_string, path)
        else:
            path = []
            time = 0.25

        return jsonify(moves=len(path), time=(time * 1000), steps=path, error=False)
    except Exception:
        return jsonify(moves=-1, time=-1, steps=[], error=True)


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

        return jsonify(success=saved, error=False)
    except Exception:
        return jsonify(success=False, error=True)


if __name__ == "__main__":
    # hoster = socket.gethostbyname(socket.gethostname())
    # app.run(host=hoster)
    app.run()
