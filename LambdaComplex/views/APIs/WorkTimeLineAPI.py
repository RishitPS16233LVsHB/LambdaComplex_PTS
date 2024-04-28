import json
from flask import jsonify, request ,Blueprint
from SessionManagement import SessionManagement, GetUserSessionDetails
from LambdaComplex_DataAccess.WorkTimeLineModule import WorkTimeLineModule
from LambdaComplex_Entities.Common import Response

WorkTimeLineAPI = Blueprint("WorkTimeLineAPI",__name__)

@WorkTimeLineAPI.route('/WorkTimeLineCalendarResource/')
@SessionManagement('Admin,Lead,Dev')
def WorkTimeLineCalendarResource():
    try:
        response = Response()
        userSessionDetails = GetUserSessionDetails()
        userId = userSessionDetails["USER_ID"]
        resource = {}

        resource["CalendarReadUrl"] = "WorkTimeLineAPI/CalendarRead/"+userId      
        resource["GridViewResourceUrl"] = "WorkTimeLineAPI/WorkTimeLineGridViewResource/"+userId
        resource["TimeLineViewReadUrl"] = "WorkTimeLineAPI/WorkTimeTimeLineRead/"+userId

        response.Data = resource
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@WorkTimeLineAPI.route('/CalendarRead/<userId>')
@SessionManagement('Admin,Lead,Dev')
def WorkTimeLineCalendarRead(userId):
    try:
        response = Response()
        response.Data = WorkTimeLineModule.GetWorkTimelineGroupedByDate(userId)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@WorkTimeLineAPI.route('/WorkTimeLineGridViewRead/<userId>/<dateString>')
@SessionManagement('Admin,Lead,Dev')
def WorkTimeLineGridViewRead(userId,dateString):
    try:
        response = Response()
        response.Data = WorkTimeLineModule.GetWorkTimeLineForDate(userId,dateString)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@WorkTimeLineAPI.route('/WorkTimeLineGridViewResource/<userId>/<dateString>')
@SessionManagement('Admin,Lead,Dev')
def WorkTimeLineGridViewResource(userId,dateString):
    try:
        response = Response()
        resource = {}
        resource["Fields"] = {
                    "WorkTimeLineID" : {"type" : "string"},
                    "Message" : {"type" : "string"},
                    "RecordID": {"type": "string"},
                    "AffectedModule" : {"type" : "string"},
                    "CreatedOn" : {"type": "date"},
                    "AffectedEntityName": {"type": "string"},                    
                    "ActionDoneBy": {"type": "string"},
                    "ActionDoneByID": {"type": "string"},                
                }

        resource["Columns"] = [
            {
                "field" : "Message",
                "title" : "Message",
                "width": 200,
            },
            {
                "field" : "AffectedEntityName",
                "title" : "Entity Affected",
                "width": 200,
            },
            {
                "field": "AffectedModule",
                "title": "Module",
                "width": 200,
            },
            {
                "field" : "CreatedOn",
                "title" : "Creation date",                
                "format" : "{0:dd/MM/yyyy hh:mm:ss}",
                "width":200,
            },
            {
                "field" : "ActionDoneBy",
                "title" : "Action done by",
                "encoded": False,
                "width": 200,
            },
        ]
        resource["ReadURL"] = "WorkTimeLineAPI/WorkTimeLineGridViewRead/"+userId+"/"+dateString


        response.Data = resource
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@WorkTimeLineAPI.route('/WorkTimeTimeLineRead/<userId>/<dateString>')
@SessionManagement('Admin,Lead,Dev')
def WorkTimeTimeLineRead(userId,dateString):
    try:
        response = Response()
        resource = {}
        resource["Data"] = WorkTimeLineModule.GetWorkTimeLineForDate(userId,dateString)
        resource["Mappings"] = {
            "time" : "CreatedOn",
            "header" : "AffectedModule",
            "h1Body" : "AffectedEntityName",
            "paraBody" : "Message",
            "footer": "CreatedOn" 
        }
        response.Data = resource 
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)