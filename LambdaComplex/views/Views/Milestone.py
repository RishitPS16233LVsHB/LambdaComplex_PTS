from flask import Blueprint, Flask, request, session, render_template, redirect, url_for, jsonify
from LambdaComplex_Entities.Common import Response
from LambdaComplex_DataAccess.MilestoneModule import MilestoneModule
from SessionManagement import SessionManagement,GetUserSessionDetails

Milestone = Blueprint('Milestone', __name__)

@Milestone.route('/Create/<projectId>')
@SessionManagement('Admin')
def CreateView(projectId):
    return render_template('Milestone/Create.html', parentID = projectId)

@Milestone.route('/Update/<projectId>/<milestoneId>')
@SessionManagement('Admin')
def UpdateView(projectId,milestoneId):
    milestoneDetails = MilestoneModule.GetLatestStableVersionOfMilestone(milestoneId)[0]
    return render_template('Milestone/Update.html',
        parentID = projectId,
        recordID = milestoneId,
        milestoneName = milestoneDetails["Name"],
        milestoneDescription = milestoneDetails["Description"],
        expectedDeadline = milestoneDetails["Deadline"],
        milestoneRemarks = milestoneDetails["Remarks"],
        milestoneRating = milestoneDetails["Rating"],        
        milestoneAssignedTo = milestoneDetails["AssignedTo"]
    )

@Milestone.route('/ChildUpdate/<projectId>/<milestoneId>')
@SessionManagement('Lead')
def ChidlUpdateView(projectId,milestoneId):
    milestoneDetails = MilestoneModule.GetLatestStableVersionOfMilestone(milestoneId)[0]
    return render_template('Milestone/ChildUpdate.html',
        parentID = projectId,
        recordID = milestoneId,
        milestoneName = milestoneDetails["Name"],
        milestoneDescription = milestoneDetails["Description"],
        expectedDeadline = milestoneDetails["Deadline"],
        milestoneRemarks = milestoneDetails["Remarks"],
        milestoneRating = milestoneDetails["Rating"],        
        milestoneAssignedTo = milestoneDetails["AssignedTo"],
        milestoneCreatedBy = milestoneDetails["CreatedBy"]
    )