var goalIds = {
    goalName: "#txtGoalName",
    goalDeadLine: "#dtExpectedDeadLine",
    goalDescription: "#txtGoalDescription",
    goalRemarks: "#txtGoalRemarks",
    goalRating: "#rtGoalRating",

    parentId: "#hdnParentId",
    developerId: "#cmbDeveloper",
    goalId: "#hdnGoalId",
};

function InitGoalCreate() {
    try {
        $(goalIds.goalRating).kendoRating();
        $(goalIds.goalDescription).kendoEditor(kendoEditorConfig($(goalIds.goalDescription).val()));

        var milestoneId = $(goalIds.parentId).val();
        var userId = $(sessionIds.userId).val();
        $(goalIds.developerId).kendoComboBox({
            placeholder: "Select developer...",
            dataTextField: "UserName",
            dataValueField: "ID",
            dataSource: {
                transport: {
                    read: function (options) {
                        var result = QuickAPIRead('UserAPI/GetDevelopersInMilestone/' + milestoneId + "/" + userId);
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
        toastr.error("Error while initing goal create: " + ex.message);
    }
}
function InitGoalUpdate() {
    try {
        $(goalIds.goalDescription).kendoEditor(kendoEditorConfig($(goalIds.goalDescription).val()));
        var deadLine = new Date($(goalIds.goalDeadLine).attr('valueAttr')).toISOString().slice(0, 10);
        $(goalIds.goalDeadLine).val(deadLine);
        $(goalIds.goalRating).kendoRating();


        var milestoneId = $(goalIds.parentId).val();
        var userId = $(sessionIds.userId).val();
        $(goalIds.developerId).kendoComboBox({
            placeholder: "Select developer...",
            dataTextField: "UserName",
            dataValueField: "ID",
            dataSource: {
                transport: {
                    read: function (options) {
                        var result = QuickAPIRead('UserAPI/GetDevelopersInMilestone/' + milestoneId + "/" + userId);
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
        toastr.error("Error while initing goal create: " + ex.message);
    }
}

function CreateGoal() {
    try {
        debugger;
        if (!ValidateForm()) return;

        ConfirmationAlert("Create Goal...", "Are you sure you want to create new goal?", function (value) {

            var dataToSend = {
                GoalName: $(goalIds.goalName).val(),
                GoalDescription: $(goalIds.goalDescription).val(),
                GoalDeadLine: $(goalIds.goalDeadLine).val(),
                GoalRemarks: $(goalIds.goalRemarks).val(),
                GoalRating: $(goalIds.goalRating).val(),
                UserID: $(sessionIds.userId).val(),
                ParentID: $(goalIds.parentId).val(),
                AssignedTo: $(goalIds.developerId).val(),
            }

            var url = "GoalAPI/CreateGoal/";
            AjaxPOSTRequest(url, dataToSend, function (response) {
                response = SafeJSONparse(response);
                if (response.WasSuccessful) {
                    AlertSuccess("Goal created successfully");
                    RefreshDataView();
                }
                else {
                    AlertError("Goal creation error: " + response.Message);
                }
            }, function (error) {
                Toastr.error(str(error));
            }, true, true, true);
        });
    }
    catch (ex) {
        toastr.error("Error while creating goal " + ex.message);
    }
}
function UpdateGoal() {
    try {
        if (!ValidateForm()) return;

        ConfirmationAlert("Update Goal...", "Are you sure you want to update this goal?", function (value) {

            var dataToSend = {
                GoalName: $(goalIds.goalName).val(),
                GoalDescription: $(goalIds.goalDescription).val(),
                GoalDeadLine: $(goalIds.goalDeadLine).val(),
                GoalRemarks: $(goalIds.goalRemarks).val(),
                GoalRating: $(goalIds.goalRating).val(),
                RecordID: $(goalIds.goalId).val(),
                UserID: $(sessionIds.userId).val(),
                ParentID: $(goalIds.parentId).val(),
                AssignedTo: $(goalIds.developerId).val(),
            }

            var url = "GoalAPI/UpdateGoal/";
            AjaxPOSTRequest(url, dataToSend, function (response) {
                response = SafeJSONparse(response);
                if (response.WasSuccessful) {
                    AlertSuccess("Goal updated successfully");
                    RefreshDataView();
                }
                else {
                    AlertError("Goal updation error: " + response.Message);
                }
            }, function (error) {
                Toastr.error(str(error));
            }, true, true, true);
        });
    }
    catch (ex) {
        toastr.error("Error while updating goal " + ex.message);
    }
}

function FinishGoal(goalChangeID = null) {
    try {
        if (IsNullOrEmpty(goalChangeID)) return;
        ConfirmationAlert('Goal', 'Do you really want to finsh this goal?', function (value) {
            var url = 'GoalAPI/FinishGoal/' + goalChangeID
            AjaxGETRequest(
                url,
                function (response) {
                    response = SafeJSONparse(response);
                    if (response.WasSuccessful) {
                        AlertSuccess("Yay! Finished goal....");
                        RefreshDataView();
                    }
                    else {
                        toastr.error("Alas! Error finishing goal: " + response.Message);
                    }
                },
                function (error) {

                }, true, true, true
            );
        });
    }
    catch (ex) {
        toastr.error("Error while finishing goal: " + ex.message);
    }
}
function AbandonGoal(goalChangeID = null) {
    try {
        if (IsNullOrEmpty(goalChangeID)) return;
        ConfirmationAlert('Goal', 'Do you really want to abandon this goal?', function (value) {
            var url = 'GoalAPI/AbandonGoal/' + goalChangeID
            AjaxGETRequest(
                url,
                function (response) {
                    response = SafeJSONparse(response);
                    if (response.WasSuccessful) {
                        AlertWarning("Abandoned goal....");
                        RefreshDataView();
                    }
                    else {
                        toastr.error("Alas! Error abandoning goal: " + response.Message);
                    }
                },
                function (error) {

                }, true, true, true
            );
        });
    }
    catch (ex) {
        toastr.error("Error while abandoning goal: " + ex.message);
    }
}
function ReviveGoal(goalChangeID = null) {
    try {
        if (IsNullOrEmpty(goalChangeID)) return;
        ConfirmationAlert('Goal', 'Do you really want to revive this goal?', function (value) {
            var url = 'GoalAPI/ReviveGoal/' + goalChangeID
            AjaxGETRequest(
                url,
                function (response) {
                    response = SafeJSONparse(response);
                    if (response.WasSuccessful) {
                        AlertWarning("Revive goal....");
                        RefreshDataView();
                    }
                    else {
                        toastr.error("Alas! Error reviving goal: " + response.Message);
                    }
                },
                function (error) {

                }, true, true, true
            );
        });
    }
    catch (ex) {
        toastr.error("Error while reviving goal: " + ex.message);
    }
}


function DisplayMacroTrackingForGoalInGrid(recordID = null) {
    try {
        if (IsNullOrEmpty(recordID)) return;
        var resourceUrl = "GoalAPI/MacroTrackingGridResource/" + recordID;
        LoadGridView(resourceUrl, true, true, divMainPage);
    }
    catch (ex) {
        toastr.error('Error while displaying Macro Tracking for the goal in grid: ' + ex.message);
    }
}
function DisplayMacroTrackingForGoalInTimeLine(recordID = null) {
    try {
        if (IsNullOrEmpty(recordID)) return;
        var resourceUrl = "GoalAPI/MacroTrackingTimeLineRead/" + recordID;
        LoadTimeLineView(resourceUrl, true, true, divMainPage);
    }
    catch (ex) {
        toastr.error('Error while displaying Macro Tracking for the goal in timeline: ' + ex.message);
    }
}
function DisplayMicroTrackingForGoalInGrid(recordID = null) {
    try {
        if (IsNullOrEmpty(recordID)) return;
        var resourceUrl = "GoalAPI/MicroTrackingGridResource/" + recordID;
        LoadGridView(resourceUrl, true, true, divMainPage);
    }
    catch (ex) {
        toastr.error('Error while displaying Micro Tracking for the goal in grid: ' + ex.message);
    }
}
function DisplayMicroTrackingForGoalInTimeLine(recordID = null) {
    try {
        if (IsNullOrEmpty(recordID)) return;
        var resourceUrl = "GoalAPI/MicroTrackingTimeLineRead/" + recordID;
        LoadTimeLineView(resourceUrl, true, true, divMainPage);
    }
    catch (ex) {
        toastr.error('Error while displaying Micro Tracking for the goal in timeline: ' + ex.message);
    }
}


function RebootGoal(goalID = null) {
    try {
        if (IsNullOrEmpty(goalID)) return;
        ConfirmationAlert('Goal', 'Do you really want to reboot this goal?', function (value) {
            var url = 'GoalAPI/RebootGoal/' + goalID
            AjaxGETRequest(
                url,
                function (response) {
                    response = SafeJSONparse(response);
                    if (response.WasSuccessful) {
                        AlertWarning("Rebooted goal!");
                        RefreshDataView();
                    }
                    else {
                        toastr.error("Alas! Error rebooting goal: " + response.Message);
                    }
                },
                function (error) {

                }, true, true, true
            );
        });
    }
    catch (ex) {
        toastr.error("Error while rebooting goal: " + ex.message);
    }
}
function ReversionGoal(goalChangeID = null) {
    try {
        if (IsNullOrEmpty(goalChangeID)) return;
        ConfirmationAlert('Goal', 'Do you really want to reversion this goal to an older version?', function (value) {
            var url = 'GoalAPI/ReversionGoal/' + goalChangeID
            AjaxGETRequest(
                url,
                function (response) {
                    response = SafeJSONparse(response);
                    if (response.WasSuccessful) {
                        AlertWarning("Reversioned goal!");
                        RefreshDataView();
                    }
                    else {
                        toastr.error("Alas! Error reversioning goal: " + response.Message);
                    }
                },
                function (error) {

                }, true, true, true
            );
        });
    }
    catch (ex) {
        toastr.error("Error while reversioning goal: " + ex.message);
    }
}
function LoadGoalReversionView(recordID = null) {
    try {
        if (IsNullOrEmpty(recordID)) return;
        var resourceUrl = "GoalAPI/GoalReversionGridViewResource/" + recordID;
        LoadGridView(resourceUrl, true, true, divMainPage);
    }
    catch (ex) {
        toastr.error('Error while displaying Goal reversion tracking in grid: ' + ex.message);
    }
}


function LoadTasks(recordId = null) {
    try {
        if (IsNullOrEmpty(recordId)) return;
        LoadGridView("TaskAPI/Resource/" + recordId);
    }
    catch (ex) {
        toastr.error("Error while loading list of milestones: " + ex.message);
    }
}
function LoadTasksHierarchy(recordId = null) {
    try {
        if (IsNullOrEmpty(recordId)) return;
        LoadGridView("TaskAPI/WorkHierarchyResource/" + recordId);
    }
    catch (ex) {
        toastr.error("Error while loading list of milestones: " + ex.message);
    }
}