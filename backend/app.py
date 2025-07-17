from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__, template_folder="../templates")

@app.route("/", methods=["GET", "POST"])
def success():
    return "<h1> Button was clicked! Hooray! </h1>"

if __name__ == "__main__":
    app.run(debug=True)