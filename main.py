from website import create_app

# create folder website/uploads if not exist
import os

if not os.path.exists('website/uploads'):
    os.makedirs('website/uploads')

app = create_app()

if __name__ == '__main__':
    app.run()

# app.run(debug=True, port=8010)
