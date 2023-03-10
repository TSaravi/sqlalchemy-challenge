import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import os 

from flask import Flask, jsonify

curr_dir = os.path.abspath(os.path.dirname(__file__))

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///"+os.path.join(curr_dir, "Resources/hawaii.sqlite"))

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# View all of the classes that automap found
for class_ in Base.classes:
    print(class_)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation"""
    # Query all precip
    results = session.query(Measurement.date, Measurement.prcp).all()

    res = {}

    for result in results:
        date, prcp = result[0], result[1]
        if date in res:
            res[date].append(prcp)
        else:
            res[date] = [prcp]
    
    session.close()

    return jsonify(res)


@app.route("/api/v1.0/stations")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all precip
    results = session.query(Station.station).all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation"""
    # Query all precip
    results = session.query(Measurement.date, Measurement.tobs).all()

    
    session.close()

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
