"""app.py: render and route to webpages"""
from flask import render_template

from db.server import app

# create a webpage based off of the html in templates/index.html
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/page1')
def page1():
    return render_template("page1.html")

@app.route('/page2')
def page2():
    return render_template("page2.html")

if __name__ == "__main__":
    # debug refreshes your application with your new changes every time you save
    app.run(debug=True)

