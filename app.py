import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def home():
    return (
        f"The following routes are available:</br>"
        f"</br>"
        f"<a href=/api/v1.0/precipitation> /api/v1.0/precipitation<a></br>"
        f"<a href=/api/v1.0/stations> /api/v1.0/stations<a></br>"
        f"<a href=/api/v1.0/tobs> /api/v1.0/tobs<a></br>"
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Fetch the precipitation for the date that matches
       the path variable supplied by the user, or a 404 if not."""

    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return precipitation data"""
    # Query the measurement table for dates and prcp values
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary with the data as the key and prcp as the value
    prcp_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    """Fetch a list of weather stations"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return stations"""
    # Query the station table
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Create a dictionary for each station that contains the station and name
    station_data = []
    for station, name in results:
        station_dict = {}
        station_dict["station id"] = station
        station_dict["station name"] = name
        station_data.append(station_dict)

    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    """Fetch temp observations from the most active station (USC00519397) from the most recent year of data"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return stations"""
    # Query the station table starting from the selected date for the selected station
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(
        (Measurement.date > '2016-08-22') & (Measurement.station == 'USC00519397')).all()

    session.close()

    # Create a dictionary for the selected station that contains the date and tobs
    station_tobs = []
    for station, date, tobs in results:
        station_tobs_dict = {}
        station_tobs_dict[date] = tobs
        station_tobs.append(station_tobs_dict)

    return jsonify(station_tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    """Fetch min temp, avg temp, and max temp beginning at the start date"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return stations"""
    # Query the station table starting from the selected date for the selected station
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(
        Measurement.date >= start).all()

    session.close()

    start_tobs = []
    for tmin, tavg, tmax in results:
        start_tobs_dict = {}
        start_tobs_dict["tmin"] = tmin
        start_tobs_dict["tavg"] = tavg
        start_tobs_dict["tmax"] = tmax
        start_tobs.append(start_tobs_dict)

    return jsonify(start_tobs)

@app.route("/api/v1.0/<start>/<end>")

def start_end(start, end):
    """Fetch min temp, avg temp, and max temp from the provided date range"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return stations"""
    # Query the station table starting from the selected date for the selected station
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(
        (Measurement.date >= start) & (Measurement.date <= end)).all()

    session.close()

    stend_tobs = []
    for tmin, tavg, tmax in results:
        stend_tobs_dict = {}
        stend_tobs_dict["tmin"] = tmin
        stend_tobs_dict["tavg"] = tavg
        stend_tobs_dict["tmax"] = tmax
        stend_tobs.append(stend_tobs_dict)

    return jsonify(stend_tobs)

if __name__ == "__main__":
    app.run(debug=True)