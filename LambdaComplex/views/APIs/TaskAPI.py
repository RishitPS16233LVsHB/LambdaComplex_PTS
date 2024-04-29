import json
from flask import jsonify, Blueprint, request
from LambdaComplex_DataAccess.TaskModule import TaskModule
from SessionManagement import SessionManagement
from LambdaComplex_Entities.Common import Response
from SessionManagement import SessionManagement,GetUserSessionDetails

TaskAPI = Blueprint("TaskAPI",__name__)

@TaskAPI.route('/Resource/<goalId>')
@SessionManagement('Admin,Lead,Dev')
def Resource(goalId):
    try:
        response = Response()
        userSessionDetails = GetUserSessionDetails()
        userId = userSessionDetails.get("USER_ID")
        role = userSessionDetails.get("USER_ROLE")
        role = role.lower()
        resource = {}

        if role == 'admin' :
            resource = ResourcesForAdmin(userId,goalId)
        elif role == 'lead' :
            resource = ResourcesForLead(userId,goalId)
        elif role == 'dev':
            resource = ResourcesForDev(userId,goalId)

        response.Data = resource
        response.WasSuccessful = True
    except Exception as ex:
        response.message = str(ex)
        response.WasSuccessful = False 
    return jsonify(response.__dict__)

def ResourcesForAdmin(userId,goalId):
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
            "title" : "Task Name",
            "width": 200,
        },
        {
            "field" : "Description",
            "title" : "Task description",
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
            "template": "<button class=\"btn btn-outline-secondary\" onclick='LoadReadOnlyFileView(\"#: ID #\")'> <i class=\"mdi mdi-file-multiple\"></i> </button>",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForTaskInGrid(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-table\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForTaskInTimeLine(\"#: RecordID #\")'> <i class=\"mdi mdi-source-branch\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Micro Tracking",
            "template": "<button class=\"btn btn-outline-secondary\" onclick='DisplayMicroTrackingForTaskInGrid(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-table\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Micro Tracking",
            "template": "<button class=\"btn btn-outline-secondary\" onclick='DisplayMicroTrackingForTaskInTimeLine(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-source-branch\"> </button>",
            "excludeFromExport": True,
            "width":80,
        },    
        {
            "field" : "CreatedOn",
            "title" : "Task creation date",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Deadline",
            "title" : "Task deadline",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Rating",
            "title" : "Task rating",
            "template": "<div id=\"ratingBar#: ID #\"></div>",
            "width":200,
        },
        {
            "field" : "Remarks",
            "title" : "Task name",
            "width":200,
        },
        {
            "field" : "CreatedByName",
            "title" : "Task Created by",
            "width":200,
        }        
    ]

    resource["ReadURL"] = "TaskAPI/DataRead/Admin/" + userId + "/" + goalId
    return resource

def ResourcesForDev(userId,goalId):
    resource = {};  
    resource["UpdateViewUrl"] = "Task/ChildUpdate/" + goalId
    resource["ReadURL"] = "TaskAPI/DataRead/Dev/" + userId + "/" + goalId
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
            "template": "# if(data.ReportingStatus == 'PAR' || data.ReportingStatus == 'INITIAL') { # <button class=\"btn btn-outline-primary\" onclick='LoadUpdateView(\"#: RecordID #\")'> <i class=\"mdi mdi-grease-pencil\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\"> #: data.ReportingStatus #</p> # } #",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "field" : "Name",
            "title" : "Task Name",
            "width": 200,
        },
        {
            "field" : "ReportingStatus",
            "title" : "Task status",
            "width": 200,
        },   
        {
            "field" : "Description",
            "title" : "Task description",
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
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForTaskInGrid(\"#: RecordID #\")'> <i class=\"mdi mdi-table\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForTaskInTimeLine(\"#: RecordID #\")'> <i class=\"mdi mdi-source-branch\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Micro Tracking",
            "template": "<button class=\"btn btn-outline-secondary\" onclick='DisplayMicroTrackingForTaskInGrid(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-table\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Micro Tracking",
            "template": "<button class=\"btn btn-outline-secondary\" onclick='DisplayMicroTrackingForTaskInTimeLine(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-source-branch\"> </button>",
            "excludeFromExport": True,
            "width":80,
        },   
        {
            "title" : "File submissions",
            "template": "# if(data.ReportingStatus != 'CHR' && data.ReportingStatus != 'PGR') { # <button class=\"btn btn-outline-secondary\" onclick='LoadReadOnlyFileView(\"#: ID #\",true,true,divMainPage)'> <i class=\"mdi mdi-file-multiple\"></i> </button> # } else { # <button class=\"btn btn-outline-warning\" onclick='LoadFileSubmissionView(\"#: ID #\",true,true,divMainPage)'> <i class=\"mdi mdi-file-multiple\"></i> </button> # } #",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "field" : "CreatedOn",
            "title" : "Task creation date",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Deadline",
            "title" : "Task deadline",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Rating",
            "title" : "Task rating",
            "template": "<div id=\"ratingBar#: ID #\"></div>",
            "width":200,
        },
        {
            "field" : "Remarks",
            "title" : "Task name",
            "width":200,
        },
        {
            "field" : "CreatedByName",
            "title" : "Task Created by",
            "width":200,
        }        
    ]

    return resource

