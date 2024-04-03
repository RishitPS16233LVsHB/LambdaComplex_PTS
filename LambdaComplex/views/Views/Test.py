from flask import render_template, Blueprint
from SessionManagement import SessionManagement

Test = Blueprint("Test",__name__)

@Test.route('/CreateView/')
@SessionManagement('Admin,Lead,Dev')
def CreateView():
    return render_template('Test/Create.html')

@Test.route('/UpdateView/<itemId>')
@SessionManagement('Admin,Lead,Dev')
def UpdateView(itemId):
    return render_template('Test/Update.html')

