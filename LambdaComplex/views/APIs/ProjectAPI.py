import json
from flask import jsonify, Blueprint, request
from LambdaComplex_DataAccess.ProjectModule import ProjectModule
from SessionManagement import SessionManagement
from LambdaComplex_Entities.Common import Response
from SessionManagement import SessionManagement,GetUserSessionDetails

ProjectAPI = Blueprint("ProjectAPI",__name__)

@ProjectAPI.route('/GetProjects/', methods = ['GET'])
@SessionManagement('Admin')
def GetProjects():
    try:
        userId = GetUserSessionDetails()["USER_ID"]
        response = Response()        
        result = ProjectModule.GetProjectNameID(userId)
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@ProjectAPI.route('/MacroTrackingGridResource/<projectId>')
@SessionManagement('Admin,Lead,Dev')
def MacroTrackingGridResource(projectId):
    try:
        response = Response()
        resource = {}
        resource["ReadURL"] = "ProjectAPI/MacroTrackingGridViewRead/" + projectId
        
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
                "title" : "Project Name",
                "width": 200,
            },
            {
                "field" : "ReportingStatus",
                "title" : "Project status",
                "width": 200,
            },
            {
                "field" : "CreatedOn",
                "title" : "Project creation date",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Deadline",
                "title" : "Project deadline",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Description",
                "title" : "Project description",
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
                "title" : "Project rating",
                "template": "<div id=\"ratingBar#: ID #\"></div>",
                "width":200,
            },
            {
                "field" : "Remarks",
                "title" : "Project remarks",
                "width":200,
            },
            {
                "field" : "CreatedByName",
                "title" : "Project Created by",
                "width":200,
            }        
        ]
        response.Data = resource
        response.WasSuccessful = True
    except Exception as ex:
        response.message = str(ex)
        response.WasSuccessful = False 
    return jsonify(response.__dict__)

@ProjectAPI.route('/MacroTrackingGridViewRead/<projectId>', methods = ['GET'])
@SessionManagement('Admin,Lead,Dev')
def MacroTrackingGridViewRead(projectId):
    try:
        response = Response()        
        result = ProjectModule.GetMacroHistory(projectId)
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@ProjectAPI.route('/MacroTrackingTimeLineRead/<projectId>')
@SessionManagement('Admin,Lead,Dev')
def MacroTrackingTimeLineRead(projectId):
    try:
        response = Response()
        resource = {}
        resource["Data"] = ProjectModule.GetMacroHistory(projectId)
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

@ProjectAPI.route('/MicroTrackingGridResource/<projectId>')
@SessionManagement('Admin,Lead,Dev')
def MicroTrackingGridResource(projectId):
    try:
        response = Response()
        resource = {}
        resource["ReadURL"] = "ProjectAPI/MicroTrackingGridViewRead/" + projectId
        
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
                "title" : "Project Name",
                "width": 200,
            },
            {
                "field" : "ReportingStatus",
                "title" : "Project status",
                "width": 200,
            },
            {
                "field" : "CreatedOn",
                "title" : "Project creation date",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Deadline",
                "title" : "Project deadline",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Description",
                "title" : "Project description",
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
                "title" : "Project rating",
                "template": "<div id=\"ratingBar#: ID #\"></div>",
                "width":200,
            },
            {
                "field" : "Remarks",
                "title" : "Project remarks",
                "width":200,
            },
            {
                "field" : "CreatedByName",
                "title" : "Project Created by",
                "width":200,
            }        
        ]
        response.Data = resource
        response.WasSuccessful = True
    except Exception as ex:
        response.message = str(ex)
        response.WasSuccessful = False 
    return jsonify(response.__dict__)

@ProjectAPI.route('/MicroTrackingGridViewRead/<projectId>', methods = ['GET'])
@SessionManagement('Admin,Lead,Dev')
def MicroTrackingGridViewRead(projectId):
    try:
        response = Response()        
        result = ProjectModule.GetMicroHistory(projectId)
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@ProjectAPI.route('/MicroTrackingTimeLineRead/<projectId>')
@SessionManagement('Admin,Lead,Dev')
def MicroTrackingTimeLineRead(projectId):
    try:
        response = Response()
        resource = {}
        resource["Data"] = ProjectModule.GetMicroHistory(projectId)
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


