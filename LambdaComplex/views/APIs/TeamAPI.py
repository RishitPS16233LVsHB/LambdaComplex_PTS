import json
from flask import jsonify, Blueprint, request
from LambdaComplex_DataAccess.TeamModule import TeamModule
from SessionManagement import SessionManagement
from LambdaComplex_Entities.Common import Response
from SessionManagement import SessionManagement,GetUserSessionDetails

TeamAPI = Blueprint("TeamAPI",__name__)

@TeamAPI.route('/Resource/')
@SessionManagement('Admin,Lead,Dev')
def Resource():
    try:
        response = Response()
        userSessionDetails = GetUserSessionDetails()
        userId = userSessionDetails.get("USER_ID")
        role = userSessionDetails.get("USER_ROLE")
        role = role.lower()
        resource = {}

        if role == 'admin' :
            resource = ResourcesForAdmin(userId)
        elif role == 'lead' :
            resource = ResourcesForLead(userId)
        elif role == 'dev':
            resource = ResourcesForDev(userId)

        response.Data = resource
        response.WasSuccessful = True
    except Exception as ex:
        response.message = str(ex)
        response.WasSuccessful = False 
    return jsonify(response.__dict__)

@TeamAPI.route('/MemberManagementResource/<teamId>')
@SessionManagement('Admin')
def MemberManagementResource(teamId):
    try:
        response = Response()
        resource = {}
        resource["ReadURL"] = "TeamAPI/GetTeamMemberList/" + teamId
        resource["GridHeight"] = "500px"
        resource["Fields"] = {
                "RecordID" : {"type" : "string"},
                "ID" : {"type" : "string"},
                "FirstName" : {"type" : "string"},
                "LastName" : {"type": "string"},
                "EmailId": {"type": "string"}, 
            }

        # Grid View only
        resource["Columns"] = [
            {
                "title" : "Remove memmber",
                "template": "<button class=\"btn btn-outline-danger\" onclick='RemoveMember(\"#: ID #\")'> <i class=\"mdi mdi-account-minus\"> </button>",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "field" : "FirstName",
                "title" : "First name",
                "width":200,
            },
            {
                "field" : "LastName",
                "title" : "Last name",
                "width":200,
            },
            {
                "field" : "EmailId",
                "title" : "Email Id",
                "width":200,
            },        
        ]
        response.Data = resource
        response.WasSuccessful = True
    except Exception as ex:
        response.message = str(ex)
        response.WasSuccessful = False 
    return jsonify(response.__dict__)

@TeamAPI.route('/InformaticsMemberManagementResource/<teamId>')
@SessionManagement('Admin')
def InformaticsMemberManagementResource(teamId):
    try:
        response = Response()
        resource = {}
        resource["ReadURL"] = "TeamAPI/GetTeamMemberList/" + teamId
        resource["GridHeight"] = "500px"
        resource["Fields"] = {
                "RecordID" : {"type" : "string"},
                "ID" : {"type" : "string"},
                "FirstName" : {"type" : "string"},
                "LastName" : {"type": "string"},
                "EmailId": {"type": "string"}, 
            }

        # Grid View only
        resource["Columns"] = [
            {
                "field" : "FirstName",
                "title" : "First name",
                "width":200,
            },
            {
                "field" : "LastName",
                "title" : "Last name",
                "width":200,
            },
            {
                "field" : "EmailId",
                "title" : "Email Id",
                "width":200,
            },        
        ]
        response.Data = resource
        response.WasSuccessful = True
    except Exception as ex:
        response.message = str(ex)
        response.WasSuccessful = False 
    return jsonify(response.__dict__)



