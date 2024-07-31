# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for precipitation for for the last year of data
    query = session.query(measurement.date, measurement.prcp).filter(measurement.date >= '2016-08-23').order_by(measurement.date).all()

    # Close the session
    session.close()

    # Create a list of dictionaries to hold the data
    past_year_prec = []
    for date, prec in results:
        prec_dict = {}
        prec_dict[date] = prec
        past_year_prec.append(prec_dict)

    # Return Jsonified List
    return jsonify(past_year_prec)

@app.route("/api/v1.0/stations")
def stations():

     # Create our session (link) from Python to the DB   
    session = Session(engine)

    # Query for all the station number and station names
    results = session.query(station.station, station.name).all()

    # Close the session
    session.close()

    # Create a list of dictionaries to hold the data
    station_list = []
    for station, name in results:
        station_dict = {}
        station_dict["Station"] = station
        station_dict['Name'] = name
        station_list.append(station_dict)

    # Return Jsonified List
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for the past year of temperatures and dates
    # for the most active station USC00519281
    query = session.query(measurement.tobs, measurement.date).filter(measurement.date >= '2016-08-23', measurement.station == 'USC00519281').order_by(measurement.date).all()

    # Close the session
    session.close()

    # Create a list of dictionaries to hold the data
    tobs_list = []
    for tob, date in query:
        tob_dict = {}
        tob_dict["Temp"] = tob
        tob_dict["Date"] = date
        tobs_list.append(tob_dict)

    # Return Jsonified List
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start_date>")
def start_date(start_date):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for all the dates greater than or equal to the inputed start date.
    # Find the minimum temp, average temp, and maximum temp for data after
    # and including the start date. 
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start_date).all()

    # Close the session
    session.close()

    # Create a list of dictionaries to hold the data
    temp_list = []
    for min, avg, max in results:
        temp_dict = {}
        temp_dict['Min Temperature'] = min
        temp_dict['Avg Temperature'] = avg
        temp_dict['Max Temperature'] = max
        temp_list.append(temp_dict)

    # Return Jsonified List
    return jsonify(temp_list)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_date(start_date, end_date):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for all the dates greater than or equal to the inputed start date,
    # and less than or equal to the inputed end date.
    # Find the minimum temp, average temp, and maximum temp for data
    # within the date range. 
    query = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start_date, measurement.date <= end_date).all()

    # Close the session
    session.close()

    # Create a list of dictionaries to hold the data
    temp_list = []
    for min, avg, max in query:
        temp_dict = {}
        temp_dict['Min Temperature'] = min
        temp_dict['Avg Temperature'] = avg
        temp_dict['Max Temperature'] = max
        temp_list.append(temp_dict)

    # Return Jsonified List
    return jsonify(temp_list)



if __name__ == '__main__':
    app.run(debug=True)