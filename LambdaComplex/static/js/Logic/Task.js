var taskIds = {
    taskName: "#txtTaskName",
    taskDeadLine: "#dtExpectedDeadLine",
    taskDescription: "#txtTaskDescription",
    taskRemarks: "#txtTaskRemarks",
    taskRating: "#rtTaskRating",
    taskDeveloper: "#hdnDeveloper",

    taskId: "#hdnTaskId",
    taskParentId: "#hdnParentId",
    taskCreatedBy: "#hdnTaskCreatedBy",
}

function InitTaskCreate() {
    try {
        $(taskIds.taskDescription).kendoEditor(kendoEditorConfig($(taskIds.taskDescription).val()));
        $(taskIds.taskRating).kendoRating();
    }
    catch (ex) {
        toastr.error("Error while initing task create: " + ex.message);
    }
}
function InitTaskUpdate() {
    try {
        $(taskIds.taskDescription).kendoEditor(kendoEditorConfig($(taskIds.taskDescription).val()));
        var deadLine = new Date($(taskIds.taskDeadLine).attr('valueAttr')).toISOString().slice(0, 10);
        $(taskIds.taskDeadLine).val(deadLine);
        $(taskIds.taskRating).kendoRating();
    }
    catch (ex) {
        toastr.error("Error while initing task create: " + ex.message);
    }
}


function CreateTask() {
    try {
        if (!ValidateForm()) return;

        ConfirmationAlert("Create task...", "Are you sure you want to create new task for this project?", function (value) {
            var dataToSend = {
                TaskName: $(taskIds.taskName).val(),
                TaskDescription: $(taskIds.taskDescription).val(),
                TaskDeadLine: $(taskIds.taskDeadLine).val(),
                TaskRemarks: $(taskIds.taskRemarks).val(),
                TaskRating: $(taskIds.taskRating).val(),
                AssignedTo: $(taskIds.taskDeveloper).val(),
                ParentID: $(taskIds.taskParentId).val(),
                UserID: $(sessionIds.userId).val(),
            }

            var url = "TaskAPI/CreateTask/";
            AjaxPOSTRequest(url, dataToSend, function (response) {
                response = SafeJSONparse(response);
                if (response.WasSuccessful) {
                    AlertSuccess("Task created successfully");
                    RefreshDataView();
                }
                else {
                    AlertError("Task creation error: " + response.Message);
                }
            }, function (error) {
                Toastr.error(str(error));
            }, true, true, true);
        });
    }
    catch (ex) {
        toastr.error("Error while creating task " + ex.message);
    }
}
function UpdateTask() {
    try {
        if (!ValidateForm()) return;

        ConfirmationAlert("Update task...", "Are you sure you want to update this task?", function (value) {
            var dataToSend = {
                TaskName: $(taskIds.taskName).val(),
                TaskDescription: $(taskIds.taskDescription).val(),
                TaskDeadLine: $(taskIds.taskDeadLine).val(),
                TaskRemarks: $(taskIds.taskRemarks).val(),
                TaskRating: $(taskIds.taskRating).val(),
                AssignedTo: $(taskIds.taskDeveloper).val(),
                ParentID: $(taskIds.taskParentId).val(),
                UserID: $(sessionIds.userId).val(),
                RecordID: $(taskIds.taskId).val(),
            }

            var url = "TaskAPI/UpdateTask/";
            AjaxPOSTRequest(url, dataToSend, function (response) {
                response = SafeJSONparse(response);
                if (response.WasSuccessful) {
                    AlertSuccess("Task updated successfully");
                    RefreshDataView();
                }
                else {
                    AlertError("Task updation error: " + response.Message);
                }
            }, function (error) {
                Toastr.error(str(error));
            }, true, true, true);
        });
    }
    catch (ex) {
        toastr.error("Error while updating task " + ex.message);
    }
}
function ChildUpdateTask() {
    try {
        YesNoCancelAlert(
            "Report/Request...",
            "You are about to update this task, how would you like it updated?",
            "Change request",
            "Progress report",
            ChangeRequestForTask,
            ProgressReportOnTask
        );
    }
    catch (ex) {
        toastr.error("Error while child updating the task: " + ex.message);
    }
}
function ChangeRequestForTask() {
    try {
        if (!ValidateForm()) return;

        ConfirmationAlert("Change request...", "Are you sure you want to provide change request for this task?", function (value) {
            var dataToSend = {
                TaskName: $(taskIds.taskName).val(),
                TaskDescription: $(taskIds.taskDescription).val(),
                TaskDeadLine: $(taskIds.taskDeadLine).val(),
                TaskRemarks: $(taskIds.taskRemarks).val(),
                TaskRating: $(taskIds.taskRating).val(),
                AssignedTo: $(taskIds.taskDeveloper).val(),
                ParentID: $(taskIds.taskParentId).val(),
                UserID: $(sessionIds.userId).val(),
                RecordID: $(taskIds.taskId).val(),
                CreatedBy: $(taskIds.taskCreatedBy).val(),
            }

            var url = "TaskAPI/ChildUpdateTaskCHR/";
            AjaxPOSTRequest(url, dataToSend, function (response) {
                response = SafeJSONparse(response);
                if (response.WasSuccessful) {
                    AlertSuccess("Task requested successfully");
                    RefreshDataView();
                }
                else {
                    AlertError("Task request error: " + response.Message);
                }
            }, function (error) {
                Toastr.error(str(error));
            }, true, true, true);
        });
    }
    catch (ex) {
        toastr.error("Error while requesting for task " + ex.message);
    }
}
function ProgressReportOnTask() {
    try {
        if (!ValidateForm()) return;

        ConfirmationAlert("Progress report...", "Are you sure you want to provide progress report on this task?", function (value) {
            var dataToSend = {
                TaskName: $(taskIds.taskName).val(),
                TaskDescription: $(taskIds.taskDescription).val(),
                TaskDeadLine: $(taskIds.taskDeadLine).val(),
                TaskRemarks: $(taskIds.taskRemarks).val(),
                TaskRating: $(taskIds.taskRating).val(),
                AssignedTo: $(taskIds.taskDeveloper).val(),
                ParentID: $(taskIds.taskParentId).val(),
                UserID: $(sessionIds.userId).val(),
                RecordID: $(taskIds.taskId).val(),
                CreatedBy: $(taskIds.taskCreatedBy).val(),
            }

            var url = "TaskAPI/ChildUpdateTaskPGR/";
            AjaxPOSTRequest(url, dataToSend, function (response) {
                response = SafeJSONparse(response);
                if (response.WasSuccessful) {
                    AlertSuccess("Reported successfully");
                    RefreshDataView();
                }
                else {
                    AlertError("Task reporting error: " + response.Message);
                }
            }, function (error) {
                Toastr.error(str(error));
            }, true, true, true);
        });
    }
    catch (ex) {
        toastr.error("Error while reporting on task " + ex.message);
    }
}

