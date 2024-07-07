import json
from flask import jsonify, Blueprint, request
from LambdaComplex_Entities.Common import Response
from LambdaComplex_DataAccess.ChatModule import ChatModule
from SessionManagement import SessionManagement,GetUserSessionDetails

ChatAPI = Blueprint("ChatAPI",__name__)

