import json
from flask import render_template, request, Blueprint
from SessionManagement import SessionManagement

ChartView = Blueprint("ChartView",__name__)

@ChartView.route('/Rendering/', methods=['POST'])
@SessionManagement('Admin,Lead,Dev')
def Index():
    eventData = json.loads(request.data)
    return render_template('ChartView/Index.html',eventData)
