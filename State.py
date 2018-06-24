from heapq import heappush, heappop, heapify
from copy import deepcopy
import time

GOAL = [1, 2, 3, 4, 5, 6, 7, 8, 0]
# GOAL = [1, 2, 3, 8, 0, 4, 7, 6, 5]
MAX_ITERS = 5000

UP_KEY = "w"
DOWN_KEY = "s"
LEFT_KEY = "a"
RIGHT_KEY = "d"

UP = "u"
DOWN = "d"
LEFT = "l"
RIGHT = "r"


class Queue:
    def __init__(self):
        self.pq = []

    def append(self, item):
        self.add(item)

    def add(self, item):
        heappush(self.pq, item)

    def pop(self):
        return heappop(self.pq)

    def peek(self):
        return self.pq[0]

    def remove(self, item):
        if item in self.pq:
            copy = deepcopy(item)
            self.pq.remove(item)
            heapify(self.pq)
            return copy is not None
        return False

    def __len__(self):
        return len(self.pq)


# noinspection PyBroadException
class State(object):
    def __init__(self, initial_values):
        self.steps = []
        self.parent = None
        self.depth = 0
        self.mvmnt = ''
        val = 0
        mat = []
        for i in range(0, 3):
            row = []
            for j in range(0, 3):
                row.append(initial_values[val])
                val += 1
            mat.append(row)
        self.matrix = mat

    def __cmp__(self, other):
        return self.matrix == other.matrix

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.__cmp__(other)

    def __hash__(self):
        return hash(str(self.matrix))

    def __lt__(self, other):
        return self.score() < other.score()

    def __contains__(self, item):
        pos = self.index_of(item)
        try:
            return pos[0] >= 0 and pos[1] >= 0
        except Exception:
            return False

    def __str__(self):
        res = "=========\n"
        for row in range(3):
            res += "[ "
            res += " ".join(map(str, self.matrix[row])).replace("0", "x")
            res += " ]"
            res += "\r\n"
        res += "========="
        return res

    def clone(self):
        clon = State(self.to_array())
        for i in range(3):
            clon.matrix[i] = self.matrix[i][:]
        return clon

    def get_path(self):
        path = [self]
        state = self.parent
        while state.parent:
            path.append(state)
            state = state.parent
        return reversed(path)

    def score(self):
        return self.errors_count() + self.depth

    def errors_count(self):
        vals = self.to_array()
        errors = 0
        for k in range(len(vals)):
            if vals[k] != GOAL[k]:
                errors += 1
        return errors

    def is_solved(self):
        return self.errors_count() <= 0

    def index_of(self, n):
        ist = [-1, -1]
        for i in range(0, 3):
            for j in range(0, 3):
                try:
                    if self.matrix[i][j] == n:
                        ist = [i, j]
                        break
                except Exception:
                    pass
        return ist

    def to_array(self):
        nums = []
        for i in range(0, 3):
            for j in range(0, 3):
                nums.append(self.matrix[i][j])
        return nums

    def move(self, key):
        if key == UP_KEY:
            return self.move_up()
        elif key == DOWN_KEY:
            return self.move_down()
        elif key == LEFT_KEY:
            return self.move_left()
        elif key == RIGHT_KEY:
            return self.move_right()
        else:
            return False, None

    def move_up(self):
        index = self.index_of(0)
        col = index[1]
        cur_row = index[0]
        new_row = index[0] - 1
        moved = False
        clon = self.clone()
        if 0 <= new_row <= 2:
            pre_val = clon.matrix[new_row][col]
            clon.matrix[new_row][col] = 0
            clon.matrix[cur_row][col] = pre_val

            new_steps = []
            for step in self.steps:
                new_steps.append(step)
            new_steps.append(UP_KEY)
            clon.steps = new_steps

            clon.mvmnt = UP_KEY
            clon.parent = self
            clon.depth = self.depth + 1
            moved = True
        return moved, clon

    def move_down(self):
        index = self.index_of(0)
        col = index[1]
        cur_row = index[0]
        new_row = index[0] + 1
        moved = False
        clon = self.clone()
        if 0 <= new_row <= 2:
            pre_val = clon.matrix[new_row][col]
            clon.matrix[new_row][col] = 0
            clon.matrix[cur_row][col] = pre_val

            new_steps = []
            for step in self.steps:
                new_steps.append(step)
            new_steps.append(DOWN_KEY)
            clon.steps = new_steps

            clon.mvmnt = DOWN_KEY
            clon.parent = self
            clon.depth = self.depth + 1
            moved = True
        return moved, clon

    def move_left(self):
        index = self.index_of(0)
        row = index[0]
        cur_col = index[1]
        new_col = index[1] - 1
        moved = False
        clon = self.clone()
        if 0 <= new_col <= 2:
            pre_val = clon.matrix[row][new_col]
            clon.matrix[row][new_col] = 0
            clon.matrix[row][cur_col] = pre_val

            new_steps = []
            for step in self.steps:
                new_steps.append(step)
            new_steps.append(LEFT_KEY)
            clon.steps = new_steps

            clon.mvmnt = LEFT_KEY
            clon.parent = self
            clon.depth = self.depth + 1
            moved = True
        return moved, clon

    def move_right(self):
        index = self.index_of(0)
        row = index[0]
        cur_col = index[1]
        new_col = index[1] + 1
        moved = False
        clon = self.clone()
        if 0 <= new_col <= 2:
            pre_val = clon.matrix[row][new_col]
            clon.matrix[row][new_col] = 0
            clon.matrix[row][cur_col] = pre_val

            new_steps = []
            for step in self.steps:
                new_steps.append(step)
            new_steps.append(RIGHT_KEY)
            clon.steps = new_steps

            clon.mvmnt = RIGHT_KEY
            clon.parent = self
            clon.depth = self.depth + 1
            moved = True
        return moved, clon

    def get_possible_movements(self):
        mu, att_one = self.move_up()
        md, att_two = self.move_down()
        ml, att_thr = self.move_left()
        mr, att_fou = self.move_right()

        options = []
        if mu:
            options.append(att_one)
        if md:
            options.append(att_two)
        if ml:
            options.append(att_thr)
        if mr:
            options.append(att_fou)

        return sorted(options, key=lambda p: p.score())

    def create_solution_tree(self, path):
        if self.parent is None:
            return path
        else:
            path.append(self)
            return self.parent.create_solution_tree(path)

    def _a_star(self, max_duration=120):
        openset = Queue()
        openset.add(self.clone())
        closedset = []
        start = time.time()

        while openset:
            end = time.time()
            if float(end - start) > max_duration or len(openset) <= 0:
                return None, -1

            current = openset.pop()
            if current.is_solved():
                moves = []
                temp = current
                while True:
                    moves.insert(0, temp.mvmnt)
                    if temp.depth <= 1:
                        break
                    temp = temp.parent
                end = time.time()
                return moves, float(end - start)
            new_moves = current.get_possible_movements()
            for state in new_moves:
                if state not in closedset:
                    openset.add(state)
            closedset.append(current)
        return None, -1

    def _bfs(self, max_duration=120):
        start = time.time()
        nodes = [self.clone()]
        while nodes:
            end = time.time()
            if float(end - start) > max_duration or len(nodes) <= 0:
                return None, -1

            node = nodes.pop(0)
            if node.is_solved():
                moves = []
                temp = node
                while True:
                    moves.insert(0, temp.mvmnt)
                    if temp.depth <= 1:
                        break
                    temp = temp.parent
                end = time.time()
                return moves, float(end - start)

            nodes.extend(node.get_possible_movements())
        return None, -1

    def _dfs(self, max_depth=20, max_duration=120):
        start = time.time()
        nodes = [self.clone()]
        while nodes:
            end = time.time()
            if float(end - start) > max_duration or len(nodes) <= 0:
                return None, -1

            node = nodes.pop(0)
            if node.is_solved():
                moves = []
                temp = node
                while True:
                    moves.insert(0, temp.mvmnt)
                    if temp.depth <= 1:
                        break
                    temp = temp.parent
                end = time.time()
                return moves, float(end - start)
            # Add all the expansions to the beginning of the stack if we are under the depth limit
            if node.depth < max_depth:
                new_nodes = node.get_possible_movements()
                new_nodes.extend(nodes)
                nodes = new_nodes
        return None, -1

    def _ids(self, max_depth=10, max_duration=120):
        start = time.time()
        for i in range(max_depth):
            end = time.time()
            if float(end - start) > max_duration:
                return None, -1
            result, total = self._dfs(max_depth=i, max_duration=max_duration)
            if result is not None:
                return result, total
        return None, -1

    def optimal_solution(self, max_duration=30, include_ids=False, use_all=False):
        print("Attempting to solve:")
        print(str(self))
        print("... ...")

        algo = "A*"

        print("Attempting to use %s algorithm" % algo)
        path, total = self._a_star(max_duration=max_duration * (1 if use_all else 1.5))

        if use_all:
            if path is None or len(path) <= 0:
                algo = "Breadth First Search"
                print("Attempting to use %s algorithm" % algo)
                path, total = self._bfs(max_duration=max_duration - 5)
            if path is None or len(path) <= 0:
                algo = "Depth First Search"
                print("Attempting to use %s algorithm" % algo)
                path, total = self._dfs(max_duration=max_duration - 5)
            if path is None or len(path) <= 0:
                if include_ids:
                    algo = "Iterative Depth First Search"
                    print("Attempting to use %s algorithm" % algo)
                    path, total = self._ids(max_duration=max_duration)

        if path is None or len(path) <= 0:
            algo = "None"
            path = []
            total = -1

        if path is not None and len(path) > 0 and total >= 0:
            print("Solution found using %s algorithm in %d movement(s) and %.3f seconds" % (
                algo, len(path), total))
            print("Steps: " + str(path))
        else:
            print("Solution not found")
        return path, total
