from flask import Flask, session

from flask_session import Session

from LambdaComplex_Entities import Credentials
from views.Views.Home import Home
from views.Views.CalendarEvent import CalendarEvent
from views.Views.Project import Project
from views.Views.TimeTrackingView import TimeTrackingView
from views.Views.User import User
from views.Views.Login import Login
from views.Views.ChartView import ChartView
from views.Views.DataView import DataView
from views.Views.Team import Team
from views.Views.FileUpload import FileUpload
from views.Views.Milestone import Milestone
from views.Views.Goal import Goal

from views.APIs.UserAPI import UserAPI
from views.APIs.CalendarEventAPI import CalendarEventAPI
from views.APIs.TeamAPI import TeamAPI
from views.APIs.FileUploadAPI import FileUploadAPI
from views.APIs.WorkTimeLineAPI import WorkTimeLineAPI
from views.APIs.ProjectAPI import ProjectAPI
from views.APIs.MilestoneAPI import MilestoneAPI
from views.APIs.GoalAPI import GoalAPI


# non functional for testing new controls only 
from views.Views.Test import Test
from views.APIs.TestAPI import TestAPI


App = Flask(__name__)
App.secret_key = 'HTV-BDNWL-XYZ'
App.config["SESSION_PERMANENT"] = True
App.config["PERMANENT_SESSION_LIFETIME"] = 300
App.config['SESSION_TYPE'] = 'filesystem'
Session(App)

Credentials.RootPath = App.root_path

# register views or controllers here 
App.register_blueprint(Home)
App.register_blueprint(Login,url_prefix='/Login/')
App.register_blueprint(CalendarEvent,url_prefix='/CalendarEvent/')
App.register_blueprint(User, url_prefix='/User')
App.register_blueprint(ChartView, url_prefix='/ChartView/')
App.register_blueprint(DataView, url_prefix='/DataView/')
App.register_blueprint(TimeTrackingView, url_prefix='/TimeTrackingView/')
App.register_blueprint(Team,url_prefix="/Team/")
App.register_blueprint(FileUpload,url_prefix="/FileUpload/")
App.register_blueprint(Project,url_prefix="/Project/")
App.register_blueprint(Milestone,url_prefix="/Milestone/")
App.register_blueprint(Goal,url_prefix="/Goal/")

# register APIs Views of APIs controllers here
App.register_blueprint(UserAPI, url_prefix='/api/UserAPI/')
App.register_blueprint(CalendarEventAPI, url_prefix='/api/CalendarEventAPI/')
App.register_blueprint(TeamAPI,url_prefix="/api/TeamAPI/")
App.register_blueprint(FileUploadAPI, url_prefix='/api/FileUploadAPI/')
App.register_blueprint(WorkTimeLineAPI, url_prefix='/api/WorkTimeLineAPI/')
App.register_blueprint(ProjectAPI, url_prefix='/api/ProjectAPI/')
App.register_blueprint(MilestoneAPI, url_prefix='/api/MilestoneAPI/')
App.register_blueprint(GoalAPI, url_prefix='/api/GoalAPI/')

# temporary testing purpose API
App.register_blueprint(Test, url_prefix='/Test/')
App.register_blueprint(TestAPI,url_prefix="/api/TestAPI/")

if(__name__ == "__main__"):
    App.run(debug=True)