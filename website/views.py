import os
import time

import cv2
import folium
from flask import (Blueprint, render_template, request, jsonify, render_template_string, url_for,
                   redirect, send_file, flash, send_from_directory)
from werkzeug.utils import secure_filename
from datetime import datetime
import openai
from . import db
from .models import File, Post, Feedback
import boto3
import uuid
import pandas as pd
import json
import plotly
import plotly.express as px
from dotenv import load_dotenv
from website.config.db import db
from PyPDF2 import PdfReader
from gtts import gTTS

from newsapi import NewsApiClient

# print("db", db)

## MONGO SETUP
files_uploaded = db.files
feedback_db = db.feedback

load_dotenv()

views = Blueprint("views", __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

bucket_name = "eccentrictoadperfectstaffbucket"

openai.api_key = os.getenv("OPENI_API")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route("/", methods=["GET", "POST"])
def home():
    result = list(files_uploaded.find())
    print("result", result)
    return render_template("home.html")


@views.route("/index")
def index():
    return render_template("index.html")


@views.route("/uploads", methods=["GET", "POST"])
def uploads():
    # if website/static/uploads folder does not exist, create it
    try:
        if not os.path.exists("website/static/uploads"):
            os.makedirs("website/static/uploads")
        if request.method == "POST":
            if request.files:
                doc = request.files["file"]
                if doc and allowed_file(doc.filename):
                    fileName = secure_filename(doc.filename)
                    fileName = f"{fileName.rsplit('.')[0]}_{datetime.now()}.{fileName.rsplit('.', 1)[1]}"
                    doc.save(os.path.join("website/static/uploads", fileName))
                    print("File Saved")
                    # get a list of all files in the uploads folder
                    files = os.listdir("website/static/uploads")
                    # return redirect(url_for("uploads"))
                    flash("File Uploaded", category="success")

                    return render_template("uploads.html", files=files)
                else:
                    print("That file extension is not allowed")
                    files = os.listdir("website/static/uploads")
                    flash("That file extension is not allowed", category="error")
                    return render_template("uploads.html", files=files)
        else:
            files = os.listdir("website/static/uploads")
            print(files)
            return render_template("uploads.html", message=None, files=files)
    except Exception as e:
        print("Error:", e)
        return render_template("uploads.html", message=None, files=None)


@views.route("/download/<filename>")
def download(filename):
    exact_path = f"static/uploads/{filename}"
    return send_file(exact_path, as_attachment=True)
    # return send_from_directory("website/static/uploads", filename=filename)


@views.route("/delete/<filename>")
def delete(filename):
    os.remove(os.path.join("website/static/uploads", filename))
    files = os.listdir("website/static/uploads")
    flash("File Deleted", category="success")
    return redirect(url_for("views.uploads", files=files))
    # return render_template("uploads.html", message="File Deleted", files=files)


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
    <link rel="icon" href="{{ url_for('static', filename='favicon-32x32.png') }}" type="image/png">
    <link rel="icon" href="{{ url_for('static', filename='favicon-16x16.png') }}" type="image/png">
    <script type="text/javascript" src="{{ url_for('static', filename='index.js') }}"></script>
    {{ header|safe }}
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9" crossorigin="anonymous">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='index.css') }}">
</head>
<body class="body">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top navMap">
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar">
            <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbar">
                <div class="navbar-nav">
                    <a class="nav-item nav-link mapA" id="home" href="/">Home</a>
                    <a class="nav-item nav-link mapA" id="index" href="/index">About Me</a>
                    <a class="nav-item nav-link mapA" id="sudoku" href="/sudoku">Sudoku</a>
                    <a class="nav-item nav-link mapA" id="sudoku" href="/map">Map</a>
                    <a class="nav-item nav-link mapA" id="s3example" href="/s3example">S3</a>
                 
                    <a class="nav-item nav-link mapA" id="dashboard" href="/dashboard">Dashboard</a>
                    <a class="nav-item nav-link mapA" id="csv2json" href="/csv2json">CSV2JSON</a>
                    <a class="nav-item nav-link mapA" id="chatbotn" href="/chatbot">Chatbot</a>
                    <a class="nav-item nav-link mapA" id="pdftext" href="/pdftext">TTS</a>
                    <a class="nav-item nav-link mapA" id="nextup" href="/feedback">Feedback</a>
                    <a class="nav-item nav-link mapA" id="nextup" href="/nextup">What's Next</a>
                </div>
            </div>
        </div>
    </nav>
    <br><br><br>
    <h2 class="text-center" style="margin-top: 20px; color: white;">Folium Example</h2>
    <div class="row">
        <div class="col-md-2"></div>
        <div class="col-md-8" style="margin-top: 30px;">
            <br>
            <br>
            <a class="text-center" href="https://github.com/WayneBruton/flaskPersonal/" target="_blank" style="color: 
            white; text-decoration: underline; color: yellow; font-size: 16px;">Source Code</a>
            <br>
            <br>
            <p class="text-center" style="margin-top: 30px; color: white; font-size: 15px;">Just a simple Folium 
            Example with hardcoded coordinates & markers, this could easily be very interactive where the user can 
            enter their own coordinates and place their own markers (perhaps branch locations, places of interest, 
            clients etc. <br />
            <br />
            <strong>ISSUES TO SORT:</strong> Folium it appears uses a different version of bootstrap, as result the 
            NavBar looks slightly different, I will sort it eventually.
            <br />
            Also, a marker can have an image, please see the purple marker on the map, I have added an image to the
            popup.
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

    for btn in data:
        btn["value"] = int(btn["value"])
        grid_row = btn["id"].replace("btn", "")[0]
        grid_cell = btn["id"].replace("btn", "")[1]
        grid[int(grid_row)][int(grid_cell)] = btn["value"]

    solved = solve(grid)

    solved_data = []
    for row_index, row in enumerate(solved):
        # print( row_index)
        for cell_index, cell in enumerate(row):
            # print(row_index, cell_index)
            insert = {"id": f"btn{row_index}{cell_index}", "value": cell}
            solved_data.append(insert)
    # print(solved_data)

    return jsonify(solved_data)


@views.route("/nextup")
def nextup():
    return render_template("nextup.html")


@views.route("/s3example", methods=["GET", "POST"])
def s3example():
    try:
        if request.method == "POST":
            uploaded_file = request.files["file"]
            if not allowed_file(uploaded_file.filename):
                flash("This type of file is not allowed", category="error")
                return redirect(request.url)
            new_fileName = uuid.uuid4().hex + '.' + uploaded_file.filename.rsplit('.', 1)[1].lower()
            AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
            AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
            s3 = boto3.client(
                "s3",
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            )

            s3.upload_fileobj(
                uploaded_file,
                bucket_name,
                new_fileName,
                ExtraArgs={
                    "ACL": "public-read",
                    "ContentType": uploaded_file.content_type
                }
            )
            region = "eu-central-1"

            insert = {
                "original_fileName": uploaded_file.filename,
                "fileName": new_fileName,
                "bucket": bucket_name,
                "region": region
            }
            response = files_uploaded.insert_one(insert)

            # files = list(files_uploaded.find())
            # for file in files:
            #     file["id"] = str(file["_id"])

            # return render_template("s3example.html", files=files)

            return redirect(url_for("views.s3example"))

        # files = File.query.all()
        files = list(files_uploaded.find())
        for file in files:
            file["id"] = str(file["_id"])

        # reverse the list
        files = files[::-1]

        # for file in files:
        #     print(file.fileName)

        return render_template("s3example.html", files=files)
    except Exception as e:
        print("Error:", e)
        return render_template("s3example.html", files=None)


@views.route("/delete_file/<id>/<filename>")
def delete_file(id, filename):
    try:
        AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
        AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        s3.delete_object(Bucket=bucket_name, Key=filename)
        file = files_uploaded.delete_one({"fileName": filename})
        return redirect(url_for("views.s3example"))
    except Exception as e:
        print("Error:", e)
        return redirect(url_for("views.s3example"))


@views.route("/imagemanipulation", methods=["GET", "POST"])
def imagemainpulation():
    try:
        global image_name
        if request.method == "POST":
            # delete all files in uploads folder
            files = os.listdir("website/uploads")
            for file in files:
                os.remove(f"website/uploads/{file}")
            if 'image' not in request.files:
                return redirect(request.url)
            doc = request.files["image"]
            if doc.filename == '':
                return redirect(request.url)

            if doc and allowed_file(doc.filename):
                fileName = secure_filename(doc.filename)
                fileName = f"{fileName.rsplit('.')[0]}_{datetime.now()}.{fileName.rsplit('.', 1)[1]}"
                doc.save(os.path.join("website/uploads", fileName))
                # print("File Saved")
                uploaded_img = url_for('views.uploaded_image', filename=fileName)

                if os.path.isfile("website/uploads/cropped_image.jpg"):
                    cropped_img1 = url_for('views.cropped_image', filename='cropped_image.jpg')

                else:
                    cropped_img1 = None

                # print("uploaded_image", uploaded_img)
                flash("File Uploaded", category="success")

                return render_template("image_manipulation.html",
                                       uploaded_image=uploaded_img, cropped_image=cropped_img1)

        # check if the file cropped_image.jpg is in the uploads folder, if yes, do the following: cropped_img1 = url_for(
        # 'views.cropped_image', filename='cropped_image.jpg') else set cropped_img1 = None
        if os.path.isfile("website/uploads/cropped_image.jpg"):
            cropped_img1 = url_for('views.cropped_image', filename='cropped_image.jpg')
            uploaded_img = url_for('views.uploaded_image', filename=image_name)


        else:
            cropped_img1 = None
            uploaded_img = None
            # delete all files in uploads folder
            files = os.listdir("website/uploads")
            for file in files:
                os.remove(f"website/uploads/{file}")

        return render_template("image_manipulation.html", uploaded_image=uploaded_img, cropped_image=cropped_img1)
    except Exception as e:
        print("Error:", e)
        return render_template("image_manipulation.html", uploaded_image=None, cropped_image=None)


@views.route("/uploaded_image/<filename>")
def uploaded_image(filename):
    print("filename", filename)
    return send_from_directory("uploads", filename)


image_name = ""


@views.route('/send-data-to-server', methods=['POST'])
def send_data_to_server():
    try:
        global image_name
        data = request.json
        image_name = data['imageName']
        new_left = data['newLeft']
        new_top = data['newTop']

        image_name = image_name.replace("%20", " ")
        image_name = image_name.rsplit("/", 1)[-1]

        image = cv2.imread(f"website/uploads/{image_name}")
        height = image.shape[0]
        width = image.shape[1]

        scaling_factor = width / 500  # Scaling factor from displayed image to actual image

        overlay_left_on_actual_image = new_left * scaling_factor
        overlay_top_on_actual_image = new_top * scaling_factor

        crop_width = int(150 * scaling_factor)  # Width of the cropping rectangle
        crop_height = int(150 * scaling_factor)  # Height of the cropping rectangle

        # Calculate the cropping rectangle coordinates
        crop_x = int(max(overlay_left_on_actual_image, 0))
        crop_y = int(max(overlay_top_on_actual_image, 0))

        # Calculate the right and bottom coordinates of the cropping rectangle
        crop_right = int(min(crop_x + crop_width, width))  # Limit to image width
        crop_bottom = int(min(crop_y + crop_height, height))  # Limit to image height

        cropped_img = image[crop_y:crop_bottom, crop_x:crop_right]
        cv2.imwrite('website/uploads/cropped_image.jpg', cropped_img)

        flash("Image Cropped", category="success")

        print("Good So Far")

        try:
            return jsonify({'success': True})
        except Exception as e:
            print("Error:", e)
            return jsonify({'success': False})
    except Exception as e:
        print("Error:", e)
        return jsonify({'success': False})


@views.route("/cropped_image/<filename>")
def cropped_image(filename):
    # print("filename", filename)
    # filename = filename.split("/")[1]
    # print("filename", filename)
    return send_from_directory("uploads", filename)


@views.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback = request.form
        # post = Post(title=feedback['title'], email=feedback['email'], content=feedback['content'])
        insert = {
            "title": feedback['title'],
            "email": feedback['email'],
            "content": feedback['content'],
            "date": datetime.now()
        }
        response = feedback_db.insert_one(insert)

        # get feedback from database and order by newest first
        posts = list(feedback_db.find().sort("date", -1))
        for post in posts:
            post["id"] = str(post["_id"])
            del post["_id"]

        # print(feedback)
        flash('Feedback Submitted', category='success')
        return redirect(url_for('views.feedback', posts=posts))

    posts = list(feedback_db.find().sort("date", -1))
    for post in posts:
        post["id"] = str(post["_id"])
        del post["_id"]

    return render_template('feedback.html', posts=posts)


@views.route('/dashboard')
def dashboard():
    # graph1
    df = px.data.medals_wide()
    fig1 = px.bar(df, x="nation", y=["gold", "silver", "bronze"], title="Medals")
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    # graph2
    df = px.data.gapminder().query("continent=='Oceania'")
    fig2 = px.line(df, x="year", y="lifeExp", color='country', title='Life expectancy in Oceania')
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    # graph3
    df = px.data.iris()
    # fig3 = px.scatter_3d(df, x="sepal_width", y="sepal_length", color="species",
    #                      size='petal_length', hover_data=['petal_width'])
    fig3 = px.scatter_3d(df, x="sepal_width", y="sepal_length", z="petal_length", color="species",
                         size='petal_width', hover_data=['petal_width'], title="Iris Data")
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graph1JSON=graph1JSON, graph2JSON=graph2JSON, graph3JSON=graph3JSON)


@views.route('/csv2json', methods=['GET', 'POST'])
def csv2json():
    if request.method == 'POST':
        csv_file = request.files['file']
        # get the filename
        filename = secure_filename(csv_file.filename)

        # remove the extension from the filename
        filename = filename.rsplit(".", 1)[0]

        df = pd.read_csv(csv_file)
        json_data = df.to_json(orient='records')
        # save json_data to website/uploads/json folder as json file
        with open(f'website/uploads/json/{filename}.json', 'w') as f:
            json.dump(json_data, f)
        # attach json_data.json to render_template

        files = os.listdir("website/uploads/json")
        for file in files:
            if file.endswith(".json"):
                filename = file

        if os.path.isfile(f"website/uploads/json/{filename}.json"):
            flash("CSV File Uploaded", category="success")
            # return the filename to the user
            return render_template('csv2json.html', filename=files)
        return render_template('csv2json.html', filename=files)

        # print("json_data", json_data)
    files = os.listdir("website/uploads/json")
    for file in files:
        if file.endswith(".json"):
            filename = file

    return render_template('csv2json.html', filename=files)


@views.route("/download_json/<filename>")
def download_json(filename):
    exact_path = f"uploads/json/{filename}"
    return send_file(exact_path, as_attachment=True)


@views.route("/uploaded_csv2jsn/<filename>")
def uploaded_csv2json(filename):
    # print("filename", filename)
    return send_from_directory("uploads/json", filename)


@views.route("/delete_json/<filename>")
def delete_json(filename):
    os.remove(os.path.join("website/uploads/json", filename))
    files = os.listdir("website/uploads/json")
    flash("JSON File Deleted", category="error")
    return redirect(url_for("views.csv2json", files=files))


@views.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    if request.method == "POST":
        user_input = request.form["message"]
        prompt = f"User: {user_input}\nChatbot: "
        chat_history = []
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,

        )
        # print("response", response)
        bot_response = response["choices"][0]["text"].strip()
        chat_history.append(f"User: {user_input}\nChatbot: {bot_response}")
        return render_template("chatbot.html", message=user_input, bot_response=bot_response)
    return render_template("chatbot.html", message=None, bot_response=None)


