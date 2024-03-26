from flask import Flask, session, render_template, redirect, url_for, Blueprint
from LambdaComplex_DataAccess.UserModule import UserModule
from SessionManagement import SessionManagement

CalendarEvent = Blueprint("CalendarEvent",__name__)

@CalendarEvent.route('/GetCalendarEvent')
@SessionManagement('Admin,Lead,Dev')
def Index():
    return render_template('Calendar/Index.html')