@ProjectAPI.route('/DataRead/Dev/<userId>', methods = ['GET'])
@SessionManagement('Dev')
def DataReadForDevs(userId):
    try:
        response = Response()        
        result = ProjectModule.GetLatestProjectForDev(userId)
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@ProjectAPI.route('/DataRead/Lead/<userId>', methods = ['GET'])
@SessionManagement('Lead')
def DataReadForLead(userId):
    try:
        response = Response()        
        result = ProjectModule.GetLatestProjectForLead(userId)
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@ProjectAPI.route('/DataRead/Admin/<userId>', methods = ['GET'])
@SessionManagement('Admin')
def DataReadForAdmin(userId):
    try:
        response = Response()        
        result = ProjectModule.GetLatestProjectsForAdmins(userId)
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@ProjectAPI.route('/Resource/')
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

def ResourcesForDev(userId):
    resource = {};  
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
            "title" : "Project Name",
            "width": 200,
        },
        {
            "field" : "Description",
            "title" : "Project description",
            "width":200,
            "encoded": False,
        },
        {
            "title" : "Milestones",
            "template": "# if(data.ReportingStatus != 'ABD' && data.ReportingStatus != 'CMP') { # <button class=\"btn btn-outline-primary\" onclick='LoadMileStones(\"#: RecordID #\")'> <i class=\"mdi mdi-flag-checkered\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\"> #: data.ReportingStatus #</p> # } #",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForProjectInGrid(\"#: RecordID #\")'> <i class=\"mdi mdi-table\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForProjectInTimeLine(\"#: RecordID #\")'> <i class=\"mdi mdi-source-branch\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "File submissions",
            "template": "<button class=\"btn btn-outline-secondary\" onclick='LoadReadOnlyFileView(\"#: ID #\",true,true,divMainPage)'> <i class=\"mdi mdi-file-multiple\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "field" : "CreatedOn",
            "title" : "Project creation date",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Deadline",
            "title" : "Project deadline",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Rating",
            "title" : "Project rating",
            "template": "<div id=\"ratingBar#: ID #\"></div>",
            "width":200,
        },
        {
            "field" : "Remarks",
            "title" : "Project name",
            "width":200,
        },
        {
            "field" : "CreatedByName",
            "title" : "Project Created by",
            "width":200,
        }        
    ]

    resource["ReadURL"] = "ProjectAPI/DataRead/Dev/" + userId
    return resource

def ResourcesForLead(userId):
    resource = {};  
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
            "title" : "Project Name",
            "width": 200,
        },
        {
            "field" : "Description",
            "title" : "Project description",
            "width":200,
            "encoded": False,
        }, 
        {
            "title" : "Milestones",
            "template": "# if(data.ReportingStatus != 'ABD' && data.ReportingStatus != 'CMP') { # <button class=\"btn btn-outline-primary\" onclick='LoadMileStones(\"#: RecordID #\")'> <i class=\"mdi mdi-flag-checkered\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\"> #: data.ReportingStatus #</p> # } #",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForProjectInGrid(\"#: RecordID #\")'> <i class=\"mdi mdi-table\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForProjectInTimeLine(\"#: RecordID #\")'> <i class=\"mdi mdi-source-branch\"> </button>",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "title" : "File submissions",
            "template": "<button class=\"btn btn-outline-secondary\" onclick='LoadReadOnlyFileView(\"#: ID #\",true,true,divMainPage)'> <i class=\"mdi mdi-file-multiple\"> </button>",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "field" : "CreatedOn",
            "title" : "Project creation date",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Deadline",
            "title" : "Project deadline",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Rating",
            "title" : "Project rating",
            "template": "<div id=\"ratingBar#: ID #\"></div>",
            "width":200,
        },
        {
            "field" : "Remarks",
            "title" : "Project name",
            "width":200,
        },
        {
            "field" : "CreatedByName",
            "title" : "Project Created by",
            "width":200,
        }        
    ]

    resource["ReadURL"] = "ProjectAPI/DataRead/Lead/" + userId
    return resource

