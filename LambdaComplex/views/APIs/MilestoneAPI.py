import json
from flask import jsonify, Blueprint, request
from LambdaComplex_DataAccess.MilestoneModule import MilestoneModule
from SessionManagement import SessionManagement
from LambdaComplex_Entities.Common import Response
from SessionManagement import SessionManagement,GetUserSessionDetails

MilestoneAPI = Blueprint("MilestoneAPI",__name__)

@MilestoneAPI.route('/Resource/<projectId>')
@SessionManagement('Admin,Lead,Dev')
def Resource(projectId):
    try:
        response = Response()
        userSessionDetails = GetUserSessionDetails()
        userId = userSessionDetails.get("USER_ID")
        role = userSessionDetails.get("USER_ROLE")
        role = role.lower()
        resource = {}

        if role == 'admin' :
            resource = ResourcesForAdmin(userId,projectId)
        elif role == 'lead' :
            resource = ResourcesForLead(userId,projectId)
        elif role == 'dev':
            resource = ResourcesForDev(userId,projectId)

        response.Data = resource
        response.WasSuccessful = True
    except Exception as ex:
        response.message = str(ex)
        response.WasSuccessful = False 
    return jsonify(response.__dict__)

def ResourcesForDev(userId,projectId):
    resource = {};  
    resource["Fields"] = {
            "ID" : {"type" : "string"},
            "RecordID" : {"type" : "string"},
            "Name" : {"type" : "string"},                
            "Description" : {"type" : "string"},
            "CreatedByName" : {"type" : "string"},
            "AssignedToName" : {"type" : "string"},
            "ParentID" : {"type" : "string"},
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
            "title" : "Milestone Name",
            "width": 200,
        },
        {
            "field" : "Description",
            "title" : "Milestone description",
            "width":200,
            "encoded": False,
        },
        {
            "field" : "AssignedToName",
            "title" : "Assigned to",
            "width":200,
        },
        {
            "title" : "File submissions",
            "template": "<button class=\"btn btn-outline-warning\" onclick='LoadFileSubmissionView(\"#: ID #\",true,true,divMainPage)'> <i class=\"mdi mdi-file-multiple\"></i> </button>",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForMilestoneInGrid(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-table\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForMilestoneInTimeLine(\"#: RecordID #\")'> <i class=\"mdi mdi-source-branch\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Micro Tracking",
            "template": "<button class=\"btn btn-outline-secondary\" onclick='DisplayMicroTrackingForMilestoneInGrid(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-table\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Micro Tracking",
            "template": "<button class=\"btn btn-outline-secondary\" onclick='DisplayMicroTrackingForMilestoneInTimeLine(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-source-branch\"> </button>",
            "excludeFromExport": True,
            "width":80,
        },    
        {
            "field" : "CreatedOn",
            "title" : "Milestone creation date",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Deadline",
            "title" : "Milestone deadline",
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
            "title" : "Milestone name",
            "width":200,
        },
        {
            "field" : "CreatedByName",
            "title" : "Milestone Created by",
            "width":200,
        }        
    ]

    resource["ReadURL"] = "MilestoneAPI/DataRead/Dev/" + userId + "/" + projectId
    return resource

def ResourcesForLead(userId,projectId):
    resource = {};  
    resource["UpdateViewUrl"] = "Milestone/ChildUpdate/" + projectId
    resource["ReadURL"] = "MilestoneAPI/DataRead/Lead/" + userId + "/" + projectId
    resource["Fields"] = {
        "ID" : {"type" : "string"},
        "RecordID" : {"type" : "string"},
        "Name" : {"type" : "string"},                
        "Description" : {"type" : "string"},
        "CreatedByName" : {"type" : "string"},
        "AssignedToName" : {"type" : "string"},
        "ParentID" : {"type" : "string"},
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
            "title" : "Edit ",
            "template": "# if(data.ReportingStatus == 'PAR') { # <button class=\"btn btn-outline-primary\" onclick='LoadUpdateView(\"#: RecordID #\")'> <i class=\"mdi mdi-grease-pencil\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\"> #: data.ReportingStatus #</p> # } #",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "field" : "Name",
            "title" : "Milestone Name",
            "width": 200,
        },
        {
            "field" : "ReportingStatus",
            "title" : "Milestone status",
            "width": 200,
        },   
        {
            "field" : "Description",
            "title" : "Milestone description",
            "width":200,
            "encoded": False,
        },        
        {
            "field" : "AssignedToName",
            "title" : "Assigned to",
            "width":200,
        },
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForMilestoneInGrid(\"#: RecordID #\")'> <i class=\"mdi mdi-table\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForMilestoneInTimeLine(\"#: RecordID #\")'> <i class=\"mdi mdi-source-branch\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Micro Tracking",
            "template": "<button class=\"btn btn-outline-secondary\" onclick='DisplayMicroTrackingForMilestoneInGrid(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-table\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Micro Tracking",
            "template": "<button class=\"btn btn-outline-secondary\" onclick='DisplayMicroTrackingForMilestoneInTimeLine(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-source-branch\"> </button>",
            "excludeFromExport": True,
            "width":80,
        },   
        {
            "title" : "File submissions",
            "template": "# if(data.ReportingStatus == 'PAR') { # <button class=\"btn btn-outline-secondary\" onclick='LoadReadOnlyFileView(\"#: ID #\",true,true,divMainPage)'> <i class=\"mdi mdi-file-multiple\"> </button> # } else { # <button class=\"btn btn-outline-warning\" onclick='LoadFileSubmissionView(\"#: ID #\",true,true,divMainPage)'> <i class=\"mdi mdi-file-multiple\"></i> </button> # } #",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "field" : "CreatedOn",
            "title" : "Milestone creation date",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Deadline",
            "title" : "Milestone deadline",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Rating",
            "title" : "Milestone rating",
            "template": "<div id=\"ratingBar#: ID #\"></div>",
            "width":200,
        },
        {
            "field" : "Remarks",
            "title" : "Milestone name",
            "width":200,
        },
        {
            "field" : "CreatedByName",
            "title" : "Milestone Created by",
            "width":200,
        }        
    ]

    return resource

