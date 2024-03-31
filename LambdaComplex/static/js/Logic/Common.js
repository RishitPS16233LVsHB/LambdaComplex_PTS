/** 
 * Base addresses for making MVC or API calls to Manage Web application state and Manage Database data
 */
const apiHost = "http://127.0.0.1:5000/api/"
const mvcHost = "http://127.0.0.1:5000/"

const sessionIds = {
    userId: "#USER_ID",
    role: "#ROLE",
    userName: "#USERNAME",
};

/**
 * @param {any} url "URL or Controller action, API or web url data"
 * @param {any} data "if POST request was to be made"
 * @param {any} successCallback "Callback function for when web request was a success"
 * @param {any} errorCallback "Callback function for when web request was an error"
 * @param {any} isAPI "To get HTML or Web Application state related then set this to false but data or database management api are to be called then set this to true"
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

function SetViewInMainPageUsingGet(url, isAsync, isLoader) {
    try {
        AjaxGETRequest(url, function (htmlResponse) {

            $("#divMainPage").html(htmlResponse);
        }, function (error) {

        }, isLoader, isAsync, false);
    }
    catch (e) {
        toastr.error("Error occured while fixing view in MainPage: " + e.message);
    }
}




function SetViewInMainPageUsingPost(url, data, isAsync, isLoader) {
    try {
        AjaxPOSTRequest(url, data, function (htmlResponse) {
            $("#divMainPage").html(htmlResponse);
        }, function (error) {

        }, isLoader, isAsync, false);
    }
    catch (e) {
        toastr.error("Error occured while fixing view in MainPage: " + e.message);
    }
}


function IsNullOrEmpty(item) {
    if (item === undefined || item === null || item === '') {
        return true;
    }
    return false;
}


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


// Success message
function AlertSuccess(message) {
    Swal.fire({
        icon: 'success',
        title: 'Success',
        text: message
    });
}

// Error message
function AlertError(message) {
    Swal.fire({
        icon: 'error',
        title: 'Error',
        text: message
    });
}

// Warning message
function AlertWarning(message) {
    Swal.fire({
        icon: 'warning',
        title: 'Warning',
        text: message
    });
}

// Info message
function AlertInfo(message) {
    Swal.fire({
        icon: 'info',
        title: 'Info',
        text: message
    });
}

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

function safeJSONparse(obj) {
    if (typeof (obj) === 'string') return JSON.parse(obj);

    return obj;
}

function LoadListView(resourceUrl, isAsync, isLoader) {
    let dataToSend = {
        ResourceUrl: resourceUrl,
        RenderType: "list"
    }
    SetViewInMainPageUsingPost('DataView/Rendering/', dataToSend, isAsync, isLoader);
}

function LoadGridView(resourceUrl, isAsync, isLoader) {
    let dataToSend = {
        ResourceUrl: resourceUrl,
        RenderType: "grid"
    }
    SetViewInMainPageUsingPost('DataView/Rendering/', dataToSend, isAsync, isLoader);
}