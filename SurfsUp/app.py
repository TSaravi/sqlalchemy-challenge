import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import os 
import datetime as dt
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
def precip():
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
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    results = session.query(Station.station).all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all tobs"""
    recent_date = session.query(Measurement).order_by(Measurement.date.desc()).first().date

    dt_recent_date = dt.datetime.strptime(recent_date, '%Y-%m-%d')

    prev_year = dt_recent_date - dt.timedelta(days= 365)

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > prev_year).all()
    
    res = {}

    for result in results:
        date, tobs = result[0], result[1]
        if date in res:
            res[date].append(tobs)
        else:
            res[date] = [tobs]
    
    session.close()

    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)
