from flask import render_template, Blueprint
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

@User.route('/CreateUser/')
@SessionManagement('Admin')
def CreateUser():
    return render_template('User/CreateUser.html')

