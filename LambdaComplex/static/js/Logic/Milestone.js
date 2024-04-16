var milestoneIds = {
    milestoneName: "#txtMilestoneName",
    milestoneDeadLine: "#dtExpectedDeadLine",
    milestoneDescription: "#txtMilestoneDescription",
    milestoneRemarks: "#txtMilestoneRemarks",
    milestoneRating: "#rtMilestoneRating",
    milestoneLeader: "#cmbLeader",

    milestoneId: "#hdnMilestoneId",
    milestoneParentId: "#hdnParentId",
    milestoneCreatedBy: "#hdnMilestoneCreatedBy",
}

function InitMilestoneCreate() {
    try {
        $(milestoneIds.milestoneDescription).kendoEditor(kendoEditorConfig($(milestoneIds.milestoneDescription).val()));
        $(milestoneIds.milestoneRating).kendoRating();

        var projectId = $(milestoneIds.milestoneParentId).val();
        $(milestoneIds.milestoneLeader).kendoComboBox({
            placeholder: "Select Leader...",
            dataTextField: "UserName",
            dataValueField: "ID",
            dataSource: {
                transport: {
                    read: function (options) {
                        var result = QuickAPIRead('UserAPI/GetLeadsOfProject/' + projectId);
                        if (result)
                            options.success(result);
                    }
                }
            },
            filter: "contains",
            suggest: true,
            separator: ",",
            change: function (e) {

            }
        });
    }
    catch (ex) {
        toastr.error("Error while initing milestone create: " + ex.message);
    }
}
function InitMilestoneUpdate() {
    try {
        $(milestoneIds.milestoneDescription).kendoEditor(kendoEditorConfig($(milestoneIds.milestoneDescription).val()));
        var deadLine = new Date($(milestoneIds.milestoneDeadLine).attr('valueAttr')).toISOString().slice(0, 10);
        $(milestoneIds.milestoneDeadLine).val(deadLine);
        $(milestoneIds.milestoneRating).kendoRating();

        var projectId = $(milestoneIds.milestoneParentId).val();
        $(milestoneIds.milestoneLeader).kendoComboBox({
            placeholder: "Select Leader...",
            dataTextField: "UserName",
            dataValueField: "ID",
            dataSource: {
                transport: {
                    read: function (options) {
                        var result = QuickAPIRead('UserAPI/GetLeadsOfProject/' + projectId);
                        if (result)
                            options.success(result);
                    }
                }
            },
            filter: "contains",
            suggest: true,
            readonly: true,
            separator: ",",
            change: function (e) {

            }
        });

    }
    catch (ex) {
        toastr.error("Error while initing milestone create: " + ex.message);
    }
}


