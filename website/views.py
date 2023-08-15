import folium
from flask import Blueprint, render_template, request, jsonify, render_template_string

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@views.route("/index")
def index():
    return render_template("index.html")


@views.route("/map")
def map():
    m = folium.Map(location=[-34.06242588810792, 18.45535459626709], zoom_start=9, width='70%', height='70%',
                   control_scale=True,
                   position='relative', left='15%')
    folium.Marker(location=[-34.09242588810792, 18.45535459626709], popup="My Home", tooltip="My Home",
                  icon=folium.Icon(icon='home', color='green')).add_to(m)

    folium.Marker(location=[-33.905147163594094, 18.41910346311488], popup="<strong>The Waterfront</strong>"
                                                                           "<br>"
                                                                           "<img src='/static/images/background.jpg'"
                                                                           "width='100px' height='100px'>",

                  tooltip="V&A Waterfront!", icon=folium.Icon(icon="info-sign", color='purple')).add_to(m)

    folium.Marker(location=[-34.339651476024976, 18.49386103891301], popup="Cape Point",
                  tooltip="Cape Point!", icon=folium.Icon(icon="info-sign", color='orange')).add_to(m)

    m.get_root().render()
    header = m.get_root().header.render()
    body_html = m.get_root().html.render()
    script = m.get_root().script.render()

    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <title>Folium</title>
	    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='index.css') }}">
	    <link rel="icon" href="{{ url_for('static', filename='favicon-32x32.png') }}" type="image/png">
	    <link rel="icon" href="{{ url_for('static', filename='favicon-16x16.png') }}" type="image/png">
	    <script type="text/javascript" src="{{ url_for('static', filename='index.js') }}"></script>
        {{ header|safe }}
    </head>
    <body class="body">
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
	        <div class="container-fluid">
		        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar">
			        <span class="navbar-toggler-icon"></span>
		        </button>
		        <div class="collapse navbar-collapse" id="navbar">
			        <div class="navbar-nav">
                        <a class="nav-item nav-link" id="home" href="/">Home</a>
                        <a class="nav-item nav-link" id="index" href="/index">About Me</a>
                        <a class="nav-item nav-link" id="sudoku" href="/sudoku">Sudoku</a>
                        <a class="nav-item nav-link" id="sudoku" href="/map">Map</a>
                        <a class="nav-item nav-link" id="nextup" href="/nextup">What's Next</a>
			        </div>
		        </div>
	        </div>
        </nav>
        <h2 class="text-center" style="margin-top: 20px; color: white;">Folium Example</h2>
        <div class="row">
            <div class="col-md-2"></div>
            <div class="col-md-8" style="margin-top: 30px;">
        <p class="text-center" style="margin-top: 30px; color: white;">Just a simple Folium Example with hardcoded 
        coordinates & markers, this could easily be very interactive where the user can enter their own coordinates and 
        place their own markers (perhaps branch locations, places of interest, clients etc. <br />
        <br />
        <strong>ISSUES TO SORT:</strong> Folium it appears uses a different version of bootstrap, as result the NavBar 
        looks slightly different, I will sort it eventually.
        </p>
        </div>
        <div class="col-md-2"></div>
        </div>
        {{ body_html | safe }}
        <div class="row" style="margin-top: 30px;">
            <div class="col"></div>
            </div>
    <script type="text/javascript">
    {{ script | safe }}
    </script>
    
    </body>
   
    ''', header=header, body_html=body_html, script=script)


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


# @views.route("/map")
# def map():
#     return render_template("map.html", map=m._repr_html_())
@views.route("/nextup")
def nextup():
    return render_template("nextup.html")