def ResourcesForLead(userId,goalId):        
        resource = {};  
        resource["CreateViewUrl"] = "Task/Create/" + goalId
        resource["UpdateViewUrl"] = "Task/Update/" + goalId
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
                "template": "# if(data.ReportingStatus == 'PAR' || data.ReportingStatus == 'INITIAL') { # <button class=\"btn btn-outline-primary\" onclick='LoadUpdateView(\"#: RecordID #\")'> <i class=\"mdi mdi-grease-pencil\"></i> </button> # } else if(ReportingStatus == 'CHR' || ReportingStatus == 'PGR') { # <button class=\"btn btn-outline-success\" onclick='ApproveTaskEdit(\"#: ID #\")'> <i class=\"mdi mdi-thumb-up\"></i> </button> <button class=\"btn btn-outline-danger\" onclick='RejectTaskEdit(\"#: ID #\")'> <i class=\"mdi mdi-thumb-down\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\"> #: data.ReportingStatus #</p> # } #",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "field" : "Name",
                "title" : "Task Name",
                "width": 200,
            },
            {
                "field" : "ReportingStatus",
                "title" : "Task status",
                "width": 200,
            },
            {
                "title" : "Revive",
                "template": "# if(data.ReportingStatus == 'ABD' || data.ReportingStatus == 'CMP') { # <button class=\"btn btn-outline-success\" onclick='ReviveTask(\"#: ID #\")'> <i class=\"mdi mdi-book-open-page-variant\"></i> </button> # } #",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "title" : "Reboot",
                "template": "# if(data.ReportingStatus != 'ABD' && data.ReportingStatus != 'CMP') { # <button class=\"btn btn-outline-danger\" onclick='RebootTask(\"#: RecordID #\")'> <i class=\"mdi mdi-backup-restore\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\"> #: data.ReportingStatus #</p> # } #",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "title" : "Reversion",
                "template": "# if(data.ReportingStatus != 'ABD' && data.ReportingStatus != 'CMP') { # <button class=\"btn btn-outline-warning\" onclick='LoadTaskReversionView(\"#: RecordID #\")'> <i class=\"mdi mdi-undo-variant\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\"> #: data.ReportingStatus #</p> # } #",
                "excludeFromExport": True,
                "width":80,
            },                      
            {
                "field" : "AssignedToName",
                "title" : "Assigned to",
                "width":200,
            },
            {
                "field" : "CreatedOn",
                "title" : "Task creation date",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Deadline",
                "title" : "Task deadline",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Description",
                "title" : "Task description",
                "width":200,
                "encoded": False,
            },  
            {
                "title" : "Macro Tracking",
                "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForTaskInGrid(\"#: RecordID #\")'> <i class=\"mdi mdi-table\"> </button>",
                "excludeFromExport": True,
                "width":80,
            }, 
            {
                "title" : "Macro Tracking",
                "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForTaskInTimeLine(\"#: RecordID #\")'> <i class=\"mdi mdi-source-branch\"> </button>",
                "excludeFromExport": True,
                "width":80,
            }, 
            {
                "title" : "Micro Tracking",
                "template": "<button class=\"btn btn-outline-secondary\" onclick='DisplayMicroTrackingForTaskInGrid(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-table\"> </button>",
                "excludeFromExport": True,
                "width":80,
            }, 
            {
                "title" : "Micro Tracking",
                "template": "<button class=\"btn btn-outline-secondary\" onclick='DisplayMicroTrackingForTaskInTimeLine(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-source-branch\"> </button>",
                "excludeFromExport": True,
                "width":80,
            },         
            {
                "title" : "File submissions",
                "template": "# if(data.ReportingStatus == 'PAR' || data.ReportingStatus == 'INITIAL') { # <button class=\"btn btn-outline-warning\" onclick='LoadFileSubmissionView(\"#: ID #\")'> <i class=\"mdi mdi-file-multiple\"></i> </button> # } else { # <button class=\"btn btn-outline-secondary\" onclick='LoadReadOnlyFileView(\"#: ID #\")'> <i class=\"mdi mdi-file-multiple\"> </i></button> # } #",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "title" : "Abandon",
                "template": "# if(data.ReportingStatus == 'PAR' || data.ReportingStatus == 'INITIAL') { # <button class=\"btn btn-outline-danger\" onclick='AbandonTask(\"#: ID #\")'> <i class=\"mdi mdi-close\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\">#: data.ReportingStatus #</p> # } #",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "title" : "Complete",
                "template": "# if(data.ReportingStatus == 'PAR' || data.ReportingStatus == 'INITIAL') { # <button class=\"btn btn-outline-success\" onclick='FinishTask(\"#: ID #\")'> <i class=\"mdi mdi-check\"></i> </button> # } else { var color = (ReportingStatus == 'CMP') ? 'green' : 'red' # <p style=\"color:#: color #\">#: data.ReportingStatus #</p> # } #",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "field" : "Rating",
                "title" : "Task rating",
                "template": "<div id=\"ratingBar#: ID #\"></div>",
                "width":200,
            },
            {
                "field" : "Remarks",
                "title" : "Task remarks",
                "width":200,
            },
            {
                "field" : "CreatedByName",
                "title" : "Task Created by",
                "width":200,
            }        
        ]

        resource["ReadURL"] = "TaskAPI/DataRead/Lead/" + userId + "/" + goalId
        return resource

