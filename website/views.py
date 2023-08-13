from flask import Blueprint, render_template, request, jsonify

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@views.route("/index")
def index():
    return render_template("index.html")


@views.route("/sudoku")
def sudoku():
    return render_template("sudoku.html")


@views.route("/solve-sudoku", methods=["POST"])
def solve_sudoku():
    data = request.get_json()
    # print("data",data)
    # global grid
    grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    # print(grid)

    for btn in data:
        btn["value"] = int(btn["value"])
        grid_row = btn["id"].replace("btn", "")[0]
        grid_cell = btn["id"].replace("btn", "")[1]
        grid[int(grid_row)][int(grid_cell)] = btn["value"]

    print("grid", grid)

    solved = solve(grid)

    print("SOLVED", solved)
    solved_data = []
    for row_index, row in enumerate(solved):
        # print( row_index)
        for cell_index, cell in enumerate(row):
            # print(row_index, cell_index)
            insert = {"id": f"btn{row_index}{cell_index}", "value": cell}
            solved_data.append(insert)
    # print(solved_data)

    return jsonify(solved_data)


def possible(grid, row, column, number):
    # Is the number appearing in the given row?
    for i in range(0, 9):
        if grid[row][i] == number:
            return False
    # Is the number appearing in the given column?
    for i in range(0, 9):
        if grid[i][column] == number:
            return False
    # Is the number appearing in the given square?
    x0 = (column // 3) * 3
    y0 = (row // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[y0 + i][x0 + j] == number:
                return False
    return True


def solve(grid):
    for row in range(0, 9):
        for column in range(0, 9):
            if grid[row][column] == 0:
                for number in range(1, 10):
                    if possible(grid, row, column, number):
                        grid[row][column] = number
                        if solve(grid) is not None:  # Capture the return value
                            return grid
                        grid[row][column] = 0
                return
    return grid