@views.route("/pdftext", methods=["GET", "POST"])
def pdftext():
    if os.path.isfile("website/uploads/story.mp3"):
        os.remove("website/uploads/story.mp3")
    if request.method == "POST":
        extract = request.form['words']
        # delete story.mp3 if it exists

        language = 'en'
        myobj = gTTS(text=extract, lang=language, slow=False, tld="co.za")
        myobj.save(f"website/uploads/story.mp3")
        mp3_filename = 'story.mp3'

        return render_template("pdftext.html", text=extract, filename=mp3_filename)
    extract = ("Just a basic text to speech example using gTTS. Feel free to change the text and click the \"Upload\" "
               "button.")
    return render_template("pdftext.html", text=extract, filename=None)


@views.route("/uploaded_mp3/<filename>")
def uploaded_mp3(filename):
    return send_from_directory("uploads", filename)


@views.route("/news")
def news():
    newsapi = NewsApiClient(api_key=os.getenv("NEWS_API"))

    top_headlines = newsapi.get_top_headlines(
        # q='bitcoin',
        # sources='bbc-news,the-verge',
        # category='technology',
        language='en',
        # country='us'
    )
    # sources = newsapi.get_sources()
    # print("top_headlines", top_headlines['articles'])
    # newsapi = NewsApiClient(api_key='dcb1aad26e88428385fb0916aaa983b2')
    # response = https://newsapi.org/v2/top-headlines?country=us&apiKey=dcb1aad26e88428385fb0916aaa983b2
    return render_template("news.html", top_headlines=top_headlines['articles'])


@views.route("/kanban")
def kanban():
    return render_template("kanban.html")


## SUDUKU SOLVER

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
