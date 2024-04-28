var fileUploadIds = {
    submissions: "#flSubmissions",
    fileList: "#grdFileList",
    recordId: "#hdnRecordId",
}

function InitFileUpload() {
    try {
        var recordId = $(fileUploadIds.recordId).val();
        LoadGridView('FileUploadAPI/FileListResource/' + recordId, true, true, fileUploadIds.fileList);
    }
    catch (ex) {
        toastr.error("Error while initing File Upload: " + ex.message);
    }
}

function InitReadOnlyFile() {
    try {
        var recordId = $(fileUploadIds.recordId).val();
        LoadGridView('FileUploadAPI/ReadOnlyFileListResource/' + recordId, true, true, fileUploadIds.fileList);
    }
    catch (ex) {
        toastr.error("Error while initing File Upload: " + ex.message);
    }
}

function UploadFilesToServer() {
    try {
        var recordId = $(fileUploadIds.recordId).val();
        var formdata = new FormData();

        files = $(fileUploadIds.submissions)[0].files;
        for (var i = 0; i < files.length; i++) {
            formdata.append(i + '', files[i]);
        }
        AjaxFormDataRequest(uploadUrl + "/" + recordId, formdata, function (response) {
            response = SafeJSONparse(response);
            if (response.WasSuccessful) {
                AlertSuccess("Uploaded successfully");
                InitFileUpload();
            }
            else {
                toastr.error("Error while uploading file(s)... " + response.Message);
            }
        }, function (error) { }, false, false);
    }
    catch (ex) {
        toastr.error("Error while uploading the files to the server: " + ex.message);
    }
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


function DownloadFile(fileName, fileType) {
    // Static URL
    var url = `/static/Uploads/` + fileName;

    // Create a new anchor element
    var a = document.createElement('a');
    // Set the href attribute to the static URL
    a.href = url;
    // Set the download attribute to the desired file name
    a.target = +"_Blank";

    // Append the anchor element to the body
    document.body.appendChild(a);

    // Trigger a click event on the anchor element
    a.click();

    // Clean up: remove the anchor element from the DOM
    document.body.removeChild(a);
}


function IsValidFileTypeForBrowser(fileName) {
    // Extract the file extension
    var fileExtension = fileName.split('.').pop().toLowerCase();

    // Define an array of allowed file extensions
    var allowedExtensions = ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mpeg', 'pdf'];

    // Check if the file extension is in the allowedExtensions array
    return allowedExtensions.includes(fileExtension);
}

function ViewFile(fileName, fileType) {
    // Static URL
    var url = `/static/Uploads/` + fileName;

    // Validate the file type
    if (IsValidFileTypeForBrowser(fileType)) {
        // Create a new anchor element
        var a = document.createElement('a');
        // Set the href attribute to the static URL
        a.href = url;
        // Set the download attribute to the desired file name
        a.target = "_blank";

        // Append the anchor element to the body
        document.body.appendChild(a);

        // Trigger a click event on the anchor element
        a.click();

        // Clean up: remove the anchor element from the DOM
        document.body.removeChild(a);
    }
    else {
        AlertError("Cannot view that file type!");
    }
}