def ResourcesForAdmin(userId,projectId):        
        resource = {};  
        resource["CreateViewUrl"] = "Milestone/Create/" + projectId
        resource["UpdateViewUrl"] = "Milestone/Update/" + projectId
        resource["Fields"] = {
                "ID" : {"type" : "string"},
                "RecordID" : {"type" : "string"},
                "Name" : {"type" : "string"},                
                "Description" : {"type" : "string"},
                "CreatedByName" : {"type" : "string"},
                "AssignedToName" : {"type" : "string"},
                "ParentID" : {"type" : "string"},
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
                "template": "# if(data.ReportingStatus == 'PAR' || data.ReportingStatus == 'INITIAL') { # <button class=\"btn btn-outline-primary\" onclick='LoadUpdateView(\"#: RecordID #\")'> <i class=\"mdi mdi-grease-pencil\"></i> </button> # } else if(ReportingStatus == 'CHR' || ReportingStatus == 'PGR') { # <button class=\"btn btn-outline-success\" onclick='ApproveMilestoneEdit(\"#: ID #\")'> <i class=\"mdi mdi-thumb-up\"></i> </button> <button class=\"btn btn-outline-danger\" onclick='RejectMilestoneEdit(\"#: ID #\")'> <i class=\"mdi mdi-thumb-down\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\"> #: data.ReportingStatus #</p> # } #",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "field" : "Name",
                "title" : "Milestone Name",
                "width": 200,
            },
            {
                "field" : "ReportingStatus",
                "title" : "Milestone status",
                "width": 200,
            },            
            {
                "field" : "AssignedToName",
                "title" : "Assigned to",
                "width":200,
            },
            {
                "field" : "CreatedOn",
                "title" : "Milestone creation date",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Deadline",
                "title" : "Milestone deadline",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Description",
                "title" : "Milestone description",
                "width":200,
                "encoded": False,
            },  
            {
                "title" : "Macro Tracking",
                "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForMilestoneInGrid(\"#: RecordID #\")'> <i class=\"mdi mdi-table\"> </button>",
                "excludeFromExport": True,
                "width":80,
            }, 
            {
                "title" : "Macro Tracking",
                "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForMilestoneInTimeLine(\"#: RecordID #\")'> <i class=\"mdi mdi-source-branch\"> </button>",
                "excludeFromExport": True,
                "width":80,
            }, 
            {
                "title" : "Micro Tracking",
                "template": "<button class=\"btn btn-outline-secondary\" onclick='DisplayMicroTrackingForMilestoneInGrid(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-table\"> </button>",
                "excludeFromExport": True,
                "width":80,
            }, 
            {
                "title" : "Micro Tracking",
                "template": "<button class=\"btn btn-outline-secondary\" onclick='DisplayMicroTrackingForMilestoneInTimeLine(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-source-branch\"> </button>",
                "excludeFromExport": True,
                "width":80,
            },         
            {
                "title" : "File submissions",
                "template": "# if(data.ReportingStatus == 'PAR' || data.ReportingStatus == 'INITIAL') { # <button class=\"btn btn-outline-warning\" onclick='LoadFileSubmissionView(\"#: ID #\",true,true,divMainPage)'> <i class=\"mdi mdi-file-multiple\"></i> </button> # } else { # <button class=\"btn btn-outline-secondary\" onclick='LoadReadOnlyFileView(\"#: ID #\",true,true,divMainPage)'> <i class=\"mdi mdi-file-multiple\"> </i></button> # } #",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "title" : "Abandon",
                "template": "# if(data.ReportingStatus == 'PAR' || data.ReportingStatus == 'INITIAL') { # <button class=\"btn btn-outline-danger\" onclick='AbandonMilestone(\"#: ID #\")'> <i class=\"mdi mdi-close\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\">#: data.ReportingStatus #</p> # } #",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "title" : "Complete",
                "template": "# if(data.ReportingStatus == 'PAR' || data.ReportingStatus == 'INITIAL') { # <button class=\"btn btn-outline-success\" onclick='FinishMilestone(\"#: ID #\")'> <i class=\"mdi mdi-check\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\">#: data.ReportingStatus #</p> # } #",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "field" : "Rating",
                "title" : "Milestone rating",
                "template": "<div id=\"ratingBar#: ID #\"></div>",
                "width":200,
            },
            {
                "field" : "Remarks",
                "title" : "Milestone remarks",
                "width":200,
            },
            {
                "field" : "CreatedByName",
                "title" : "Milestone Created by",
                "width":200,
            }        
        ]

        resource["ReadURL"] = "MilestoneAPI/DataRead/Admin/" + userId + "/" + projectId
        return resource

