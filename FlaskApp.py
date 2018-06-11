import json
from puzzle import State as pst
from random import shuffle
import os
import time

from flask import Flask, render_template, request, jsonify

app = Flask("Sliding Puzzle")


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/solve', methods=['GET'])
def solve():
    state_string = str(request.args.get('initial_state')).replace('[', '').replace(']', '').replace(
        "'", '')
    state_array = []
    for char in state_string:
        state_array.append(int(char))
    print(state_array)

    initial_state = pst.State(state_array)
    moves, time, path, steps = initial_state.solve(print_states=True)

    return jsonify(moves=moves, time=time, path=path, steps=steps)


if __name__ == "__main__":
    app.run()
