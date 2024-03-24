from flask import Flask, session, render_template, request, redirect, url_for,Blueprint
from SessionManagement import SessionManagement
import uuid 

Home = Blueprint("Home",__name__)

@Home.route('/')
@SessionManagement('Admin,Lead,Dev')
def Index():
    id = str(uuid.uuid4())
    user_id = session.get('UserID')
    user_role = session.get('Role')
    user_name = session.get('UserName')
    return render_template('Home/Index.html',UserID=user_id, Role=user_role, UserName=user_name)