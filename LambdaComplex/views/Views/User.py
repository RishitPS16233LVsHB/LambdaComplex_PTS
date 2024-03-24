from flask import Flask, session, render_template, redirect, url_for, Blueprint
from LambdaComplex_DataAccess.UserModule import UserModule
from SessionManagement import SessionManagement

User = Blueprint("User",__name__)

@User.route('/GetUserDetails/')
@SessionManagement('Admin,Lead,Dev')
def Index():
    return render_template('User/Index.html')

@User.route('/ChangePassword/')
@SessionManagement('Admin,Lead,Dev')
def ChangePassword():
    return render_template('User/ChangePassword.html')