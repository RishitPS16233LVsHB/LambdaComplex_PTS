from flask import Flask, request, session, render_template, redirect, url_for, jsonify, Blueprint
from LambdaComplex_DataAccess.LoginModule import LoginModule
from LambdaComplex_Entities.Common import Response
import uuid 
import json

Login = Blueprint('Login', __name__)

@Login.route('/',methods=['GET'])
def Index():
    id = str(uuid.uuid4())
    return render_template('Login/Index.html',uuid = id)

@Login.route('/UserLogin', methods=['POST'])
def UserLogin():
    response = Response()
    creds = json.loads(request.data)
    try:
        user = LoginModule.CheckLogin(creds['UserName'], creds['Password'])
        if user is None:
            response.WasSuccessful = False
            response.Message = "Wrong password or username"
        else:
            session['UserID'] = user["ID"]
            session['UserName'] = user["Username"]
            session['Role'] = user["Role"]
            response.WasSuccessful = True
            response.Message = "Login Successful"
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False
    return jsonify(response.__dict__)
    

@Login.route('/Sessioned',methods=['GET'])
def Sessioned():
    session.clear()
    return render_template('Login/Sessioned.html')

@Login.route('/Forbidden',methods=['GET'])
def Forbidden():
    return render_template('Login/Forbidden.html')


@Login.route('/ResetSessionTimeout')
def ResetSessionTimeout():
    response = Response()
    try:
        session['TimeLeft'] = 20
        response.Message = "Successfully set session timeout"
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = "Error while Resetting Session timeout: " + str(ex)
        response.WasSuccessful = False
    return jsonify(response.__dict__)

@Login.route('/UserLogout')
def UserLogout():
    session.clear()
    return redirect(url_for('/Login'))