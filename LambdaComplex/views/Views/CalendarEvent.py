import html
import json
from flask import Flask, request, session, render_template, redirect, url_for, Blueprint
from LambdaComplex_DataAccess.CalendarEventModule import CalendarEventModule
from SessionManagement import SessionManagement
from datetime import datetime

CalendarEvent = Blueprint("CalendarEvent",__name__)

@CalendarEvent.route('/GetCalendarEvent')
@SessionManagement('Admin,Lead,Dev')
def Index():
    return render_template('Calendar/Index.html')


@CalendarEvent.route('/CreateCalendarEventView', methods = ['POST'])
@SessionManagement('Admin,Lead,Dev')
def CreateEvent():
    calendarData = json.loads(request.data)
    selectedCalendarDate =  str(calendarData["selectedCalendarDate"])        
    return render_template('Calendar/CreateEvent.html', selectedCalendarDate = selectedCalendarDate)

@CalendarEvent.route('/UpdateCalendarEventView/<recordId>')
@SessionManagement('Admin,Lead,Dev')
def UpdateEvent(recordId):
    eventData = CalendarEventModule.GetEventData(recordId)[0]
    return render_template('Calendar/UpdateEvent.html', 
        id = eventData["ID"],
        eventName = str(eventData["EventName"]),
        eventDescription = html.unescape(eventData["EventDescription"]),
        eventDate = str(eventData["EventDate"]),
        eventTime = str(eventData["EventTime"])                                
    )

@CalendarEvent.route('/CalendarEventViewInformaticView/<recordId>')
@SessionManagement('Admin,Lead,Dev')
def Informatics(recordId):
    eventData = CalendarEventModule.GetEventData(recordId)[0]
    return render_template('Calendar/Informatic.html', 
        eventName = str(eventData["EventName"]),
        eventDescription = html.unescape(eventData["EventDescription"]),
        eventDate = str(eventData["EventDate"]),
        eventTime = str(eventData["EventTime"])                                  
    )


