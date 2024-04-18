import json
from flask import jsonify, Blueprint, request
from LambdaComplex_DataAccess.GoalModule import GoalModule
from SessionManagement import SessionManagement
from LambdaComplex_Entities.Common import Response
from SessionManagement import SessionManagement,GetUserSessionDetails

GoalAPI = Blueprint("GoalAPI",__name__)

@GoalAPI.route('/GetGoals/', methods = ['GET'])
@SessionManagement('Lead')
def GetGoals():
    try:
        userId = GetUserSessionDetails()["USER_ID"]
        response = Response()        
        result = GoalModule.GetGoalNameID(userId)
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@GoalAPI.route('/MacroTrackingGridResource/<goalId>')
@SessionManagement('Admin,Lead,Dev')
def MacroTrackingGridResource(goalId):
    try:
        response = Response()
        resource = {}
        resource["ReadURL"] = "GoalAPI/MacroTrackingGridViewRead/" + goalId
        
        resource["Fields"] = {
                "ID" : {"type" : "string"},
                "RecordID" : {"type" : "string"},
                "Name" : {"type" : "string"},                
                "Description" : {"type" : "string"},
                "CreatedByName" : {"type" : "string"},
                "CreatedBy" : {"type": "string"},
                "CreatedOn": {"type": "date"},
                "Deadline": {"type": "date"},
                "IsStable": {"type": "string"},
                "ReportingStatus": {"type": "string"},
                "Remarks": {"type": "string"},
                "Rating": {"type": "string"},
            }

        resource["Columns"] = [
            {
                "field" : "Name",
                "title" : "Goal Name",
                "width": 200,
            },
            {
                "field" : "ReportingStatus",
                "title" : "Goal status",
                "width": 200,
            },
            {
                "field" : "CreatedOn",
                "title" : "Goal creation date",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Deadline",
                "title" : "Goal deadline",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Description",
                "title" : "Goal description",
                "width":200,
                "encoded": False,
            },
            {
                "title" : "File submissions",
                "template": "<button class=\"btn btn-outline-secondary\" onclick='LoadReadOnlyFileView(\"#: ID #\",true,true,divMainPage)'> <i class=\"mdi mdi-file-multiple\"> </i></button>",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "field" : "Rating",
                "title" : "Goal rating",
                "template": "<div id=\"ratingBar#: ID #\"></div>",
                "width":200,
            },
            {
                "field" : "Remarks",
                "title" : "Goal remarks",
                "width":200,
            },
            {
                "field" : "CreatedByName",
                "title" : "Goal Created by",
                "width":200,
            }        
        ]
        response.Data = resource
        response.WasSuccessful = True
    except Exception as ex:
        response.message = str(ex)
        response.WasSuccessful = False 
    return jsonify(response.__dict__)

@GoalAPI.route('/MacroTrackingGridViewRead/<goalId>', methods = ['GET'])
@SessionManagement('Admin,Lead,Dev')
def MacroTrackingGridViewRead(goalId):
    try:
        response = Response()        
        result = GoalModule.GetMacroHistory(goalId)
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@GoalAPI.route('/MacroTrackingTimeLineRead/<goalId>')
@SessionManagement('Admin,Lead,Dev')
def MacroTrackingTimeLineRead(goalId):
    try:
        response = Response()
        resource = {}
        resource["Data"] = GoalModule.GetMacroHistory(goalId)
        resource["Mappings"] = {
            "time" : "CreatedOn",
            "header" : "ReportingStatus",
            "h1Body" : "CreatedOn",
            "paraBody" : "Remarks",
            "footer": "CreatedByName" 
        }
        response.Data = resource 
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@GoalAPI.route('/DataRead/Dev/<userId>/<parentId>', methods = ['GET'])
@SessionManagement('Dev')
def DataReadForDevs(userId,parentId):
    try:
        response = Response()        
        result = GoalModule.GetLatestGoalForDev(parentId,userId)
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@GoalAPI.route('/DataRead/Lead/<userId>/<parentId>', methods = ['GET'])
@SessionManagement('Lead')
def DataReadForLead(userId,parentId):
    try:
        response = Response()        
        result = GoalModule.GetLatestGoalForLead(parentId,userId)
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@GoalAPI.route('/DataRead/Admin/<userId>/<parentId>', methods = ['GET'])
@SessionManagement('Admin')
def DataReadForAdmin(userId,parentId):
    try:
        response = Response()  
        "" + userId # totally not functional      
        result = GoalModule.GetLatestGoalsForAdmins(parentId)
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@GoalAPI.route('/Resource/<parentId>')
@SessionManagement('Admin,Lead,Dev')
def Resource(parentId):
    try:
        response = Response()
        userSessionDetails = GetUserSessionDetails()
        userId = userSessionDetails.get("USER_ID")
        role = userSessionDetails.get("USER_ROLE")
        role = role.lower()
        resource = {}

        if role == 'admin' :
            resource = ResourcesForAdmin(userId,parentId)
        elif role == 'lead' :
            resource = ResourcesForLead(userId,parentId)
        elif role == 'dev':
            resource = ResourcesForDev(userId,parentId)

        response.Data = resource
        response.WasSuccessful = True
    except Exception as ex:
        response.message = str(ex)
        response.WasSuccessful = False 
    return jsonify(response.__dict__)

