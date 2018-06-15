const target = [1, 2, 3, 4, 5, 6, 7, 8, 0];
const test = [4, 0, 2, 5, 7, 3, 8, 1, 6];
const debug = false;

let game_started = false;
let game_finished = false;

let moves = 0;
let initial_time = 0;
let end_time = 0;

let bot_moves = -1;
let bot_time = -1;
let bot_path = [];

let solving = false;
let user_solved = false;
let bot_solved = false;

let initial_state = debug ? clone(test) : shuffle([1, 2, 3, 4, 5, 6, 7, 8, 0]);
let user_state = clone(initial_state);
let user_steps = [];
let bot_state = clone(initial_state);

let update_user_results = function () {
    if (!user_solved) {
        let text = document.getElementById('user-results');
        let realEnd = user_solved ? end_time : moves > 0 ? new Date().getTime() : 0;
        let time = msToTime(realEnd - initial_time);
        text.innerHTML = "🙋 You: " + moves + " movement(s) - Time: " + time;
    }
    update_winner();
};

function update_bot_results() {
    let text = document.getElementById('bot-results');
    if (bot_moves < 0 || bot_time <= 0) {
        text.innerHTML = "🤖 Robot: Not solved yet";
    } else {
        let time = msToTime(bot_time);
        text.innerHTML = "🤖 Robot: " + bot_moves + " movement(s) - Time: " + time;
    }
    update_winner();
}

function update_winner() {
    let text = document.getElementById('winner');
    text.innerHTML = "";
    if (user_solved || bot_solved) {
        let you = "🙋 You!";
        let bot = "🤖 Robot!";
        let winner = user_solved ? (moves <= bot_moves || bot_moves < 0) ? you : bot : bot;
        if (user_solved && moves === bot_moves) {
            let btns = document.getElementsByClassName('robot-btn');
            for (let a = 0; a < btns.length; a++) {
                btns[a].disabled = true;
            }
        }
        text.innerHTML = "Winner → " + winner;
    }
}

function new_game() {
    enable_ui(false);
    initial_state = debug ? clone(test) : shuffle([1, 2, 3, 4, 5, 6, 7, 8, 0]);
    moves = 0;
    initial_time = 0;
    solving = false;
    bot_solved = false;
    bot_path = [];
    bot_moves = -1;
    bot_time = -1;
    bot_state = clone(initial_state);
    restart();
    enable_ui(true);
    update_user_results();
    update_bot_results();
}

function restart() {
    game_started = false;
    end_time = 0;
    user_solved = false;
    user_steps = [];
    game_finished = false;
    user_state = clone(initial_state);
    init_puzzle(user_state);
}

function init_puzzle(which) {
    let user_puzzle = document.getElementById("user-puzzle");
    user_puzzle.innerHTML = "";
    let tr = document.createElement("tr");
    which.forEach(function (el, i) {
        let td = document.createElement("td");
        td.classList.add("piece");
        td.classList.add("no-select");
        if (el === 0) {
            td.innerHTML = " ";
        } else {
            td.innerHTML = el;
        }
        tr.appendChild(td);
        if ((i + 1) % 3 === 0) {
            user_puzzle.appendChild(tr);
            tr = document.createElement("tr");
        }
    })
}

addEventListener('keydown', function (ev) {
    // 87 - 38 --> Up
    // 65 - 37 --> Left
    // 83 - 40 --> Down
    // 68 - 39 --> Right

    if (solving || user_solved || game_finished) {
        return false;
    }

    let key = ev.keyCode;
    switch (key) {
        case 87:
        case 38:
            move('up', true);
            break;
        case 65:
        case 37:
            move('le', true);
            break;
        case 83:
        case 40:
            move('do', true);
            break;
        case 68:
        case 39:
            move('ri', true);
            break;
        default:
            break;
    }
});

function move(direction, isUser) {
    if (isUser) {
        if (solving || user_solved || game_finished) {
            update_winner();
            return;
        }
    }

    let space_index = isUser ? index_of(user_state, 0) : index_of(bot_state, 0);

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

    let new_index = space_index;
    if (new_row === 0) {
        new_index = new_col;
    } else {
        new_index = (3 * new_row) + new_col;
    }

    if (isUser) {
        let old = user_state[new_index];
        user_state[space_index] = old;
        user_state[new_index] = 0;
    } else {
        let old = bot_state[new_index];
        bot_state[space_index] = old;
        bot_state[new_index] = 0;
    }

    init_puzzle(isUser ? user_state : bot_state);

    if (moved && !solving && isUser) {
        let right_step = '';
        switch (direction) {
            case 'up':
                right_step = 'w';
                break;
            case 'do':
                right_step = 's';
                break;
            case 'le':
                right_step = 'a';
                break;
            case 'ri':
                right_step = 'd';
                break;
        }
        if (right_step.length > 0) {
            user_steps.push(right_step);
        }
        moves += 1;
        if (!game_started && !game_finished) {
            game_started = true;
            initial_time = new Date().getTime();
            window.setInterval(update_user_results, 100);
        }
        update_user_results();
    }

    let points = 0;
    for (let i = 0; i < target.length; i++) {
        if (target[i] === user_state[i]) {
            points += 1;
        }
    }

    if (points >= 9) {
        if (user_solved) {
            document.getElementById('restart-btn').disabled = true;
        }
        if (!solving) {
            window.clearInterval(update_user_results);
            end_time = new Date().getTime();
        }
        if (isUser) {
            user_solved = true;
            update_user_results();
            post_solution();
        } else {
            bot_solved = true;
            update_bot_results();
        }
    }
}

