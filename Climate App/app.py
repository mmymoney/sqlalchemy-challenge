import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template

# Database Setup

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement



# Flask Setup

app = Flask(__name__)

#route list
route_list = ["/api/v1.0/precipitation","/api/v1.0/stations","/api/v1.0/tobs"]

@app.route("/")
def welcome():
    return render_template("index.html",routelist = route_list)


@app.route("/api/v1.0/precipitation")
def precipitation():
#     # Create our session (link) from Python to the DB
    session = Session(engine)

#     # Query all precipitation and date data
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

#Create a dictionary from the row data and append to a list of precipitation_data
    precipitation_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        precipitation_data.append(prcp_dict)

    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station).group_by(Station.station).filter(Measurement.date>='2016-08-23')

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results[:]))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all tobs"""
    # Query all stations
    results = session.query(Measurement.tobs).filter(Measurement.date>='2016-08-23')

    session.close()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(results[:]))

    return jsonify(tobs_list)

if __name__ == '__main__':
    app.run(debug=True)