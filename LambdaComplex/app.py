from flask import Flask, session

from flask_session import Session
from views.Views.Home import Home
from views.Views.CalendarEvent import CalendarEvent
from views.Views.User import User
from views.Views.Login import Login

from views.APIs.UserAPI import UserAPI
from views.APIs.CalendarEventAPI import CalendarEventAPI

app = Flask(__name__)
app.secret_key = 'HTV-TNJ-XYZ'
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = 300
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# register views or controllers here 
app.register_blueprint(Home)
app.register_blueprint(Login,url_prefix='/Login/')
app.register_blueprint(CalendarEvent,url_prefix='/CalendarEvent/')
app.register_blueprint(User, url_prefix='/User')
#register APIs Views of APIs controllers here
app.register_blueprint(UserAPI, url_prefix='/api/UserAPI/')
app.register_blueprint(CalendarEventAPI, url_prefix='/api/CalendarEventAPI/')



if(__name__ == "__main__"):
    app.run(debug=True)