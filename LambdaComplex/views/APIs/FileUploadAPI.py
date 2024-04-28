import json
from flask import jsonify, Blueprint, request
from SessionManagement import SessionManagement, GetUserSessionDetails
from LambdaComplex_Entities.Common import Response
from LambdaComplex_DataAccess.FileUploadModule import FileUploadModule


FileUploadAPI = Blueprint("FileUploadAPI",__name__)

@FileUploadAPI.route('/Upload/<recordId>',methods=['POST'])
@SessionManagement('Admin,Lead,Dev')
def upload_file(recordId):
    response = Response()
    try:
        if len(request.files) == 0:
            response.Message = 'No Files'
            response.WasSuccessful = False
            return response
        
        userId = GetUserSessionDetails()["USER_ID"]
        processedFiles = []
        files = request.files

        for k in list(files):
            file = files[k]
            if file.filename == '':
                continue

            file_info = {
                'filename': file.filename,
                'ext': file.filename.split('.')[-1],
                'file': file
            }

            processedFiles.append(file_info)

        FileUploadModule.SaveFile(recordId,userId,processedFiles)

        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)

@FileUploadAPI.route('/FileList/<recordId>',methods=['GET'])
@SessionManagement('Admin,Lead,Dev')
def FileList(recordId):
    try:
        response = Response()
        response.Data = FileUploadModule.GetFileSubmission(recordId)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False
    return jsonify(response.__dict__)

@FileUploadAPI.route('/RemoveFile/<recordId>',methods=['GET'])
@SessionManagement('Admin,Lead,Dev')
def RemoveFile(recordId):
    try:        
        userId = GetUserSessionDetails()["USER_ID"]
        response = Response()
        response.Data = FileUploadModule.RemoveFile(recordId,userId)
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False
    return jsonify(response.__dict__)

@FileUploadAPI.route('/FileListResource/<recordId>',methods=['GET'])
@SessionManagement('Admin,Lead,Dev')
def FileListResource(recordId):
    try:
        response = Response()
        resource = {};

        resource["Fields"] = {
                "ID" : {"type" : "string"},
                "FileName" : {"type" : "string"},                
                "FileType" : {"type" : "string"},
                "CreatedOn" : {"type" : "string"},
                "StoredFileName" : {"type" : "string"},
            }
        resource["GridHeight"] = "500px"
        resource["Columns"] = [
            {
                "title" : "Delete",
                "template": "<button class=\"btn btn-outline-danger\" onclick='DeleteRecord(\"#: ID #\")'> <i class=\"mdi mdi-delete\"> </button>",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "title" : "Download",
                "template": "<button class=\"btn btn-outline-warning\" onclick='DownloadFile(\"#: StoredFileName #\")'> <i class=\"mdi mdi-file-multiple\"> </button>",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "title" : "View",
                "template": "<button class=\"btn btn-outline-secondary\" onclick='ViewFile(\"#: StoredFileName #\",\"#: FileType #\")'> <i class=\"mdi mdi-eye\"> </button>",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "field" : "FileName",
                "title" : "Filename",
                "width":200,
            },
            {
                "field" : "FileType",
                "title" : "Filetype",
                "width":200,
            },
            {
                "field" : "CreatedOn",
                "title" : "Upload date",
                "format" : "{0:dd/MM/ yyyy}",
                "width": 200,            
            },  
        ]

        resource["DeleteUrl"] = "FileUploadAPI/RemoveFile/"
        resource["ReadURL"] = "FileUploadAPI/FileList/"+recordId
        response.Data = resource
        response.WasSuccessful = True

    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)


@FileUploadAPI.route('/ReadOnlyFileListResource/<recordId>',methods=['GET'])
@SessionManagement('Admin,Lead,Dev')
def ReadOnlyFileListResource(recordId):
    try:
        response = Response()
        resource = {};

        resource["Fields"] = {
                "ID" : {"type" : "string"},
                "FileName" : {"type" : "string"},                
                "FileType" : {"type" : "string"},
                "CreatedOn" : {"type" : "string"},
                "StoredFileName" : {"type" : "string"},
            }
        resource["GridHeight"] = "500px"
        resource["Columns"] = [
            {
                "title" : "Download",
                "template": "<button class=\"btn btn-outline-warning\" onclick='DownloadFile(\"#: StoredFileName #\")'> <i class=\"mdi mdi-file-multiple\"> </button>",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "title" : "View",
                "template": "<button class=\"btn btn-outline-secondary\" onclick='ViewFile(\"#: StoredFileName #\",\"#: FileType #\")'> <i class=\"mdi mdi-eye\"> </button>",
                "excludeFromExport": True,
                "width":80,
            },
            {
                "field" : "FileName",
                "title" : "Filename",
                "width":200,
            },
            {
                "field" : "FileType",
                "title" : "Filetype",
                "width":200,
            },
            {
                "field" : "CreatedOn",
                "title" : "Upload date",
                "format" : "{0:dd/MM/ yyyy}",
                "width": 200,            
            },  
        ]

        resource["ReadURL"] = "FileUploadAPI/FileList/"+recordId
        response.Data = resource
        response.WasSuccessful = True

    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False

    return jsonify(response.__dict__)