@TaskAPI.route('/DataRead/Dev/<userId>/<goalId>', methods = ['GET'])
@SessionManagement('Dev')
def DataReadForDev(userId,goalId):
    try:
        response = Response()        
        result = TaskModule.GetLatestTaskForDevs(goalId,userId)
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@TaskAPI.route('/DataRead/Lead/<userId>/<goalId>', methods = ['GET'])
@SessionManagement('Lead')
def DataReadForLead(userId,goalId):
    try:
        response = Response()        
        result = TaskModule.GetLatestTasksForLeads(goalId,userId)
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@TaskAPI.route('/DataRead/Admin/<userId>/<goalId>', methods = ['GET'])
@SessionManagement('Admin')
def DataReadForAdmin(userId,goalId):
    try:
        print(userId)# remove this if you really want to use user id
        response = Response()        
        result = TaskModule.GetLatestTaskForAdmins(goalId)
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)


@TaskAPI.route('/CreateTask/', methods = ['POST'])
@SessionManagement('Lead')
def CreateTask():
    try:
        goalDetails = json.loads(request.data)
        response = Response()
        response.Data = TaskModule.CreateTask(goalDetails)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@TaskAPI.route('/UpdateTask/', methods = ['POST'])
@SessionManagement('Lead')
def UpdateTask():    
    try:
        goalDetails = json.loads(request.data)
        response = Response()
        response.Data = TaskModule.ParentUpdateTask(goalDetails)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@TaskAPI.route('/ChildUpdateTaskCHR/', methods = ['POST'])