function CreateMilestone() {
    try {
        if (!ValidateForm()) return;

        ConfirmationAlert("Create milestone...", "Are you sure you want to create new milestone for this project?", function (value) {
            var dataToSend = {
                MilestoneName: $(milestoneIds.milestoneName).val(),
                MilestoneDescription: $(milestoneIds.milestoneDescription).val(),
                MilestoneDeadLine: $(milestoneIds.milestoneDeadLine).val(),
                MilestoneRemarks: $(milestoneIds.milestoneRemarks).val(),
                MilestoneRating: $(milestoneIds.milestoneRating).val(),
                AssignedTo: $(milestoneIds.milestoneLeader).val(),
                ParentID: $(milestoneIds.milestoneParentId).val(),
                UserID: $(sessionIds.userId).val(),
            }

            var url = "MilestoneAPI/CreateMilestone/";
            AjaxPOSTRequest(url, dataToSend, function (response) {
                response = SafeJSONparse(response);
                if (response.WasSuccessful) {
                    AlertSuccess("Milestone created successfully");
                    RefreshDataView();
                }
                else {
                    AlertError("Milestone creation error: " + response.Message);
                }
            }, function (error) {
                Toastr.error(str(error));
            }, true, true, true);
        });
    }
    catch (ex) {
        toastr.error("Error while creating milestone " + ex.message);
    }
}
function UpdateMilestone() {
    try {
        if (!ValidateForm()) return;

        ConfirmationAlert("Update milestone...", "Are you sure you want to update this milestone?", function (value) {
            var dataToSend = {
                MilestoneName: $(milestoneIds.milestoneName).val(),
                MilestoneDescription: $(milestoneIds.milestoneDescription).val(),
                MilestoneDeadLine: $(milestoneIds.milestoneDeadLine).val(),
                MilestoneRemarks: $(milestoneIds.milestoneRemarks).val(),
                MilestoneRating: $(milestoneIds.milestoneRating).val(),
                AssignedTo: $(milestoneIds.milestoneLeader).val(),
                ParentID: $(milestoneIds.milestoneParentId).val(),
                UserID: $(sessionIds.userId).val(),
                RecordID: $(milestoneIds.milestoneId).val(),
            }

            var url = "MilestoneAPI/UpdateMilestone/";
            AjaxPOSTRequest(url, dataToSend, function (response) {
                response = SafeJSONparse(response);
                if (response.WasSuccessful) {
                    AlertSuccess("Milestone updated successfully");
                    RefreshDataView();
                }
                else {
                    AlertError("Milestone updation error: " + response.Message);
                }
            }, function (error) {
                Toastr.error(str(error));
            }, true, true, true);
        });
    }
    catch (ex) {
        toastr.error("Error while updating milestone " + ex.message);
    }
}
function ChildUpdateMilestone() {
    try {
        YesNoCancelAlert(
            "Report/Request...",
            "You are about to update this milestone, how would you like it updated?",
            "Change request",
            "Progress report",
            ChangeRequestForMilestone,
            ProgressReportOnMilestone
        );
    }
    catch (ex) {
        toastr.error("Error while child updating the milestone: " + ex.message);
    }
}
function ChangeRequestForMilestone() {
    try {
        if (!ValidateForm()) return;

        ConfirmationAlert("Change request...", "Are you sure you want to provide change request for this milestone?", function (value) {
            var dataToSend = {
                MilestoneName: $(milestoneIds.milestoneName).val(),
                MilestoneDescription: $(milestoneIds.milestoneDescription).val(),
                MilestoneDeadLine: $(milestoneIds.milestoneDeadLine).val(),
                MilestoneRemarks: $(milestoneIds.milestoneRemarks).val(),
                MilestoneRating: $(milestoneIds.milestoneRating).val(),
                AssignedTo: $(milestoneIds.milestoneLeader).val(),
                ParentID: $(milestoneIds.milestoneParentId).val(),
                UserID: $(sessionIds.userId).val(),
                RecordID: $(milestoneIds.milestoneId).val(),
                CreatedBy: $(milestoneIds.milestoneCreatedBy).val(),
            }

            var url = "MilestoneAPI/ChildUpdateMilestoneCHR/";
            AjaxPOSTRequest(url, dataToSend, function (response) {
                response = SafeJSONparse(response);
                if (response.WasSuccessful) {
                    AlertSuccess("Milestone requested successfully");
                    RefreshDataView();
                }
                else {
                    AlertError("Milestone request error: " + response.Message);
                }
            }, function (error) {
                Toastr.error(str(error));
            }, true, true, true);
        });
    }
    catch (ex) {
        toastr.error("Error while requesting for milestone " + ex.message);
    }
}
function ProgressReportOnMilestone() {
    try {
        if (!ValidateForm()) return;

        ConfirmationAlert("Progress report...", "Are you sure you want to provide progress report on this milestone?", function (value) {
            var dataToSend = {
                MilestoneName: $(milestoneIds.milestoneName).val(),
                MilestoneDescription: $(milestoneIds.milestoneDescription).val(),
                MilestoneDeadLine: $(milestoneIds.milestoneDeadLine).val(),
                MilestoneRemarks: $(milestoneIds.milestoneRemarks).val(),
                MilestoneRating: $(milestoneIds.milestoneRating).val(),
                AssignedTo: $(milestoneIds.milestoneLeader).val(),
                ParentID: $(milestoneIds.milestoneParentId).val(),
                UserID: $(sessionIds.userId).val(),
                RecordID: $(milestoneIds.milestoneId).val(),
                CreatedBy: $(milestoneIds.milestoneCreatedBy).val(),
            }

            var url = "MilestoneAPI/ChildUpdateMilestonePGR/";
            AjaxPOSTRequest(url, dataToSend, function (response) {
                response = SafeJSONparse(response);
                if (response.WasSuccessful) {
                    AlertSuccess("Reported successfully");
                    RefreshDataView();
                }
                else {
                    AlertError("Milestone reporting error: " + response.Message);
                }
            }, function (error) {
                Toastr.error(str(error));
            }, true, true, true);
        });
    }
    catch (ex) {
        toastr.error("Error while reporting on milestone " + ex.message);
    }
}

