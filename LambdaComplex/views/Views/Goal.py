from flask import Blueprint,render_template
from LambdaComplex_Entities.Common import Response
from LambdaComplex_DataAccess.GoalModule import GoalModule
from SessionManagement import SessionManagement

Goal = Blueprint('Goal', __name__)

@Goal.route('/Create/<parentId>')
@SessionManagement('Lead')
def CreateView(parentId):
    return render_template('Goal/Create.html', parentID = parentId)

@Goal.route('/Update/<parentId>/<goalId>')
@SessionManagement('Lead')
def UpdateView(goalId,parentId):
    goalDetails = GoalModule.GetLatestStableVersionOfGoal(goalId)[0]
    return render_template('Goal/Update.html',
        recordID = goalId,
        parentID = parentId,
        goalName = goalDetails["Name"],
        goalDescription = goalDetails["Description"],
        expectedDeadline = goalDetails["Deadline"],
        goalRemarks = goalDetails["Remarks"],
        goalRating = goalDetails["Rating"],
        goalAssignedTo = goalDetails["AssignedTo"]
    )
