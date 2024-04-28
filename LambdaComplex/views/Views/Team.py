from flask import render_template, Blueprint
from SessionManagement import SessionManagement
from LambdaComplex_DataAccess.TeamModule import TeamModule
import html

Team = Blueprint("Team",__name__)

@Team.route('/CreateView/')
@SessionManagement('Admin')
def CreateView():
    return render_template('Team/Create.html')

@Team.route('/TeamMemberManagement/<teamId>')
@SessionManagement('Admin')
def TeamMemberManagement(teamId):
    return render_template('Team/ManageTeam.html', TeamId = teamId)

@Team.route('/LisTeamMembers/<teamId>')
@SessionManagement('Admin,Lead,Dev')
def LisTeamMembers(teamId):
    return render_template('Team/ListMembers.html', TeamId = teamId)

@Team.route('/UpdateView/<teamId>')
@SessionManagement('Admin')
def UpdateView(teamId):
    teamData = TeamModule.GetTeamData(teamId);

    # teamDescription is editor value always unescape editor values
    teamDescription = html.unescape(teamData["TeamDescription"])

    return render_template('Team/Update.html',
    TeamName = teamData["TeamName"],
    TeamDescription = teamDescription,
    LeaderID = teamData["LeaderID"],
    ProjectID = teamData["ProjectID"],
    ID = teamData["ID"])

@Team.route('/InformaticView/<teamId>')
@SessionManagement('Admin')
def InformaticView(teamId):
    teamData = TeamModule.GetTeamData(teamId)[0];

    # teamDescription is editor value always unescape editor values
    teamDescription = html.unescape(teamData["TeamDescription"])

    return render_template('Team/Informatic.html',
    TeamName = teamData["TeamName"],
    TeamDescription = teamDescription,
    LeaderID = teamData["LeaderID"],
    ProjectID = teamData["ProjectID"],
    ID = teamData["ID"])