function enable_ui(enable) {
    var txt = document.getElementById('wait-txt');
    txt.style.display = enable ? 'none' : 'block';

    var buttons = document.getElementsByTagName('button');
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].disabled = !enable;
    }

    var keys = document.getElementsByClassName('kbd-key');
    for (var i = 0; i < keys.length; i++) {
        if (enable) {
            keys[i].classList.remove('disabled-key');
            keys[i].classList.remove('no-select');
        } else {
            keys[i].classList.add('disabled-key');
            keys[i].classList.add('no-select');
        }
    }
}

new_game();

function solve_by_pc(shouldFinishGame) {
    if (solving) {
        return false;
    }
    enable_ui(false);
    if (shouldFinishGame) {
        bot_state = clone(initial_state);
        init_puzzle(bot_state);
    }
    if (bot_path.length > 0) {
        solve_in_ui(bot_moves, bot_path, bot_time, shouldFinishGame);
    } else {
        call_py_code(shouldFinishGame, user_solved);
    }
}

function call_py_code(shouldFinishGame, force) {
    solving = true;
    let datos = 'initial_state=' + initial_state.join('') + '&force=' + force.toString();
    // console.log("Sending: " + datos);

    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'solve?' + datos, true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onreadystatechange = function () {
        var DONE = 4; // readyState 4 means the request is done.
        var OK = 200; // status 200 is a successful return.
        if (xhr.readyState === DONE) {
            if (xhr.status === OK) {
                let resp = JSON.parse(xhr.responseText);
                bot_moves = resp.moves;
                bot_path = resp.steps;
                bot_time = resp.time;
                if (bot_moves >= 0 && bot_path.length >= 0) {
                    if (shouldFinishGame) {
                        solve_in_ui(bot_moves, bot_path, bot_time, true);
                    } else {
                        bot_solved_it(false);
                    }
                } else {
                    bot_moves = -1;
                    bot_path = [];
                    bot_time = -1;
                    bot_not_solved();
                }
            } else {
                console.log('Error: ' + xhr.status); // An error occurred during the request.
                bot_not_solved();
            }
        }
    };
    xhr.send(null);
}

function solve_in_ui(moves, solution, time, shouldFinishGame) {
    // console.log("Puzzle solved");
    if (shouldFinishGame) {
        if (moves >= 0) {
            for (let a = 0; a < solution.length; a++) {
                move_by_pc(solution[a]);
                sleep(10);
            }

            setTimeout(function () {
                bot_solved_it(true);
            }, 100);
        } else {
            bot_not_solved();
        }
    } else {
        bot_solved_it(false);
    }
}

function bot_solved_it(shouldFinishGame) {
    solving = false;
    bot_solved = true;

    enable_ui(true);
    update_bot_results();

    if (shouldFinishGame) {
        game_finished = true;
        window.clearInterval(update_user_results);
        end_time = new Date().getTime();
        update_user_results();
    }

    document.getElementById('restart-btn').disabled = shouldFinishGame || game_finished;
}

function bot_not_solved() {
    solving = false;
    bot_solved = false;
    enable_ui(true);
    update_bot_results();
    alert("Sorry, our 🤖 robot could not solve this puzzle 😓")
}

function move_by_pc(sol) {
    let correct = "";
    switch (sol) {
        case "a":
            correct = "le";
            break;
        case "s":
            correct = "do";
            break;
        case "d":
            correct = "ri";
            break;
        case "w":
            correct = "up";
            break;
        default:
            correct = "";
            break;
    }
    if (correct.length > 0) {
        move(correct, false);
    }
}

function post_solution() {
    let datos = 'initial_state=' + initial_state.join('') + '&steps=' + user_steps.join('');
    // console.log("Sending: " + datos);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'save?' + datos, true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onreadystatechange = function () {
        var DONE = 4; // readyState 4 means the request is done.
        var OK = 200; // status 200 is a successful return.
        if (xhr.readyState === DONE) {
            if (xhr.status === OK) {
                let resp = JSON.parse(xhr.responseText);
                if (resp.success) {
                    console.log("User solution saved");
                } else {
                    console.warn("Bot has a better solution already");
                }
            } else {
                console.log('Error saving solution: ' + xhr.status); // An error occurred during the request.
            }
        }
    };
    xhr.send(null);
}