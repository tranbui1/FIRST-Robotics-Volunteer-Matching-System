from flask import Flask
import sqlalchemy
from sqlalchemy import create_engine

app = Flask(__name__)

data_path = "/Users/chansoon/Downloads/Matching Logic - Sheet1.csv"

# Establish a connection with SQL database
with open(data_path, "r") as f:
    conn = create_engine("postgresql+psycopg://postgres:1209@localhost:5432/postgres")
    print(conn)

@app.route("/")
def hello_world():
    return "<p> Hello world! <p>"