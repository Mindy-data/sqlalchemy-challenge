# Import the dependencies.
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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement

station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return last 12 months of data date and prcp"""
    # Query measurement
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    last_year_data = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= last_year).all()

    # Convert list of tuples into normal list
    prcp_dict = list(np.ravel(last_year_data))

    return jsonify(prcp_dict)



@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations"""
    # Query station
    s_list = session.query(station.station, station.name).all()

    # Convert list of tuples into normal list
    station_dict = list(np.ravel(s_list))

    return jsonify(station_dict)



@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observations"""
    # Query measurement
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    last_year_data = session.query(measurement.prcp, measurement.date).\
        filter(measurement.date >= last_year).all()

    # Convert list of tuples into normal list
    tobs_dict = list(np.ravel(last_year_data))

    return jsonify(tobs_dict)



@app.route("/api/v1.0/<start>/<end>")
def end():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, max and avg temperatures during defined timeframe"""
    # Query tobs for min, max and avg during timeframe
    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")
    
    tobs_tf = session.query(
        func.min(measurement.tobs).label('min_temperature'),
        func.max(measurement.tobs).label('max_temperature'),
        func.avg(measurement.tobs).label('avg_temperature')
        ).filter(measurement.date <= '2017-05-27')\
        .filter(measurement.date >= '2017-03-05').all()



    return jsonify(tobs_tf)


if __name__ == "__main__":
     app.run(debug=True)

session.close()
