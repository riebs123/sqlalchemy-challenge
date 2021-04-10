import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
station = Base.classes.station
measurement = Base.classes.measurement


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/precipitation<br/>"
        f"/tobs<br/>"
        f"/stations"
    )


@app.route("/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(station.station).group_by(station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_precipitation = []
    for key, value in results:
        precipitation_dict = {}
        precipitation_dict["date"] = key
        precipitation_dict["prcp"] = value
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

@app.route("/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    year_earlier_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    
    # Query all passengers
    results = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date >= year_earlier_date). \
    filter(measurement.station == 'USC00519281').all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_tobs = []
    for key, value in results:
        tobs_dict = {}
        tobs_dict["date"] = key
        tobs_dict["prcp"] = value
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)



if __name__ == '__main__':
    app.run(debug=True)
