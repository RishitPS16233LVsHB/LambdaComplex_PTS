/**
 * Base addresses for making MVC or API calls to Manage Web application state and Manage Database data
 */
const apiHost = "http://127.0.0.1:5000/api/"
const mvcHost = "http://127.0.0.1:5000/"
const uploadUrl = "FileUploadAPI/Upload"

const divMainPage = "#divMainPage"
const sessionIds = {
    userId: "#USER_ID",
    role: "#ROLE",
    userName: "#USERNAME",
};

function kendoEditorConfig(value) {
    return {
        encoded: true,
        value: value,
        tools: [
            "bold", "italic", "underline", "undo", "redo", "justifyLeft", "justifyCenter", "justifyRight", "insertUnorderedList",
            "createLink", "unlink", "tableWizard", "tableProperties", "tableCellProperties", "createTable",
            "addRowAbove", "addRowBelow", "addColumnLeft", "addColumnRight", "deleteRow", "deleteColumn", "mergeCellsHorizontally",
            "mergeCellsVertically", "splitCellHorizontally", "splitCellVertically", "tableAlignLeft", "tableAlignCenter",
            "tableAlignRight", "formatting",
            {
                name: "fontName",
                items: [
                    { text: "Andale Mono", value: "\"Andale Mono\"" }, // Font-family names composed of several words should be wrapped in \" \"
                    { text: "Arial", value: "Arial" },
                    { text: "Arial Black", value: "\"Arial Black\"" },
                    { text: "Book Antiqua", value: "\"Book Antiqua\"" },
                    { text: "Comic Sans MS", value: "\"Comic Sans MS\"" },
                    { text: "Courier New", value: "\"Courier New\"" },
                    { text: "Georgia", value: "Georgia" },
                    { text: "Helvetica", value: "Helvetica" },
                    { text: "Impact", value: "Impact" },
                    { text: "Symbol", value: "Symbol" },
                    { text: "Tahoma", value: "Tahoma" },
                    { text: "Terminal", value: "Terminal" },
                    { text: "Times New Roman", value: "\"Times New Roman\"" },
                    { text: "Trebuchet MS", value: "\"Trebuchet MS\"" },
                    { text: "Verdana", value: "Verdana" },
                ]
            },
            "fontSize",
            "foreColor",
            "backColor",
        ]
    };
}

/**
 * Makes an HTTP GET request to the provided URL.
 * @param {string} url The URL to make the GET request to.
 * @param {function} successCallback Callback function to be executed upon successful response.
 * @param {function} errorCallback Callback function to be executed upon error response.
 * @param {boolean} isLoader Indicates whether to display a loader while the request is being processed.
 * @param {boolean} isAsync Indicates whether the request should be asynchronous.
 * @param {boolean} isAPI Indicates whether the request is an API call or MVC call.
 */
function AjaxGETRequest(url, successCallback, errorCallback, isLoader, isAsync, isAPI = true) {
    url = ((isAPI) ? apiHost : mvcHost) + url;

    if (isLoader)
        $("#loader-screen").show();

    $.ajax({
        url: url,
        method: "GET",
        contentType: 'application/json',
        async: isAsync,
        success: function (responseData) {
            $("#loader-screen").hide();
            if (successCallback) {
                successCallback(responseData);
            }
        },
        error: function (xhr, status, error) {
            toastr.error("error occured in AJAX GET: " + error);
            $("#loader-screen").hide();
            if (errorCallback) {
                errorCallback(error);
            }
        }
    });
}

/**
 * Makes an HTTP POST request to the provided URL.
 * @param {string} url The URL to make the POST request to.
 * @param {object} data The data to be sent in the request body.
 * @param {function} successCallback Callback function to be executed upon successful response.
 * @param {function} errorCallback Callback function to be executed upon error response.
 * @param {boolean} isLoader Indicates whether to display a loader while the request is being processed.
 * @param {boolean} isAsync Indicates whether the request should be asynchronous.
 * @param {boolean} isAPI Indicates whether the request is an API call or MVC call.
 */