def ResourcesForDev(userId):
    resource = {};

    resource["Fields"] = {
            "ID" : {"type" : "string"},
            "TeamName" : {"type" : "string"},                
            "TeamDescription" : {"type" : "string"},
            "LeaderFirstName" : {"type" : "string"},
            "LeaderLastName" : {"type": "string"},
            "AdminFirstName": {"type": "string"},
            "AdminLastName": {"type": "string"},
            "CreatedOn": {"type": "string"},
        }

    resource["Columns"] = [
        {
            "title" : "Info",
            "template": "<button class=\"btn btn-outline-info\" onclick='LoadTeamInformaticsView(\"#: ID #\")'> <i class=\"mdi mdi-information-outline\"> </button>",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "field" : "TeamName",
            "title" : "Team Name",
            "width": 200,
        },
        {
            "field" : "CreatedOn",
            "title" : "Team creation date",
            "format" : "{0:dd/MM/ yyyy}",
            "width": 200,            
        },
        {
            "field" : "TeamDescriptiom",
            "title" : "Team description",
            "width":200,
            "encoded": False,
        },
        {
            "field" : "LeaderFirstName",
            "title" : "Leader first name",
            "width":200,
        },
        {
            "field" : "LeaderLastName",
            "title" : "Leader Last name",
            "width":200,
        },
        {
            "field" : "AdminFirstName",
            "title" : "Admin first name",
            "width":200,
        },
        {
            "field" : "AdminLastName",
            "title" : "Admin last name",
            "width":200,
        },        
    ]

    resource["ReadURL"] = "TeamAPI/DataRead/Dev/" + userId
    resource["InformaticView"] = "Team/InformaticView/"
    return resource

def ResourcesForLead(userId):
    resource = {};

    resource["Fields"] = {
            "ID" : {"type" : "string"},
            "CreatedBy" : {"type" : "string"},
            "TeamName" : {"type" : "string"},            
            "TeamDescription" : {"type" : "string"},
            "LeaderFirstName" : {"type" : "string"},
            "LeaderLastName" : {"type": "string"},
            "AdminFirstName": {"type": "string"},
            "AdminLastName": {"type": "string"},
            "CreatedOn": {"type": "string"},
        }

    resource["Columns"] = [
        {
            "title" : "Info",
            "template": "<button class=\"btn btn-outline-info\" onclick='LoadTeamInformaticsView(\"#: ID #\")'> <i class=\"mdi mdi-information-outline\"> </button>",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "title" : "Raise issue",
            "template": "<button class=\"btn btn-outline-warning\" onclick='RaiseIssues(\"#: CreatedBy #\")'> <i class=\"mdi mdi-exclamation\"> </button>",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "field" : "TeamName",
            "title" : "Team Name",
            "width":200,
        },
        {
            "field" : "CreatedOn",
            "title" : "Team creation date",
            "format" : "{0:dd/MM/ yyyy}",
            "width":200,            
        },        
        {
            "field" : "TeamDescriptiom",
            "title" : "Team description",
            "width":200,
            "encoded": False,
        },
        {
            "field" : "LeaderFirstName",
            "title" : "Leader first name",
            "width":200,
        },
        {
            "field" : "LeaderLastName",
            "title" : "Leader Last name",
            "width":200,
        },
        {
            "field" : "AdminFirstName",
            "title" : "Admin first name",
            "width":200,
        },
        {
            "field" : "AdminLastName",
            "title" : "Admin last name",
            "width":200,
        },        
    ]

    resource["ReadURL"] = "TeamAPI/DataRead/Lead/" + userId
    resource["InformaticView"] = "Team/InformaticView/"

    return resource