function ApproveTaskEdit(taskChangeId = null) {
    try {
        if (IsNullOrEmpty(taskChangeId)) return;
        ConfirmationAlert('Task', 'Do you really want to approve this changes/report in task?', function (value) {
            var url = 'TaskAPI/AcceptChangesTask/' + taskChangeId
            AjaxGETRequest(
                url,
                function (response) {
                    response = SafeJSONparse(response);
                    if (response.WasSuccessful) {
                        AlertSuccess("Accepted changes....");
                        RefreshDataView();
                    }
                    else {
                        toastr.error("Alas! Error accepeting changes: " + response.Message);
                    }
                },
                function (error) {

                }, true, true, true
            );
        });
    }
    catch (ex) {
        toastr.error("Error while accepting task changes: " + ex.message);
    }
}
function RejectTaskEdit(taskChangeId = null) {
    try {
        if (IsNullOrEmpty(taskChangeId)) return;
        ConfirmationAlert('Task', 'Do you really want to reject this changes/report in task?', function (value) {
            var url = 'TaskAPI/RejectChangesTask/' + taskChangeId
            AjaxGETRequest(
                url,
                function (response) {
                    response = SafeJSONparse(response);
                    if (response.WasSuccessful) {
                        AlertWarning("Rejected changes....");
                        RefreshDataView();
                    }
                    else {
                        toastr.error("Alas! Error rejecting changes: " + response.Message);
                    }
                },
                function (error) {

                }, true, true, true
            );
        });
    }
    catch (ex) {
        toastr.error("Error while rejecting task changes: " + ex.message);
    }
}

