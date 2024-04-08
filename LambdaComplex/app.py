from flask import Flask, session

from flask_session import Session

from views.Views.Home import Home
from views.Views.CalendarEvent import CalendarEvent
from views.Views.TimeTrackingView import TimeTrackingView
from views.Views.User import User
from views.Views.Login import Login
from views.Views.ChartView import ChartView
from views.Views.DataView import DataView
from views.Views.Team import Team

from views.APIs.UserAPI import UserAPI
from views.APIs.CalendarEventAPI import CalendarEventAPI
from views.APIs.TeamAPI import TeamAPI


# non functional for testing new controls only 
from views.Views.Test import Test
from views.APIs.TestAPI import TestAPI



app = Flask(__name__)
app.secret_key = 'HTV-BDNWL-XYZ'
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = 300
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# register views or controllers here 
app.register_blueprint(Home)
app.register_blueprint(Login,url_prefix='/Login/')
app.register_blueprint(CalendarEvent,url_prefix='/CalendarEvent/')
app.register_blueprint(User, url_prefix='/User')
app.register_blueprint(ChartView, url_prefix='/ChartView/')
app.register_blueprint(DataView, url_prefix='/DataView/')
app.register_blueprint(TimeTrackingView, url_prefix='/TimeTrackingView/')
app.register_blueprint(Team,url_prefix="/Team/")

# register APIs Views of APIs controllers here
app.register_blueprint(UserAPI, url_prefix='/api/UserAPI/')
app.register_blueprint(CalendarEventAPI, url_prefix='/api/CalendarEventAPI/')
app.register_blueprint(TeamAPI,url_prefix="/api/TeamAPI/")

# temporary testing purpose API
app.register_blueprint(Test, url_prefix='/Test/')
app.register_blueprint(TestAPI,url_prefix="/api/TestAPI/")

if(__name__ == "__main__"):
    app.run(debug=True)