def ResourcesForAdmin(userId):
    resource = {};
    resource["ReadURL"] = "TeamAPI/DataRead/Admin/" + userId
    resource["CreateViewUrl"] = "Team/CreateView/"
    resource["UpdateViewUrl"] = "Team/UpdateView/"
    resource["InformaticView"] = "Team/InformaticView/"
    resource["DeleteUrl"] = "TeamAPI/RemoveTeam/"

    resource["Fields"] = {
            "ID" : {"type" : "string"},
            "TeamName" : {"type" : "string"},
            "TeamDescription" : {"type" : "string"},
            "LeaderFirstName" : {"type" : "string"},
            "LeaderLastName" : {"type": "string"},
            "AdminFirstName": {"type": "string"},
            "AdminLastName": {"type": "string"},
            "CreatedOn": {"type": "string"},
        }

    # Grid View only
    resource["Columns"] = [
        {
            "title" : "Delete",
            "template": "<button class=\"btn btn-outline-danger\" onclick='DeleteRecord(\"#: ID #\")'> <i class=\"mdi mdi-delete\"> </button>",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "title" : "Edit",
            "template": "<button class=\"btn btn-outline-primary\" onclick='LoadUpdateView(\"#: ID #\")'> <i class=\"mdi mdi-grease-pencil\"> </button>",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "title" : "Info",
            "template": "<button class=\"btn btn-outline-info\" onclick='LoadTeamInformaticsView(\"#: ID #\")'> <i class=\"mdi mdi-information-outline\"> </button>",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "field" : "TeamName",
            "title" : "Team Name",
            "width":200,
        },
        {
            "field" : "TeamDescription",
            "title" : "Team description",
            "width":200,
            "encoded": False,
        },
        {
            "title" : "Manage Team",
            "template": "<button class=\"btn btn-outline-warning\" onclick='LoadTeamManagementView(\"#: ID #\")'> <i class=\"mdi mdi-account-multiple-outline\"> </button>",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "field" : "CreatedOn",
            "title" : "Team creation date",
            "format" : "{0:dd/MM/ yyyy}",
            "width":200,            
        },
        {
            "field" : "LeaderFirstName",
            "title" : "Leader first name",
            "width":200,
        },
        {
            "field" : "LeaderLastName",
            "title" : "Leader Last name",
            "width":200,
        },
        {
            "field" : "AdminFirstName",
            "title" : "Admin first name",
            "width":200,
        },
        {
            "field" : "AdminLastName",
            "title" : "Admin last name",
            "width":200,
        },        
    ]


    return resource



@TeamAPI.route('/DataRead/Dev/<userId>')
@SessionManagement('Dev')
def DataReadDev(userId):
    try:
        response = Response()
        result = TeamModule.GetTeamsForDev(userId)
        response.Data = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False
    return jsonify(response.__dict__)

@TeamAPI.route('/DataRead/Lead/<userId>')
@SessionManagement('Lead')
def DataReadLead(userId):
    try:
        response = Response()
        result = TeamModule.GetTeamsForLead(userId)
        response.Data = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False
    return jsonify(response.__dict__)

@TeamAPI.route('/DataRead/Admin/<userId>')
@SessionManagement('Admin')
def DataReadAdmin(userId):
    try:
        response = Response()
        result = TeamModule.GetTeamsForAdmin(userId)
        response.Data = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False
    return jsonify(response.__dict__)

@TeamAPI.route('/GetTeamMemberList/<teamId>')
@SessionManagement('Admin')
def GetTeamMemberList(teamId):
    try:
        response = Response()
        result = TeamModule.GetTeamMemberList(teamId)
        response.Data = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False
    return jsonify(response.__dict__)


@TeamAPI.route('/UpdateTeam/',methods=['POST'])
@SessionManagement('Admin')
def UpdateTeam():
    try:
        response = Response()
        teamData = json.loads(request.data)
        result = TeamModule.UpdateTeam(teamData)
        response.Data = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False
    return jsonify(response.__dict__)

@TeamAPI.route('/CreateTeam/',methods=['POST'])
@SessionManagement('Admin')
def CreateTeam():
    try:
        response = Response()
        teamData = json.loads(request.data)
        result = TeamModule.CreateTeam(teamData)
        response.Data = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False
    return jsonify(response.__dict__)

@TeamAPI.route('/RemoveTeam/<teamId>',methods=['GET'])
@SessionManagement('Admin')
def RemoveTeam(teamId):
    try:
        response = Response()
        result = TeamModule.RemoveTeam(teamId)
        response.Data = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False
    return jsonify(response.__dict__)

@TeamAPI.route('/AddTeamMember/',methods=['POST'])
@SessionManagement('Admin')
def AddTeamMember():
    try:
        response = Response()
        teamData = json.loads(request.data)
        teamId = teamData["teamId"]
        teamMemberId = teamData["teamMemberId"]
        userId = teamData["userId"]
        result = TeamModule.AddTeamMember(teamId,teamMemberId,userId)
        response.Data = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False
    return jsonify(response.__dict__)

@TeamAPI.route('/RemoveTeamMember/<recordId>',methods=['GET'])
@SessionManagement('Admin')
def RemoveTeamMember(recordId):
    try:
        response = Response()
        result = TeamModule.RemoveTeamMember(recordId)
        response.Data = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False
    return jsonify(response.__dict__)