function FinishTask(taskChangeId = null) {
    try {
        if (IsNullOrEmpty(taskChangeId)) return;
        ConfirmationAlert('Task', 'Do you really want to finsh this task?', function (value) {
            var url = 'TaskAPI/FinishTask/' + taskChangeId
            AjaxGETRequest(
                url,
                function (response) {
                    response = SafeJSONparse(response);
                    if (response.WasSuccessful) {
                        AlertSuccess("Yay! Finished task....");
                        RefreshDataView();
                    }
                    else {
                        toastr.error("Alas! Error finishing task: " + response.Message);
                    }
                },
                function (error) {

                }, true, true, true
            );
        });
    }
    catch (ex) {
        toastr.error("Error while finishing task: " + ex.message);
    }
}
function AbandonTask(taskChangeId = null) {
    try {
        if (IsNullOrEmpty(taskChangeId)) return;
        ConfirmationAlert('Task', 'Do you really want to abandon this task?', function (value) {
            var url = 'TaskAPI/AbandonTask/' + taskChangeId
            AjaxGETRequest(
                url,
                function (response) {
                    response = SafeJSONparse(response);
                    if (response.WasSuccessful) {
                        AlertWarning("Abandoned task....");
                        RefreshDataView();
                    }
                    else {
                        toastr.error("Alas! Error abandoning task: " + response.Message);
                    }
                },
                function (error) {

                }, true, true, true
            );
        });
    }
    catch (ex) {
        toastr.error("Error while finishing task: " + ex.message);
    }
}


function RebootTask(taskID = null) {
    try {
        if (IsNullOrEmpty(taskID)) return;
        ConfirmationAlert('Task', 'Do you really want to reboot this task?', function (value) {
            var url = 'TaskAPI/RebootTask/' + taskID
            AjaxGETRequest(
                url,
                function (response) {
                    response = SafeJSONparse(response);
                    if (response.WasSuccessful) {
                        AlertWarning("Rebooted task!");
                        RefreshDataView();
                    }
                    else {
                        toastr.error("Alas! Error rebooting task: " + response.Message);
                    }
                },
                function (error) {

                }, true, true, true
            );
        });
    }
    catch (ex) {
        toastr.error("Error while rebooting task: " + ex.message);
    }
}
function ReversionTask(taskChangeID = null) {
    try {
        if (IsNullOrEmpty(taskChangeID)) return;
        ConfirmationAlert('Task', 'Do you really want to reversion this task to an older version?', function (value) {
            var url = 'TaskAPI/ReversionTask/' + taskChangeID
            AjaxGETRequest(
                url,
                function (response) {
                    response = SafeJSONparse(response);
                    if (response.WasSuccessful) {
                        AlertWarning("Reversioned task!");
                        RefreshDataView();
                    }
                    else {
                        toastr.error("Alas! Error reversioning task: " + response.Message);
                    }
                },
                function (error) {

                }, true, true, true
            );
        });
    }
    catch (ex) {
        toastr.error("Error while reversioning task: " + ex.message);
    }
}
function LoadTaskReversionView(recordID = null) {
    try {
        if (IsNullOrEmpty(recordID)) return;
        var resourceUrl = "TaskAPI/TaskReversionGridViewResource/" + recordID;
        LoadGridView(resourceUrl, true, true, divMainPage);
    }
    catch (ex) {
        toastr.error('Error while displaying Task reversion tracking in grid: ' + ex.message);
    }
}


function DisplayMacroTrackingForTaskInGrid(recordID = null) {
    try {
        if (IsNullOrEmpty(recordID)) return;
        var resourceUrl = "TaskAPI/MacroTrackingGridResource/" + recordID;
        LoadGridView(resourceUrl, true, true, divMainPage);
    }
    catch (ex) {
        toastr.error('Error while displaying Macro Tracking for the task in grid: ' + ex.message);
    }
}
function DisplayMacroTrackingForTaskInTimeLine(recordID = null) {
    try {
        if (IsNullOrEmpty(recordID)) return;
        var resourceUrl = "TaskAPI/MacroTrackingTimeLineRead/" + recordID;
        LoadTimeLineView(resourceUrl, true, true, divMainPage);
    }
    catch (ex) {
        toastr.error('Error while displaying Macro Tracking for the task in timeline: ' + ex.message);
    }
}
function DisplayMicroTrackingForTaskInGrid(recordID = null) {
    try {
        if (IsNullOrEmpty(recordID)) return;
        var resourceUrl = "TaskAPI/MicroTrackingGridResource/" + recordID;
        LoadGridView(resourceUrl, true, true, divMainPage);
    }
    catch (ex) {
        toastr.error('Error while displaying Micro Tracking for the task in grid: ' + ex.message);
    }
}
function DisplayMicroTrackingForTaskInTimeLine(recordID = null) {
    try {
        if (IsNullOrEmpty(recordID)) return;
        var resourceUrl = "TaskAPI/MicroTrackingTimeLineRead/" + recordID;
        LoadTimeLineView(resourceUrl, true, true, divMainPage);
    }
    catch (ex) {
        toastr.error('Error while displaying Micro Tracking for the task in timeline: ' + ex.message);
    }
}