import json
from flask import jsonify, request ,Blueprint
from SessionManagement import SessionManagement
from LambdaComplex_DataAccess.UserModule import UserModule
from LambdaComplex_Entities.Common import Response

UserAPI = Blueprint("UserAPI",__name__)

@UserAPI.route('/GetUserDetails/<userId>')
@SessionManagement('Admin,Lead,Dev')
def GetUserDetails(userId):
    try:
        response = Response()
        userDetails = UserModule.GetUserDetails(userId)
        response.Data = userDetails
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@UserAPI.route('/CreateUser/', methods = ['POST'])
@SessionManagement('Admin')
def CreateUser():
    try:
        response = Response()        
        userDetails = json.loads(request.data)
        UserModule.CreateUser(userDetails)
        response.Data  = None
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@UserAPI.route('/UpdateUserDetails/', methods = ['POST'])
@SessionManagement('Admin,Lead,Dev')
def UpdateUserDetails():
    try:
        response = Response()        
        userDetails = json.loads(request.data)
        UserModule.UpdateUserDetails(userDetails)
        response.Data  = None
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)


@UserAPI.route('/ChangePassword/', methods = ['POST'])
@SessionManagement('Admin,Lead,Dev')
def ChangePassword():
    try:
        response = Response()        
        userDetails = json.loads(request.data)
        UserModule.ChangePassword(userDetails)
        response.Data  = None
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@UserAPI.route('/GetDevs/', methods = ['GET'])
@SessionManagement('Admin')
def GetDevs():
    try:
        response = Response()        
        result = UserModule.GetDeveloperNamesAndIds()
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@UserAPI.route('/GetLeads/', methods = ['GET'])
@SessionManagement('Admin')
def GetLeads():
    try:
        response = Response()        
        result = UserModule.GetLeadNamesAndIds()
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@UserAPI.route('/GetLeadsOfProject/<projectId>', methods = ['GET'])
@SessionManagement('Admin,Lead')
def GetLeadsOfProject(projectId):
    try:
        response = Response()        
        result = UserModule.GetLeadNamesAndIdsOfTeamInProject(projectId)
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)


@UserAPI.route('/GetDevelopersInMilestone/<milestoneId>/<userId>', methods = ['GET'])
@SessionManagement('Admin,Lead')
def GetDevelopersInMilestone(milestoneId,userId):
    try:
        response = Response()        
        result = UserModule.GetDevNamesAndIdsOfTeamInMilestone(milestoneId,userId)
        response.Data  = result
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)