@MilestoneAPI.route('/DataRead/Dev/<userId>/<projectId>', methods = ['GET'])
@SessionManagement('Dev')
def DataReadForDevs(userId,projectId):
    try:
        response = Response()        
        result = MilestoneModule.GetLatestMilestoneForDev(projectId,userId)
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@MilestoneAPI.route('/DataRead/Lead/<userId>/<projectId>', methods = ['GET'])
@SessionManagement('Lead')
def DataReadForLead(userId,projectId):
    try:
        response = Response()        
        result = MilestoneModule.GetLatestMilestoneForLead(projectId,userId)
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@MilestoneAPI.route('/DataRead/Admin/<userId>/<projectId>', methods = ['GET'])
@SessionManagement('Admin')
def DataReadForAdmin(userId,projectId):
    try:
        response = Response()        
        result = MilestoneModule.GetLatestMilestonesForAdmins(projectId,userId)
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)


@MilestoneAPI.route('/CreateMilestone/', methods = ['POST'])
@SessionManagement('Admin')
def CreateMilestone():
    try:
        projectDetails = json.loads(request.data)
        response = Response()
        response.Data = MilestoneModule.CreateMilestone(projectDetails)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@MilestoneAPI.route('/UpdateMilestone/', methods = ['POST'])
@SessionManagement('Admin')
def UpdateMilestone():    
    try:
        projectDetails = json.loads(request.data)
        response = Response()
        response.Data = MilestoneModule.ParentUpdateMilestone(projectDetails)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@MilestoneAPI.route('/ChildUpdateMilestoneCHR/', methods = ['POST'])