def ResourcesForAdmin(userId):        
        resource = {};  
        resource["CreateViewUrl"] = "Project/Create/"
        resource["UpdateViewUrl"] = "Project/Update/"
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
                "title" : "Edit",
                "template": "# if(data.ReportingStatus != 'ABD' && data.ReportingStatus != 'CMP') { # <button class=\"btn btn-outline-primary\" onclick='LoadUpdateView(\"#: RecordID #\")'> <i class=\"mdi mdi-grease-pencil\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\"> #: data.ReportingStatus #</p> # } #",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "title" : "Milestones",
                "template": "# if(data.ReportingStatus != 'ABD' && data.ReportingStatus != 'CMP') { # <button class=\"btn btn-outline-primary\" onclick='LoadMileStones(\"#: RecordID #\")'> <i class=\"mdi mdi-flag-checkered\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\"> #: data.ReportingStatus #</p> # } #",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "title" : "Reboot",
                "template": "# if(data.ReportingStatus != 'ABD' && data.ReportingStatus != 'CMP') { # <button class=\"btn btn-outline-danger\" onclick='RebootProject(\"#: RecordID #\")'> <i class=\"mdi mdi-backup-restore\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\"> #: data.ReportingStatus #</p> # } #",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "title" : "Reversion",
                "template": "# if(data.ReportingStatus != 'ABD' && data.ReportingStatus != 'CMP') { # <button class=\"btn btn-outline-warning\" onclick='LoadProjectReversionView(\"#: RecordID #\")'> <i class=\"mdi mdi-undo-variant\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\"> #: data.ReportingStatus #</p> # } #",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "field" : "Name",
                "title" : "Project Name",
                "width": 200,
            },
            {
                "field" : "ReportingStatus",
                "title" : "Project status",
                "width": 200,
            },
            {
                "title" : "Abandon",
                "template": "# if(data.ReportingStatus != 'ABD' && data.ReportingStatus != 'CMP') { # <button class=\"btn btn-outline-danger\" onclick='AbandonProject(\"#: ID #\")'> <i class=\"mdi mdi-close\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\">#: data.ReportingStatus #</p> # } #",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "title" : "Complete",
                "template": "# if(data.ReportingStatus != 'ABD' && data.ReportingStatus != 'CMP') { # <button class=\"btn btn-outline-success\" onclick='FinishProject(\"#: ID #\")'> <i class=\"mdi mdi-check\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\">#: data.ReportingStatus #</p> # } #",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "field" : "CreatedOn",
                "title" : "Project creation date",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Deadline",
                "title" : "Project deadline",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Description",
                "title" : "Project description",
                "width":200,
                "encoded": False,
            },
            {
                "title" : "Macro Tracking",
                "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForProjectInGrid(\"#: RecordID #\")'> <i class=\"mdi mdi-table\"> </button>",
                "excludeFromExport": True,
                "width":80,
            }, 
            {
                "title" : "Macro Tracking",
                "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForProjectInTimeLine(\"#: RecordID #\")'> <i class=\"mdi mdi-source-branch\"> </button>",
                "excludeFromExport": True,
                "width":80,
            }, 
            {
                "title" : "Micro Tracking",
                "template": "<button class=\"btn btn-outline-secondary\" onclick='DisplayMicroTrackingForProjectInGrid(\"#: RecordID #\")'> <i class=\"mdi mdi-table\"> </button>",
                "excludeFromExport": True,
                "width":80,
            }, 
            {
                "title" : "Micro Tracking",
                "template": "<button class=\"btn btn-outline-secondary\" onclick='DisplayMicroTrackingForProjectInTimeLine(\"#: RecordID #\")'> <i class=\"mdi mdi-source-branch\"> </button>",
                "excludeFromExport": True,
                "width":80,
            },                         
            {
                "title" : "File submissions",
                "template": "# if(data.ReportingStatus != 'ABD' && data.ReportingStatus != 'CMP') { # <button class=\"btn btn-outline-warning\" onclick='LoadFileSubmissionView(\"#: ID #\",true,true,divMainPage)'> <i class=\"mdi mdi-file-multiple\"></i> </button> # } else { # <button class=\"btn btn-outline-secondary\" onclick='LoadReadOnlyFileView(\"#: ID #\",true,true,divMainPage)'> <i class=\"mdi mdi-file-multiple\"> </i></button> # } #",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "field" : "Rating",
                "title" : "Project rating",
                "template": "<div id=\"ratingBar#: ID #\"></div>",
                "width":200,
            },
            {
                "field" : "Remarks",
                "title" : "Project remarks",
                "width":200,
            },
            {
                "field" : "CreatedByName",
                "title" : "Project Created by",
                "width":200,
            }        
        ]

        resource["ReadURL"] = "ProjectAPI/DataRead/Admin/" + userId
        return resource

