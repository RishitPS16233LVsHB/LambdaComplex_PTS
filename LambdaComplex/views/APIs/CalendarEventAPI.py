import json
from flask import jsonify, request ,Blueprint
from SessionManagement import SessionManagement
from LambdaComplex_DataAccess.CalendarEventModule import CalendarEventModule
from LambdaComplex_Entities.Common import Response

CalendarEventAPI = Blueprint("CalendarEventAPI",__name__)

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

@CalendarEventAPI.route('/DeleteCalendarEvent/',methods=['POST'])
@SessionManagement('Admin,Lead,Dev')
def DeleteCalendarEvent():
    try:
        response = Response()
        eventData = json.loads(request.data)
        result = CalendarEventModule.DeleteCalendarEvent(eventData)
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

