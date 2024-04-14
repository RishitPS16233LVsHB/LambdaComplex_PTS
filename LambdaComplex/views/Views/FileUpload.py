from flask import Flask, session, render_template, request, redirect, url_for,Blueprint
from SessionManagement import SessionManagement

FileUpload = Blueprint("FileUpload",__name__)

@FileUpload.route('/Upload/<recordId>')
@SessionManagement('Admin,Lead,Dev')
def Index(recordId):
    return render_template('FileUpload/Upload.html', recordId = recordId)

@FileUpload.route('/FileReadOnly/<recordId>')
@SessionManagement('Admin,Lead,Dev')
def ReadOnly(recordId):
    return render_template('FileUpload/ReadOnly.html', recordId = recordId)