def ResourcesForDev(userId,parentId):
    resource = {};  
    resource["Fields"] = {
            "ID" : {"type" : "string"},
            "RecordID" : {"type" : "string"},
            "Name" : {"type" : "string"},                
            "Description" : {"type" : "string"},
            "CreatedByName" : {"type" : "string"},
            "AssignedToName" : {"type" : "string"},
            "CreatedBy" : {"type": "string"},
            "CreatedOn": {"type": "date"},
            "Deadline": {"type": "date"},
            "IsStable": {"type": "string"},
            "ReportingStatus": {"type": "string"},
            "Remarks": {"type": "string"},
            "Rating": {"type": "string"},
        }

    resource["Columns"] = [
        {
            "field" : "Name",
            "title" : "Goal Name",
            "width": 200,
        },
        {
            "field" : "Description",
            "title" : "Goal description",
            "width":200,
            "encoded": False,
        },
        {
            "field" : "AssignedToName",
            "title" : "Assigned to",
            "width": 200,
        },
        {
            "title" : "Tasks",
            "template": "# if(data.ReportingStatus != 'ABD' && data.ReportingStatus != 'CMP') { # <button class=\"btn btn-outline-primary\" onclick='LoadTasks(\"#: RecordID #\")'> <i class=\"mdi mdi-clipboard-check\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\"> #: data.ReportingStatus #</p> # } #",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForGoalInGrid(\"#: RecordID #\")'> <i class=\"mdi mdi-table\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForGoalInTimeLine(\"#: RecordID #\")'> <i class=\"mdi mdi-source-branch\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "File submissions",
            "template": "<button class=\"btn btn-outline-secondary\" onclick='LoadReadOnlyFileView(\"#: ID #\")'> <i class=\"mdi mdi-file-multiple\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "field" : "CreatedOn",
            "title" : "Goal creation date",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Deadline",
            "title" : "Goal deadline",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Rating",
            "title" : "Goal rating",
            "template": "<div id=\"ratingBar#: ID #\"></div>",
            "width":200,
        },
        {
            "field" : "Remarks",
            "title" : "Goal remarks",
            "width":200,
        },
        {
            "field" : "CreatedByName",
            "title" : "Goal Created by",
            "width":200,
        }        
    ]

    resource["ReadURL"] = "GoalAPI/DataRead/Dev/" + userId + "/" + parentId
    return resource

def ResourcesForLead(userId,parentId):
    resource = {};  
    resource["Fields"] = {
            "ID" : {"type" : "string"},
            "RecordID" : {"type" : "string"},
            "Name" : {"type" : "string"},                
            "Description" : {"type" : "string"},
            "CreatedByName" : {"type" : "string"},
            "AssignedToName" : {"type" : "string"},
            "CreatedBy" : {"type": "string"},
            "CreatedOn": {"type": "date"},
            "Deadline": {"type": "date"},            
            "IsStable": {"type": "string"},
            "ReportingStatus": {"type": "string"},
            "Remarks": {"type": "string"},
            "Rating": {"type": "string"},
        }
    resource["CreateViewUrl"] = "Goal/Create/" + parentId
    resource["UpdateViewUrl"] = "Goal/Update/" + parentId
    resource["Columns"] = [
        {
            "title" : "Edit",
            "template": "# if(data.ReportingStatus != 'ABD' && data.ReportingStatus != 'CMP') { # <button class=\"btn btn-outline-primary\" onclick='LoadUpdateView(\"#: RecordID #\")'> <i class=\"mdi mdi-grease-pencil\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\"> #: data.ReportingStatus #</p> # } #",
            "excludeFromExport": True,
            "width":80,
        },   
        {
            "title" : "Abandon",
            "template": "# if(data.ReportingStatus != 'ABD' && data.ReportingStatus != 'CMP') { # <button class=\"btn btn-outline-danger\" onclick='AbandonGoal(\"#: ID #\")'> <i class=\"mdi mdi-close\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\">#: data.ReportingStatus #</p> # } #",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "title" : "Complete",
            "template": "# if(data.ReportingStatus != 'ABD' && data.ReportingStatus != 'CMP') { # <button class=\"btn btn-outline-success\" onclick='FinishGoal(\"#: ID #\")'> <i class=\"mdi mdi-check\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\">#: data.ReportingStatus #</p> # } #",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "field" : "Name",
            "title" : "Goal Name",
            "width": 200,
        },
        {
            "field" : "Description",
            "title" : "Goal description",
            "width":200,
            "encoded": False,
        },  
        {
            "field" : "AssignedToName",
            "title" : "Assigned to",
            "width": 200,
        }, 
        {
            "title" : "Tasks",
            "template": "# if(data.ReportingStatus != 'ABD' && data.ReportingStatus != 'CMP') { # <button class=\"btn btn-outline-primary\" onclick='LoadTasks(\"#: RecordID #\")'> <i class=\"mdi mdi-clipboard-check\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\"> #: data.ReportingStatus #</p> # } #",
            "excludeFromExport": True,
            "width":80,
        },  
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForGoalInGrid(\"#: RecordID #\")'> <i class=\"mdi mdi-table\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForGoalInTimeLine(\"#: RecordID #\")'> <i class=\"mdi mdi-source-branch\"> </button>",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "title" : "File submissions",
            "template": "<button class=\"btn btn-outline-warning\" onclick='LoadFileSubmissionView(\"#: ID #\")'> <i class=\"mdi mdi-file-multiple\"> </button>",
            "excludeFromExport": True,
            "width":80,
        },        
        {
            "field" : "CreatedOn",
            "title" : "Goal creation date",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Deadline",
            "title" : "Goal deadline",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Rating",
            "title" : "Goal rating",
            "template": "<div id=\"ratingBar#: ID #\"></div>",
            "width":200,
        },
        {
            "field" : "Remarks",
            "title" : "Goal remarks",
            "width":200,
        },
        {
            "field" : "CreatedByName",
            "title" : "Goal Created by",
            "width":200,
        }        
    ]

    resource["ReadURL"] = "GoalAPI/DataRead/Lead/" + userId + "/" + parentId
    return resource

def ResourcesForAdmin(userId,parentId):        
        resource = {};  
        resource["Fields"] = {
                "ID" : {"type" : "string"},
                "RecordID" : {"type" : "string"},
                "Name" : {"type" : "string"},                
                "Description" : {"type" : "string"},
                "CreatedByName" : {"type" : "string"},
                "AssignedToName" : {"type" : "string"},
                "CreatedBy" : {"type": "string"},
                "CreatedOn": {"type": "date"},
                "Deadline": {"type": "date"},
                "IsStable": {"type": "string"},
                "ReportingStatus": {"type": "string"},
                "Remarks": {"type": "string"},
                "Rating": {"type": "string"},
            }

        resource["Columns"] = [
            {
                "field" : "Name",
                "title" : "Goal Name",
                "width": 200,
            },
            {
                "field" : "ReportingStatus",
                "title" : "Goal status",
                "width": 200,
            },            
            {
                "field" : "CreatedOn",
                "title" : "Goal creation date",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "AssignedToName",
                "title" : "Assigned to",
                "width": 200,
            },
            {
                "field" : "Deadline",
                "title" : "Goal deadline",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "title" : "Tasks",
                "template": "# if(data.ReportingStatus != 'ABD' && data.ReportingStatus != 'CMP') { # <button class=\"btn btn-outline-primary\" onclick='LoadTasks(\"#: RecordID #\")'> <i class=\"mdi mdi-clipboard-check\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\"> #: data.ReportingStatus #</p> # } #",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "field" : "Description",
                "title" : "Goal description",
                "width":200,
                "encoded": False,
            },
            {
                "title" : "Macro Tracking",
                "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForGoalInGrid(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-table\"> </button>",
                "excludeFromExport": True,
                "width":80,
            }, 
            {
                "title" : "Macro Tracking",
                "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForGoalInTimeLine(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-source-branch\"> </button>",
                "excludeFromExport": True,
                "width":80,
            },            
            {
                "title" : "File submissions",
                "template": "<button class=\"btn btn-outline-secondary\" onclick='LoadReadOnlyFileView(\"#: ID #\")'> <i class=\"mdi mdi-file-multiple\"> </i></button>",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "field" : "Rating",
                "title" : "Goal rating",
                "template": "<div id=\"ratingBar#: ID #\"></div>",
                "width":200,
            },
            {
                "field" : "Remarks",
                "title" : "Goal remarks",
                "width":200,
            },
            {
                "field" : "CreatedByName",
                "title" : "Goal Created by",
                "width":200,
            }        
        ]

        resource["ReadURL"] = "GoalAPI/DataRead/Admin/" + userId + "/" + parentId
        return resource

@GoalAPI.route('/CreateGoal/', methods = ['POST'])
@SessionManagement('Lead')
def CreateGoal():
    try:
        milestoneDetails = json.loads(request.data)
        response = Response()
        response.Data = GoalModule.CreateGoal(milestoneDetails)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@GoalAPI.route('/UpdateGoal/', methods = ['POST'])
@SessionManagement('Lead')
def UpdateGoal():    
    try:
        milestoneDetails = json.loads(request.data)
        response = Response()
        response.Data = GoalModule.ParentUpdateGoal(milestoneDetails)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@GoalAPI.route('/FinishGoal/<milestoneChangeID>', methods = ['GET'])
@SessionManagement('Lead')
def FinishGoal(milestoneChangeID):    
    try:
        response = Response()
        userId = GetUserSessionDetails()["USER_ID"]
        response.Data = GoalModule.FinishGoal(milestoneChangeID,userId)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@GoalAPI.route('/AbandonGoal/<milestoneChangeID>', methods = ['GET'])
@SessionManagement('Lead')
def AbandonGoal(milestoneChangeID):    
    try:
        response = Response()
        userId = GetUserSessionDetails()["USER_ID"]
        response.Data = GoalModule.AbandonGoal(milestoneChangeID,userId)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)