@SessionManagement('Lead')
def CHRUpdateMilestone():    
    try:
        projectDetails = json.loads(request.data)
        response = Response()
        response.Data = MilestoneModule.ChildCHRUpdateMilestone(projectDetails)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@MilestoneAPI.route('/ChildUpdateMilestonePGR/', methods = ['POST'])
@SessionManagement('Lead')
def PGRUpdateMilestone():        
    try:
        projectDetails = json.loads(request.data)
        response = Response()
        response.Data = MilestoneModule.ChildPGRUpdateMilestone(projectDetails)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@MilestoneAPI.route('/FinishMilestone/<milestoneChangeId>', methods = ['GET'])
@SessionManagement('Admin')
def FinishMilestone(milestoneChangeId):    
    try:
        response = Response()
        userId = GetUserSessionDetails()["USER_ID"]
        response.Data = MilestoneModule.FinishMilestone(milestoneChangeId,userId)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@MilestoneAPI.route('/AbandonAbandon/<milestoneChangeId>', methods = ['GET'])
@SessionManagement('Admin')
def AbandonMilestone(milestoneChangeId):    
    try:
        response = Response()
        userId = GetUserSessionDetails()["USER_ID"]
        response.Data = MilestoneModule.AbandonMilestone(milestoneChangeId,userId)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@MilestoneAPI.route('/AcceptChangesMilestone/<milestoneChangeId>', methods = ['GET'])
@SessionManagement('Admin')
def AcceptChangesMilestone(milestoneChangeId):    
    try:
        response = Response()
        userId = GetUserSessionDetails()["USER_ID"]
        response.Data = MilestoneModule.AcceptChangesMilestone(milestoneChangeId,userId)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@MilestoneAPI.route('/RejectChangesMilestone/<milestoneChangeId>', methods = ['GET'])
@SessionManagement('Admin')
def RejectChangesMilestone(milestoneChangeId):    
    try:
        response = Response()
        userId = GetUserSessionDetails()["USER_ID"]
        response.Data = MilestoneModule.RejectChangesMilestone(milestoneChangeId,userId)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)


@MilestoneAPI.route('/MacroTrackingGridResource/<milestoneId>')
@SessionManagement('Admin,Lead,Dev')
def MacroTrackingGridResource(milestoneId):
    try:
        response = Response()
        resource = {}
        resource["ReadURL"] = "MilestoneAPI/MacroTrackingGridViewRead/" + milestoneId
        
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
                "AssignedToName" : {"type": "string"},
                "ProjectName": {"type":"string"},
            }

        resource["Columns"] = [
            {
                "field" : "Name",
                "title" : "Milestone Name",
                "width": 200,
            },               
            {
                "field" : "ProjectName",
                "title" : "Project name",
                "width":200,
            },
            {
                "field" : "ReportingStatus",
                "title" : "Milestone status",
                "width": 200,
            },
            {
                "field" : "CreatedOn",
                "title" : "Miklestone creation date",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Deadline",
                "title" : "Milestone deadline",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Description",
                "title" : "Milestone description",
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
                "title" : "Milestone rating",
                "template": "<div id=\"ratingBar#: ID #\"></div>",
                "width":200,
            },
            {
                "field" : "Remarks",
                "title" : "Milestine remarks",
                "width":200,
            },
            {
                "field" : "CreatedByName",
                "title" : "Milestone Created by",
                "width":200,
            },      
            {
                "field" : "AssignedTo",
                "title" : "Milestone Assigned to",
                "width":200,
            }
        ]
        response.Data = resource
        response.WasSuccessful = True
    except Exception as ex:
        response.message = str(ex)
        response.WasSuccessful = False 
    return jsonify(response.__dict__)

