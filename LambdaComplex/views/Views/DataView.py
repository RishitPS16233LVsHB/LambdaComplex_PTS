import json
from flask import render_template, request, Blueprint
from SessionManagement import SessionManagement

DataView = Blueprint("DataView",__name__)

@DataView.route('/Rendering/', methods=['POST'])
@SessionManagement('Admin,Lead,Dev')
def Index():
    eventData = json.loads(request.data)
    resourceUrl = eventData["ResourceUrl"]
    renderType = eventData["RenderType"]
    return render_template('DataView/Index.html',ResourceUrl = resourceUrl,RenderType = renderType)

