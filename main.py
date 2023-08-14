from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=8010)


# app.run(debug=True, port=8010)
