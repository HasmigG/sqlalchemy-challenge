# Import the dependencies.
import sqlalchemy
from flask import Flask
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
M = Base.classes.measurement
S = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    return '''
<h1>Hawaii's Climate Analysis</h1>
<h3>The following routes are available:</h3>
<ul>
    <li>api/v1.0/precipitation</li>
    <li>api/v1.0/stations</li>
    <li>api/v1.0/tobs</li>
    <li>api/v1.0/[start]/[end]</li>
</ul>
'''

@app.route('/api/v1.0/precipitation')
def precipitation():
    
    return { date:prcp for date,prcp in session.query(M.date,M.prcp).filter(M.date>='2016-08-23').all() }

@app.route('/api/v1.0/stations')
def stations():

    return { id:loc for id,loc in session.query(S.station,S.name).all() }

@app.route('/api/v1.0/tobs')
def tobs():

    return { d:t for d,t in session.query(M.date,M.tobs).all() }

@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def temp_range(start,end='2017-08-23'):

    results = session.query(
        func.min(M.tobs),
        func.max(M.tobs),
        func.avg(M.tobs)
        ).filter((M.date>=start)&(M.date<=end)).first()
    
    return {'Min':results[0],'Max':results[1],'AVG':results[2],'StartDate':start,'EndDate':end}