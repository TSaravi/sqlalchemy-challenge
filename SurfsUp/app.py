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


@app.route("/api/v1.0/passengers")
def passengers():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    for name, age, sex in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
