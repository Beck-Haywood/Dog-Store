from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

@app.route("/")
def homepage():

    pass

if __name__ == '__main__':
    app.run(debug=True)