@SessionManagement('Dev')
def CHRUpdateTask():    
    try:
        goalDetails = json.loads(request.data)
        response = Response()
        response.Data = TaskModule.ChildCHRUpdateTask(goalDetails)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@TaskAPI.route('/ChildUpdateTaskPGR/', methods = ['POST'])
@SessionManagement('Dev')
def PGRUpdateTask():        
    try:
        goalDetails = json.loads(request.data)
        response = Response()
        response.Data = TaskModule.ChildPGRUpdateTask(goalDetails)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@TaskAPI.route('/FinishTask/<taskChangeId>', methods = ['GET'])
@SessionManagement('Lead')
def FinishTask(taskChangeId):    
    try:
        response = Response()
        userId = GetUserSessionDetails()["USER_ID"]
        response.Data = TaskModule.FinishTask(taskChangeId,userId)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@TaskAPI.route('/AbandonTask/<taskChangeId>', methods = ['GET'])
@SessionManagement('Lead')
def AbandonTask(taskChangeId):    
    try:
        response = Response()
        userId = GetUserSessionDetails()["USER_ID"]
        response.Data = TaskModule.AbandonTask(taskChangeId,userId)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@TaskAPI.route('/ReviveTask/<taskChangeId>', methods = ['GET'])
@SessionManagement('Lead')
def ReviveTask(taskChangeId):    
    try:
        response = Response()
        userId = GetUserSessionDetails()["USER_ID"]
        response.Data = TaskModule.ReviveTask(taskChangeId,userId)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@TaskAPI.route('/AcceptChangesTask/<taskChangeId>', methods = ['GET'])
@SessionManagement('Lead')
def AcceptChangesTask(taskChangeId):    
    try:
        response = Response()
        userId = GetUserSessionDetails()["USER_ID"]
        response.Data = TaskModule.AcceptChangesTask(taskChangeId,userId)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@TaskAPI.route('/RejectChangesTask/<taskChangeId>', methods = ['GET'])
@SessionManagement('Lead')
def RejectChangesTask(taskChangeId):    
    try:
        response = Response()
        userId = GetUserSessionDetails()["USER_ID"]
        response.Data = TaskModule.RejectChangesTask(taskChangeId,userId)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)


@TaskAPI.route('/MacroTrackingGridResource/<taskId>')
@SessionManagement('Admin,Lead,Dev')
def MacroTrackingGridResource(taskId):
    try:
        response = Response()
        resource = {}
        resource["ReadURL"] = "TaskAPI/MacroTrackingGridViewRead/" + taskId
        
        resource["Fields"] = {
                "ID" : {"type" : "string"},
                "RecordID" : {"type" : "string"},
                "Name" : {"type" : "string"},                
                "Description" : {"type" : "string"},
                "CreatedByName" : {"type" : "string"},                
                "ModifiedByName" : {"type" : "string"},
                "CreatedBy" : {"type": "string"},
                "CreatedOn": {"type": "date"},
                "Deadline": {"type": "date"},
                "IsStable": {"type": "string"},
                "ReportingStatus": {"type": "string"},
                "Remarks": {"type": "string"},
                "Rating": {"type": "string"},
                "AssignedToName" : {"type": "string"},
                "TaskName": {"type":"string"},
            }

        resource["Columns"] = [
            {
                "field" : "Name",
                "title" : "Task Name",
                "width": 200,
            },               
            {
                "field" : "TaskName",
                "title" : "Task name",
                "width":200,
            },
            {
                "field" : "ReportingStatus",
                "title" : "Task status",
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
                "title" : "Task deadline",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Description",
                "title" : "Task description",
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
                "title" : "Task rating",
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
                "title" : "Task Created by",
                "width":200,
            },  
            {
                "field" : "ModifiedByName",
                "title" : "Task Modified by",
                "width":200,
            },     
            {
                "field" : "AssignedTo",
                "title" : "Task Assigned to",
                "width":200,
            }
        ]
        response.Data = resource
        response.WasSuccessful = True
    except Exception as ex:
        response.message = str(ex)
        response.WasSuccessful = False 
    return jsonify(response.__dict__)