function AjaxPOSTRequest(url, data, successCallback, errorCallback, isLoader, isAsync, isAPI = true) {
    url = ((isAPI) ? apiHost : mvcHost) + url;

    if (isLoader)
        $("#loader-screen").show();

    $.ajax({
        url: url,
        method: "POST",
        contentType: 'application/json',
        async: isAsync,
        data: JSON.stringify(data),
        success: function (responseData) {
            $("#loader-screen").hide();
            if (successCallback) {
                successCallback(responseData);
            }
        },
        error: function (xhr, status, error) {
            toastr.error("error occured in AJAX POST: " + error);
            $("#loader-screen").hide();
            if (errorCallback) {
                errorCallback(error);
            }
        }
    });
}

/**
 * Makes an HTTP POST request to submit form data and it is API only
 * @param {*} url 
 * @param {*} formData 
 * @param {*} successCallback 
 * @param {*} errorCallback 
 * @param {*} isLoader 
 * @param {*} isAsync 
 */
function AjaxFormDataRequest(url, formData, successCallback, errorCallback, isLoader, isAsync) {
    url = apiHost + url;

    if (isLoader)
        $("#loader-screen").show();

    $.ajax({
        url: url,
        method: "POST",
        contentType: false,
        cache: false,
        processData: false,
        async: isAsync,
        data: formData,
        success: function (responseData) {
            $("#loader-screen").hide();
            if (successCallback) {
                successCallback(responseData);
            }
        },
        error: function (xhr, status, error) {
            toastr.error("error occured in AJAX POST: " + error);
            $("#loader-screen").hide();
            if (errorCallback) {
                errorCallback(error);
            }
        }
    });
}

/**
 * Fetches HTML content from the provided URL using a GET request and sets it as the content of the main page.
 * @param {string} url The URL to fetch HTML content from.
 * @param {boolean} isAsync Indicates whether the request should be asynchronous.
 * @param {boolean} isLoader Indicates whether to display a loader while the request is being processed.
 */
function SetViewInMainPageUsingGet(url, isAsync, isLoader, element = "#divMainPage") {
    try {
        AjaxGETRequest(url, function (htmlResponse) {
            $(element).html(htmlResponse);
        }, function (error) {

        }, isLoader, isAsync, false);
    }
    catch (e) {
        toastr.error("Error occured while fixing view in MainPage: " + e.message);
    }
}

/**
 * Fetches HTML content from the provided URL using a POST request and sets it as the content of the main page.
 * @param {string} url The URL to fetch HTML content from.
 * @param {object} data The data to be sent in the request body.
 * @param {boolean} isAsync Indicates whether the request should be asynchronous.
 * @param {boolean} isLoader Indicates whether to display a loader while the request is being processed.
 */
function SetViewInMainPageUsingPost(url, data, isAsync, isLoader, element = "#divMainPage") {
    try {
        AjaxPOSTRequest(url, data, function (htmlResponse) {
            $(element).html(htmlResponse);
        }, function (error) {

        }, isLoader, isAsync, false);
    }
    catch (e) {
        toastr.error("Error occured while fixing view in MainPage: " + e.message);
    }
}


/**
 * Checks if the provided item is null, undefined, or empty.
 * @param {any} item The item to check.
 * @returns {boolean} True if the item is null, undefined, or empty; otherwise, false.
 */
function IsNullOrEmpty(item) {
    if (item === undefined || item === null || item === '' || item == 'None' || item == 'null') {
        return true;
    }
    return false;
}

/**
 * Displays a prompt dialog with custom options and executes a callback function on success.
 * @param {string} control The type of control to display (e.g., 'text', 'number', 'select').
 * @param {string} inputLable The label for the input control.
 * @param {string} placeHolder The placeholder text for the input control.
 * @param {function} successCallback Callback function to be executed on successful input.
 * @param {array} inputOptions Array of options for the input control (for select control).
 */
