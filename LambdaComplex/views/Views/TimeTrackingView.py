import json
from flask import render_template, request, Blueprint
from SessionManagement import SessionManagement

TimeTrackingView = Blueprint("TimeTrackingView",__name__)

@TimeTrackingView.route('/Rendering/', methods=['POST'])
@SessionManagement('Admin,Lead,Dev')
def Index():
    eventData = json.loads(request.data)
    resourceUrl = eventData["ResourceUrl"]
    renderType = eventData["RenderType"]
    return render_template('TimeTrackingView/Index.html',ResourceUrl = resourceUrl,RenderType = renderType)