@ProjectAPI.route('/CreateProject/', methods = ['POST'])
@SessionManagement('Admin')
def CreateProject():
    try:
        projectDetails = json.loads(request.data)
        response = Response()
        response.Data = ProjectModule.CreateProject(projectDetails)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@ProjectAPI.route('/UpdateProject/', methods = ['POST'])
@SessionManagement('Admin')
def UpdateProject():    
    try:
        projectDetails = json.loads(request.data)
        response = Response()
        response.Data = ProjectModule.ParentUpdateProject(projectDetails)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@ProjectAPI.route('/FinishProject/<projectChangeID>', methods = ['GET'])
@SessionManagement('Admin')
def FinishProject(projectChangeID):    
    try:
        response = Response()
        userId = GetUserSessionDetails()["USER_ID"]
        response.Data = ProjectModule.FinishProject(projectChangeID,userId)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@ProjectAPI.route('/AbandonProject/<projectChangeID>', methods = ['GET'])
@SessionManagement('Admin')
def AbandonProject(projectChangeID):    
    try:
        response = Response()
        userId = GetUserSessionDetails()["USER_ID"]
        response.Data = ProjectModule.AbandonProject(projectChangeID,userId)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)


@ProjectAPI.route('/ReversionProject/<projectChangeID>', methods = ['GET'])
@SessionManagement('Admin')
def Reversion(projectChangeID):    
    try:
        response = Response()
        userId = GetUserSessionDetails()["USER_ID"]
        response.Data = ProjectModule.Reversion(projectChangeID,userId)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@ProjectAPI.route('/RebootProject/<projectId>', methods = ['GET'])
@SessionManagement('Admin')
def Reboot(projectId):    
    try:
        response = Response()
        userId = GetUserSessionDetails()["USER_ID"]
        response.Data = ProjectModule.Reboot(projectId,userId)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@ProjectAPI.route('/ProjectReversionGridViewResource/<projectId>')
@SessionManagement('Admin')
def ProjectReversionGridViewResource(projectId):
    try:
        response = Response()
        resource = {}
        resource["ReadURL"] = "ProjectAPI/MacroTrackingGridViewRead/" + projectId
        
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
                "title" : "Project Name",
                "width": 200,
            },
            {
                "field" : "ReportingStatus",
                "title" : "Project status",
                "width": 200,
            },
            {
                "field" : "CreatedOn",
                "title" : "Project creation date",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Deadline",
                "title" : "Project deadline",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Description",
                "title" : "Project description",
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
                "title" : "Revert project",
                "template": "<button class=\"btn btn-outline-danger\" onclick='ReversionProject(\"#: ID #\")'> <i class=\"mdi mdi-undo\"> </i></button>",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "field" : "Rating",
                "title" : "Project rating",
                "template": "<div id=\"ratingBar#: ID #\"></div>",
                "width":200,
            },
            {
                "field" : "Remarks",
                "title" : "Project remarks",
                "width":200,
            },
            {
                "field" : "CreatedByName",
                "title" : "Project Created by",
                "width":200,
            }        
        ]
        response.Data = resource
        response.WasSuccessful = True
    except Exception as ex:
        response.message = str(ex)
        response.WasSuccessful = False 
    return jsonify(response.__dict__)


@ProjectAPI.route('/WorkHierarchyResource/')
@SessionManagement('Admin,Lead,Dev')
def WorkHierarchyResource():
    try:
        response = Response()
        userSessionDetails = GetUserSessionDetails()
        userId = userSessionDetails.get("USER_ID")
        role = userSessionDetails.get("USER_ROLE")
        role = role.lower()
        resource = {}

        if role == 'admin' :
            resource = WorkHierarchyResourcesForAdmin(userId)
        elif role == 'lead' :
            resource = WorkHierarchyResourcesForLead(userId)
        elif role == 'dev':
            resource = WorkHierarchyResourcesForDev(userId)

        response.Data = resource
        response.WasSuccessful = True
    except Exception as ex:
        response.message = str(ex)
        response.WasSuccessful = False 
    return jsonify(response.__dict__)