@TaskAPI.route('/MicroTrackingGridResource/<taskId>')
@SessionManagement('Admin,Lead,Dev')
def MicroTrackingGridResource(taskId):
    try:
        response = Response()
        resource = {}
        resource["ReadURL"] = "TaskAPI/MicroTrackingGridViewRead/" + taskId
        
        resource["Fields"] = {
                "ID" : {"type" : "string"},
                "RecordID" : {"type" : "string"},
                "Name" : {"type" : "string"},                
                "Description" : {"type" : "string"},
                "CreatedByName" : {"type" : "string"},                              
                "ModifiedByName" : {"type" : "string"},
                "CreatedBy" : {"type": "string"},
                "CreatedOn": {"type": "date"},
                "Deadline": {"type": "date"},
                "IsStable": {"type": "string"},
                "ReportingStatus": {"type": "string"},
                "Remarks": {"type": "string"},
                "Rating": {"type": "string"},
                "AssignedToName" : {"type": "string"},
                "TaskName": {"type":"string"},
            }

        resource["Columns"] = [
            {
                "field" : "Name",
                "title" : "Task Name",
                "width": 200,
            },               
            {
                "field" : "TaskName",
                "title" : "Task name",
                "width":200,
            },
            {
                "field" : "ReportingStatus",
                "title" : "Task status",
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
                "title" : "Task deadline",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Description",
                "title" : "Task description",
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
                "title" : "Task rating",
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
                "title" : "Task Created by",
                "width":200,
            },
            {
                "field" : "ModifiedByName",
                "title" : "Task Modified by",
                "width":200,
            },      
            {
                "field" : "AssignedTo",
                "title" : "Task Assigned to",
                "width":200,
            }
        ]
        response.Data = resource
        response.WasSuccessful = True
    except Exception as ex:
        response.message = str(ex)
        response.WasSuccessful = False 
    return jsonify(response.__dict__)



@TaskAPI.route('/MacroTrackingGridViewRead/<taskId>', methods = ['GET'])
@SessionManagement('Admin,Lead,Dev')
def MacroTrackingGridViewRead(taskId):
    try:
        response = Response()        
        result = TaskModule.GetMacroHistory(taskId)
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@TaskAPI.route('/MacroTrackingTimeLineRead/<taskId>')
@SessionManagement('Admin,Lead,Dev')
def MacroTrackingTimeLineRead(taskId):
    try:
        response = Response()
        resource = {}
        resource["Data"] = TaskModule.GetMacroHistory(taskId)
        resource["Mappings"] = {
            "time" : "CreatedOn",
            "header" : "ReportingStatus",
            "h1Body" : "ModifiedByName",
            "paraBody" : "Remarks",
            "footer": "CreatedByName" 
        }
        response.Data = resource 
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@TaskAPI.route('/MicroTrackingGridViewRead/<taskId>', methods = ['GET'])
@SessionManagement('Admin,Lead,Dev')
def MicroTrackingGridViewRead(taskId):
    try:
        response = Response()        
        result = TaskModule.GetMicroHistory(taskId)
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@TaskAPI.route('/MicroTrackingTimeLineRead/<taskId>')
@SessionManagement('Admin,Lead,Dev')
def MicroTrackingTimeLineRead(taskId):
    try:
        response = Response()
        resource = {}
        resource["Data"] = TaskModule.GetMicroHistory(taskId)
        resource["Mappings"] = {
            "time" : "CreatedOn",
            "header" : "ReportingStatus",
            "h1Body" : "ModifiedByName",
            "paraBody" : "Remarks",
            "footer": "CreatedByName" 
        }
        response.Data = resource 
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)


