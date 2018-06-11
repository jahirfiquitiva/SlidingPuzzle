class Queue {
    constructor() {
        this.pq = [];
    }

    push(item) {
        this.add(item);
    }

    add(item) {
        this.pq.push(item);
        heapSort(this.pq);
    }

    pop() {
        return this.pq.pop()
    }

    peek() {
        return this.pq[0]
    }

    remove(item) {
        if (index_of(this.pq, item) !== -1) {
            this.pq.remove(item);
            heapSort(this.pq);
            return true;
        }
        return false;
    }

    get length() {
        return this.pq.length
    }
}

class State {
    constructor(initial_state) {
        this.steps = [];
        this.parent = null;
        this.depth = 0;
        this.array = clone(initial_state);
    }

    compare(other) {
        return this.score - other.score;
    }

    equals(other) {
        try {
            return this.array === other.array;
        } catch (e) {
            return false;
        }
    }

    lessThan(other) {
        return this.score < other.score;
    }

    contains(item) {
        let pos = index_of(this.array, item);
        try {
            return pos >= 0;
        } catch (e) {
            return false;
        }
    }

    toString() {
        let res = "=========\n";
        for (let i = 0; i < 3; i++) {
            res += "[ ";
            res += this.toMatrix()[i].join(' ').replace('0', 'x');
            res += " ]";
            res += "\r\n";
        }
        res += "=========";
        return res;
    }

    toMatrix() {
        let val = 0;
        let mat = [];
        for (let i = 0; i < 3; i++) {
            let row = [];
            for (let j = 0; j < 3; j++) {
                row[j] = this.array[val];
                val += 1;
            }
            mat[i] = row;
        }
        return mat;
    }

    getPath() {
        let path = [this];
        let pathIndex = 1;
        let state = this.parent;
        while (state.parent) {
            path[pathIndex] = state;
            state = state.parent;
            pathIndex += 1;
        }
        return path.reverse();
    }

    get score() {
        return this.errorsCount() + this.depth;
    };

    errorsCount() {
        let errors = 0;
        for (let i = 0; i < this.array.length; i++) {
            if (this.array[i] !== target[i]) {
                errors += 1;
            }
        }
        return errors;
    }

    get isSolved() {
        return this.errorsCount() <= 0;
    }

    move(direction) {
        let clon = new State(this.array);
        let space_index = index_of(clon.array, 0);

        let row = 0;
        if (space_index < 3) {
            row = 0;
        } else if (space_index >= 6) {
            row = 2;
        } else {
            row = 1;
        }
        let col = 0;
        if (row === 0) {
            col = space_index;
        } else {
            col = space_index - (3 * row);
        }

        let new_row = row;
        let new_col = col;
        let moved = false;

        switch (direction) {
            case 'up':
                if (row > 0) {
                    new_row = row - 1;
                    moved = true;
                }
                break;
            case 'do':
                if (row < 2) {
                    new_row = row + 1;
                    moved = true;
                }
                break;
            case 'le':
                if (col > 0) {
                    new_col = col - 1;
                    moved = true;
                }
                break;
            case 'ri':
                if (col < 2) {
                    new_col = col + 1;
                    moved = true;
                }
                break;
        }

        if (!moved) {
            return {
                moved: false,
                state: clon
            };
        }

        let new_index = space_index;
        if (new_row === 0) {
            new_index = new_col;
        } else {
            new_index = (3 * new_row) + new_col;
        }

        clon.array[space_index] = clon.array[new_index];
        clon.array[new_index] = 0;

        clon.parent = this;
        clon.depth = this.depth + 1;

        let new_steps = [];
        this.steps.forEach((e) => new_steps.push(e));
        new_steps.push(direction.substr(0, 1));
        clon.steps = new_steps;

        return {
            moved: true,
            state: clon
        };
    }

    get getPossibleMovements() {
        let up = this.move('up');
        let down = this.move('do');
        let le = this.move('le');
        let ri = this.move('ri');

        let options = [];
        if (up.moved) {
            options.push(up.state);
        }
        if (down.moved) {
            options.push(down.state);
        }
        if (le.moved) {
            options.push(le.state);
        }
        if (ri.moved) {
            options.push(ri.state);
        }

        timsort.sort(options, (a, b) => a.score - b.score);

        return options;
    }

    createSolutionTree(path) {
        if (this.parent === null) {
            return path;
        } else {
            path.push(this);
            return this.parent.createSolutionTree(path);
        }
    }

    _createNewState(array, parent, depth, steps) {
        let clon = new State(array);
        if (parent !== null) {
            clon.parent = this._createNewState(parent.array,
                                               parent.parent,
                                               parent.depth,
                                               parent.steps);
        } else {
            clon.parent = null
        }
        clon.depth = depth;
        clon.steps = steps;
        return clon;
    }

    _createNewStateObject(array, parent, depth, steps, score) {
        let correctParent = null;
        if (parent !== null) {
            correctParent = this._createNewStateObject(parent.array,
                                                       parent.parent,
                                                       parent.depth,
                                                       parent.steps,
                                                       parent.score);
        } else {
            correctParent = null
        }

        return {
            array: array,
            parent: correctParent,
            depth: depth,
            steps: steps,
            score: score
        };
    }

    solve(print = true, fun = null) {
        let openset = new Queue();

        openset.push(
            this._createNewStateObject(this.array, this.parent, this.depth, this.steps, this.score)
        );

        let closedset = [];
        let moves = 0;
        let iters = 0;

        console.log("Solving..");
        console.log(openset.peek());

        let start = new Date().getTime();
        let end = 0;
        let solved_path = [];

        let pp = false;
        let printed = false;

        while (openset) {
            let current = openset.pop();

            if (iters >= 10000) {
                moves = -1;
                break;
            }

            if (iters % 1000 === 0) {
                if (print) {
                    console.log("Iteration #" + iters);
                }
            }

            if (current.isSolved) {
                end = new Date().getTime();
                let path = current.createSolutionTree([]);
                let reversedPath = clone(path).reverse();

                for (let i = 0; i < reversedPath.length; i++) {
                    if (!printed) {
                        console.log(reversedPath[i]);
                        printed = true;
                    }
                    solved_path.append(reversedPath[i].array);
                    if (fun !== null) {
                        fun(reversedPath[i].array);
                    }
                    if (print) {
                        console.log(reversedPath[i]);
                    }
                }

                moves = path.length;
                let last = path.pop(0);
                if (print) {
                    console.log("Solution found");
                    console.log(moves + " steps: " + last.steps)
                }
                break;
            }

            let obj = this._createNewState(current.array, current.parent, current.depth,
                                           current.steps);
            let new_moves = obj.getPossibleMovements;
            if (new_moves.length > 0) {
                iters += 1;

                for (let j = 0; j < new_moves.length; j++) {
                    let new_state = new_moves[j];
                    let index = index_of(closedset, new_moves[j]);
                    if (index === -1) {
                        openset.push(this._createNewStateObject(new_state.array,
                                                                new_state.parent,
                                                                new_state.depth,
                                                                new_state.steps,
                                                                new_state.score));
                    }
                }
            }
            closedset.push(current);
        }

        if (moves <= 0) {
            console.log("Solution not found!");
        }

        return {
            moves: moves,
            time: end - start,
            solution: solved_path
        };
    }

}