function PromptAlert(control, inputLable, placeHolder, successCallback, inputOptions = []) {
    Swal.fire({
        input: control,
        inputOptions: inputOptions,
        inputLabel: inputLable,
        inputPlaceholder: placeHolder,
        showCancelButton: true
    }).then((result) => {
        if (result.value) {
            successCallback(result.value);
        }
    });
}

/**
 * Displays a success message using SweetAlert.
 * @param {string} message The message to display.
 */
function AlertSuccess(message) {
    Swal.fire({
        icon: 'success',
        title: 'Success',
        text: message
    });
}

/**
 * Displays an error message using SweetAlert.
 * @param {string} message The message to display.
 */
function AlertError(message) {
    Swal.fire({
        icon: 'error',
        title: 'Error',
        text: message
    });
}

/**
 * Displays a warning message using SweetAlert.
 * @param {string} message The message to display.
 */
function AlertWarning(message) {
    Swal.fire({
        icon: 'warning',
        title: 'Warning',
        text: message
    });
}

/**
 * Displays a info message using SweetAlert.
 * @param {string} message The message to display.
 */
function AlertInfo(message) {
    Swal.fire({
        icon: 'info',
        title: 'Info',
        text: message
    });
}

/**
 * To display yes no cancel dialog and call its callbacks
 * @param {*} title
 * @param {*} yesButtonText 
 * @param {*} noButtonText 
 * @param {*} yesCallback 
 * @param {*} noCallback 
 */
function YesNoCancelAlert(title, message, yesButtonText, noButtonText, yesCallback, noCallback) {

    Swal.fire({
        title: title,
        text: message,
        showDenyButton: true,
        showCancelButton: true,
        confirmButtonText: yesButtonText,
        denyButtonText: noButtonText
    }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
            yesCallback();
        } else if (result.isDenied) {
            noCallback();
        }
    });
}


/**
 * Show loading screen
 */
function ShowLoadingScreen() {
    $("#loader-screen").show();
}
/**
 * Hide loading screen
 */
function HideLoadingScreen() {
    $("#loader-screen").hide();
}

/**
 * Displays a confirmation dialog and executes a callback function on confirmation.
 * @param {string} title The title of the confirmation dialog.
 * @param {string} text The text content of the confirmation dialog.
 * @param {function} confirmationCallback Callback function to be executed on confirmation.
 */
function ConfirmationAlert(title = 'Are you sure?', text, confirmationCallback) {
    Swal.fire({
        icon: 'info',
        title: title,
        text: text,
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes',
        cancelButtonText: 'No'
    }).then((result) => {
        if (result.isConfirmed) {
            // If user confirms, execute the confirmationCallback function
            if (typeof confirmationCallback === 'function') {
                confirmationCallback();
            }
        }
    });
}

/**
 * Safely parses a JSON string.
 * @param {string|object} obj The JSON string or object to parse.
 * @returns {object} The parsed JSON object.
 */
function SafeJSONparse(obj) {
    if (typeof (obj) === 'string') return JSON.parse(obj);

    return obj;
}

/**
 * Loads a list view using a POST request.
 * @param {string} resourceUrl The URL of the resource to load.
 * @param {boolean} isAsync Indicates whether the request should be asynchronous.
 * @param {boolean} isLoader Indicates whether to display a loader while the request is being processed.
 */
function LoadListView(resourceUrl, isAsync, isLoader, element = "#divMainPage") {
    let dataToSend = {
        ResourceUrl: resourceUrl,
        RenderType: "list",
        UserId: $(sessionIds.userId).val(),
    }
    SetViewInMainPageUsingPost('DataView/Rendering/', dataToSend, isAsync, isLoader, element);
}

/**
 * Loads a grid view using a POST request.
 * @param {string} resourceUrl The URL of the resource to load.
 * @param {boolean} isAsync Indicates whether the request should be asynchronous.
 * @param {boolean} isLoader Indicates whether to display a loader while the request is being processed.
 */