@TaskAPI.route('/WorkHierarchyResource/<goalId>')
@SessionManagement('Admin,Lead,Dev')
def WorkHierarchyResource(goalId):
    try:
        response = Response()
        userSessionDetails = GetUserSessionDetails()
        userId = userSessionDetails.get("USER_ID")
        role = userSessionDetails.get("USER_ROLE")
        role = role.lower()
        resource = {}

        if role == 'admin' :
            resource = WorkHierarchyResourcesForAdmin(userId,goalId)
        elif role == 'lead' :
            resource = WorkHierarchyResourcesForLead(userId,goalId)
        elif role == 'dev':
            resource = WorkHierarchyResourcesForDev(userId,goalId)

        response.Data = resource
        response.WasSuccessful = True
    except Exception as ex:
        response.message = str(ex)
        response.WasSuccessful = False 
    return jsonify(response.__dict__)

def WorkHierarchyResourcesForAdmin(userId,goalId):
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
            "title" : "Task Name",
            "width": 200,
        },
        {
            "field" : "Description",
            "title" : "Task description",
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
            "template": "<button class=\"btn btn-outline-secondary\" onclick='LoadReadOnlyFileView(\"#: ID #\")'> <i class=\"mdi mdi-file-multiple\"></i> </button>",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForTaskInGrid(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-table\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForTaskInTimeLine(\"#: RecordID #\")'> <i class=\"mdi mdi-source-branch\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Micro Tracking",
            "template": "<button class=\"btn btn-outline-secondary\" onclick='DisplayMicroTrackingForTaskInGrid(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-table\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Micro Tracking",
            "template": "<button class=\"btn btn-outline-secondary\" onclick='DisplayMicroTrackingForTaskInTimeLine(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-source-branch\"> </button>",
            "excludeFromExport": True,
            "width":80,
        },    
        {
            "field" : "CreatedOn",
            "title" : "Task creation date",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Deadline",
            "title" : "Task deadline",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Rating",
            "title" : "Task rating",
            "template": "<div id=\"ratingBar#: ID #\"></div>",
            "width":200,
        },
        {
            "field" : "Remarks",
            "title" : "Task name",
            "width":200,
        },
        {
            "field" : "CreatedByName",
            "title" : "Task Created by",
            "width":200,
        }        
    ]

    resource["ReadURL"] = "TaskAPI/DataRead/Admin/" + userId + "/" + goalId
    return resource

def WorkHierarchyResourcesForDev(userId,goalId):
    resource = {};  
    resource["ReadURL"] = "TaskAPI/DataRead/Dev/" + userId + "/" + goalId
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
            "title" : "Task Name",
            "width": 200,
        },
        {
            "field" : "Description",
            "title" : "Task description",
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
            "template": "<button class=\"btn btn-outline-secondary\" onclick='LoadReadOnlyFileView(\"#: ID #\")'> <i class=\"mdi mdi-file-multiple\"></i> </button>",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForTaskInGrid(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-table\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForTaskInTimeLine(\"#: RecordID #\")'> <i class=\"mdi mdi-source-branch\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Micro Tracking",
            "template": "<button class=\"btn btn-outline-secondary\" onclick='DisplayMicroTrackingForTaskInGrid(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-table\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Micro Tracking",
            "template": "<button class=\"btn btn-outline-secondary\" onclick='DisplayMicroTrackingForTaskInTimeLine(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-source-branch\"> </button>",
            "excludeFromExport": True,
            "width":80,
        },    
        {
            "field" : "CreatedOn",
            "title" : "Task creation date",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Deadline",
            "title" : "Task deadline",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Rating",
            "title" : "Task rating",
            "template": "<div id=\"ratingBar#: ID #\"></div>",
            "width":200,
        },
        {
            "field" : "Remarks",
            "title" : "Task name",
            "width":200,
        },
        {
            "field" : "CreatedByName",
            "title" : "Task Created by",
            "width":200,
        }             
    ]

    return resource

def WorkHierarchyResourcesForLead(userId,goalId):        
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
            "title" : "Task Name",
            "width": 200,
        },
        {
            "field" : "Description",
            "title" : "Task description",
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
            "template": "<button class=\"btn btn-outline-secondary\" onclick='LoadReadOnlyFileView(\"#: ID #\")'> <i class=\"mdi mdi-file-multiple\"></i> </button>",
            "excludeFromExport": True,
            "width":80,
        },
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForTaskInGrid(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-table\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Macro Tracking",
            "template": "<button class=\"btn btn-outline-info\" onclick='DisplayMacroTrackingForTaskInTimeLine(\"#: RecordID #\")'> <i class=\"mdi mdi-source-branch\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Micro Tracking",
            "template": "<button class=\"btn btn-outline-secondary\" onclick='DisplayMicroTrackingForTaskInGrid(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-table\"> </button>",
            "excludeFromExport": True,
            "width":80,
        }, 
        {
            "title" : "Micro Tracking",
            "template": "<button class=\"btn btn-outline-secondary\" onclick='DisplayMicroTrackingForTaskInTimeLine(\"#: RecordID #\",true,true,divMainPage)'> <i class=\"mdi mdi-source-branch\"> </button>",
            "excludeFromExport": True,
            "width":80,
        },    
        {
            "field" : "CreatedOn",
            "title" : "Task creation date",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Deadline",
            "title" : "Task deadline",
            "format" : "{0:dd/MM/yyyy}",
            "width": 200,            
        },
        {
            "field" : "Rating",
            "title" : "Task rating",
            "template": "<div id=\"ratingBar#: ID #\"></div>",
            "width":200,
        },
        {
            "field" : "Remarks",
            "title" : "Task name",
            "width":200,
        },
        {
            "field" : "CreatedByName",
            "title" : "Task Created by",
            "width":200,
        }             
        ]

        resource["ReadURL"] = "TaskAPI/DataRead/Lead/" + userId + "/" + goalId
        return resource