def WorkHierarchyResourcesForDev(userId):
    resource = {};  
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
            "title" : "Project Name",
            "width": 200,
        },
        {
            "field" : "Description",
            "title" : "Project description",
            "width":200,
            "encoded": False,
        },
        {
            "title" : "Milestones",
            "template": "<button class=\"btn btn-outline-primary\" onclick='LoadMileStonesHierarchy(\"#: RecordID #\")'> <i class=\"mdi mdi-flag-checkered\"></i> </button>",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForProjectInGrid(\"#: RecordID #\")'> <i class=\"mdi mdi-table\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForProjectInTimeLine(\"#: RecordID #\")'> <i class=\"mdi mdi-source-branch\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "File submissions",
            "template": "<button class=\"btn btn-outline-secondary\" onclick='LoadReadOnlyFileView(\"#: ID #\",true,true,divMainPage)'> <i class=\"mdi mdi-file-multiple\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "field" : "CreatedOn",
            "title" : "Project creation date",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Deadline",
            "title" : "Project deadline",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Rating",
            "title" : "Project rating",
            "template": "<div id=\"ratingBar#: ID #\"></div>",
            "width":200,
        },
        {
            "field" : "Remarks",
            "title" : "Project name",
            "width":200,
        },
        {
            "field" : "CreatedByName",
            "title" : "Project Created by",
            "width":200,
        }        
    ]

    resource["ReadURL"] = "ProjectAPI/DataRead/Dev/" + userId
    return resource

def WorkHierarchyResourcesForLead(userId):
    resource = {};  
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
            "title" : "Project Name",
            "width": 200,
        },
        {
            "field" : "Description",
            "title" : "Project description",
            "width":200,
            "encoded": False,
        },
        {
            "title" : "Milestones",
            "template": "<button class=\"btn btn-outline-primary\" onclick='LoadMileStonesHierarchy(\"#: RecordID #\")'> <i class=\"mdi mdi-flag-checkered\"></i> </button>",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForProjectInGrid(\"#: RecordID #\")'> <i class=\"mdi mdi-table\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForProjectInTimeLine(\"#: RecordID #\")'> <i class=\"mdi mdi-source-branch\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "File submissions",
            "template": "<button class=\"btn btn-outline-secondary\" onclick='LoadReadOnlyFileView(\"#: ID #\",true,true,divMainPage)'> <i class=\"mdi mdi-file-multiple\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "field" : "CreatedOn",
            "title" : "Project creation date",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Deadline",
            "title" : "Project deadline",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Rating",
            "title" : "Project rating",
            "template": "<div id=\"ratingBar#: ID #\"></div>",
            "width":200,
        },
        {
            "field" : "Remarks",
            "title" : "Project name",
            "width":200,
        },
        {
            "field" : "CreatedByName",
            "title" : "Project Created by",
            "width":200,
        }           
    ]

    resource["ReadURL"] = "ProjectAPI/DataRead/Lead/" + userId
    return resource

def WorkHierarchyResourcesForAdmin(userId):        
        resource = {};  
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
                "title" : "Project Name",
                "width": 200,
            },
            {
                "field" : "Description",
                "title" : "Project description",
                "width":200,
                "encoded": False,
            },
            {
                "title" : "Milestones",
                "template": "<button class=\"btn btn-outline-primary\" onclick='LoadMileStonesHierarchy(\"#: RecordID #\")'> <i class=\"mdi mdi-flag-checkered\"></i> </button>",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "title" : "Macro Tracking",
                "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForProjectInGrid(\"#: RecordID #\")'> <i class=\"mdi mdi-table\"> </button>",
                "excludeFromExport": True,
                "width":80,
            }, 
            {
                "title" : "Macro Tracking",
                "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForProjectInTimeLine(\"#: RecordID #\")'> <i class=\"mdi mdi-source-branch\"> </button>",
                "excludeFromExport": True,
                "width":80,
            }, 
            {
                "title" : "File submissions",
                "template": "<button class=\"btn btn-outline-secondary\" onclick='LoadReadOnlyFileView(\"#: ID #\",true,true,divMainPage)'> <i class=\"mdi mdi-file-multiple\"> </button>",
                "excludeFromExport": True,
                "width":80,
            }, 
            {
                "field" : "CreatedOn",
                "title" : "Project creation date",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Deadline",
                "title" : "Project deadline",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Rating",
                "title" : "Project rating",
                "template": "<div id=\"ratingBar#: ID #\"></div>",
                "width":200,
            },
            {
                "field" : "Remarks",
                "title" : "Project name",
                "width":200,
            },
            {
                "field" : "CreatedByName",
                "title" : "Project Created by",
                "width":200,
            }           
        ]

        resource["ReadURL"] = "ProjectAPI/DataRead/Admin/" + userId
        return resource