function ApproveMilestoneEdit(milestoneChangeId = null) {
    try {
        if (IsNullOrEmpty(milestoneChangeId)) return;
        ConfirmationAlert('Milestone', 'Do you really want to approve this changes/report in milestone?', function (value) {
            var url = 'MilestoneAPI/AcceptChangesMilestone/' + milestoneChangeId
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
        toastr.error("Error while accepting milestone changes: " + ex.message);
    }
}
function RejectMilestoneEdit(milestoneChangeId = null) {
    try {
        if (IsNullOrEmpty(milestoneChangeId)) return;
        ConfirmationAlert('Milestone', 'Do you really want to reject this changes/report in milestone?', function (value) {
            var url = 'MilestoneAPI/RejectChangesMilestone/' + milestoneChangeId
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
        toastr.error("Error while rejecting milestone changes: " + ex.message);
    }
}

function FinishMilestone(milestoneChangeId = null) {
    try {
        if (IsNullOrEmpty(milestoneChangeId)) return;
        ConfirmationAlert('Milestone', 'Do you really want to finsh this milestone?', function (value) {
            var url = 'MilestoneAPI/FinishMilestone/' + milestoneChangeId
            AjaxGETRequest(
                url,
                function (response) {
                    response = SafeJSONparse(response);
                    if (response.WasSuccessful) {
                        AlertSuccess("Yay! Finished milestone....");
                        RefreshDataView();
                    }
                    else {
                        toastr.error("Alas! Error finishing milestone: " + response.Message);
                    }
                },
                function (error) {

                }, true, true, true
            );
        });
    }
    catch (ex) {
        toastr.error("Error while finishing milestone: " + ex.message);
    }
}
function AbandonMilestone(milestoneChangeId = null) {
    try {
        if (IsNullOrEmpty(milestoneChangeId)) return;
        ConfirmationAlert('Milestone', 'Do you really want to abandon this milestone?', function (value) {
            var url = 'MilestoneAPI/AbandonMilestone/' + milestoneChangeId
            AjaxGETRequest(
                url,
                function (response) {
                    response = SafeJSONparse(response);
                    if (response.WasSuccessful) {
                        AlertWarning("Abandoned milestone....");
                        RefreshDataView();
                    }
                    else {
                        toastr.error("Alas! Error abandoning milestone: " + response.Message);
                    }
                },
                function (error) {

                }, true, true, true
            );
        });
    }
    catch (ex) {
        toastr.error("Error while finishing milestone: " + ex.message);
    }
}

function DisplayMacroTrackingForMilestoneInGrid(recordID = null) {
    try {
        if (IsNullOrEmpty(recordID)) return;
        var resourceUrl = "MilestoneAPI/MacroTrackingGridResource/" + recordID;
        LoadGridView(resourceUrl, true, true, divMainPage);
    }
    catch (ex) {
        toastr.error('Error while displaying Macro Tracking for the milestone in grid: ' + ex.message);
    }
}
function DisplayMacroTrackingForMilestoneInTimeLine(recordID = null) {
    try {
        if (IsNullOrEmpty(recordID)) return;
        var resourceUrl = "MilestoneAPI/MacroTrackingTimeLineRead/" + recordID;
        LoadTimeLineView(resourceUrl, true, true, divMainPage);
    }
    catch (ex) {
        toastr.error('Error while displaying Macro Tracking for the milestone in timeline: ' + ex.message);
    }
}
function DisplayMicroTrackingForMilestoneInGrid(recordID = null) {
    try {
        if (IsNullOrEmpty(recordID)) return;
        var resourceUrl = "MilestoneAPI/MicroTrackingGridResource/" + recordID;
        LoadGridView(resourceUrl, true, true, divMainPage);
    }
    catch (ex) {
        toastr.error('Error while displaying Micro Tracking for the milestone in grid: ' + ex.message);
    }
}
function DisplayMicroTrackingForMilestoneInTimeLine(recordID = null) {
    try {
        if (IsNullOrEmpty(recordID)) return;
        var resourceUrl = "MilestoneAPI/MicroTrackingTimeLineRead/" + recordID;
        LoadTimeLineView(resourceUrl, true, true, divMainPage);
    }
    catch (ex) {
        toastr.error('Error while displaying Micro Tracking for the milestone in timeline: ' + ex.message);
    }
}