@MilestoneAPI.route('/MicroTrackingGridResource/<milestoneId>')
@SessionManagement('Admin,Lead,Dev')
def MicroTrackingGridResource(milestoneId):
    try:
        response = Response()
        resource = {}
        resource["ReadURL"] = "MilestoneAPI/MicroTrackingGridViewRead/" + milestoneId
        
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
                "AssignedToName" : {"type": "string"},
                "ProjectName": {"type":"string"},
            }

        resource["Columns"] = [
            {
                "field" : "Name",
                "title" : "Milestone Name",
                "width": 200,
            },               
            {
                "field" : "ProjectName",
                "title" : "Project name",
                "width":200,
            },
            {
                "field" : "ReportingStatus",
                "title" : "Milestone status",
                "width": 200,
            },
            {
                "field" : "CreatedOn",
                "title" : "Miklestone creation date",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Deadline",
                "title" : "Milestone deadline",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Description",
                "title" : "Milestone description",
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
                "title" : "Milestone rating",
                "template": "<div id=\"ratingBar#: ID #\"></div>",
                "width":200,
            },
            {
                "field" : "Remarks",
                "title" : "Milestine remarks",
                "width":200,
            },
            {
                "field" : "CreatedByName",
                "title" : "Milestone Created by",
                "width":200,
            },      
            {
                "field" : "AssignedTo",
                "title" : "Milestone Assigned to",
                "width":200,
            }
        ]
        response.Data = resource
        response.WasSuccessful = True
    except Exception as ex:
        response.message = str(ex)
        response.WasSuccessful = False 
    return jsonify(response.__dict__)



@MilestoneAPI.route('/MacroTrackingGridViewRead/<milestoneId>', methods = ['GET'])
@SessionManagement('Admin,Lead,Dev')
def MacroTrackingGridViewRead(milestoneId):
    try:
        response = Response()        
        result = MilestoneModule.GetMacroHistory(milestoneId)
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@MilestoneAPI.route('/MacroTrackingTimeLineRead/<milestoneId>')
@SessionManagement('Admin,Lead,Dev')
def MacroTrackingTimeLineRead(milestoneId):
    try:
        response = Response()
        resource = {}
        resource["Data"] = MilestoneModule.GetMacroHistory(milestoneId)
        resource["Mappings"] = {
            "time" : "CreatedOn",
            "header" : "ReportingStatus",
            "h1Body" : "CreatedByName",
            "paraBody" : "Remarks",
            "footer": "CreatedOn" 
        }
        response.Data = resource 
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@MilestoneAPI.route('/MicroTrackingGridViewRead/<milestoneId>', methods = ['GET'])
@SessionManagement('Admin,Lead,Dev')
def MicroTrackingGridViewRead(milestoneId):
    try:
        response = Response()        
        result = MilestoneModule.GetMicroHistory(milestoneId)
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@MilestoneAPI.route('/MicroTrackingTimeLineRead/<milestoneId>')
@SessionManagement('Admin,Lead,Dev')
def MicroTrackingTimeLineRead(milestoneId):
    try:
        response = Response()
        resource = {}
        resource["Data"] = MilestoneModule.GetMicroHistory(milestoneId)
        resource["Mappings"] = {
            "time" : "CreatedOn",
            "header" : "ReportingStatus",
            "h1Body" : "CreatedByName",
            "paraBody" : "Remarks",
            "footer": "CreatedOn" 
        }
        response.Data = resource 
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)
