let game_started = false;
let moves = 0;
let initial_time = 0;
let end_time = 0;

let solving = false;
let solved = false;

const target = [1, 2, 3, 4, 5, 6, 7, 8, 0];
let initial_state = [4, 1, 3, 0, 5, 7, 6, 2, 8]; // shuffle([1, 2, 3, 4, 5, 6, 7, 8, 0]);
let user_state = clone(initial_state);

function init_puzzle() {
    let user_puzzle = document.getElementById("user-puzzle");
    user_puzzle.innerHTML = "";
    let tr = document.createElement("tr");
    user_state.forEach(function (el, i) {
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
            // console.log(i + "Divisible por 3");
            user_puzzle.appendChild(tr);
            tr = document.createElement("tr");
        }
    })
}

new_game();

addEventListener('keydown', function (ev) {
    // 87 - 38 --> Up
    // 65 - 37 --> Left
    // 83 - 40 --> Down
    // 68 - 39 --> Right

    if (solving || solved) {
        return false;
    }

    let key = ev.keyCode;
    switch (key) {
        case 87:
        case 38:
            move('up');
            break;
        case 65:
        case 37:
            move('le');
            break;
        case 83:
        case 40:
            move('do');
            break;
        case 68:
        case 39:
            move('ri');
            break;
        default:
            break;
    }
});

function restart(force) {
    if (solved && !force) {
        return;
    }
    user_state = clone(initial_state);
    init_puzzle();
}

function new_game() {
    enable_ui(false);
    initial_state = [4, 1, 3, 0, 5, 7, 6, 2, 8]; // shuffle([1, 2, 3, 4, 5, 6, 7, 8, 0]);
    game_started = false;
    moves = 0;
    initial_time = 0;
    end_time = 0;
    solving = false;
    solved = false;
    restart(true);
    enable_ui(true);
}

function move(direction) {
    if (solved) {
        return false;
    }

    let space_index = index_of(user_state, 0);

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

    /*
    console.log("Moving to " + direction);
    console.log("Index of 0 -> " + space_index);
    console.log("Current position: [" + row + ", " + col + "]");
    console.log("Target position: [" + new_row + ", " + new_col + "]");
    console.log("Target index -> " + new_index);
    */

    let old = user_state[new_index];
    user_state[space_index] = old;
    user_state[new_index] = 0;
    init_puzzle();

    if (solving) {
        sleep(500);
    }

    if (!game_started && moved) {
        game_started = true;
        initial_time = new Date().getTime();
    }

    if (moved) {
        moves += 1;
    }

    let points = 0;
    for (let i = 0; i < target.length; i++) {
        if (target[i] === user_state[i]) {
            points += 1;
        }
    }

    if (points >= 9) {
        solved = true;
        if (!solving) {
            end_time = new Date().getTime();
            alert("You solved it with " + moves + " movements in " +
                  msToTime(end_time - initial_time));
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

function solve_by_pc() {
    if (solving || solved) {
        return false;
    }
    enable_ui(false);
    call_py_code();
}

function call_py_code() {
    solving = true;
    let datos = 'initial_state=' + initial_state.join('');
    console.log("Sending: " + datos);

    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'solve?' + datos, true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onreadystatechange = function () {
        var DONE = 4; // readyState 4 means the request is done.
        var OK = 200; // status 200 is a successful return.
        if (xhr.readyState === DONE) {
            if (xhr.status === OK) {
                let resp = JSON.parse(xhr.responseText);
                solve_in_ui(resp.moves, resp.steps, resp.time);
            } else {
                console.log('Error: ' + xhr.status); // An error occurred during the request.
                pc_not_solved();
            }
        }
    };
    xhr.send(null);
}

function solve_in_ui(moves, solution, time) {
    console.log("Puzzle solved");
    if (moves >= 0) {
        // move_by_pc(solution[0]);
        // move_by_pc(solution[1]);
        for (var a = 0; a < solution.length; a++) {
            move_by_pc(solution[a]);
            sleep(10);
        }

        setTimeout(function () {
            solved = true;
            solving = false;
            enable_ui(true);
            alert("PC solved it with " + moves + " movements in " + msToTime(time));
        }, 100);
    } else {
        pc_not_solved();
    }
}

function pc_not_solved() {
    enable_ui(true);
    solved = false;
    solving = false;
    alert("PC couldn't solve it! D:");
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
        move(correct);
    }
}