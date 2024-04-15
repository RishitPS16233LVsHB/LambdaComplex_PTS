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