@TaskAPI.route('/ReversionTask/<taskChangeID>', methods = ['GET'])
@SessionManagement('Lead')
def Reversion(taskChangeID):    
    try:
        response = Response()
        userId = GetUserSessionDetails()["USER_ID"]
        response.Data = TaskModule.Reversion(taskChangeID,userId)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@TaskAPI.route('/RebootTask/<taskId>', methods = ['GET'])
@SessionManagement('Lead')
def Reboot(taskId):    
    try:
        response = Response()
        userId = GetUserSessionDetails()["USER_ID"]
        response.Data = TaskModule.Reboot(taskId,userId)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@TaskAPI.route('/TaskReversionGridViewResource/<taskId>')
@SessionManagement('Lead')
def TaskReversionGridViewResource(taskId):
    try:
        response = Response()
        resource = {}
        resource["ReadURL"] = "TaskAPI/MacroTrackingGridViewRead/" + taskId
        
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
                "title" : "Task Name",
                "width": 200,
            },
            {
                "field" : "ReportingStatus",
                "title" : "Task status",
                "width": 200,
            },
            {
                "field" : "CreatedOn",
                "title" : "Task creation date",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Deadline",
                "title" : "Task deadline",
                "format" : "{0:dd/MM/yyyy}",
                "width": 200,            
            },
            {
                "field" : "Description",
                "title" : "Task description",
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
                "title" : "Revert task",
                "template": "<button class=\"btn btn-outline-danger\" onclick='ReversionTask(\"#: ID #\")'> <i class=\"mdi mdi-undo\"> </i></button>",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "field" : "Rating",
                "title" : "Task rating",
                "template": "<div id=\"ratingBar#: ID #\"></div>",
                "width":200,
            },
            {
                "field" : "Remarks",
                "title" : "Task remarks",
                "width":200,
            },
            {
                "field" : "CreatedByName",
                "title" : "Task Created by",
                "width":200,
            }        
        ]
        response.Data = resource
        response.WasSuccessful = True
    except Exception as ex:
        response.message = str(ex)
        response.WasSuccessful = False 
    return jsonify(response.__dict__)
