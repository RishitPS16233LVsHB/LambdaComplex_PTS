import json
from flask import jsonify, Blueprint
from SessionManagement import SessionManagement
from LambdaComplex_Entities.Common import Response

TestAPI = Blueprint("TestAPI",__name__)


@TestAPI.route('/DataRead/')
@SessionManagement('Admin,Lead,Dev')
def DataRead():
    response = Response()
    response.WasSuccessful = True
    response.Data =  [
        {
            "ID": 1,
            "Name": "John Doe",
            "Age": 30,
            "JoiningDate": "2023-01-15",
            "Progress": 50,
            "Rating": 4.2,
            "availability": 1
        },
        {
            "ID": 2,
            "Name": "Jane Smith",
            "Age": 25,
            "JoiningDate": "2022-11-20",
            "Progress": 75,
            "Rating": 3.9,
            "availability": 0
        },
        {
            "ID": 3,
            "Name": "Michael Johnson",
            "Age": 35,
            "JoiningDate": "2023-03-05",
            "Progress": 90,
            "Rating": 4.5,
            "availability": 1
        },        
        {
            "ID": 4,
            "Name": "John Doe",
            "Age": 30,
            "JoiningDate": "2023-01-15",
            "Progress": 50,
            "Rating": 4.2,
            "availability": 1
        },
        {
            "ID": 5,
            "Name": "Jane Smith",
            "Age": 25,
            "JoiningDate": "2022-11-20",
            "Progress": 75,
            "Rating": 3.9,
            "availability": 0
        },
        {
            "ID": 6,
            "Name": "Michael Johnson",
            "Age": 35,
            "JoiningDate": "2023-03-05",
            "Progress": 90,
            "Rating": 4.5,
            "availability": 1
        },        {
            "ID": 7,
            "Name": "John Doe",
            "Age": 30,
            "JoiningDate": "2023-01-15",
            "Progress": 50,
            "Rating": 4.2,
            "availability": 1
        },
        {
            "ID": 8,
            "Name": "Jane Smith",
            "Age": 25,
            "JoiningDate": "2022-11-20",
            "Progress": 75,
            "Rating": 3.9,
            "availability": 0
        },
        {
            "ID": 9,
            "Name": "Michael Johnson",
            "Age": 35,
            "JoiningDate": "2023-03-05",
            "Progress": 90,
            "Rating": 4.5,
            "availability": 1
        },        {
            "ID": 10,
            "Name": "John Doe",
            "Age": 30,
            "JoiningDate": "2023-01-15",
            "Progress": 50,
            "Rating": 4.2,
            "availability": 1
        },
        {
            "ID": 11,
            "Name": "Jane Smith",
            "Age": 25,
            "JoiningDate": "2022-11-20",
            "Progress": 75,
            "Rating": 3.9,
            "availability": 0
        },
        {
            "ID": 12,
            "Name": "Michael Johnson",
            "Age": 35,
            "JoiningDate": "2023-03-05",
            "Progress": 90,
            "Rating": 4.5,
            "availability": 1
        },        {
            "ID": 13,
            "Name": "John Doe",
            "Age": 30,
            "JoiningDate": "2023-01-15",
            "Progress": 50,
            "Rating": 4.2,
            "availability": 1
        },
        {
            "ID": 14,
            "Name": "Jane Smith",
            "Age": 25,
            "JoiningDate": "2022-11-20",
            "Progress": 75,
            "Rating": 3.9,
            "availability": 0
        },
        {
            "ID": 15,
            "Name": "Michael Johnson",
            "Age": 35,
            "JoiningDate": "2023-03-05",
            "Progress": 90,
            "Rating": 4.5,
            "availability": 1
        },
    ]
    return jsonify(response.__dict__)


@TestAPI.route('/Resource/')
@SessionManagement('Admin,Lead,Dev')
def TestResource():    
    try:
        response = Response()
        resource = {} 

        resource["Fields"] = {
            "ID" : {"type" : "number"},
            "Name" : {"type" : "string"},
            "Age" : {"type" : "number"},
            "JoiningDate" : {"type": "date"},
            "Progress": {"type": "number"},
            "Rating": {"type": "number"},
            "Availability": {"type": "number"},
        }

        # Grid View only
        resource["Columns"] = [
            {
                "title" : "Delete",
                "template": "<button class=\"btn btn-outline-danger\" onclick='DeleteRecord(#: ID #)'> <i class=\"mdi mdi-delete\"> </button>",
                "excludeFromExport": True,
                "width":200,
            },
            {
                "title" : "Edit",
                "template": "<button class=\"btn btn-outline-primary\" onclick='LoadUpdateView(#: ID #)'> <i class=\"mdi mdi-grease-pencil\"> </button>",
                "excludeFromExport": True,
                "width":200,
            },
            {
                "title" : "Info",
                "template": "<button class=\"btn btn-outline-info\" onclick='LoadInformaticView(#: ID #)'> <i class=\"mdi mdi-information-outline\"> </button>",
                "excludeFromExport": True,
                "width":200,
            },
            {
                "field" : "ID",
                "title" : "Employee ID",
                "width": 200,
                "groupable": False,
            },
            {
                "field" : "Name",
                "title" : "Employee Name",
                "width":200,
            },
            {
                "field" : "Age",
                "title" : "Employee Age",
                "width":200,            
            },
            {
                "field" : "JoiningDate",
                "title" : "Employee joining date",
                "format" : "{0:dd/MM/ yyyy}",
                "width":200,            
            },
            {
                "field": "Availability", 
                "title": "Availability",
                "template": "<div id=\"badge#: ID #\"></div>",
                "width":200,
            },
            {
                "field": "Progress", 
                "title": "Progress",
                "template": "<div id=\"progressBar#: ID #\"></div>",
                "width":200,                
                "filterable":False,
            },
            {
                "field": "Rating", 
                "title": "Rating",
                "template": "<div id=\"ratingBar#: ID #\"></div>",
                "width":200,
            },
        ]
        
        # essential to load CRUD Views and Delete API
        resource["ReadURL"] = "TestAPI/DataRead/"
        resource["CreateViewUrl"] = "Test/CreateView/"
        resource["UpdateViewUrl"] = "Test/UpdateView/"
        resource["InformaticView"] = "Test/InformaticView/"
        # resource["EditURL"] = "TestAPI/Edit/" # not in this module
        resource["DeleteURL"] = "TestAPI/Delete/"
        
        # List View only
        resource["Template"] = """
            <div class="list-item">
                <span class="list-item__field"><strong>ID:</strong> #: ID #</span>
                <span class="list-item__field"><strong>Name:</strong> #: Name #</span>
                <span class="list-item__field"><strong>Age:</strong> #: Age #</span>
                <span class="list-item__field"><strong>Joining Date:</strong> #: JoiningDate #</span>
            </div>
        """
        response.Data = resource
        response.WasSuccessful = True
    except Exception as ex:
        response.Message = str(ex)
        response.WasSuccessful = False
        
    jsonRes = jsonify(response.__dict__) 
    return jsonRes

