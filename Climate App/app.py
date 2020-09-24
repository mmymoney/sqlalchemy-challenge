import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template

# Flask Setup

app = Flask(__name__)

#route list
route_list = ["/api/v1.0/csvtojson"]

@app.route("/")
def welcome():
    return render_template("index.html",routelist = route_list)

@app.route("/api/v1.0/precipitation")
def precipitation():
    file = pd.read_csv("/Data/ww_grouped.csv")
    # json = file.to_json()
    return file.to_json()

if __name__ == '__main__':
    app.run(debug=True)