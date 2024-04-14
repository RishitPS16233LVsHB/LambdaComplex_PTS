from flask import Blueprint, Flask, request, session, render_template, redirect, url_for, jsonify
from LambdaComplex_Entities.Common import Response
from LambdaComplex_DataAccess.ProjectModule import ProjectModule
from SessionManagement import SessionManagement,GetUserSessionDetails

Project = Blueprint('Project', __name__)

@Project.route('/Create/')
@SessionManagement('Admin')
def CreateView():
    return render_template('Project/Create.html')

@Project.route('/Update/<projectId>')
@SessionManagement('Admin')
def UpdateView(projectId):
    projectDetails = ProjectModule.GetLatestStableVersionOfProject(projectId)[0]
    return render_template('Project/Update.html',
        recordID = projectId,
        projectName = projectDetails["Name"],
        projectDescription = projectDetails["Description"],
        expectedDeadline = projectDetails["Deadline"],
        projectRemarks = projectDetails["Remarks"],
        projectRating = projectDetails["Rating"]
    )
