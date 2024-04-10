import json
from flask import jsonify, request ,Blueprint
from SessionManagement import SessionManagement, GetUserSessionDetails
from LambdaComplex_DataAccess.CalendarEventModule import CalendarEventModule
from LambdaComplex_Entities.Common import Response

CalendarEventAPI = Blueprint("CalendarEventAPI",__name__)

@CalendarEventAPI.route('/CalendarViewResource/')
@SessionManagement('Admin,Lead,Dev')
def CalendarResource():
    try:
        response = Response()
        userSessionDetails = GetUserSessionDetails()
        userId = userSessionDetails["USER_ID"]
        resource = {}

        resource["CalendarReadUrl"] = "CalendarEventAPI/GetGroupedCalendarEvent/"+userId
        resource["CreateViewUrl"] = "CalendarEvent/CreateCalendarEventView"
        resource["GridViewResourceUrl"] = "CalendarEventAPI/CalendarGridViewResource"
        resource["TimeLineViewReadUrl"] = "CalendarEventAPI/CalendarTimeLineReadUrl"

        response.Data = resource
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@CalendarEventAPI.route('/CalendarTimeLineReadUrl/<calendarDate>')
@SessionManagement('Admin,Lead,Dev')
def CalendarTimeLineReadUrl(calendarDate):
    try:
        response = Response()
        userSessionData = GetUserSessionDetails()
        userId = userSessionData["USER_ID"]
        calendarDate = calendarDate.replace('L','-')
        resource = {}
        resource["Data"] = CalendarEventModule.GetCalendarEventsForEventDate(userId,calendarDate)
        resource["Mappings"] = {
            "time" : "EventDate",
            "header" : "EventName",
            "h1Body" : "EventTime",
            "paraBody" : "EventDescription",
            "footer": "ID" 
        };

        response.Data = resource
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@CalendarEventAPI.route('/CalendarGridViewResource/<calendarDate>')
@SessionManagement('Admin,Lead,Dev')
def CalendarGridViewResource(calendarDate):
    try:
        response = Response()
        resource = {}

        resource["Fields"] = {
                    "ID" : {"type" : "string"},
                    "EventName" : {"type" : "string"},
                    "EventTime": {"type": "string"},
                    "EventDate" : {"type" : "date"},
                    "CreatedOn" : {"type": "date"},
                    "EventPriotity": {"type": "string"},
                    "EventDescription" : {"type" : "string"},
                }

        resource["Columns"] = [
            {
                "title" : "Delete",
                "template": "# if (!data.IsExpired) { # <button class='btn btn-outline-danger' onclick='DeleteRecord(\"#: ID #\")'> <i class='mdi mdi-delete'></i> </button> # } #",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "title" : "Edit",
                "template": "# if (!data.IsExpired) { # <button class=\"btn btn-outline-primary\" onclick='LoadUpdateView(\"#: ID #\")'> <i class=\"mdi mdi-grease-pencil\"></i> </button>  # } #",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "title" : "Info",
                "template": "<button class=\"btn btn-outline-info\" onclick='LoadInformaticView(\"#: ID #\")'> <i class=\"mdi mdi-information-outline\"> </button>",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "field" : "EventName",
                "title" : "Event Name",
                "width": 200,
            },
            {
                "field" : "EventDescription",
                "title" : "Event description",
                "encoded": False,
                "width": 200,
            },
            {
                "field": "EventPriority",
                "title": "Event priority",
                "width": 200,
            },
            {
                "field" : "EventTime",
                "title" : "Event time",
                "width": 200,            
            },
            {
                "field" : "EventDate",
                "title" : "Event date",                
                "format" : "{0:dd/MM/yyyy}",
                "width":200,
            },
            {
                "field" : "CreatedOn",
                "title" : "Event creation date",                
                "format" : "{0:dd/MM/yyyy}",
                "width":200,
            },
        ]

        resource["DeleteUrl"] = "CalendarEventAPI/DeleteCalendarEvent/"
        resource["UpdateViewUrl"] = "CalendarEvent/UpdateCalendarEventView/"
        resource["ReadURL"] = "CalendarEventAPI/GetCalendarEventsForEventDate/"+calendarDate
        resource["InformaticView"] = "CalendarEvent/CalendarEventViewInformaticView/"

        response.Data = resource
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@CalendarEventAPI.route('/GetGroupedCalendarEvent/<userId>')
@SessionManagement('Admin,Lead,Dev')
def GetGroupedCalendarEvent(userId):
    try:
        response = Response()
        response.Data = CalendarEventModule.GetGroupedCalendarEvent(userId)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@CalendarEventAPI.route('/GetCalendarEventsForEventDate/<calendarDate>')
@SessionManagement('Admin,Lead,Dev')
def GetCalendarEventsForEventDate(calendarDate):
    try:
        calendarDate = calendarDate.replace('L','-')
        userSessionDetails = GetUserSessionDetails()
        userId = userSessionDetails["USER_ID"]
        response = Response()
        response.Data = CalendarEventModule.GetCalendarEventsForEventDate(userId,calendarDate)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)


@CalendarEventAPI.route('/GetCalendarEvent/<userId>')
@SessionManagement('Admin,Lead,Dev')
def GetCalendarEvent(userId):
    try:
        response = Response()
        userDetails = CalendarEventModule.GetCalendarEvent(userId)
        response.Data = userDetails
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@CalendarEventAPI.route('/GetPriorityEventCount/<userId>')
@SessionManagement('Admin,Lead,Dev')
def GetPriorityEvents(userId):
    try:
        response = Response()
        priorityEventCount = CalendarEventModule.GetPriorityEventCount(userId)
        response.Data = priorityEventCount
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@CalendarEventAPI.route('/CreateCalendarEvent/',methods=['POST'])
@SessionManagement('Admin,Lead,Dev')
def CreateCalendarEvent():
    try:
        response = Response()
        eventData = json.loads(request.data)
        result = CalendarEventModule.CreateCalendarEvent(eventData)
        response.Data = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@CalendarEventAPI.route('/UpdateCalendarEvent/',methods=['POST'])
@SessionManagement('Admin,Lead,Dev')
def UpdateCalendarEvent():
    try:
        response = Response()
        eventData = json.loads(request.data)
        result = CalendarEventModule.UpdateCalendarEvent(eventData)
        response.Data = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@CalendarEventAPI.route('/DeleteCalendarEvent/<recordId>')
@SessionManagement('Admin,Lead,Dev')
def DeleteCalendarEvent(recordId):
    try:
        response = Response()
        userSessionDetails = GetUserSessionDetails();
        userId = userSessionDetails["USER_ID"]  
        result = CalendarEventModule.DeleteCalendarEvent(userId,recordId)
        response.Data = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@CalendarEventAPI.route('/ExpireOutOfDateEvent/')
@SessionManagement('Admin,Lead,Dev')
def ExpireOutOfDateEvents():
    try:
        response = Response()
        result = CalendarEventModule.ExpireOutOfDateEvents()
        response.Data = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

