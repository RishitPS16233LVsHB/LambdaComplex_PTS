from flask import Blueprint, Flask, request, session, render_template, redirect, url_for, jsonify
from LambdaComplex_Entities.Common import Response
from LambdaComplex_DataAccess.TaskModule import TaskModule
from SessionManagement import SessionManagement,GetUserSessionDetails

Task = Blueprint('Task', __name__)

@Task.route('/Create/<goalId>')
@SessionManagement('Lead')
def CreateView(goalId):
    devDetails = TaskModule.GetGoalAssignedToNameAndID(goalId)[0]
    taskAssignedToName = devDetails["AssignedToName"]
    taskAssignedTo = devDetails["AssignedToID"]
    return render_template(
        'Task/Create.html', 
        parentID = goalId, 
        taskAssignedToName = taskAssignedToName, 
        taskAssignedTo = taskAssignedTo
    )

@Task.route('/Update/<goalId>/<taskId>')
@SessionManagement('Lead')
def UpdateView(goalId,taskId):
    taskDetails = TaskModule.GetLatestStableVersionOfTask(taskId)[0]
    return render_template('Task/Update.html',
        parentID = goalId,
        recordID = taskId,
        taskName = taskDetails["Name"],
        taskDescription = taskDetails["Description"],
        expectedDeadline = taskDetails["Deadline"],
        taskRemarks = taskDetails["Remarks"],
        taskRating = taskDetails["Rating"],        
        taskAssignedTo = taskDetails["AssignedTo"],        
        taskAssignedToName = taskDetails["AssignedToName"]
    )

@Task.route('/ChildUpdate/<goalId>/<taskId>')
@SessionManagement('Dev')
def ChidlUpdateView(goalId,taskId):
    taskDetails = TaskModule.GetLatestStableVersionOfTask(taskId)[0]
    return render_template('Task/ChildUpdate.html',
        parentID = goalId,
        recordID = taskId,
        taskName = taskDetails["Name"],
        taskDescription = taskDetails["Description"],
        expectedDeadline = taskDetails["Deadline"],
        taskRemarks = taskDetails["Remarks"],
        taskRating = taskDetails["Rating"],        
        taskAssignedTo = taskDetails["AssignedTo"],
        taskAssignedToName = taskDetails["AssignedToName"],
        taskCreatedBy = taskDetails["CreatedBy"]
    )