function LoadGridView(resourceUrl, isAsync, isLoader, element = "#divMainPage") {
    let dataToSend = {
        ResourceUrl: resourceUrl,
        RenderType: "grid",
        UserId: $(sessionIds.userId).val(),
    }
    SetViewInMainPageUsingPost('DataView/Rendering/', dataToSend, isAsync, isLoader, element);
}


/**
 * Loads a calendar view using a POST request.
 * @param {string} resourceUrl The URL of the resource to load.
 * @param {boolean} isAsync Indicates whether the request should be asynchronous.
 * @param {boolean} isLoader Indicates whether to display a loader while the request is being processed.
 */
function LoadCalendarView(resourceUrl, isAsync, isLoader, element = "#divMainPage") {
    let dataToSend = {
        ResourceUrl: resourceUrl,
        RenderType: "calendar",
        UserId: $(sessionIds.userId).val(),
    }
    SetViewInMainPageUsingPost('TimeTrackingView/Rendering/', dataToSend, isAsync, isLoader, element);
}

/**
 * Loads a timeline view using a POST request.
 * @param {string} resourceUrl The URL of the resource to load.
 * @param {boolean} isAsync Indicates whether the request should be asynchronous.
 * @param {boolean} isLoader Indicates whether to display a loader while the request is being processed.
 */
function LoadTimeLineView(resourceUrl, isAsync, isLoader, element = "#divMainPage") {
    let dataToSend = {
        ResourceUrl: resourceUrl,
        RenderType: "timeline",
        UserId: $(sessionIds.userId).val(),
    }
    SetViewInMainPageUsingPost('TimeTrackingView/Rendering/', dataToSend, isAsync, isLoader, element);
}

/**
 * Loads File Upload view
 * @param {*} recordId 
 * @param {*} isAsync 
 * @param {*} isLoader 
 * @param {*} element 
 */
function LoadFileSubmissionView(recordId, isAsync, isLoader, element = "#divMainPage") {
    SetViewInMainPageUsingGet('FileUpload/Upload/' + recordId, isAsync, isLoader, element);
}

function LoadReadOnlyFileView(recordId, isAsync, isLoader, element = "#divMainPage") {
    SetViewInMainPageUsingGet('FileUpload/FileReadOnly/' + recordId, isAsync, isLoader, element);
}

/**
 * validates the form and reports validity and return boolean
 * @returns 
 */
function ValidateForm() {

    var kendoValidate = false;
    try {
        var validator = $("#FORM").kendoValidator().data("kendoValidator");
        kendoValidate = validator.validate()
    }
    catch (ex) { }

    var form = document.getElementById("FORM");
    if (!form.checkValidity()) {
        form.reportValidity();
    }

    return form.checkValidity();
}

/**
 * 
 * @param {string} url GET request url only
 * @returns JSON object on success or empty object on error returned from URL
 */
function QuickAPIRead(url) {
    try {
        var result = {};
        AjaxGETRequest(url, function (response) {
            response = SafeJSONparse(response);
            if (response.WasSuccessful) {
                result = response.Data;
            }
        },
            function (error) {

            }, false, false, true);

        return result;
    }
    catch (ex) {
        toastr.error("error while quick reading " + ex.message);
    }
    return result;
}

/**
 * tries to convert escaped html string to html string
 * @param {*} htmlString 
 * @returns 
 */
function DecodeHtmlEntities(htmlString) {
    var textarea = document.createElement("textarea");
    textarea.innerHTML = htmlString;
    return textarea.value;
}

function DownloadFile(fileName) {
    // Static URL
    var url = `/static/Uploads/` + fileName;

    // Create a new anchor element
    var a = document.createElement('a');
    // Set the href attribute to the static URL
    a.href = url;
    // Set the download attribute to the desired file name
    a.download = fileName;

    // Append the anchor element to the body
    document.body.appendChild(a);

    // Trigger a click event on the anchor element
    a.click();

    // Clean up: remove the anchor element from the DOM
    document.body.removeChild(a);
}
